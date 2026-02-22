from enum import Enum


class ProgramType(Enum):
    """
    Enum for program types.
    """

    GENERAL = "general"
    CREDIT = "credit"


class SemesterRegistrationStatus(Enum):
    """
    Enum for semester registration status.
    """

    CLOSED = "closed"
    OPEN = "open"


class SectionType(Enum):
    LECTURE = "lecture"
    LAB = "lab"
    TUTORIAL = "tutorial"


class WeekDay(Enum):
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"


class EnrollmentStatus(Enum):
    ACTIVE = "active"
    WITHDRAWN = "withdrawn"
    FAILED = "failed"


class StudentStatus(Enum):
    ACTIVE = "active"
    PROBATION = "probation"
    SUSPENDED = "suspended"
    GRADUATED = "graduated"


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"


class Religion(Enum):
    MUSLIM = "muslim"
    CHRISTIAN = "christian"
    OTHER = "other"


class MilitaryStatus(Enum):
    EXEMPTED = "exempted"
    POSTPONED = "postponed"
    COMPLETED = "completed"
    SERVING = "serving"


class InvoiceStatus(Enum):
    PAID = "paid"
    UNPAID = "unpaid"
    PARTIAL = "partial"


class PaymentMethod(Enum):
    FAWRY = "fawry"
    VISA = "visa"
