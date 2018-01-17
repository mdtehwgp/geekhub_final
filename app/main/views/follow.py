from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from .. import main
from app.models import User, Permission, Post
from app.decorators import permission_required


@main.route('/follow/<int:id>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(id):
    user = Post.query.filter_by(id=id).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.post', id=id))
    current_user.follow(user)
    flash('You are now following %s.' % id)
    return redirect(url_for('.post', id=id))


@main.route('/unfollow/<int:id>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(id):
    user = Post.query.filter_by(id=id).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.post', id=id))
    current_user.unfollow(user)
    flash('You are not following %s anymore.' % id)
    return redirect(url_for('.post', id=id))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed-by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'task': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)
