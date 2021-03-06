from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_login import current_user
from inventor.models import User, Idea

# from app.models import User


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name',
                             validators=[DataRequired(), Length(min=2, max=64)])
    last_name = StringField('Last Name',
                            validators=[DataRequired(), Length(min=2, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    address1 = StringField('Address 1', validators=[DataRequired()])
    address2 = StringField('Address 2')
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    postal_code = StringField('Postal Code', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
    
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()

        if email:
            raise ValidationError('The email you selected is aready taken. Please choose a differrent one.')
            

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    first_name = StringField('First Name',
                             validators=[DataRequired(), Length(min=2, max=64)])
    last_name = StringField('Last Name',
                            validators=[DataRequired(), Length(min=2, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address1 = StringField('Address 1', validators=[DataRequired()])
    address2 = StringField('Address 2')
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    postal_code = StringField('Postal Code', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('The email you selected is aready taken. Please choose a differrent one.')


class IdeaForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    company = StringField('Company', validators=[DataRequired()])
    featured_image = FileField('Featured Image', validators=[FileAllowed(['jpg', 'png'])])
    secondary_image = FileField('Secondary Image', validators=[FileAllowed(['jpg', 'png'])])
    primary_document = FileField('Primary Document', validators=[FileAllowed(['doc', 'pdf', 'xls'])])
    secondary_document = FileField('Secondary Document', validators=[FileAllowed(['doc', 'pdf', 'xls'])])
    submit = SubmitField('Create New Idea')


class EditIdeaForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    company = StringField('Company', validators=[DataRequired()])
    featured_image = FileField('Featured Image', validators=[FileAllowed(['jpg', 'png'])])
    secondary_image = FileField('Secondary Image', validators=[FileAllowed(['jpg', 'png'])])
    primary_document = FileField('Primary Document', validators=[FileAllowed(['doc', 'pdf', 'xls'])])
    secondary_document = FileField('Secondary Document', validators=[FileAllowed(['doc', 'pdf', 'xls'])])
    submit = SubmitField('Edit')
