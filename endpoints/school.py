from flask import Blueprint, render_template, redirect, url_for, session, request
from models import (
    Admin,
    get_roles,
    Student,
    # create_admin
)
from flask_login import login_required, current_user, login_user, logout_user
from passlib.hash import pbkdf2_sha256 as hasher
from decorators import check_authenticated


school = Blueprint("school", __name__)


@school.route("/", methods=["GET"])
@check_authenticated
def landing_page():
    # print(get_roles())
    # print(create_admin())
    alert = session.pop("alert", None)
    bg_color = session.pop("bg_color", None)
    return render_template("index.html", alert=alert, bg_color=bg_color)


@school.route("/login", methods=["GET", "POST"])
@check_authenticated
def login():
    alert = session.pop("alert", None)
    bg_color = session.pop("bg_color", None)

    if request.method == "POST":
        login_code = request.form.get("login_code")
        password = request.form.get("password")

        if not login_code or not password:
            alert = "Please fill all the fields"
            bg_color = "danger"
            return render_template(
                "login.html",
                alert=alert,
                bg_color=bg_color,
                login_code=login_code,
                password=password,
            )

        user, user_type = (
            (Admin.query.filter_by(adm_id=login_code).first(), "admin")
            if login_code.startswith("ADMIN")
            else (Student.query.filter_by(stud_id=login_code).first(), "student")
        )

        if user and hasher.verify(password, user.password):
            if not user.active:
                alert = "Your account has been suspended"
                bg_color = "danger"
                return render_template(
                    "login.html",
                    alert=alert,
                    bg_color=bg_color,
                    login_code=login_code,
                    password=password,
                )
            session["alert"] = "Login successful"
            session["bg_color"] = "success"
            login_user(user)
            if user_type == "admin":
                return redirect(url_for("admin.admin_dashboard"))
            return redirect(url_for("student.student_dashboard"))
        alert = "Invalid login code or password"
        bg_color = "danger"
        return render_template(
            "login.html",
            alert=alert,
            bg_color=bg_color,
            login_code=login_code,
            password=password,
        )
    return render_template("login.html", alert=alert, bg_color=bg_color)


@school.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("school.landing_page"))
