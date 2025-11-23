"""
Audit log and usage tracking models
"""
import uuid
from datetime import datetime, date
from sqlalchemy import (
    Column,
    String,
    Integer,
    Date,
    TIMESTAMP,
    Text,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, INET
from sqlalchemy.orm import relationship

from backend.core.database import Base


class AuditLog(Base):
    """Audit log for tracking all user actions (required for customs compliance)"""

    __tablename__ = "audit_logs"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    # Action information
    action = Column(String(100), nullable=False, index=True)
    resource_type = Column(String(50))
    resource_id = Column(String(100))

    # Details
    details = Column(JSONB)
    ip_address = Column(INET)
    user_agent = Column(Text)

    # Timestamp
    created_at = Column(TIMESTAMP, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog(id={self.id}, action={self.action}, user_id={self.user_id})>"


class UsageMonthly(Base):
    """Monthly usage tracking for rate limiting and billing"""

    __tablename__ = "usage_monthly"
    __table_args__ = (UniqueConstraint("user_id", "month", name="uix_user_month"),)

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Month (first day of month)
    month = Column(Date, nullable=False)

    # Usage counters
    classifications_count = Column(Integer, default=0)
    documents_generated = Column(Integer, default=0)
    api_calls = Column(Integer, default=0)

    # Relationships
    user = relationship("User", back_populates="usage_monthly")

    def __repr__(self):
        return f"<UsageMonthly(user_id={self.user_id}, month={self.month}, classifications={self.classifications_count})>"

    @classmethod
    def get_or_create_current_month(cls, db, user_id: uuid.UUID):
        """Get or create usage record for current month"""
        current_month = date.today().replace(day=1)
        usage = db.query(cls).filter(
            cls.user_id == user_id,
            cls.month == current_month
        ).first()

        if not usage:
            usage = cls(user_id=user_id, month=current_month)
            db.add(usage)
            db.commit()
            db.refresh(usage)

        return usage
