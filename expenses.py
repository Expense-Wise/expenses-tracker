from flask import Flask, render_template, jsonify, url_for, flash, redirect
# from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm, UpdateForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "c4f86fdd81408bf0607e35b661f845a8"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# login_manager=LoginManager()
# login_manager.init_app(app)




class User(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    expenses = db.relationship('Expense', backref='user', lazy='dynamic')


class Expense(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    amount = db.Column(db.Integer, index=True)
    description = db.Column(db.String, index=True)
    category = db.Column(db.String, index=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))


with app.app_context():
    db.create_all()
 
 
# @app.route("/")
# @app.route("/home")
# def home():
#     user = User.query.first()  # Get the first user from the database
#     expenses = user.expenses.all()  # Get all expenses related to that user
#     return render_template("home.html", expenses=expenses)


@app.route("/<int:user_id>", methods=["GET"])
def home(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return "User not found", 404

    expenses = Expense.query.filter_by(userId=user_id).all()
    return render_template("home.html", expenses=expenses, userId=user_id)

@app.route("/add", methods=["GET", "POST"])
def add_expense():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_id = user.id
        expense = Expense(amount=form.amount.data, description=form.description.data,
                          category=form.category.data, user_id=user_id)
        db.session.add(expense)
        db.session.commit()
        flash(f"Expense added", "success")
        return redirect(url_for("home"))
    return render_template("add_expense.html", title="Add Expense", form=form)


@app.route("/update", methods=["GET", "PUT", "DELETE", "POST"])
def update():
    form = UpdateForm()
    if form.validate_on_submit():
        expense = Expense.query.get(form.id.data)
        expense.amount = form.amount.data
        expense.description = form.description.data
        expense.category = form.category.data
        db.session.commit()
        flash(f"Expense updated", "success")
        return redirect(url_for("home"))
    return render_template("update.html", title="Update", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "password":
            flash("You have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login unsuccessful. Please check username and password", "danger")
    return render_template("login.html", title="Log In", form=form)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
