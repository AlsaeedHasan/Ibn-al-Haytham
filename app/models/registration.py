import uuid
from datetime import time

from sqlalchemy import UUID, Enum, ForeignKey, Integer, String, Time, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enum import EnrollmentStatus, SectionType, WeekDay

from .base import Base


class CourseOffering(Base):
    __tablename__ = "course_offerings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("courses.id"), nullable=False
    )
    semester_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("semesters.id"), nullable=False
    )
    max_capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    enrolled_count: Mapped[int] = mapped_column(Integer, default=0)

    course = relationship("Course", back_populates="course_offerings")
    sections = relationship(
        "Section", back_populates="course_offering", cascade="all, delete-orphan"
    )
    semester = relationship("Semester", back_populates="course_offerings")
    enrollments = relationship(
        "Enrollment", back_populates="course_offering", cascade="all, delete-orphan"
    )
    grade_distributions = relationship(
        "GradeDistribution", back_populates="offering", cascade="all, delete-orphan"
    )


class Section(Base):
    __tablename__ = "sections"

    __table_args__ = (
        UniqueConstraint(
            "location_id",
            "day",
            "start_time",
            "end_time",
            name="uq_section_location_time",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_offering_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("course_offerings.id"), nullable=False
    )
    name_ar: Mapped[str] = mapped_column(String(255), nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[SectionType] = mapped_column(
        Enum(SectionType, name="section_type", create_type=True), nullable=False
    )
    day: Mapped[WeekDay] = mapped_column(
        Enum(WeekDay, name="day_of_week", create_type=True), nullable=False
    )
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    location_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("locations.id"), nullable=False
    )
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)

    course_offering = relationship("CourseOffering", back_populates="sections")
    enrollments = relationship(
        "EnrollmentSection", back_populates="section", cascade="all, delete-orphan"
    )
    location = relationship("Location", back_populates="sections")


class Enrollment(Base):
    __tablename__ = "enrollments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("students.user_id"), nullable=False
    )
    course_offering_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("course_offerings.id"), nullable=False
    )
    status: Mapped[EnrollmentStatus] = mapped_column(
        Enum(EnrollmentStatus, name="enrollment_status", create_type=True),
        nullable=False,
    )

    course_offering = relationship("CourseOffering", back_populates="enrollments")
    sections = relationship(
        "EnrollmentSection", back_populates="enrollment", cascade="all, delete-orphan"
    )
    student = relationship("Student", back_populates="enrollments")
    student_scores = relationship(
        "StudentScore", back_populates="enrollment", cascade="all, delete-orphan"
    )


class EnrollmentSection(Base):
    __tablename__ = "enrollment_sections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enrollment_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("enrollments.id"), nullable=False
    )
    section_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sections.id"), nullable=False
    )

    enrollment = relationship("Enrollment", back_populates="sections")
    section = relationship("Section", back_populates="enrollments")


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_ar: Mapped[str] = mapped_column(String(255), nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)

    sections: Mapped[list["Section"]] = relationship(
        "Section", back_populates="location", cascade="all, delete-orphan"
    )
