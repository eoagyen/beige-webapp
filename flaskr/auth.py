"""
User authentication views
"""
import functools

from flask import(
    Blueprint, request, redirect, url_for, flash, render_template, 
    session
)
from werkzeug.security import generate_password_hash, check_password_hash

from db import get_db


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Registration of users"""
    if request.methof == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None 

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password))
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered"
            else: 
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template("auth/register.html")


@bp.route("/login", methods=("Get", "POST"))
def login():
    """Hnadle the login"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username"
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password"

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))
        flash(error)
    return render_template("auth/login.html")
 
