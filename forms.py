from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, validators, FloatField, IntegerField


class AddForm(FlaskForm):
    amount = FloatField(
        "Amount", [validators.DataRequired(message="Please enter an amount")])
    description = StringField(
        "Description", [validators.DataRequired(message="Please enter a descrtiption")])
    category = StringField("Category", [validators.DataRequired(
        message="Please enter a category")])
    submit = SubmitField("Submit")


class UpdateForm(FlaskForm):
    amount = FloatField(
        "Amount", [validators.DataRequired(message="Please enter an amount")])
    description = StringField(
        "Description", [validators.DataRequired(message="Please enter a description")])
    category = StringField("Category", [validators.DataRequired(
        message="Please enter a category")])
    repaid = StringField("Repaid", render_kw={'readonly': True})
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    email = EmailField(
        "Email", [validators.DataRequired(), validators.Email()])
    password = PasswordField("Password", [validators.DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")
