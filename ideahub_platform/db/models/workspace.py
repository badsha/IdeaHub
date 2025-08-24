from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ideahub_platform.db.base import Base


class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    url = Column(String(255), nullable=False, unique=True, index=True)  # Multi-tenancy identifier
    public_default = Column(Boolean, default=True)
    features = Column(JSON, default=list)
    owner_id = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    communities = relationship("Community", back_populates="workspace", cascade="all, delete-orphan")
    members = relationship("Member", back_populates="workspace", cascade="all, delete-orphan")
