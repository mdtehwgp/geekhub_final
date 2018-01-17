from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp

from ..models import User


class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('keep me logged in')
    submit = SubmitField('Log in')


class RegistrationForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                          'usernames must have only letters, '
                                                                          'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     EqualTo('password_repeat', message='passwords must mutch')])
    password_repeat = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('email already registered')

    def validate_user(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('username already in use')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('Reset password')


class PasswordResetForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     EqualTo('password_repeat', message='passwords must mutch')])
    password_repeat = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address')


class ChangePasswordForm(FlaskForm):

    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password',
                             validators=[DataRequired(),
                                         EqualTo('password_repeat', message='passwords must match')])
    password_repeat = PasswordField('Confirm new password', validators=[DataRequired()])
    submit = SubmitField('Update password')


class ChangeEmailForm(FlaskForm):

    email = StringField('New email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Update email address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')









