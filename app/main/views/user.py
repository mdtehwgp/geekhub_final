import os
import hashlib
from flask import render_template, redirect, url_for, flash, current_app, request
from flask_login import login_required, current_user
from . import main
from app.main.forms.user import EditProfileForm, EditProfileAdminForm
from app import db
from app.models import Role, User, Post
from app.decorators import admin_required


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False)
    tasks = pagination.items
    return render_template('user.html', user=user, tasks=tasks,
                           pagination=pagination)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.first_name.data
        current_user.surname = form.last_name.data
        current_user.performance_story_points = form.pts.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        image_name = form.image_file.data.filename
        image_path = current_app.config.get('IMAGES_PATH')
        image_folder = os.path.join(current_app.static_folder, image_path)

        if not os.path.exists(image_folder):
            os.makedirs(image_folder)

        image_name = hashlib.sha256(current_user.email.encode('utf-8')).hexdigest() + os.path.splitext(image_name)[1]
        form.image_file.data.save(
            os.path.join(image_folder, image_name)
            )
        current_user.avatar_url = image_path + '/' + image_name
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.first_name.data = current_user.name
    form.last_name.data = current_user.surname
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.surname = form.surname.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.surname.data = user.surname
    form.pts.data = user.performance_story_points
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)