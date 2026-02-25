from app.models.academics import (
    BylawCourse,
    Concentration,
    Course,
    CoursePrerequisite,
    Department,
    ElectiveGroup,
    FacultyBylaw,
    Program,
    ProgramBylaw,
    Semester,
)
from app.models.finance import Invoice, Payment
from app.models.grading import GradeDistribution, StudentScore
from app.models.iam import AuditLog, Role, RolePermission, User, UserRole
from app.models.registration import (
    CourseOffering,
    Enrollment,
    EnrollmentSection,
    Location,
    Section,
)
from app.models.students import Student, StudentTransferHistory
from app.models.tokens import Token

from .base import Base
