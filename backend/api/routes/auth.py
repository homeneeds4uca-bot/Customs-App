"""
Authentication routes: registration, login, password reset, email verification
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    create_verification_token,
    validate_password,
    decode_token,
)
from backend.models import User, VerificationToken, AuditLog
from backend.schemas import (
    UserCreate,
    UserLogin,
    TokenResponse,
    RefreshTokenRequest,
    PasswordResetRequest,
    PasswordResetConfirm,
    UserResponse,
)
from backend.api.deps import get_current_user
from backend.core.config import settings

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account.

    - Validates password strength
    - Creates user with hashed password
    - Sends verification email
    - Returns access and refresh tokens
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Validate password strength
    is_valid, errors = validate_password(user_data.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Password does not meet requirements", "errors": errors},
        )

    # Create user
    user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        full_name=user_data.full_name,
        company_name=user_data.company_name,
        phone=user_data.phone,
        business_type=user_data.business_type,
        monthly_shipments=user_data.monthly_shipments,
        primary_products=user_data.primary_products,
        main_origin_countries=user_data.main_origin_countries,
        has_carm_account=user_data.has_carm_account,
        current_method=user_data.current_method,
        tier="free",
        verified=False,  # Email verification required
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create email verification token
    token = create_verification_token()
    verification = VerificationToken(
        user_id=user.id,
        token=token,
        token_type="email_verify",
        expires_at=datetime.utcnow() + timedelta(hours=24),
    )
    db.add(verification)

    # Log registration
    audit = AuditLog(
        user_id=user.id,
        action="auth.register",
        resource_type="user",
        resource_id=str(user.id),
        details={"email": user.email},
    )
    db.add(audit)
    db.commit()

    # TODO: Send verification email (implement email service)
    # send_verification_email(user.email, token)

    # Create tokens
    access_token = create_access_token(
        user_id=str(user.id),
        email=user.email,
        tier=user.tier,
        verified=user.verified,
    )
    refresh_token = create_refresh_token(user_id=str(user.id))

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.from_orm(user),
    )


@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return tokens.

    - Validates credentials
    - Checks account lockout
    - Returns access and refresh tokens
    """
    # Find user
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # Check if account is locked
    if user.is_locked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Account locked until {user.locked_until} due to too many failed login attempts",
        )

    # Verify password
    if not verify_password(credentials.password, user.password_hash):
        # Increment failed login attempts
        user.failed_login_attempts += 1

        # Lock account after 5 failed attempts
        if user.failed_login_attempts >= settings.FAILED_LOGIN_LOCKOUT_ATTEMPTS:
            user.locked_until = datetime.utcnow() + timedelta(
                minutes=settings.FAILED_LOGIN_LOCKOUT_DURATION_MINUTES
            )

        db.commit()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # Reset failed login attempts on successful login
    user.failed_login_attempts = 0
    user.last_login_at = datetime.utcnow()
    db.commit()

    # Log successful login
    audit = AuditLog(
        user_id=user.id,
        action="auth.login",
        resource_type="user",
        resource_id=str(user.id),
        details={"email": user.email},
    )
    db.add(audit)
    db.commit()

    # Create tokens
    access_token = create_access_token(
        user_id=str(user.id),
        email=user.email,
        tier=user.tier,
        verified=user.verified,
    )
    refresh_token = create_refresh_token(
        user_id=str(user.id),
        remember_me=credentials.remember_me,
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.from_orm(user),
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh_access_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    """
    Refresh access token using refresh token.
    """
    payload = decode_token(request.refresh_token)

    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    # Create new access token
    access_token = create_access_token(
        user_id=str(user.id),
        email=user.email,
        tier=user.tier,
        verified=user.verified,
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=request.refresh_token,  # Return same refresh token
        user=UserResponse.from_orm(user),
    )


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Logout user (client should discard tokens).
    """
    # Log logout
    audit = AuditLog(
        user_id=current_user.id,
        action="auth.logout",
        resource_type="user",
        resource_id=str(current_user.id),
    )
    db.add(audit)
    db.commit()

    return {"message": "Logged out successfully"}


@router.get("/verify/{token}")
def verify_email(token: str, db: Session = Depends(get_db)):
    """
    Verify user email using verification token.
    """
    verification = (
        db.query(VerificationToken)
        .filter(
            VerificationToken.token == token,
            VerificationToken.token_type == "email_verify",
        )
        .first()
    )

    if not verification:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification token",
        )

    if not verification.is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token has expired or already been used",
        )

    # Mark user as verified
    user = db.query(User).filter(User.id == verification.user_id).first()
    user.verified = True

    # Mark token as used
    verification.used_at = datetime.utcnow()

    db.commit()

    return {"message": "Email verified successfully"}


@router.post("/forgot-password")
def forgot_password(request: PasswordResetRequest, db: Session = Depends(get_db)):
    """
    Request password reset email.
    """
    user = db.query(User).filter(User.email == request.email).first()

    # Always return success to prevent email enumeration
    # Don't reveal if email exists or not
    if user:
        # Create password reset token
        token = create_verification_token()
        reset_token = VerificationToken(
            user_id=user.id,
            token=token,
            token_type="password_reset",
            expires_at=datetime.utcnow() + timedelta(hours=1),
        )
        db.add(reset_token)
        db.commit()

        # TODO: Send password reset email
        # send_password_reset_email(user.email, token)

    return {
        "message": "If an account exists with this email, a password reset link has been sent"
    }


@router.post("/reset-password")
def reset_password(request: PasswordResetConfirm, db: Session = Depends(get_db)):
    """
    Reset password using reset token.
    """
    verification = (
        db.query(VerificationToken)
        .filter(
            VerificationToken.token == request.token,
            VerificationToken.token_type == "password_reset",
        )
        .first()
    )

    if not verification:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset token",
        )

    if not verification.is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token has expired or already been used",
        )

    # Validate new password
    is_valid, errors = validate_password(request.new_password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Password does not meet requirements", "errors": errors},
        )

    # Update password
    user = db.query(User).filter(User.id == verification.user_id).first()
    user.password_hash = hash_password(request.new_password)

    # Mark token as used
    verification.used_at = datetime.utcnow()

    # Log password reset
    audit = AuditLog(
        user_id=user.id,
        action="auth.password_reset",
        resource_type="user",
        resource_id=str(user.id),
    )
    db.add(audit)

    db.commit()

    return {"message": "Password reset successfully"}
