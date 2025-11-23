"""
Pydantic schemas for User-related requests and responses
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator
import uuid


class UserBase(BaseModel):
    """Base user schema with common fields"""
    email: EmailStr
    full_name: Optional[str] = None
    company_name: Optional[str] = None
    phone: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=8, max_length=128)

    # Market segmentation
    business_type: Optional[str] = None
    monthly_shipments: Optional[str] = None
    primary_products: Optional[str] = None
    main_origin_countries: Optional[List[str]] = None
    has_carm_account: Optional[bool] = False
    current_method: Optional[str] = None

    # Terms acceptance
    accepts_liability: bool = Field(..., description="User must accept liability terms")
    accepts_terms: bool = Field(..., description="User must accept terms of service")

    @validator("accepts_liability", "accepts_terms")
    def validate_acceptance(cls, v):
        if not v:
            raise ValueError("Must accept terms and conditions")
        return v


class UserUpdate(BaseModel):
    """Schema for updating user profile"""
    full_name: Optional[str] = None
    company_name: Optional[str] = None
    phone: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    business_number: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response (public data)"""
    id: uuid.UUID
    tier: str
    verified: bool
    company_name: Optional[str] = None
    business_number: Optional[str] = None
    created_at: datetime
    last_login_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str
    remember_me: bool = False


class TokenResponse(BaseModel):
    """Schema for authentication token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request"""
    refresh_token: str


class PasswordResetRequest(BaseModel):
    """Schema for password reset request"""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Schema for password reset confirmation"""
    token: str
    new_password: str = Field(..., min_length=8, max_length=128)


class PasswordChange(BaseModel):
    """Schema for password change (authenticated user)"""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)


class UsageStatsResponse(BaseModel):
    """Schema for user usage statistics"""
    tier: str
    classifications_count: int
    classifications_limit: Optional[int]  # None = unlimited
    documents_generated: int
    api_calls: int
    api_calls_limit: Optional[int]
    current_month: str

    class Config:
        from_attributes = True
