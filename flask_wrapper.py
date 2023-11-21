from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SECRET_KEY"] = "secret-key"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


@app.route("/")
def home():
    if "username" in session:
        return f'Welcome {session["username"]}!'
    return redirect(url_for("signin"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user_name = request.form.get("username", None)
        password = request.form.get("password", None)
        if user_name is None and password is None:
            return "Please enter your username and password", 400
        user = User.query.filter_by(username=user_name).first()
        if user:
            return "User already exists", 400
        hashed_password = generate_password_hash(password)
        new_user = User(username=user_name, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("signin"))
    return render_template("signup.html")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    user_name = request.form.get("username", None)
    password = request.form.get("password", None)
    msg = None
    if request.method == "POST":
        if user_name is None and password is None:
            msg = "Please enter your username and password"
        else:
            user = User.query.filter_by(username=user_name).first()
            if user is None:
                msg = "User doesn't exist"
            else:
                password = request.form["password"]
                is_valid_password = check_password_hash(user.password, password)
                if user and is_valid_password:
                    session["username"] = user.username
                    return redirect(url_for("home"))
    return render_template("signin.html", msg=msg)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
