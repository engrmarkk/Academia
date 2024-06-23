from extensions import db
from functools import wraps
from .students import code_generator
from datetime import datetime
from flask_login import UserMixin
from passlib.hash import pbkdf2_sha256
from utils import hexid
from sqlalchemy import desc


def generate_admin_id():
    return code_generator(f"ADMIN-{datetime.now().year}-")


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.String(50), default=hexid, primary_key=True, index=True)
    name = db.Column(db.String(255))

    admin = db.relationship("Admin", backref="role", cascade="all, delete", lazy=True)

    def __repr__(self):
        return f"Role('{self.name}')"


class Admin(db.Model, UserMixin):
    __tablename__ = "admin"
    # The id column is the primary key
    id = db.Column(db.String(50), default=hexid, primary_key=True, index=True)
    # the first_name and last_name columns are not nullable
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean, default=True)
    # the adm_id column is unique and not nullable
    # the default value is a function that generates a unique code
    adm_id = db.Column(
        db.String(50), unique=True, nullable=False, default=generate_admin_id
    )
    # the email column is unique and not nullable
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_superadmin = db.Column(db.Boolean, default=False)
    phone_number = db.Column(db.String(50), nullable=True)
    role_id = db.Column(db.String(50), db.ForeignKey("role.id"), nullable=False)
    # the password column is not nullable
    password = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    courses = db.relationship(
        "Course", cascade="all, delete", backref="lecturer", lazy=True
    )

    # The __repr__ method is used to print the object
    def __repr__(self):
        return "<Admin %r>" % self.email


# This decorator is used to check if the logged-in user is an admin
# def admin_required(func):
#     # This wraps the function to be decorated
#     @wraps(func)
#     # This is the wrapper function
#     def wrapper(*args, **kwargs):
#         # Get the logged-in user
#         logged_user = get_jwt_identity()
#         # Check if the logged-in user is an admin
#         if not logged_user.startswith('ADMIN'):
#             # If not, return an error
#             abort(401, message="Admin access required")
#         return func(*args, **kwargs)
#     return wrapper


roles = ["lecturer", "admin", "ict", "dean", "hod"]


# propagate data inside the role table
def add_roles():
    for role in roles:
        new_role = Role(name=role)
        db.session.add(new_role)
    db.session.commit()
    return True


def get_roles():
    print("getting roles")
    roles = Role.query.all()
    if not roles:
        add_roles()
        roles = Role.query.all()
    return [{"id": role.id, "name": role.name} for role in roles]


# def create_admin():
#     admin = Admin(
#         first_name="Olawale",
#         last_name="Michael",
#         email="admin@localhost",
#         password=pbkdf2_sha256.hash("admin"),
#         is_superadmin=True,
#         role_id=Role.query.filter_by(name="admin").first().id
#     )
#     db.session.add(admin)
#     db.session.commit()
#     return True


# get admins
def get_admins(page, per_page, role):
    admins = Admin.query.filter(
        (Admin.role_id == role) if (role and role != "all") else True
    ).order_by(desc(Admin.date_created)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    total_pages = admins.pages
    total_items = admins.total
    return (
        [
            {
                "id": admin.id,
                "first_name": admin.first_name,
                "last_name": admin.last_name,
                "email": admin.email,
                "phone_number": admin.phone_number,
                "role": admin.role.name,
                "is_superadmin": admin.is_superadmin,
                "adm_id": admin.adm_id,
                "date_created": admin.date_created.strftime("%d %b, %Y"),
                "time_created": admin.date_created.strftime("%I:%M %p"),
                "courses_assigned": len(admin.courses),
                "courses": admin.courses
            }
            for admin in admins.items
        ],
        total_pages,
        total_items,
    )


# get admins that are lecturers by role
def get_lecturers():
    admin_lecturers = Admin.query.join(Role).filter(Role.name == "lecturer").all()
    return [
        {
            "id": admin.id,
            "first_name": admin.first_name,
            "last_name": admin.last_name,
            "email": admin.email,
        }
        for admin in admin_lecturers
    ]
