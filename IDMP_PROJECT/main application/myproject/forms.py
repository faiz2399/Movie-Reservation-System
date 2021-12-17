from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField
# from wtforms.fields.html5 import TimeField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError

#########################################################

### Each of the class in this file represents the forms fields for different views
### which users can use to enter data

#########################################################

class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class DelStatus(FlaskForm):

    submit = SubmitField('Delete Status')

class UpStatus(FlaskForm):


    movie_id = IntegerField('Please Enter Movie Id', validators=[DataRequired()])

    submit = SubmitField('Update Status')


class UserCancel(FlaskForm):

    book_id = IntegerField('Please Enter Booking ID', validators=[DataRequired()])
    schedule_id = IntegerField('Please Enter Schedule ID', validators=[DataRequired()])

    submit = SubmitField('Submit')

class UserInfo(FlaskForm):

    user_name = StringField('Please Enter Username', validators=[DataRequired()])
    submit = SubmitField('Submit')



class TakeDate(FlaskForm):
    date = StringField('Please Enter the Date', validators=[DataRequired()])
    submit = SubmitField('Submit')

class TakeMovie(FlaskForm):
    movie_name = StringField('Please Enter Movie Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AdminForm(FlaskForm):

    movie_id = IntegerField('Please Enter Movie Id', validators=[DataRequired()])
    date = DateField('Please Enter the Date', validators=[DataRequired()])
    time = StringField('Please Enter the Time', validators=[DataRequired()])
    submit = SubmitField('Submit to Update')


class Book(FlaskForm):


    schedule = StringField('Enter Schedule ID', validators=[DataRequired()])
    username = StringField('Enter Username',validators=[DataRequired()])
    submit = SubmitField('Book Your Ticket!')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register!')

    def check_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def check_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')
