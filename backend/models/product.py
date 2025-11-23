"""
Product model for storing user's product library
"""
import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Boolean,
    TIMESTAMP,
    Text,
    ForeignKey,
    ARRAY,
    DECIMAL,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from backend.core.database import Base


class Product(Base):
    """Product model for user's saved product library"""

    __tablename__ = "products"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Product information
    sku = Column(String(100))
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    material = Column(String(200))
    secondary_material = Column(String(200))
    material_percentage = Column(DECIMAL(5, 2))  # e.g., 65.50%
    product_use = Column(String(50))  # decorative, functional, industrial, etc.
    additional_details = Column(Text)

    # Classification
    hs_code = Column(String(10), index=True)
    hs_code_description = Column(Text)
    confidence = Column(DECIMAL(4, 3))  # 0.000 to 1.000
    confidence_level = Column(String(10))  # HIGH, MEDIUM, LOW
    classified_at = Column(TIMESTAMP)
    user_override = Column(Boolean, default=False)  # User changed AI suggestion

    # Origin
    country_of_origin = Column(String(2))  # ISO 2-letter code

    # Images
    images = Column(ARRAY(Text))  # S3 paths

    # Status
    has_complete_documentation = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="products")
    uploaded_documents = relationship("UploadedDocument", back_populates="product")

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, hs_code={self.hs_code})>"

    @property
    def needs_review(self) -> bool:
        """Check if product classification needs review (low confidence)"""
        if self.confidence is None:
            return True
        return float(self.confidence) < 0.70
