"""
Verification token model for email verification and password resets
"""
import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    TIMESTAMP,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from backend.core.database import Base


class VerificationToken(Base):
    """Verification tokens for email verification and password resets"""

    __tablename__ = "verification_tokens"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Token information
    token = Column(String(100), unique=True, nullable=False, index=True)
    token_type = Column(String(20), nullable=False)  # email_verify, password_reset

    # Expiration
    expires_at = Column(TIMESTAMP, nullable=False)
    used_at = Column(TIMESTAMP, nullable=True)

    # Timestamp
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="verification_tokens")

    def __repr__(self):
        return f"<VerificationToken(id={self.id}, type={self.token_type}, used={self.used_at is not None})>"

    @property
    def is_expired(self) -> bool:
        """Check if token has expired"""
        return datetime.utcnow() > self.expires_at

    @property
    def is_used(self) -> bool:
        """Check if token has been used"""
        return self.used_at is not None

    @property
    def is_valid(self) -> bool:
        """Check if token is valid (not expired and not used)"""
        return not self.is_expired and not self.is_used
