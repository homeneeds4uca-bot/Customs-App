"""
Classification model for tracking AI classification requests and results
"""
import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
    TIMESTAMP,
    Text,
    ForeignKey,
    ARRAY,
    DECIMAL,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from backend.core.database import Base


class Classification(Base):
    """Classification model for audit trail of all classification requests"""

    __tablename__ = "classifications"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id", ondelete="SET NULL"), nullable=True)

    # Input data
    input_data = Column(JSONB, nullable=False)  # Full request payload

    # Result
    result_hs_code = Column(String(10))
    result_description = Column(Text)
    confidence = Column(DECIMAL(4, 3))
    alternatives = Column(JSONB)  # Top 3 alternatives
    warnings = Column(ARRAY(Text))
    reasoning = Column(Text)

    # Metadata
    processing_time_ms = Column(Integer)
    model_version = Column(String(50))

    # User actions
    user_corrected = Column(Boolean, default=False)
    corrected_hs_code = Column(String(10))
    correction_reason = Column(Text)

    # Timestamp
    created_at = Column(TIMESTAMP, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="classifications")
    product = relationship("Product")
    uploaded_documents = relationship("UploadedDocument", back_populates="classification")

    def __repr__(self):
        return f"<Classification(id={self.id}, hs_code={self.result_hs_code}, confidence={self.confidence})>"
