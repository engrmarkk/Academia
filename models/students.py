from functools import wraps
from extensions import db
from passlib.hash import pbkdf2_sha256
import random
from datetime import datetime
from flask_login import UserMixin
from utils import hexid
from sqlalchemy import desc
from .course_registered import CourseRegistered


# function to hash the default password
# it takes the default password as an argument
def student_default_password(default_password):
    # hash the default password
    pass_word = pbkdf2_sha256.hash(default_password)
    # return the hashed password
    return pass_word


# function to generate a unique code
def code_generator(prefix: str):
    # generate a random number
    unique_code = random.randint(100000, 999999)
    # convert the random number to a string
    unique_code = str(unique_code)
    # concatenate the prefix and the random number
    # the prefix is an argument passed to the function
    mat_num = prefix + unique_code
    # return the unique code
    return mat_num


# This is the model for the students
class Student(db.Model, UserMixin):
    __tablename__ = "students"
    # The id column is the primary key
    id = db.Column(db.String(50), default=hexid, primary_key=True, index=True)
    # the first_name column
    first_name = db.Column(db.String(80), nullable=False)
    # the last_name column
    last_name = db.Column(db.String(80), nullable=False)
    # the email column is unique and not nullable
    email = db.Column(db.String(120), unique=True, nullable=False)
    # student phone number
    phone = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean, default=True)
    # student_id column is unique and not nullable, this is the student's matriculation number
    # the default value is a function that generates a unique code with the prefix 'ACA' and the current year
    stud_id = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
        default=code_generator(f"ACA-{datetime.now().year}-"),
    )
    # the gpa column is not nullable, the default value is 0.00
    gpa = db.Column(db.Float, nullable=False, default=0.00)
    # the password column is not nullable, the default value is a function that hashes the default password
    # the default password is the argument passed to the function
    password = db.Column(
        db.Text, nullable=False, default=student_default_password("academia")
    )
    # the changed_password column is not nullable, the default value is False
    # this column is used to check if the student has changed the default password
    changed_password = db.Column(db.Boolean, nullable=False, default=False)
    # date
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # the registered_courses column is a relationship with the CourseRegistered model
    registered_courses = db.relationship(
        "CourseRegistered", cascade="all, delete", backref="student", lazy=True
    )

    # The __repr__ method is used to print the object
    def __repr__(self):
        return "<User %r>" % self.email


# This decorator is used to check if the logged-in user is a student
# def student_required(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         # Get the logged-in user
#         logged_user = get_jwt_identity()
#         # Check if the logged-in user is a student
#         if not logged_user.startswith('ACA'):
#             # If not, return an error
#             abort(401, message="This is students arena")
#         return func(*args, **kwargs)
#     return wrapper


# get all students
def get_students(matric_no, course_id, page, per_page):
    query = Student.query
    if course_id:
        query = query.join(CourseRegistered).filter(CourseRegistered.course_id.like(f"%{course_id}%"))
    if matric_no:
        query = query.filter(Student.stud_id.like(f"%{matric_no}%"))

    students = query.order_by(desc(Student.created_at)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    total_pages = students.pages
    total_items = students.total
    return (
        [
            {
                "id": student.id,
                "first_name": student.first_name,
                "last_name": student.last_name,
                "email": student.email,
                "phone": student.phone,
                "stud_id": student.stud_id,
                "active": student.active,
                "courses_registered": len(student.registered_courses),
            }
            for student in students.items
        ],
        total_pages,
        total_items,
    )


# add students
def add_student(first_name, last_name, email, phone):
    try:
        student = Student(
            first_name=first_name, last_name=last_name, email=email.lower(), phone=phone
        )
        db.session.add(student)
        db.session.commit()
        return True
    except Exception as e:
        print(e, "error@add_student")
        db.session.rollback()
        return False


# email exist
def email_exist(email):
    return Student.query.filter_by(email=email).first()


# phone exist
def phone_exist(phone):
    return Student.query.filter_by(phone=phone).first()


# get recent 5students
def get_recent_students():
    students = Student.query.order_by(desc(Student.created_at)).limit(5).all()
    return [
        {
            "id": student.id,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "email": student.email,
            "phone": student.phone,
            "stud_id": student.stud_id,
            "date": student.created_at.strftime("%d %b, %Y"),
            "time": student.created_at.strftime("%I:%M %p"),
        }
        for student in students
    ]
