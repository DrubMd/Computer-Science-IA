from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
import sqlite3

class LoginForm(FlaskForm):
 username = StringField('Username',validators=[DataRequired()])
 password = PasswordField('Password',validators=[DataRequired()])
 remember = BooleanField('Remember Me')
 submit = SubmitField('Login')
 
 def validate_username(self, username):
    conn = sqlite3.connect('database.db')
    curs = conn.cursor()
    curs.execute("SELECT username FROM users where username = (?)",[username.data])
    valusername = curs.fetchone()
    if valusername is None:
      raise ValidationError('This username ID is not registered. Please register before login')
    
class RegistrationForm(FlaskForm):
  username = StringField('Username',validators=[DataRequired()])
  password = PasswordField('Password',validators=[DataRequired()])
  confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
  submit = SubmitField('Sign Up')
  
  def validate_username(self, username):
      conn = sqlite3.connect('database.db')
      curs = conn.cursor()
      curs.execute("SELECT username FROM users where username = (?)",[username.data])
      valusername = curs.fetchone()
      if valusername:
        raise ValidationError('This username ID is already registered. Please login')