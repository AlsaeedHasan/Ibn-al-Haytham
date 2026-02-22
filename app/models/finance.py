import enum
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import DECIMAL, BigInteger, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enum import InvoiceStatus, PaymentMethod
from app.models.students import Student

from .base import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    student_id: Mapped[str] = mapped_column(
        ForeignKey("students.user_id"), nullable=False
    )
    semester_id: Mapped[int] = mapped_column(ForeignKey("semesters.id"), nullable=False)
    amount: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)
    status: Mapped[InvoiceStatus] = mapped_column( Enum(InvoiceStatus, name="invoice_status", create_type=True),
        nullable=False, default=InvoiceStatus.UNPAID
    )

    student: Mapped["Student"] = relationship("Student", back_populates="invoices")
    semester = relationship("Semester", back_populates="invoices")
    payments: Mapped[List["Payment"]] = relationship(
        "Payment", back_populates="invoice"
    )


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    invoice_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("invoices.id"), nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)
    method: Mapped[PaymentMethod] = mapped_column(Enum(PaymentMethod, name="payment_method", create_type=True), nullable=False)
    reference_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    invoice: Mapped["Invoice"] = relationship("Invoice", back_populates="payments")
