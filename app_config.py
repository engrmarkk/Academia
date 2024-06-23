from extensions import db, migrate, cors, login_manager
from flask import Flask, render_template, redirect, url_for, session
from config import config_object
from endpoints import admin as admin_blueprint, school as school_blueprint, student as student_blueprint
from models import Admin, Course, Student, CourseRegistered, Role


def create_app(config=config_object["development"]):

    app = Flask(__name__)

    app.config.from_object(config)

    cors.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # with app.app_context():
    #     db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        logged_user = Admin.query.get(user_id)
        if not logged_user:
            logged_user = Student.query.get(user_id)
        return logged_user

    @login_manager.unauthorized_handler
    def unauthorized():
        session["alert"] = "Please login to access this page"
        session["bg_color"] = "danger"
        return redirect(url_for("school.login"))

    # 404
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html")

    app.register_blueprint(admin_blueprint)
    app.register_blueprint(school_blueprint)
    app.register_blueprint(student_blueprint)

    return app
