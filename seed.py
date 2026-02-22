import asyncio
import uuid
from sqlalchemy import select
from app.core.enum import ProgramType  # تأكد من المسار حسب مشروعك
from app.core.database import AsyncSessionLocal # تأكد من المسار
from app.models.iam import Role, Permission, User, RolePermission
from app.models.academics import Department, Program

async def seed_roles_and_permissions(session):
    print("🌱 Seeding Roles and Permissions...")
    
    # 1. Define Basic Roles
    roles_data = [
        {"id": 1, "name_ar": "مدير النظام", "name_en": "System Admin", "slug": "sys_admin"},
        {"id": 2, "name_ar": "شئون طلبة", "name_en": "Student Affairs", "slug": "student_affairs"},
        {"id": 3, "name_ar": "أستاذ جامعي", "name_en": "Professor", "slug": "professor"},
        {"id": 4, "name_ar": "طالب", "name_en": "Student", "slug": "student"},
    ]

    for r_data in roles_data:
        stmt = select(Role).where(Role.slug == r_data["slug"])
        result = await session.execute(stmt)
        if not result.scalar_one_or_none():
            role = Role(**r_data)
            session.add(role)

    # 2. Define Basic Permissions
    permissions_data = [
        {"id": 1, "slug": "users:manage", "description": "إدارة المستخدمين"},
        {"id": 2, "slug": "grades:write", "description": "رصد الدرجات"},
        {"id": 3, "slug": "enrollment:manage", "description": "إدارة التسجيل"},
    ]

    for p_data in permissions_data:
        stmt = select(Permission).where(Permission.slug == p_data["slug"])
        result = await session.execute(stmt)
        if not result.scalar_one_or_none():
            permission = Permission(**p_data)
            session.add(permission)
            
    await session.commit()
    print("✅ Roles & Permissions Seeded!")

async def seed_academic_structure(session):
    print("🌱 Seeding Academic Structure...")
    
    # 1. Department
    dept_code = "CSE"
    stmt = select(Department).where(Department.code == dept_code)
    result = await session.execute(stmt)
    department = result.scalar_one_or_none()
    
    if not department:
        department = Department(
            name_ar="هندسة الحاسبات والنظم",
            name_en="Computer and Systems Engineering",
            code=dept_code
        )
        session.add(department)
        await session.commit()
        await session.refresh(department)

    # 2. Program
    prog_code = "CCE"
    stmt = select(Program).where(Program.code == prog_code)
    result = await session.execute(stmt)
    program = result.scalar_one_or_none()
    
    if not program:
        program = Program(
            name_ar="هندسة حاسبات (ساعات معتمدة)",
            name_en="Computer Engineering (Credit)",
            code=prog_code,
            department_id=department.id,
            type=ProgramType.CREDIT # تأكد إن الـ Enum ده موجود عندك
        )
        session.add(program)
        await session.commit()
        
    print("✅ Academic Structure Seeded!")

async def seed_admin_user(session):
    print("🌱 Seeding Admin User...")
    admin_email = "admin@bhit.bu.edu.eg"
    
    stmt = select(User).where(User.university_email == admin_email)
    result = await session.execute(stmt)
    if not result.scalar_one_or_none():
        # في الحقيقة هنستخدم passlib لعمل Hash، بس مؤقتاً هنحط قيمة وهمية عشان الـ Seed
        dummy_hashed_password = "$2b$12$DummyHashStringForAdminPassword123" 
        
        admin_user = User(
            id=uuid.uuid4(),
            national_id="29801011400000",
            university_email=admin_email,
            hashed_password=dummy_hashed_password,
            first_name_ar="مدير",
            first_name_en="Admin",
            second_name_ar="النظام",
            second_name_en="System",
            third_name_ar="ابن",
            third_name_en="Ibn",
            fourth_name_ar="الهيثم",
            fourth_name_en="Alhaytham",
            family_name_ar="الرئيسي",
            family_name_en="Main",
            is_active=True,
            is_verified=True
        )
        session.add(admin_user)
        await session.commit()
        print("✅ Admin User Seeded! (Email: admin@bhit.bu.edu.eg)")
    else:
        print("⚡ Admin User already exists.")

async def main():
    print("🚀 Starting Database Seeding for Ibn-Alhaytham...")
    async with AsyncSessionLocal() as session:
        try:
            await seed_roles_and_permissions(session)
            await seed_academic_structure(session)
            await seed_admin_user(session)
            print("🎉 Seeding Completed Successfully!")
        except Exception as e:
            await session.rollback()
            print(f"❌ Error during seeding: {e}")

if __name__ == "__main__":
    asyncio.run(main())