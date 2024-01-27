from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Configure login setup
login_manager = LoginManager()
login_manager.init_app(app)


# Create a user loader
@login_manager.user_loader()
def load_user(user_id):
    return db.get_or_404(User, user_id)


# CREATE TABLE IN DB
class User(UserMixin,db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        data = request.form
        name = data["name"]
        email = data["email"]
        password = data["password"]

        # Hash and salt the password using Werkzeug

        hash_and_salted_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        with app.app_context():
            enter_data_to_db = User(name=name, email=email, password=hash_and_salted_password)
            db.session.add(enter_data_to_db)
            db.session.commit()
            login_user(enter_data_to_db)
            return redirect(url_for("secrets"))

            # return render_template("secrets.html", name=name)

    return render_template("register.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/secrets')
def secrets():
    return render_template("secrets.html")


@app.route('/logout')
def logout():
    pass


@app.route('/download')
def download():
    return send_from_directory('static', path="files/cheat_sheet.pdf")


if __name__ == "__main__":
    app.run(debug=True)
