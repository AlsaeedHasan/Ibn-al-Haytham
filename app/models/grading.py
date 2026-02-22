from decimal import Decimal

from sqlalchemy import DECIMAL, UUID, BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class GradeDistribution(Base):
    __tablename__ = "grade_distributions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    offering_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("course_offerings.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    max_score: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)
    weight: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)

    offering = relationship("CourseOffering", back_populates="grade_distributions")
    student_scores = relationship(
        "StudentScore", back_populates="distribution", cascade="all, delete-orphan"
    )


class StudentScore(Base):
    __tablename__ = "student_scores"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    enrollment_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("enrollments.id"), nullable=False
    )
    distribution_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("grade_distributions.id"), nullable=False
    )
    score: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)
    grader_id: Mapped[str] = mapped_column(UUID, ForeignKey("users.id"), nullable=False)

    enrollment = relationship("Enrollment", back_populates="student_scores")
    distribution: Mapped["GradeDistribution"] = relationship(
        "GradeDistribution", back_populates="student_scores"
    )
    grader = relationship("User", back_populates="graded_scores")
