from flask import render_template, request, redirect, url_for, current_app
from flask_login import current_user

from .. import main
from app import db
from app.models import Post, Permission
from app.main.forms import PostForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        post = Post(body=form.body.data,
                    task_name=form.task_name.data,
                    task_story_points=form.task_story_points.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False)
    tasks = pagination.items
    return render_template('index.html', form=form, tasks=tasks,
                           show_followed=show_followed, pagination=pagination)
