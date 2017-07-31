from flask import render_template, redirect, url_for, flash, request, abort, \
    current_app, jsonify
from flask_login import current_user, login_required
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostForm
from .. import db
from ..models import Permission, Role, User, Post, Firm, Company, FirmTier, \
    FirmType, Follow, Geo, UserType
from ..decorators import admin_required, permission_required
from ..cobbler_api import CobblerApi


@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_anonymous():
        return redirect(url_for('auth.login'))
    else:
        top_vc_firms = current_user.top_firms(n=10, firm_type_code='vc')
        top_ai_firms = current_user.top_firms(n=10, firm_type_code='ai')
        top_su_firms = current_user.top_firms(n=10, firm_type_code='su')
        return render_template('index.html', top_vc_firms=top_vc_firms,
                               top_ai_firms=top_ai_firms,
                               top_su_firms=top_su_firms)


@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.outerjoin(Geo).outerjoin(UserType)\
        .with_entities(User, Geo, UserType)\
        .filter(User.username==username).first_or_404()

    # query for firms
    firms = Firm.query.join(FirmType).join(FirmTier).join(User)\
        .with_entities(Firm, FirmType, FirmTier, User)\
        .filter(User.username == username)\
        .order_by(FirmTier.firm_tier.asc(), Firm.name.asc()).all()

    # parse firms
    vc_firms = []
    ai_firms = []
    su_firms = []
    for firm in firms:
        if firm.FirmType.firm_type_code == 'vc':
            vc_firms.append(firm)
        if firm.FirmType.firm_type_code == 'ai':
            ai_firms.append(firm)
        if firm.FirmType.firm_type_code == 'su':
            su_firms.append(firm)

    return render_template('user.html', user=user, vc_firms=vc_firms,
                           ai_firms=ai_firms, su_firms=su_firms)


@main.route('/users/<username>')
@login_required
def users(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.', 'error')
        return redirect(url_for('main.index'))

    # get request arguments
    followed = request.args.get('followed', 1, type=int)

    # query for users
    if followed:
        results = user.followed.order_by(Follow.timestamp.desc()).all()
        users = [{'user': item.followed, 'timestamp': item.timestamp}
                 for item in results]
    else:
        results = User.query.order_by(User.username.asc()).all()
        users = [{'user': item, 'timestamp': None}
                 for item in results]

    return render_template('user_list.html', user=user, users=users,
                           followed=followed)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        # change values based on form input
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        current_user.geo = Geo.query.get(form.geo.data)
        current_user.user_type = UserType.query.get(form.user_type.data)
        db.session.add(current_user)
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.user', username=current_user.username))
    # set inital values
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    form.geo.data = current_user.geo_id
    form.user_type.data = current_user.user_type_id
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
        user.location = form.location.data
        user.geo = Geo.query.get(form.geo.data)
        user.user_type = UserType.query.get(form.user_type.data)
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.', 'success')
        return redirect(url_for('main.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.geo.data = user.geo_id
    form.user_type.data = user.user_type_id
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/post/<int:id>')
@login_required
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])


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
        flash('The post has been updated.', 'success')
        return redirect(url_for('main.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)

@main.route('/images/<username>')
@login_required
def images(username):
    cobblerApi = CobblerApi()
    distros_list = cobblerApi.get_distros()
    return render_template('images_list.html', user=user,
                           distros_list=distros_list)


@main.route('/nodes/<username>')
@login_required
def nodes(username):
    # query for nodes
    cobblerApi = CobblerApi()
    system_list = cobblerApi.get_systems()
    return render_template('nodes_list.html', user=user,
                           nodes_list=system_list)
