"""
Document models for uploaded and generated documents
"""
import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Integer,
    TIMESTAMP,
    Text,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from backend.core.database import Base


class UploadedDocument(Base):
    """Model for user-uploaded supporting documents"""

    __tablename__ = "uploaded_documents"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id", ondelete="SET NULL"), nullable=True, index=True)
    classification_id = Column(UUID(as_uuid=True), ForeignKey("classifications.id", ondelete="SET NULL"), nullable=True)

    # File information
    document_type = Column(String(50), nullable=False)  # manufacturer_spec, material_cert, lab_test, etc.
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)  # S3 path
    file_size = Column(Integer)  # Size in bytes
    mime_type = Column(String(100))

    # OCR results
    extracted_text = Column(Text)
    extracted_fields = Column(JSONB)

    # Validation
    validation_status = Column(String(20), default="pending")  # pending, validated, rejected
    validation_notes = Column(Text)
    validated_by = Column(String(50))  # ai, user, expert
    validated_at = Column(TIMESTAMP)

    # Timestamp
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="uploaded_documents")
    product = relationship("Product", back_populates="uploaded_documents")
    classification = relationship("Classification", back_populates="uploaded_documents")

    def __repr__(self):
        return f"<UploadedDocument(id={self.id}, type={self.document_type}, filename={self.filename})>"


class GeneratedDocument(Base):
    """Model for system-generated documents (invoices, packing lists, etc.)"""

    __tablename__ = "generated_documents"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Document information
    document_type = Column(String(50), nullable=False)  # invoice, packing_list, coo
    file_path = Column(String(500), nullable=False)  # S3 path

    # Related data (stored as JSON for flexibility)
    shipment_data = Column(JSONB)
    products = Column(JSONB)  # Product IDs and quantities

    # Timestamp
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="generated_documents")

    def __repr__(self):
        return f"<GeneratedDocument(id={self.id}, type={self.document_type})>"
