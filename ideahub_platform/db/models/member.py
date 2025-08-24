from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ideahub_platform.db.base import Base

# Association table for workspace members
workspace_members = Table(
    "workspace_members",
    Base.metadata,
    Column("workspace_id", Integer, ForeignKey("workspaces.id"), primary_key=True),
    Column("member_id", Integer, ForeignKey("members.id"), primary_key=True),
    Column("role", String(50), nullable=False, default="member"),
    Column("joined_at", DateTime(timezone=True), server_default=func.now()),
)


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)
    avatar_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    workspaces = relationship("Workspace", secondary=workspace_members, back_populates="members")
    ideas = relationship("Idea", back_populates="author", cascade="all, delete-orphan")
