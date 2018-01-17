from flask import render_template, redirect, url_for, abort, flash, request, current_app, make_response
from flask_login import login_required, current_user
from .. import main
from app.main.forms import PostForm, CommentForm
from app import db
from app.models import Permission, Post, Comment, User
from app.decorators import permission_required


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    task = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=task,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash('Your comment has been published.')
        return redirect(url_for('.post', id=id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (task.comments.count() - 1) // \
            current_app.config['COMMENTS_PER_PAGE'] + 1
    pagination = task.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', tasks=[task], form=form,
                           comments=comments, pagination=pagination)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    form.task_name.data = post.task_name
    form.body.data = post.body
    form.task_story_points.data = post.task_story_points
    return render_template('edit_post.html', form=form)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp


# @main.route('/moderate')
# @login_required
# @permission_required(Permission.MODERATE_COMMENTS)
# def moderate():
#     page = request.args.get('page', 1, type=int)
#     pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
#         page, per_page=current_app.config['COMMENTS_PER_PAGE'],
#         error_out=False)
#     comments = pagination.items
#     return render_template('moderate.html', comments=comments,
#                            pagination=pagination, page=page)

@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False)
    tasks = pagination.items
    return render_template('moderate.html', tasks=tasks,
                           pagination=pagination, page=page)


@main.route('/users')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def users():
    page = request.args.get('page', 1, type=int)
    # pagination = User.query.order_by(User.member_since.desc()).paginate(
    #     page, per_page=current_app.config['POSTS_PER_PAGE'],
    #     error_out=False)
    pagination = User.query.order_by(User.performance_story_points.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False)
    users = pagination.items
    return render_template('users.html', users=users,
                           pagination=pagination, page=page)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))