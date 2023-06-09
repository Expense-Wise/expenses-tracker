from flask import Flask, render_template, request, url_for, flash, redirect
from flask_login import LoginManager, login_user, logout_user, login_manager, login_required
from flask_sqlalchemy import SQLAlchemy
from forms import AddForm, LoginForm, UpdateForm
import plotly.graph_objects as go


app = Flask(__name__)
app.config["SECRET_KEY"] = "c4f86fdd81408bf0607e35b661f845a8"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager=LoginManager(app)
# login_manager.init_app(app)


def allexpense(user_id):
    expenses = Expense.query.filter_by(userId=user_id).all()
    totalexpense = 0
    # loop through expenses and add amount to totalexpense
    for expense in expenses:
        totalexpense += expense.amount
    return totalexpense


def totalPaid(user_id):
    expenses = Expense.query.filter_by(userId=user_id).all()
    totalpaid = 0
    # loop through expenses and add amount to totalexpense
    for expense in expenses:
        if expense.repaid == "Paid":
            totalpaid += expense.amount
    return totalpaid


def totalUnpaid(user_id):
    expenses = Expense.query.filter_by(userId=user_id).all()
    totalunpaid = 0
    # loop through expenses and add amount to totalexpense
    for expense in expenses:
        if expense.repaid == "Unpaid":
            totalunpaid += expense.amount
    return totalunpaid


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(60), index=True)
    expenses = db.relationship('Expense', backref='user', lazy='dynamic')
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Expense(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    amount = db.Column(db.Integer, index=True)
    description = db.Column(db.String, index=True)
    category = db.Column(db.String, index=True)
    repaid = db.Column(db.String, default="Unpaid", index=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))


with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        password = User.query.filter_by(password=form.password.data).first()
        if user and password:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("home", user_id=user.id))
        else:
            flash("Login unsuccessful. Please check email and password", "danger")
    return render_template("login.html", title="Log In", form=form)
    

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('/'))


@app.route("/<int:user_id>", methods=["GET"])
@login_required
def home(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return "User not found", 404

    expenses = Expense.query.filter_by(userId=user_id).all()
    return render_template("home.html", expenses=expenses, user_id=user_id,
                           totalexpense=allexpense(user_id), totalPaid=totalPaid(user_id), totalUnpaid=totalUnpaid(user_id))


@app.route("/<int:user_id>/add", methods=["GET", "POST"])
@login_required
def add_expense(user_id):
    form = AddForm()
    if form.validate_on_submit():
        expense = Expense(amount=form.amount.data, description=form.description.data,
                          category=form.category.data, userId=user_id)
        db.session.add(expense)
        db.session.commit()
        flash(f"Expense added", "success")
        return redirect(url_for("home", user_id=user_id, totalexpense=allexpense(user_id), totalPaid=totalPaid(user_id), totalUnpaid=totalUnpaid(user_id)))
    return render_template("add_expense.html", title="Add Expense", form=form, user_id=user_id,
                           totalexpense=allexpense(user_id), totalPaid=totalPaid(user_id), totalUnpaid=totalUnpaid(user_id))


@app.route("/<int:user_id>/<int:expense_id>/update", methods=["GET", "POST"])
@login_required
def update(user_id, expense_id):
    expense = Expense.query.get_or_404(expense_id)
    form = UpdateForm()
    if form.validate_on_submit():
        expense.amount = form.amount.data
        expense.description = form.description.data
        expense.category = form.category.data
        db.session.commit()
        flash(f"Expense updated", "success")
        return redirect(url_for("home", user_id=user_id, totalexpense=allexpense(user_id),
                                totalPaid=totalPaid(user_id), totalUnpaid=totalUnpaid(user_id)))
    elif request.method == "GET":
        form.amount.data = expense.amount
        form.description.data = expense.description
        form.category.data = expense.category
        form.repaid.data = expense.repaid
    return render_template("update.html", form=form, title="Update", expense_id=expense_id, user_id=user_id,
                           totalexpense=allexpense(user_id), totalPaid=totalPaid(user_id), totalUnpaid=totalUnpaid(user_id))


@app.route("/<int:user_id>/<int:expense_id>/delete", methods=['POST'])
@login_required
def delete(user_id, expense_id):
    expense = Expense.query.get_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()
    flash('Your expense has been deleted!', 'success')
    return redirect(url_for('home', user_id=user_id, expense_id=expense_id, totalexpense=allexpense(user_id),
                            totalPaid=totalPaid(user_id), totalUnpaid=totalUnpaid(user_id)))


@app.route("/<int:user_id>/view", methods=['GET'])
@login_required
def view(user_id):
    expenses = Expense.query.filter_by(userId=user_id).all()
    total = {}
    for expense in expenses:
        category = expense.category
        if category not in total:
            total[category] = 0
        total[category] += expense.amount
    fig = go.Figure(
        data=[go.Pie(labels=list(total.keys()), values=list(total.values()), textinfo='label+percent',
              insidetextorientation='radial',  hole=.3)])
    chart = fig.to_html(full_html=False)

    return render_template('view.html', user_id=user_id, chart=chart, expense_id=expense.id, totalexpense=allexpense(user_id),
                           totalPaid=totalPaid(user_id), totalUnpaid=totalUnpaid(user_id))


if __name__ == '__main__':
    app.run(debug=True, port=5001)
