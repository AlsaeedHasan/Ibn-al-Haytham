# Database Tables Info

## Table: `alembic_version`

```sql
                    Table "public.alembic_version"
   Column    |         Type          | Collation | Nullable | Default 
-------------+-----------------------+-----------+----------+---------
 version_num | character varying(32) |           | not null | 
Indexes:
    "alembic_version_pkc" PRIMARY KEY, btree (version_num)

```

## Table: `enrollments`

```sql
                                       Table "public.enrollments"
       Column       |       Type        | Collation | Nullable |                 Default                 
--------------------+-------------------+-----------+----------+-----------------------------------------
 id                 | integer           |           | not null | nextval('enrollments_id_seq'::regclass)
 student_id         | uuid              |           | not null | 
 course_offering_id | integer           |           | not null | 
 status             | enrollment_status |           | not null | 
Indexes:
    "pk_enrollments" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "fk_enrollments_course_offering_id_course_offerings" FOREIGN KEY (course_offering_id) REFERENCES course_offerings(id)
    "fk_enrollments_student_id_students" FOREIGN KEY (student_id) REFERENCES students(user_id)
Referenced by:
    TABLE "enrollment_sections" CONSTRAINT "fk_enrollment_sections_enrollment_id_enrollments" FOREIGN KEY (enrollment_id) REFERENCES enrollments(id)
    TABLE "student_scores" CONSTRAINT "fk_student_scores_enrollment_id_enrollments" FOREIGN KEY (enrollment_id) REFERENCES enrollments(id)

```

## Table: `student_transfer_history`

```sql
                                        Table "public.student_transfer_history"
     Column      |          Type          | Collation | Nullable |                       Default                        
-----------------+------------------------+-----------+----------+------------------------------------------------------
 id              | integer                |           | not null | nextval('student_transfer_history_id_seq'::regclass)
 student_id      | uuid                   |           | not null | 
 from_program_id | integer                |           | not null | 
 to_program_id   | integer                |           | not null | 
 transfer_date   | date                   |           | not null | 
 decree_number   | character varying(100) |           |          | 
Indexes:
    "pk_student_transfer_history" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "fk_student_transfer_history_from_program_id_programs" FOREIGN KEY (from_program_id) REFERENCES programs(id)
    "fk_student_transfer_history_student_id_students" FOREIGN KEY (student_id) REFERENCES students(user_id)
    "fk_student_transfer_history_to_program_id_programs" FOREIGN KEY (to_program_id) REFERENCES programs(id)

```

## Table: `course_prerequisites`

```sql
                                    Table "public.course_prerequisites"
         Column         |  Type   | Collation | Nullable |                     Default                      
------------------------+---------+-----------+----------+--------------------------------------------------
 id                     | integer |           | not null | nextval('course_prerequisites_id_seq'::regclass)
 course_id              | integer |           | not null | 
 prerequisite_course_id | integer |           | not null | 
 set_id                 | integer |           | not null | 
Indexes:
    "pk_course_prerequisites" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "fk_course_prerequisites_course_id_bylaw_courses" FOREIGN KEY (course_id) REFERENCES bylaw_courses(id)
    "fk_course_prerequisites_prerequisite_course_id_courses" FOREIGN KEY (prerequisite_course_id) REFERENCES courses(id)

```

## Table: `enrollment_sections`

```sql
                                Table "public.enrollment_sections"
    Column     |  Type   | Collation | Nullable |                     Default                     
---------------+---------+-----------+----------+-------------------------------------------------
 id            | integer |           | not null | nextval('enrollment_sections_id_seq'::regclass)
 enrollment_id | integer |           | not null | 
 section_id    | integer |           | not null | 
Indexes:
    "pk_enrollment_sections" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "fk_enrollment_sections_enrollment_id_enrollments" FOREIGN KEY (enrollment_id) REFERENCES enrollments(id)
    "fk_enrollment_sections_section_id_sections" FOREIGN KEY (section_id) REFERENCES sections(id)

```

## Table: `grade_distributions`

```sql
                                    Table "public.grade_distributions"
   Column    |       Type        | Collation | Nullable |                     Default                     
-------------+-------------------+-----------+----------+-------------------------------------------------
 id          | bigint            |           | not null | nextval('grade_distributions_id_seq'::regclass)
 offering_id | bigint            |           | not null | 
 name        | character varying |           | not null | 
 max_score   | numeric           |           | not null | 
 weight      | numeric           |           | not null | 
Indexes:
    "pk_grade_distributions" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "fk_grade_distributions_offering_id_course_offerings" FOREIGN KEY (offering_id) REFERENCES course_offerings(id)
Referenced by:
    TABLE "student_scores" CONSTRAINT "fk_student_scores_distribution_id_grade_distributions" FOREIGN KEY (distribution_id) REFERENCES grade_distributions(id)

```

## Table: `invoices`

```sql
                                  Table "public.invoices"
   Column    |      Type      | Collation | Nullable |               Default                
-------------+----------------+-----------+----------+--------------------------------------
 id          | bigint         |           | not null | nextval('invoices_id_seq'::regclass)
 student_id  | uuid           |           | not null | 
 semester_id | integer        |           | not null | 
 amount      | numeric        |           | not null | 
 status      | invoice_status |           | not null | 
Indexes:
    "pk_invoices" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "fk_invoices_semester_id_semesters" FOREIGN KEY (semester_id) REFERENCES semesters(id)
    "fk_invoices_student_id_students" FOREIGN KEY (student_id) REFERENCES students(user_id)
Referenced by:
    TABLE "payments" CONSTRAINT "fk_payments_invoice_id_invoices" FOREIGN KEY (invoice_id) REFERENCES invoices(id)

```

## Table: `payments`

```sql
                                    Table "public.payments"
    Column    |       Type        | Collation | Nullable |               Default                
--------------+-------------------+-----------+----------+--------------------------------------
 id           | bigint            |           | not null | nextval('payments_id_seq'::regclass)
 invoice_id   | bigint            |           | not null | 
 amount       | numeric           |           | not null | 
 method       | payment_method    |           | not null | 
 reference_id | character varying |           |          | 
Indexes:
    "pk_payments" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "fk_payments_invoice_id_invoices" FOREIGN KEY (invoice_id) REFERENCES invoices(id)

```

## Table: `student_scores`

```sql
                                 Table "public.student_scores"
     Column      |  Type   | Collation | Nullable |                  Default                   
-----------------+---------+-----------+----------+--------------------------------------------
 id              | bigint  |           | not null | nextval('student_scores_id_seq'::regclass)
 enrollment_id   | bigint  |           | not null | 
 distribution_id | bigint  |           | not null | 
 score           | numeric |           | not null | 
 grader_id       | uuid    |           | not null | 
Indexes:
    "pk_student_scores" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "fk_student_scores_distribution_id_grade_distributions" FOREIGN KEY (distribution_id) REFERENCES grade_distributions(id)
    "fk_student_scores_enrollment_id_enrollments" FOREIGN KEY (enrollment_id) REFERENCES enrollments(id)
    "fk_student_scores_grader_id_users" FOREIGN KEY (grader_id) REFERENCES users(id)

```

## Table: `audit_logs`

```sql
                                       Table "public.audit_logs"
   Column   |           Type           | Collation | Nullable |                Default                 
------------+--------------------------+-----------+----------+----------------------------------------
 id         | bigint                   |           | not null | nextval('audit_logs_id_seq'::regclass)
 user_id    | uuid                     |           |          | 
 action     | character varying(50)    |           | not null | 
 table_name | character varying(50)    |           | not null | 
 record_id  | character varying(50)    |           | not null | 
 changes    | jsonb                    |           |          | 
 ip_address | character varying(45)    |           |          | 
 timestamp  | timestamp with time zone |           | not null | now()
Indexes:
    "pk_audit_logs" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "fk_audit_logs_user_id_users" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL

```

## Table: `courses`

```sql
                                        Table "public.courses"
     Column     |          Type          | Collation | Nullable |               Default               
----------------+------------------------+-----------+----------+-------------------------------------
 id             | integer                |           | not null | nextval('courses_id_seq'::regclass)
 code           | character varying(20)  |           | not null | 
 name_ar        | character varying(100) |           | not null | 
 name_en        | character varying(100) |           | not null | 
 credit_hours   | integer                |           | not null | 
 lecture_hours  | integer                |           | not null | 
 lab_hours      | integer                |           | not null | 
 tutorial_hours | integer                |           | not null | 
Indexes:
    "pk_courses" PRIMARY KEY, btree (id)
    "uq_courses_code" UNIQUE CONSTRAINT, btree (code)
Referenced by:
    TABLE "bylaw_courses" CONSTRAINT "fk_bylaw_courses_course_id_courses" FOREIGN KEY (course_id) REFERENCES courses(id)
    TABLE "course_offerings" CONSTRAINT "fk_course_offerings_course_id_courses" FOREIGN KEY (course_id) REFERENCES courses(id)
    TABLE "course_prerequisites" CONSTRAINT "fk_course_prerequisites_prerequisite_course_id_courses" FOREIGN KEY (prerequisite_course_id) REFERENCES courses(id)

```

## Table: `course_offerings`

```sql
                                Table "public.course_offerings"
     Column     |  Type   | Collation | Nullable |                   Default                    
----------------+---------+-----------+----------+----------------------------------------------
 id             | integer |           | not null | nextval('course_offerings_id_seq'::regclass)
 course_id      | integer |           | not null | 
 semester_id    | integer |           | not null | 
 max_capacity   | integer |           | not null | 
 enrolled_count | integer |           | not null | 
Indexes:
    "pk_course_offerings" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "fk_course_offerings_course_id_courses" FOREIGN KEY (course_id) REFERENCES courses(id)
    "fk_course_offerings_semester_id_semesters" FOREIGN KEY (semester_id) REFERENCES semesters(id)
Referenced by:
    TABLE "enrollments" CONSTRAINT "fk_enrollments_course_offering_id_course_offerings" FOREIGN KEY (course_offering_id) REFERENCES course_offerings(id)
    TABLE "grade_distributions" CONSTRAINT "fk_grade_distributions_offering_id_course_offerings" FOREIGN KEY (offering_id) REFERENCES course_offerings(id)
    TABLE "sections" CONSTRAINT "fk_sections_course_offering_id_course_offerings" FOREIGN KEY (course_offering_id) REFERENCES course_offerings(id)

```

## Table: `semesters`

```sql
                                           Table "public.semesters"
       Column        |           Type           | Collation | Nullable |                Default                
---------------------+--------------------------+-----------+----------+---------------------------------------
 id                  | integer                  |           | not null | nextval('semesters_id_seq'::regclass)
 name_ar             | character varying(100)   |           | not null | 
 name_en             | character varying(100)   |           | not null | 
 start_date          | timestamp with time zone |           | not null | 
 end_date            | timestamp with time zone |           | not null | 
 registration_status | registration_status      |           | not null | 
Indexes:
    "pk_semesters" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "course_offerings" CONSTRAINT "fk_course_offerings_semester_id_semesters" FOREIGN KEY (semester_id) REFERENCES semesters(id)
    TABLE "invoices" CONSTRAINT "fk_invoices_semester_id_semesters" FOREIGN KEY (semester_id) REFERENCES semesters(id)

```

## Table: `users`

```sql
                              Table "public.users"
       Column        |           Type           | Collation | Nullable | Default 
---------------------+--------------------------+-----------+----------+---------
 national_id         | character varying(14)    |           | not null | 
 university_email    | character varying        |           | not null | 
 personal_email      | character varying        |           |          | 
 hashed_password     | character varying        |           | not null | 
 profile_picture_url | character varying        |           |          | 
 is_active           | boolean                  |           | not null | 
 is_verified         | boolean                  |           | not null | 
 created_at          | timestamp with time zone |           | not null | now()
 updated_at          | timestamp with time zone |           | not null | now()
 id                  | uuid                     |           | not null | 
 first_name_ar       | character varying(50)    |           | not null | 
 second_name_ar      | character varying(50)    |           | not null | 
 third_name_ar       | character varying(50)    |           | not null | 
 fourth_name_ar      | character varying(50)    |           | not null | 
 family_name_ar      | character varying(50)    |           | not null | 
 first_name_en       | character varying(50)    |           | not null | 
 second_name_en      | character varying(50)    |           | not null | 
 third_name_en       | character varying(50)    |           | not null | 
 fourth_name_en      | character varying(50)    |           | not null | 
 family_name_en      | character varying(50)    |           | not null | 
Indexes:
    "pk_users" PRIMARY KEY, btree (id)
    "ix_users_national_id" UNIQUE, btree (national_id)
    "ix_users_university_email" UNIQUE, btree (university_email)
Referenced by:
    TABLE "audit_logs" CONSTRAINT "fk_audit_logs_user_id_users" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
    TABLE "student_scores" CONSTRAINT "fk_student_scores_grader_id_users" FOREIGN KEY (grader_id) REFERENCES users(id)
    TABLE "students" CONSTRAINT "fk_students_user_id_users" FOREIGN KEY (user_id) REFERENCES users(id)
    TABLE "user_roles" CONSTRAINT "fk_user_roles_user_id_users" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE

```

## Table: `departments`

```sql
                                    Table "public.departments"
 Column  |          Type          | Collation | Nullable |                 Default                 
---------+------------------------+-----------+----------+-----------------------------------------
 id      | integer                |           | not null | nextval('departments_id_seq'::regclass)
 name_ar | character varying(100) |           | not null | 
 name_en | character varying(100) |           | not null | 
 code    | character varying(10)  |           | not null | 
Indexes:
    "pk_departments" PRIMARY KEY, btree (id)
    "uq_departments_code" UNIQUE CONSTRAINT, btree (code)
Referenced by:
    TABLE "programs" CONSTRAINT "fk_programs_department_id_departments" FOREIGN KEY (department_id) REFERENCES departments(id)

```

## Table: `programs`

```sql
                                       Table "public.programs"
    Column     |          Type          | Collation | Nullable |               Default                
---------------+------------------------+-----------+----------+--------------------------------------
 id            | integer                |           | not null | nextval('programs_id_seq'::regclass)
 name_ar       | character varying(100) |           | not null | 
 name_en       | character varying(100) |           | not null | 
 code          | character varying(10)  |           | not null | 
 department_id | integer                |           | not null | 
 type          | program_type           |           | not null | 
Indexes:
    "pk_programs" PRIMARY KEY, btree (id)
    "uq_programs_code" UNIQUE CONSTRAINT, btree (code)
Foreign-key constraints:
    "fk_programs_department_id_departments" FOREIGN KEY (department_id) REFERENCES departments(id)
Referenced by:
    TABLE "concentrations" CONSTRAINT "fk_concentrations_program_id_programs" FOREIGN KEY (program_id) REFERENCES programs(id)
    TABLE "elective_groups" CONSTRAINT "fk_elective_groups_program_id_programs" FOREIGN KEY (program_id) REFERENCES programs(id)
    TABLE "program_bylaws" CONSTRAINT "fk_program_bylaws_program_id_programs" FOREIGN KEY (program_id) REFERENCES programs(id)
    TABLE "student_transfer_history" CONSTRAINT "fk_student_transfer_history_from_program_id_programs" FOREIGN KEY (from_program_id) REFERENCES programs(id)
    TABLE "student_transfer_history" CONSTRAINT "fk_student_transfer_history_to_program_id_programs" FOREIGN KEY (to_program_id) REFERENCES programs(id)
    TABLE "students" CONSTRAINT "fk_students_program_id_programs" FOREIGN KEY (program_id) REFERENCES programs(id)

```

## Table: `permissions`

```sql
                                      Table "public.permissions"
   Column    |          Type          | Collation | Nullable |                 Default                 
-------------+------------------------+-----------+----------+-----------------------------------------
 id          | integer                |           | not null | nextval('permissions_id_seq'::regclass)
 slug        | character varying(100) |           | not null | 
 description | text                   |           |          | 
Indexes:
    "pk_permissions" PRIMARY KEY, btree (id)
    "ix_permissions_slug" UNIQUE, btree (slug)
Referenced by:
    TABLE "role_permissions" CONSTRAINT "fk_role_permissions_permission_id_permissions" FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE

```

## Table: `role_permissions`

```sql
             Table "public.role_permissions"
    Column     |  Type   | Collation | Nullable | Default 
---------------+---------+-----------+----------+---------
 role_id       | integer |           | not null | 
 permission_id | integer |           | not null | 
Indexes:
    "pk_role_permissions" PRIMARY KEY, btree (role_id, permission_id)
Foreign-key constraints:
    "fk_role_permissions_permission_id_permissions" FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE
    "fk_role_permissions_role_id_roles" FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE

```

## Table: `user_roles`

```sql
             Table "public.user_roles"
 Column  |  Type   | Collation | Nullable | Default 
---------+---------+-----------+----------+---------
 user_id | uuid    |           | not null | 
 role_id | integer |           | not null | 
Indexes:
    "pk_user_roles" PRIMARY KEY, btree (user_id, role_id)
Foreign-key constraints:
    "fk_user_roles_role_id_roles" FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
    "fk_user_roles_user_id_users" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE

```

## Table: `concentrations`

```sql
                                         Table "public.concentrations"
      Column      |          Type          | Collation | Nullable |                  Default                   
------------------+------------------------+-----------+----------+--------------------------------------------
 id               | integer                |           | not null | nextval('concentrations_id_seq'::regclass)
 name_ar          | character varying(100) |           | not null | 
 name_en          | character varying(100) |           | not null | 
 min_level        | integer                |           | not null | 
 min_credit_hours | integer                |           |          | 
 program_id       | integer                |           | not null | 
Indexes:
    "pk_concentrations" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "fk_concentrations_program_id_programs" FOREIGN KEY (program_id) REFERENCES programs(id)
Referenced by:
    TABLE "bylaw_courses" CONSTRAINT "fk_bylaw_courses_concentration_id_concentrations" FOREIGN KEY (concentration_id) REFERENCES concentrations(id)
    TABLE "students" CONSTRAINT "fk_students_concetration_id_concentrations" FOREIGN KEY (concetration_id) REFERENCES concentrations(id)

```

## Table: `faculty_bylaws`

```sql
                                      Table "public.faculty_bylaws"
   Column   |          Type          | Collation | Nullable |                  Default                   
------------+------------------------+-----------+----------+--------------------------------------------
 id         | integer                |           | not null | nextval('faculty_bylaws_id_seq'::regclass)
 name       | character varying(200) |           | not null | 
 issue_year | integer                |           | not null | 
Indexes:
    "pk_faculty_bylaws" PRIMARY KEY, btree (id)
    "uq_faculty_bylaws_name" UNIQUE CONSTRAINT, btree (name)
Referenced by:
    TABLE "program_bylaws" CONSTRAINT "fk_program_bylaws_bylaw_id_faculty_bylaws" FOREIGN KEY (bylaw_id) REFERENCES faculty_bylaws(id)

```

## Table: `program_bylaws`

```sql
                                  Table "public.program_bylaws"
       Column       |  Type   | Collation | Nullable |                  Default                   
--------------------+---------+-----------+----------+--------------------------------------------
 id                 | integer |           | not null | nextval('program_bylaws_id_seq'::regclass)
 program_id         | integer |           | not null | 
 bylaw_id           | integer |           | not null | 
 total_credit_hours | integer |           | not null | 
Indexes:
    "pk_program_bylaws" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "fk_program_bylaws_bylaw_id_faculty_bylaws" FOREIGN KEY (bylaw_id) REFERENCES faculty_bylaws(id)
    "fk_program_bylaws_program_id_programs" FOREIGN KEY (program_id) REFERENCES programs(id)
Referenced by:
    TABLE "bylaw_courses" CONSTRAINT "fk_bylaw_courses_bylaw_id_program_bylaws" FOREIGN KEY (bylaw_id) REFERENCES program_bylaws(id)
    TABLE "elective_groups" CONSTRAINT "fk_elective_groups_bylaw_id_program_bylaws" FOREIGN KEY (bylaw_id) REFERENCES program_bylaws(id)
    TABLE "students" CONSTRAINT "fk_students_bylaw_id_program_bylaws" FOREIGN KEY (bylaw_id) REFERENCES program_bylaws(id)

```

## Table: `sections`

```sql
                                          Table "public.sections"
       Column       |          Type          | Collation | Nullable |               Default                
--------------------+------------------------+-----------+----------+--------------------------------------
 id                 | integer                |           | not null | nextval('sections_id_seq'::regclass)
 course_offering_id | integer                |           | not null | 
 name_ar            | character varying(255) |           | not null | 
 name_en            | character varying(255) |           | not null | 
 type               | section_type           |           | not null | 
 day                | day_of_week            |           | not null | 
 start_time         | time without time zone |           | not null | 
 end_time           | time without time zone |           | not null | 
 location_id        | integer                |           | not null | 
 capacity           | integer                |           | not null | 
Indexes:
    "pk_sections" PRIMARY KEY, btree (id)
    "uq_section_location_time" UNIQUE CONSTRAINT, btree (location_id, day, start_time, end_time)
Foreign-key constraints:
    "fk_sections_course_offering_id_course_offerings" FOREIGN KEY (course_offering_id) REFERENCES course_offerings(id)
    "fk_sections_location_id_locations" FOREIGN KEY (location_id) REFERENCES locations(id)
Referenced by:
    TABLE "enrollment_sections" CONSTRAINT "fk_enrollment_sections_section_id_sections" FOREIGN KEY (section_id) REFERENCES sections(id)

```

## Table: `locations`

```sql
                                    Table "public.locations"
 Column  |          Type          | Collation | Nullable |                Default                
---------+------------------------+-----------+----------+---------------------------------------
 id      | integer                |           | not null | nextval('locations_id_seq'::regclass)
 name_ar | character varying(255) |           | not null | 
 name_en | character varying(255) |           | not null | 
Indexes:
    "pk_locations" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "sections" CONSTRAINT "fk_sections_location_id_locations" FOREIGN KEY (location_id) REFERENCES locations(id)

```

## Table: `elective_groups`

```sql
                                           Table "public.elective_groups"
        Column         |          Type          | Collation | Nullable |                   Default                   
-----------------------+------------------------+-----------+----------+---------------------------------------------
 id                    | integer                |           | not null | nextval('elective_groups_id_seq'::regclass)
 name_ar               | character varying(100) |           | not null | 
 name_en               | character varying(100) |           | not null | 
 program_id            | integer                |           |          | 
 bylaw_id              | integer                |           | not null | 
 required_credit_hours | integer                |           | not null | 
 min_courses           | integer                |           |          | 
Indexes:
    "pk_elective_groups" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "fk_elective_groups_bylaw_id_program_bylaws" FOREIGN KEY (bylaw_id) REFERENCES program_bylaws(id)
    "fk_elective_groups_program_id_programs" FOREIGN KEY (program_id) REFERENCES programs(id)
Referenced by:
    TABLE "bylaw_courses" CONSTRAINT "fk_bylaw_courses_elective_group_id_elective_groups" FOREIGN KEY (elective_group_id) REFERENCES elective_groups(id)

```

## Table: `roles`

```sql
                                      Table "public.roles"
   Column    |         Type          | Collation | Nullable |              Default              
-------------+-----------------------+-----------+----------+-----------------------------------
 id          | integer               |           | not null | nextval('roles_id_seq'::regclass)
 slug        | character varying(50) |           | not null | 
 description | text                  |           |          | 
 name_ar     | character varying(50) |           | not null | 
 name_en     | character varying(50) |           | not null | 
Indexes:
    "pk_roles" PRIMARY KEY, btree (id)
    "ix_roles_slug" UNIQUE, btree (slug)
    "uq_roles_name_ar" UNIQUE CONSTRAINT, btree (name_ar)
    "uq_roles_name_en" UNIQUE CONSTRAINT, btree (name_en)
Referenced by:
    TABLE "role_permissions" CONSTRAINT "fk_role_permissions_role_id_roles" FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
    TABLE "user_roles" CONSTRAINT "fk_user_roles_role_id_roles" FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE

```

## Table: `students`

```sql
                             Table "public.students"
         Column         |          Type          | Collation | Nullable | Default 
------------------------+------------------------+-----------+----------+---------
 user_id                | uuid                   |           | not null | 
 student_code           | character varying(50)  |           | not null | 
 program_id             | integer                |           | not null | 
 bylaw_id               | integer                |           | not null | 
 concetration_id        | integer                |           |          | 
 level                  | integer                |           | not null | 
 gpa                    | numeric(3,2)           |           |          | 
 earned_credits         | integer                |           | not null | 
 status                 | student_status         |           | not null | 
 gender                 | gender                 |           | not null | 
 religion               | religion               |           |          | 
 nationality            | character varying(100) |           |          | 
 date_of_birth          | date                   |           |          | 
 place_of_birth         | character varying(255) |           |          | 
 national_id_issue_date | date                   |           |          | 
 gov_address            | text                   |           |          | 
 current_address        | text                   |           |          | 
 city                   | character varying(100) |           |          | 
 governorate            | character varying(100) |           |          | 
 landline_phone         | character varying(20)  |           |          | 
 guardian_name          | character varying(255) |           |          | 
 guardian_relation      | character varying(100) |           |          | 
 guardian_job           | character varying(255) |           |          | 
 guardian_phone         | character varying(20)  |           |          | 
 guardian_national_id   | character varying(20)  |           |          | 
 military_status        | military_status        |           |          | 
 military_number        | character varying(50)  |           |          | 
Indexes:
    "pk_students" PRIMARY KEY, btree (user_id)
    "uq_students_student_code" UNIQUE CONSTRAINT, btree (student_code)
Foreign-key constraints:
    "fk_students_bylaw_id_program_bylaws" FOREIGN KEY (bylaw_id) REFERENCES program_bylaws(id)
    "fk_students_concetration_id_concentrations" FOREIGN KEY (concetration_id) REFERENCES concentrations(id)
    "fk_students_program_id_programs" FOREIGN KEY (program_id) REFERENCES programs(id)
    "fk_students_user_id_users" FOREIGN KEY (user_id) REFERENCES users(id)
Referenced by:
    TABLE "enrollments" CONSTRAINT "fk_enrollments_student_id_students" FOREIGN KEY (student_id) REFERENCES students(user_id)
    TABLE "invoices" CONSTRAINT "fk_invoices_student_id_students" FOREIGN KEY (student_id) REFERENCES students(user_id)
    TABLE "student_transfer_history" CONSTRAINT "fk_student_transfer_history_student_id_students" FOREIGN KEY (student_id) REFERENCES students(user_id)

```

## Table: `bylaw_courses`

```sql
                                  Table "public.bylaw_courses"
       Column       |  Type   | Collation | Nullable |                  Default                  
--------------------+---------+-----------+----------+-------------------------------------------
 id                 | integer |           | not null | nextval('bylaw_courses_id_seq'::regclass)
 bylaw_id           | integer |           | not null | 
 course_id          | integer |           | not null | 
 concentration_id   | integer |           |          | 
 semester_suggested | integer |           |          | 
 is_elective        | boolean |           | not null | 
 elective_group_id  | integer |           |          | 
Indexes:
    "pk_bylaw_courses" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "fk_bylaw_courses_bylaw_id_program_bylaws" FOREIGN KEY (bylaw_id) REFERENCES program_bylaws(id)
    "fk_bylaw_courses_concentration_id_concentrations" FOREIGN KEY (concentration_id) REFERENCES concentrations(id)
    "fk_bylaw_courses_course_id_courses" FOREIGN KEY (course_id) REFERENCES courses(id)
    "fk_bylaw_courses_elective_group_id_elective_groups" FOREIGN KEY (elective_group_id) REFERENCES elective_groups(id)
Referenced by:
    TABLE "course_prerequisites" CONSTRAINT "fk_course_prerequisites_course_id_bylaw_courses" FOREIGN KEY (course_id) REFERENCES bylaw_courses(id)

```

