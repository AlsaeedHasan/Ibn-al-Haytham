from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enum import ProgramType, SemesterRegistrationStatus
from app.models.finance import Invoice
from app.models.registration import CourseOffering
from app.models.students import Student

from .base import Base


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_ar: Mapped[str] = mapped_column(String(100), nullable=False)
    name_en: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    programs: Mapped[list["Program"]] = relationship(
        "Program", back_populates="department", cascade="all, delete-orphan"
    )


class FacultyBylaw(Base):
    __tablename__ = "faculty_bylaws"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    issue_year: Mapped[int] = mapped_column(Integer, nullable=False)

    program_bylaws: Mapped[list["ProgramBylaw"]] = relationship(
        "ProgramBylaw", back_populates="bylaw", cascade="all, delete-orphan"
    )


class Program(Base):
    __tablename__ = "programs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_ar: Mapped[str] = mapped_column(String(100), nullable=False)
    name_en: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    department_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("departments.id"), nullable=False
    )
    type: Mapped[ProgramType] = mapped_column(
        Enum(ProgramType, name="program_type", create_type=True), nullable=False
    )

    department: Mapped[Department] = relationship(
        "Department", back_populates="programs"
    )
    concentrations: Mapped[list["Concentration"]] = relationship(
        "Concentration", back_populates="program", cascade="all, delete-orphan"
    )
    program_bylaws: Mapped[list["ProgramBylaw"]] = relationship(
        "ProgramBylaw", back_populates="program", cascade="all, delete-orphan"
    )
    students: Mapped[list["Student"]] = relationship(
        "Student", back_populates="program", cascade="all, delete-orphan"
    )


class ProgramBylaw(Base):
    __tablename__ = "program_bylaws"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    program_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("programs.id"), nullable=False
    )
    bylaw_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("faculty_bylaws.id"), nullable=False
    )
    total_credit_hours: Mapped[int] = mapped_column(Integer, nullable=False)

    program: Mapped[Program] = relationship("Program", back_populates="program_bylaws")
    bylaw: Mapped[FacultyBylaw] = relationship(
        "FacultyBylaw", back_populates="program_bylaws"
    )
    bylaw_courses: Mapped[list["BylawCourse"]] = relationship(
        "BylawCourse", back_populates="program_bylaw", cascade="all, delete-orphan"
    )
    elective_groups: Mapped[list["ElectiveGroup"]] = relationship(
        "ElectiveGroup", back_populates="program_bylaw", cascade="all, delete-orphan"
    )
    students: Mapped[list["Student"]] = relationship(
        "Student", back_populates="bylaw", cascade="all, delete-orphan"
    )


class Concentration(Base):
    __tablename__ = "concentrations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_ar: Mapped[str] = mapped_column(String(100), nullable=False)
    name_en: Mapped[str] = mapped_column(String(100), nullable=False)
    min_level: Mapped[int] = mapped_column(Integer, nullable=False)
    min_credit_hours: Mapped[int] = mapped_column(Integer, nullable=True)
    program_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("programs.id"), nullable=False
    )
    program: Mapped[Program] = relationship("Program", back_populates="concentrations")
    students: Mapped[list["Student"]] = relationship(
        "Student", back_populates="concetration", cascade="all, delete-orphan"
    )


class Semester(Base):
    __tablename__ = "semesters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_ar: Mapped[str] = mapped_column(String(100), nullable=False)
    name_en: Mapped[str] = mapped_column(String(100), nullable=False)
    start_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    registration_status: Mapped[SemesterRegistrationStatus] = mapped_column(
        Enum(SemesterRegistrationStatus, name="registration_status", create_type=True),
        nullable=False,
    )
    course_offerings: Mapped[list[CourseOffering]] = relationship(
        "CourseOffering", back_populates="semester", cascade="all, delete-orphan"
    )
    invoices: Mapped[list["Invoice"]] = relationship(
        "Invoice", back_populates="semester", cascade="all, delete-orphan"
    )


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    name_ar: Mapped[str] = mapped_column(String(100), nullable=False)
    name_en: Mapped[str] = mapped_column(String(100), nullable=False)
    credit_hours: Mapped[int] = mapped_column(Integer, nullable=False)
    lecture_hours: Mapped[int] = mapped_column(Integer, nullable=False)
    lab_hours: Mapped[int] = mapped_column(Integer, nullable=False)
    tutorial_hours: Mapped[int] = mapped_column(Integer, nullable=False)

    course_offerings: Mapped[list["CourseOffering"]] = relationship(
        "CourseOffering", back_populates="course", cascade="all, delete-orphan"
    )


class CoursePrerequisite(Base):
    __tablename__ = "course_prerequisites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("bylaw_courses.id"), nullable=False
    )
    prerequisite_course_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("courses.id"), nullable=False
    )
    set_id: Mapped[int] = mapped_column(Integer, nullable=False)

    bylaw_course: Mapped[BylawCourse] = relationship(
        "BylawCourse", foreign_keys=[course_id], back_populates="prerequisites"
    )
    prerequisite_course: Mapped[Course] = relationship(
        "Course", foreign_keys=[prerequisite_course_id]
    )


class BylawCourse(Base):
    __tablename__ = "bylaw_courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bylaw_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("program_bylaws.id"), nullable=False
    )
    course_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("courses.id"), nullable=False
    )
    concentration_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("concentrations.id"), nullable=True
    )
    semester_suggested: Mapped[int] = mapped_column(Integer, nullable=True)
    is_elective: Mapped[bool] = mapped_column(Boolean, nullable=False)
    elective_group_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("elective_groups.id"), nullable=True
    )

    program_bylaw: Mapped[ProgramBylaw] = relationship(
        "ProgramBylaw", back_populates="bylaw_courses"
    )
    course: Mapped[Course] = relationship("Course")
    prerequisites: Mapped[list["CoursePrerequisite"]] = relationship(
        "CoursePrerequisite",
        foreign_keys="[CoursePrerequisite.course_id]",
        back_populates="bylaw_course",
        cascade="all, delete-orphan",
    )
    elective_group: Mapped["ElectiveGroup"] = relationship(
        "ElectiveGroup", back_populates="courses"
    )


class ElectiveGroup(Base):
    __tablename__ = "elective_groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_ar: Mapped[str] = mapped_column(String(100), nullable=False)
    name_en: Mapped[str] = mapped_column(String(100), nullable=False)
    program_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("programs.id"), nullable=True
    )
    bylaw_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("program_bylaws.id"), nullable=False
    )
    required_credit_hours: Mapped[int] = mapped_column(Integer, nullable=False)
    min_courses: Mapped[int] = mapped_column(Integer, nullable=True)

    program_bylaw: Mapped[ProgramBylaw] = relationship(
        "ProgramBylaw", back_populates="elective_groups"
    )
    courses: Mapped[list[BylawCourse]] = relationship(
        "BylawCourse", back_populates="elective_group"
    )
