from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    company: Mapped[str | None] = mapped_column(String(200), index=True)
    role: Mapped[str | None] = mapped_column(String(200))
    email: Mapped[str | None] = mapped_column(String(320), index=True)
    website: Mapped[str | None] = mapped_column(String(500))
    industry: Mapped[str | None] = mapped_column(String(200), index=True)
    company_size: Mapped[str | None] = mapped_column(String(100))
    source: Mapped[str | None] = mapped_column(String(200))
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    scores: Mapped[list["LeadScore"]] = relationship(
        back_populates="lead", cascade="all, delete-orphan"
    )


class LeadScore(Base):
    __tablename__ = "lead_scores"
    __table_args__ = (
        CheckConstraint("icp_fit BETWEEN 0 AND 100"),
        CheckConstraint("company_potential BETWEEN 0 AND 100"),
        CheckConstraint("role_relevance BETWEEN 0 AND 100"),
        CheckConstraint("buying_signal BETWEEN 0 AND 100"),
        CheckConstraint("data_quality BETWEEN 0 AND 100"),
        CheckConstraint("overall_score BETWEEN 0 AND 100"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id"), nullable=False)
    icp_fit: Mapped[int] = mapped_column(Integer, nullable=False)
    company_potential: Mapped[int] = mapped_column(Integer, nullable=False)
    role_relevance: Mapped[int] = mapped_column(Integer, nullable=False)
    buying_signal: Mapped[int] = mapped_column(Integer, nullable=False)
    data_quality: Mapped[int] = mapped_column(Integer, nullable=False)
    overall_score: Mapped[int] = mapped_column(Integer, nullable=False)
    rationale: Mapped[str] = mapped_column(Text, default="", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    lead: Mapped[Lead] = relationship(back_populates="scores")
