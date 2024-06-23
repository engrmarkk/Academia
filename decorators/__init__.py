# import for decorators
from functools import wraps
from models import Admin, Student
from flask import request, redirect, url_for, session
from flask_login import login_user, logout_user, current_user


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        admin_user = Admin.query.filter_by(id=current_user.id).first()
        # get previous endpoint
        # previous_endpoint = request.referrer
        # print(previous_endpoint, "previous endpoint")
        if not admin_user:
            session["alert"] = "You cannot access this page"
            session["bg_color"] = "danger"
            return redirect(url_for("student.student_dashboard"))
        return func(*args, **kwargs)

    return wrapper


# student required
def student_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        student_user = Student.query.filter_by(id=current_user.id).first()
        if not student_user:
            session["alert"] = "You cannot access this page"
            session["bg_color"] = "danger"
            return redirect(url_for("admin.admin_dashboard"))
        return func(*args, **kwargs)

    return wrapper


# check if authenticated
def check_authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            student_user = Student.query.filter_by(id=current_user.id).first()
            if student_user:
                session["alert"] = "You cannot access this page"
                session["bg_color"] = "danger"
                return redirect(url_for("student.student_dashboard"))
            admin = Admin.query.filter_by(id=current_user.id).first()
            if admin:
                session["alert"] = "You cannot access this page"
                session["bg_color"] = "danger"
                return redirect(url_for("admin.admin_dashboard"))
        return func(*args, **kwargs)

    return wrapper
