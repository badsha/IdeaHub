from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ideahub_platform.db.base import Base


class Idea(Base):
    __tablename__ = "ideas"

    id = Column(Integer, primary_key=True, index=True)
    community_id = Column(Integer, ForeignKey("communities.id"), nullable=False, index=True)
    author_id = Column(Integer, ForeignKey("members.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    visibility = Column(String(50), default="public")  # public, private, workspace
    status = Column(String(50), default="draft")  # draft, active, implemented, archived
    tags = Column(JSON, default=list)
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    community = relationship("Community", back_populates="ideas")
    author = relationship("Member", back_populates="ideas")
