"""
Security utilities for authentication and password management
"""
from datetime import datetime, timedelta
from typing import Optional, Tuple, List
import uuid

from jose import JWTError, jwt
from passlib.context import CryptContext

from .config import settings

# Password hashing context (bcrypt with cost factor 12)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def validate_password(password: str) -> Tuple[bool, List[str]]:
    """
    Validate password strength according to security requirements.

    Requirements:
    - 8-128 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number

    Args:
        password: Password to validate

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    if len(password) < settings.PASSWORD_MIN_LENGTH:
        errors.append(
            f"Password must be at least {settings.PASSWORD_MIN_LENGTH} characters"
        )

    if len(password) > settings.PASSWORD_MAX_LENGTH:
        errors.append(
            f"Password must be at most {settings.PASSWORD_MAX_LENGTH} characters"
        )

    if not any(c.isupper() for c in password):
        errors.append("Password must contain at least one uppercase letter")

    if not any(c.islower() for c in password):
        errors.append("Password must contain at least one lowercase letter")

    if not any(c.isdigit() for c in password):
        errors.append("Password must contain at least one number")

    return len(errors) == 0, errors


def hash_password(password: str) -> str:
    """
    Hash password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        plain_password: Plain text password
        hashed_password: Hashed password to verify against

    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    user_id: str, email: str, tier: str, verified: bool
) -> str:
    """
    Create JWT access token with 1 hour expiry.

    Args:
        user_id: User's UUID
        email: User's email
        tier: Subscription tier (free, starter, growth, professional)
        verified: Whether email is verified

    Returns:
        Encoded JWT token
    """
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": user_id,
        "email": email,
        "tier": tier,
        "verified": verified,
        "exp": expire,
        "iat": datetime.utcnow(),
        "jti": str(uuid.uuid4()),  # JWT ID for revocation
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(user_id: str, remember_me: bool = False) -> str:
    """
    Create refresh token with 7 or 30 days expiry.

    Args:
        user_id: User's UUID
        remember_me: If True, token expires in 30 days, otherwise 7 days

    Returns:
        Encoded JWT token
    """
    days = 30 if remember_me else settings.REFRESH_TOKEN_EXPIRE_DAYS
    expire = datetime.utcnow() + timedelta(days=days)

    payload = {
        "sub": user_id,
        "exp": expire,
        "type": "refresh",
        "jti": str(uuid.uuid4()),
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    """
    Decode and validate JWT token.

    Args:
        token: JWT token to decode

    Returns:
        Token payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def create_verification_token() -> str:
    """
    Create a random verification token for email verification or password reset.

    Returns:
        Random UUID string
    """
    return str(uuid.uuid4())
