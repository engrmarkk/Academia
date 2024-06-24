from flask import Blueprint, render_template, redirect, url_for, session, request
from flask_login import login_required, current_user
from models import (
    get_roles,
    Admin,
    get_admins,
    get_students,
    get_lecturers,
    create_course,
    get_courses,
    Course,
    add_student,
    email_exist,
    phone_exist,
    Student,
    CourseRegistered,
    get_recent_students,
)
from passlib.hash import pbkdf2_sha256 as hasher
from extensions import db
from utils import is_valid_email, get_grade, calculate_gpa
from decorators import admin_required, super_admin_required

admin = Blueprint("admin", __name__)


# ADMIN-2024-660252


@admin.route("/admin", methods=["GET"])
def get_admin():
    return render_template("index.html")


# student_quarters
@admin.route("/student_quarters", methods=["GET", "POST"])
@login_required
@admin_required
def student_quarters():
    try:
        alert = session.pop("alert", None)
        bg_color = session.pop("bg_color", None)
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 5))
        matric_no = request.args.get("matric_no")
        course_id = request.args.get("course_id")
        print(matric_no, ":", course_id)
        all_students, total_pages, total_items = get_students(matric_no, course_id, page, per_page)
        all_courses = Course.query.all()

        reset_filter = False if not (matric_no or course_id) else True
        if request.method == "POST":
            first_name = request.form.get("fname")
            last_name = request.form.get("lname")
            email = request.form.get("email")
            phone_number = request.form.get("phone")

            if not first_name or not last_name or not email or not phone_number:
                alert = "Please fill all the fields"
                bg_color = "danger"
                return render_template(
                    "admin_templates/student_quarters.html",
                    alert=alert,
                    bg_color=bg_color,
                    student_quarters=True,
                    all_students=all_students,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number,
                    page=page,
                    per_page=per_page,
                    total_pages=total_pages,
                    total_items=total_items,
                    all_courses=all_courses,
                    reset_filter=reset_filter,
                    matric_no=matric_no,
                    course_id=course_id
                )
            if not is_valid_email(email):
                alert = "Invalid email address"
                bg_color = "danger"
                return render_template(
                    "admin_templates/student_quarters.html",
                    alert=alert,
                    bg_color=bg_color,
                    student_quarters=True,
                    all_students=all_students,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number,
                    page=page,
                    per_page=per_page,
                    total_pages=total_pages,
                    total_items=total_items,
                    all_courses=all_courses,
                    reset_filter=reset_filter,
                    matric_no=matric_no,
                    course_id=course_id
                )
            if len(phone_number) != 11 or phone_number[0] != "0":
                alert = "Invalid phone number"
                bg_color = "danger"
                return render_template(
                    "admin_templates/student_quarters.html",
                    alert=alert,
                    bg_color=bg_color,
                    student_quarters=True,
                    all_students=all_students,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number,
                    page=page,
                    per_page=per_page,
                    total_pages=total_pages,
                    total_items=total_items,
                    all_courses=all_courses,
                    reset_filter=reset_filter,
                    matric_no=matric_no,
                    course_id=course_id
                )
            phone = f"+234{phone_number[1:]}"
            if email_exist(email):
                alert = "Email already exist"
                bg_color = "danger"
                return render_template(
                    "admin_templates/student_quarters.html",
                    alert=alert,
                    bg_color=bg_color,
                    student_quarters=True,
                    all_students=all_students,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number,
                    page=page,
                    per_page=per_page,
                    total_pages=total_pages,
                    total_items=total_items,
                    all_courses=all_courses,
                    reset_filter=reset_filter,
                    matric_no=matric_no,
                    course_id=course_id
                )
            if phone_exist(phone):
                alert = "Phone number already exist"
                bg_color = "danger"
                return render_template(
                    "admin_templates/student_quarters.html",
                    alert=alert,
                    bg_color=bg_color,
                    student_quarters=True,
                    all_students=all_students,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number,
                    page=page,
                    per_page=per_page,
                    total_pages=total_pages,
                    total_items=total_items,
                    all_courses=all_courses,
                    reset_filter=reset_filter,
                    matric_no=matric_no,
                    course_id=course_id
                )
            res = add_student(first_name, last_name, email, phone)
            if res:
                session["alert"] = "Student added successfully"
                session["bg_color"] = "success"
                return redirect(url_for("admin.student_quarters"))
            else:
                alert = "Error adding student"
                bg_color = "danger"
                return render_template(
                    "admin_templates/student_quarters.html",
                    alert=alert,
                    bg_color=bg_color,
                    student_quarters=True,
                    all_students=all_students,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number,
                    page=page,
                    per_page=per_page,
                    total_pages=total_pages,
                    total_items=total_items,
                    all_courses=all_courses,
                    reset_filter=reset_filter,
                    matric_no=matric_no,
                    course_id=course_id
                )
        return render_template(
            "admin_templates/student_quarters.html",
            alert=alert,
            bg_color=bg_color,
            student_quarters=True,
            all_students=all_students,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
            total_items=total_items,
            all_courses=all_courses,
            reset_filter=reset_filter,
            matric_no=matric_no,
            course_id=course_id
        )
    except Exception as e:
        print(e, "error@admin/student_quarters")
        session["alert"] = "NetworkError"
        session["bg_color"] = "danger"
        return redirect(url_for("admin.student_quarters"))


@admin.route("/admin_dashboard", methods=["GET"])
@login_required
@admin_required
def admin_dashboard():
    alert = session.pop("alert", None)
    bg_color = session.pop("bg_color", None)
    students = get_recent_students()
    return render_template(
        "admin_templates/home.html",
        alert=alert,
        bg_color=bg_color,
        admin_dashboard=True,
        students=students,
    )


# teams
@admin.route("/teams", methods=["GET", "POST"])
@login_required
@admin_required
@super_admin_required
def teams():
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 5))
        role = request.args.get("role")
        alert = session.pop("alert", None)
        bg_color = session.pop("bg_color", None)
        roles = get_roles()
        teams_list, total_pages, total_items = get_admins(page, per_page, role)
        if request.method == "POST":
            first_name = request.form.get("fname")
            last_name = request.form.get("lname")
            email = request.form.get("email")
            phone_number = request.form.get("phone")
            role = request.form.get("role")
            is_superadmin = request.form.get("is_superadmin")

            if (
                not first_name
                or not last_name
                or not email
                or not phone_number
                or not role
            ):
                alert = "Please fill all the fields"
                bg_color = "danger"
                return render_template(
                    "admin_templates/teams.html",
                    alert=alert,
                    bg_color=bg_color,
                    teams=True,
                    roles=roles,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number,
                    selected_role=role,
                    is_superadmin=is_superadmin,
                    total_pages=total_pages,
                    total_items=total_items,
                    page=page,
                    per_page=per_page,
                    teams_lists=teams_list,
                )

            if not is_valid_email(email):
                alert = "Invalid email"
                bg_color = "danger"
                return render_template(
                    "admin_templates/teams.html",
                    alert=alert,
                    bg_color=bg_color,
                    teams=True,
                    roles=roles,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number,
                    selected_role=role,
                    is_superadmin=is_superadmin,
                    total_pages=total_pages,
                    total_items=total_items,
                    teams_lists=teams_list,
                )

            email_exist = Admin.query.filter_by(email=email.lower()).first()
            if email_exist:
                alert = "Email already exist"
                bg_color = "danger"
                return render_template(
                    "admin_templates/teams.html",
                    alert=alert,
                    bg_color=bg_color,
                    teams=True,
                    roles=roles,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number,
                    selected_role=role,
                    is_superadmin=is_superadmin,
                    total_pages=total_pages,
                    total_items=total_items,
                    teams_lists=teams_list,
                    page=page,
                    per_page=per_page,
                )

            phone_exist = Admin.query.filter_by(phone_number=phone_number).first()
            if phone_exist:
                alert = "Phone number already exist"
                bg_color = "danger"
                return render_template(
                    "admin_templates/teams.html",
                    alert=alert,
                    bg_color=bg_color,
                    teams=True,
                    roles=roles,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number,
                    selected_role=role,
                    is_superadmin=is_superadmin,
                    total_pages=total_pages,
                    total_items=total_items,
                    teams_lists=teams_list,
                    page=page,
                    per_page=per_page,
                )

            admin_instance = Admin(
                first_name=first_name,
                last_name=last_name,
                email=email.lower(),
                phone_number=phone_number,
                role_id=role,
                is_superadmin=True if is_superadmin else False,
                password=hasher.hash("password"),
            )

            db.session.add(admin_instance)
            db.session.commit()

            session["alert"] = f"{admin_instance.role.name.title()} added successfully"
            session["bg_color"] = "success"

            return redirect(url_for("admin.teams"))

        return render_template(
            "admin_templates/teams.html",
            alert=alert,
            bg_color=bg_color,
            teams=True,
            roles=roles,
            fetch_role=role,
            teams_lists=teams_list,
            total_pages=total_pages,
            total_items=total_items,
            page=page,
            per_page=per_page,
        )
    except Exception as e:
        print(e, "error@teams")
        db.session.rollback()
        session["alert"] = "Network Error"
        session["bg_color"] = "danger"
        return redirect(url_for("admin.teams"))


# courses
@admin.route("/courses", methods=["GET", "POST"])
@login_required
@admin_required
def courses():
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 5))
        alert = session.pop("alert", None)
        bg_color = session.pop("bg_color", None)
        lecturers = get_lecturers()
        all_courses, total_pages, total_items = get_courses(page, per_page)
        if request.method == "POST":
            course_unit = request.form.get("course_unit")
            course_code = request.form.get("course_code")
            lecturer = request.form.get("lecturer")
            course_title = request.form.get("course_title")

            if not course_unit or not course_code or not course_title:
                alert = "Please fill all the fields"
                bg_color = "danger"
                return render_template(
                    "admin_templates/courses.html",
                    alert=alert,
                    bg_color=bg_color,
                    courses=True,
                    lecturers=lecturers,
                    course_unit=course_unit,
                    course_code=course_code,
                    course_title=course_title,
                    selected_lecturer=lecturer,
                    all_courses=all_courses,
                    total_pages=total_pages,
                    total_items=total_items,
                    page=page,
                    per_page=per_page,
                )

            course_exist = Course.query.filter_by(course_code=course_code).first()
            if course_exist:
                alert = "Course already exist"
                bg_color = "danger"
                return render_template(
                    "admin_templates/courses.html",
                    alert=alert,
                    bg_color=bg_color,
                    courses=True,
                    lecturers=lecturers,
                    course_unit=course_unit,
                    course_code=course_code,
                    course_title=course_title,
                    selected_lecturer=lecturer,
                    all_courses=all_courses,
                    total_pages=total_pages,
                    total_items=total_items,
                    page=page,
                    per_page=per_page,
                )

            create_course(course_title, course_code, course_unit, lecturer)
            session["alert"] = "Course added successfully"
            session["bg_color"] = "success"
            return redirect(url_for("admin.courses"))
        return render_template(
            "admin_templates/courses.html",
            alert=alert,
            bg_color=bg_color,
            courses=True,
            lecturers=lecturers,
            all_courses=all_courses,
            total_pages=total_pages,
            total_items=total_items,
            page=page,
            per_page=per_page,
        )
    except Exception as e:
        print(e, "error@courses")
        db.session.rollback()
        session["alert"] = "Network Error"
        session["bg_color"] = "danger"
        return redirect(url_for("admin.courses"))


# view student's details
@admin.route("/view_student/<student_id>")
@login_required
@admin_required
def view_student(student_id):
    alert = session.pop("alert", None)
    bg_color = session.pop("bg_color", None)
    student = Student.query.get(student_id)
    if not student:
        return redirect(url_for("admin.student_quarters"))
    course_registered = CourseRegistered.query.filter_by(
        student_id=student_id
    )
    total_units = sum([course.course.course_unit for course in course_registered])
    return render_template(
        "admin_templates/view_student.html",
        alert=alert,
        bg_color=bg_color,
        student=student,
        course_registered=course_registered,
        total_units=total_units,
        student_quarters=True,
    )


# view team's details
@admin.route("/view_team/<team_id>")
@login_required
@admin_required
def view_team(team_id):
    alert = session.pop("alert", None)
    bg_color = session.pop("bg_color", None)
    team = Admin.query.get(team_id)
    if not team:
        return redirect(url_for("admin.teams"))
    courses_ = team.courses
    total_units = sum([course.course_unit for course in courses_])
    return render_template(
        "admin_templates/view_team.html",
        alert=alert,
        bg_color=bg_color,
        team=team,
        course_registered=courses_,
        total_units=total_units,
        teams=True,
    )


# upload result
@admin.route("/upload_result/<student_id>", methods=["POST"])
@login_required
@admin_required
def upload_result(student_id):
    try:
        student_reg_courses = CourseRegistered.query.filter_by(
            student_id=student_id
        ).all()
        for course_reg in student_reg_courses:
            score = float(request.form.get(course_reg.course_id))
            if score:
                course_reg.score = float(score)
                course_reg.grade = get_grade(score)
                db.session.commit()
        scores = [course_reg.score for course_reg in student_reg_courses]
        units = [course_reg.course.course_unit for course_reg in student_reg_courses]
        gpa = calculate_gpa(scores, units)

        student_reg_courses[0].student.gpa = gpa
        db.session.commit()
        session["alert"] = "Result uploaded successfully"
        session["bg_color"] = "success"
        return redirect(url_for("admin.view_student", student_id=student_id))
    except Exception as e:
        print(e, "error@upload_result")
        db.session.rollback()
        session["alert"] = "Network Error"
        session["bg_color"] = "danger"
        return redirect(url_for("admin.view_student", student_id=student_id))


# change active status
@admin.route("/change_active_status/<student_id>", methods=["GET"])
@login_required
@admin_required
def change_active_status(student_id):
    try:
        student = Student.query.get(student_id)
        student.active = not student.active
        db.session.commit()
        session["alert"] = "Student suspended successfully" if not student.active else "Student activated successfully"
        session["bg_color"] = "success"
        return redirect(url_for("admin.view_student", student_id=student_id))
    except Exception as e:
        print(e, "error@change_active_status")
        db.session.rollback()
        session["alert"] = "Network Error"
        session["bg_color"] = "danger"
        return redirect(url_for("admin.view_student", student_id=student_id))


# change admin active status
# change active status
@admin.route("/change_admin_status/<team_id>", methods=["GET"])
@login_required
@admin_required
def change_admin_status(team_id):
    try:
        team = Admin.query.get(team_id)
        team.active = not team.active
        db.session.commit()
        session["alert"] = "Admin suspended successfully" if not team.active else "Admin activated successfully"
        session["bg_color"] = "success"
        return redirect(url_for("admin.view_team", team_id=team_id))
    except Exception as e:
        print(e, "error@change_active_status")
        db.session.rollback()
        session["alert"] = "Network Error"
        session["bg_color"] = "danger"
        return redirect(url_for("admin.view_team", team_id=team_id))


@admin.route("/edit_team_profile", methods=["GET", "POST"])
@login_required
@admin_required
def edit_team_profile():
    alert = session.pop("alert", None)
    bg_color = session.pop("bg_color", None)
    if request.method == "POST":
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if not old_password or not new_password or not confirm_password:
            alert = "Please fill all the fields"
            bg_color = "danger"
            return render_template(
                "admin_templates/edit_profile.html",
                admin_dashboard=True,
                alert=alert,
                bg_color=bg_color,
                old_password=old_password,
                new_password=new_password,
                confirm_password=confirm_password,
            )
        if new_password != confirm_password:
            alert = "Passwords do not match"
            bg_color = "danger"
            return render_template(
                "admin_templates/edit_profile.html",
                admin_dashboard=True,
                alert=alert,
                bg_color=bg_color,
                old_password=old_password,
                new_password=new_password,
                confirm_password=confirm_password,
            )
        if not hasher.verify(old_password, current_user.password):
            alert = "Invalid old password"
            bg_color = "danger"
            return render_template(
                "admin_templates/edit_profile.html",
                admin_dashboard=True,
                alert=alert,
                bg_color=bg_color,
                old_password=old_password,
                new_password=new_password,
                confirm_password=confirm_password,
            )
        current_user.password = hasher.hash(new_password)
        db.session.commit()
        session["alert"] = "Password changed successfully"
        session["bg_color"] = "success"
        return redirect(url_for("admin.admin_dashboard"))

    return render_template(
        "admin_templates/edit_profile.html",
        admin_dashboard=True,
        alert=alert,
        bg_color=bg_color,
    )
