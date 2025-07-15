from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DecimalField, SubmitField, SelectField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, Email

# Forms
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class CalculatorForm(FlaskForm):
    panel_capacity = DecimalField('Solar Panel Capacity (kW)', validators=[DataRequired()])
    sunlight_hours = DecimalField('Sunlight Hours (hours/day)', validators=[DataRequired()])
    number_of_panels = IntegerField('Number of Panels', validators=[DataRequired()])
    cost_per_panel = DecimalField('Cost per Panel', validators=[DataRequired()])
    electricity_cost = DecimalField('Electricity Cost per kWh', validators=[DataRequired()])
    pincode = StringField('Pincode', validators=[DataRequired()])

    submit = SubmitField('Calculate')

class DateRangeForm(FlaskForm):
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    submit = SubmitField('Calculate Usage')
