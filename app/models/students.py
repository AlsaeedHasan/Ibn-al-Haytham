import enum
import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import DATE, TEXT, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enum import Gender, MilitaryStatus, Religion, StudentStatus

from .base import Base


class Student(Base):
    __tablename__ = "students"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        primary_key=True,
        default=uuid.uuid4,
    )
    student_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    program_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("programs.id"), nullable=False
    )
    bylaw_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("program_bylaws.id"), nullable=False
    )
    concetration_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("concentrations.id"), nullable=True
    )
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    gpa: Mapped[Decimal | None] = mapped_column(Numeric(3, 2), nullable=True)
    earned_credits: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[StudentStatus] = mapped_column(
        Enum(StudentStatus, name="student_status", create_type=True),
        default=StudentStatus.ACTIVE,
        nullable=False,
    )

    gender: Mapped[Gender] = mapped_column(
        Enum(Gender, name="gender", create_type=True), nullable=False
    )
    religion: Mapped[Religion | None] = mapped_column(
        Enum(Religion, name="religion", create_type=True), nullable=True
    )
    nationality: Mapped[str | None] = mapped_column(String(100), nullable=True)
    date_of_birth: Mapped[date | None] = mapped_column(DATE, nullable=True)
    place_of_birth: Mapped[str | None] = mapped_column(String(255), nullable=True)
    national_id_issue_date: Mapped[date | None] = mapped_column(DATE, nullable=True)

    gov_address: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    current_address: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    governorate: Mapped[str | None] = mapped_column(String(100), nullable=True)

    landline_phone: Mapped[str | None] = mapped_column(String(20), nullable=True)

    guardian_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    guardian_relation: Mapped[str | None] = mapped_column(String(100), nullable=True)
    guardian_job: Mapped[str | None] = mapped_column(String(255), nullable=True)
    guardian_phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    guardian_national_id: Mapped[str | None] = mapped_column(String(20), nullable=True)

    military_status: Mapped[MilitaryStatus | None] = mapped_column(
        Enum(MilitaryStatus, name="military_status", create_type=True), nullable=True
    )
    military_number: Mapped[str | None] = mapped_column(String(50), nullable=True)

    user = relationship("User", back_populates="student")
    program = relationship("Program", back_populates="students")
    bylaw = relationship("ProgramBylaw", back_populates="students")
    concetration = relationship("Concentration", back_populates="students")
    enrollments = relationship(
        "Enrollment", back_populates="student", cascade="all, delete-orphan"
    )
    transfer_history: Mapped[list["StudentTransferHistory"]] = relationship(
        "StudentTransferHistory",
        back_populates="student",
        cascade="all, delete-orphan",
    )
    invoices = relationship(
        "Invoice", back_populates="student", cascade="all, delete-orphan"
    )


class StudentTransferHistory(Base):
    __tablename__ = "student_transfer_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.user_id"), nullable=False
    )
    from_program_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("programs.id"), nullable=False
    )
    to_program_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("programs.id"), nullable=False
    )
    transfer_date: Mapped[date] = mapped_column(DATE, nullable=False)
    decree_number: Mapped[str | None] = mapped_column(String(100), nullable=True)

    student: Mapped["Student"] = relationship(
        "Student", back_populates="transfer_history"
    )
    from_program = relationship("Program", foreign_keys=[from_program_id])
    to_program = relationship("Program", foreign_keys=[to_program_id])
