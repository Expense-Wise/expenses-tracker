from flask import Flask, render_template, url_for
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
    Amount = db.Column(db.Integer, index=True)
    Description = db.Column(db.String, index=True)
    Category = db.Column(db.String, index=True)
    UserId = db.Column(db.Integer, db.ForeignKey('user.id'))


@app.route("/")
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
