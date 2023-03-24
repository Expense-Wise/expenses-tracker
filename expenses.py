from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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


@app.route("/<int:user_id>", methods=["GET"])
def home(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return "User not found", 404

    expenses = Expense.query.filter_by(userId=user.id).all()
    return jsonify([{
        'id': expense.id,
        'amount': expense.amount,
        'description': expense.description,
        'category': expense.category
    } for expense in expenses])


if __name__ == '__main__':
    app.run(debug=True, port=5001)
