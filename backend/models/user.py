"""
User model for authentication and profile management
"""
import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
    TIMESTAMP,
    ARRAY,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from backend.core.database import Base


class User(Base):
    """User model for storing user account information"""

    __tablename__ = "users"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Authentication
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    # Profile
    full_name = Column(String(100))
    company_name = Column(String(100))
    phone = Column(String(20))

    # Address
    address_line1 = Column(String(200))
    address_line2 = Column(String(200))
    city = Column(String(100))
    province = Column(String(50))
    postal_code = Column(String(20))
    country = Column(String(2), default="CA")

    # Business information
    business_number = Column(String(15))  # BN15 for CARM

    # Account status
    tier = Column(
        String(20), default="free"
    )  # free, starter, growth, professional
    verified = Column(Boolean, default=False)
    locked_until = Column(TIMESTAMP, nullable=True)
    failed_login_attempts = Column(Integer, default=0)

    # Stripe
    stripe_customer_id = Column(String(255), nullable=True)
    stripe_subscription_id = Column(String(255), nullable=True)

    # Market segmentation (from signup)
    business_type = Column(
        String(50)
    )  # ecommerce, manufacturer, retailer, etc.
    monthly_shipments = Column(String(20))  # 1-10, 10-50, 50-200, 200+
    primary_products = Column(Text)
    main_origin_countries = Column(ARRAY(String))
    has_carm_account = Column(Boolean, default=False)
    current_method = Column(
        String(20)
    )  # broker, diy, both, none

    # Timestamps
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(TIMESTAMP, nullable=True)

    # Relationships
    products = relationship("Product", back_populates="user", cascade="all, delete-orphan")
    classifications = relationship("Classification", back_populates="user", cascade="all, delete-orphan")
    uploaded_documents = relationship("UploadedDocument", back_populates="user", cascade="all, delete-orphan")
    generated_documents = relationship("GeneratedDocument", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user")
    usage_monthly = relationship("UsageMonthly", back_populates="user", cascade="all, delete-orphan")
    verification_tokens = relationship("VerificationToken", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, tier={self.tier})>"

    @property
    def is_locked(self) -> bool:
        """Check if account is currently locked"""
        if self.locked_until is None:
            return False
        return datetime.utcnow() < self.locked_until

    @property
    def is_premium(self) -> bool:
        """Check if user has a paid subscription"""
        return self.tier in ["starter", "growth", "professional"]
