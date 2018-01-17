from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired, Length
from flask_pagedown.fields import PageDownField


class PostForm(FlaskForm):
    task_name = StringField('Task name', validators=[DataRequired(), Length(0, 16)])
    body = StringField('Task description', validators=[DataRequired()])
    # body = PageDownField('Task description', validators=[DataRequired()])
    task_story_points = IntegerField('Task capacity story points')
    submit = SubmitField('Submit')
    # delete_post = SubmitField('Delete post')
