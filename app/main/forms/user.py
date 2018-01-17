from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField, FileField, IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from app.models import Role, User
import imghdr


class EditProfileForm(FlaskForm):
    image_file = FileField('Image file')
    first_name = StringField('First name', validators=[Length(0, 64)])
    last_name = StringField('Last name', validators=[Length(0, 64)])
    pts = IntegerField('pts', default=100)
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(FlaskForm):
    image_file = FileField('Image file')
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('First name', validators=[DataRequired(), Length(0, 64)])
    surname = StringField('Last name', validators=[DataRequired(), Length(0, 64)])
    pts = IntegerField('pts')
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

    def validate_image_file(self, field):
        if field.data.filename[-4:].lower() != '.jpg':
            raise ValidationError('Invalid file extension')
        if imghdr.what(field.data) != 'jpeg':
            raise ValidationError('Invalid image format')