import os
import secrets
from PIL import Image
from flask import render_template, flash, redirect, url_for, request
from inventor import app, db, bcrypt
from inventor.forms import RegistrationForm, LoginForm, UpdateAccountForm, IdeaForm, EditIdeaForm
from inventor.models import User, Idea, Comment, Note
from flask_login import login_user, current_user, logout_user, login_required


ideas = [
    {
        'inventor': 'Jane Doe',
        'title': 'First Idea',
        'description': 'This is my cool idea',
        'category': 'Boys',
        'date_submitted': 'October 1, 2018'
    },
    {
        'inventor': 'Jane Doe',
        'title': 'Second Idea',
        'description': 'This is my cool idea',
        'category': 'Boys',
        'date_submitted': 'October 1, 2018'
    },
    {
        'inventor': 'Jill Blue',
        'title': 'Jill Idea 1',
        'description': 'Some idea',
        'category': 'Boys & Girls',
        'date_submitted': 'October 12, 2018'
    },
    {
        'inventor': 'Steve Blue',
        'title': 'Steve Idea Four',
        'description': 'Forth thing I created',
        'category': 'Outdoor',
        'date_submitted': 'October 12, 2018'
    }

]


def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
@login_required
def home():
    ideas = Idea.query.filter_by(user_id=current_user.id).all()
    return render_template('home.html', ideas=ideas)


@app.route('/about')
def about():
    return render_template('about.html', title="About")


@app.route('/terms')
def terms():
    return render_template('terms.html')


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile_image = picture_file
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.address1 = form.address1.data
        current_user.address2 = form.address2.data
        current_user.city = form.city.data
        current_user.postal_code = form.postal_code.data
        current_user.state = form.state.data
        current_user.country = form.country.data
        current_user.phone = form.phone.data
        current_user.role = 0
        # current_user.nda = 1

        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.address1.data = current_user.address1
        form.address2.data = current_user.address2
        form.city.data = current_user.city
        form.postal_code.data = current_user.postal_code
        form.state.data = current_user.state
        form.country.data = current_user.country
        form.phone.data = current_user.phone

    image_file = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data,
                    email=form.email.data, password=hashed_password,
                    address1=form.address1.data, address2=form.address2.data,
                    city=form.city.data, state=form.state.data,
                    postal_code=form.postal_code.data, country=form.country.data,
                    phone=form.phone.data, nda=0,
                    role=0)
        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {form.first_name.data} {form.last_name.data}', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', form=form, title='Register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Welcome back {user.first_name}', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check your email and password', 'danger')
    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    # resize the image
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    # form_picture.save()

    return picture_fn


@app.route('/idea/new', methods=['GET', 'POST'])
@login_required
def new_idea():
    form = IdeaForm()
    if form.validate_on_submit():
        idea = Idea(title=form.title.data,
                description=form.description.data,
                category=form.category.data,
                company=form.company.data,
                user_id=current_user.id)
        db.session.add(idea)
        db.session.commit()

        flash(f'New Idea created for ', 'success')
        return redirect(url_for('home'))

    return render_template('create_idea.html', form=form, title='New Idea')


@app.route('/idea/edit/<int:id>')
@login_required
def edit_idea(id):
    form = EditIdeaForm()

    if form.validate_on_submit():
        idea = Idea()
    return render_template('edit_idea.html', form=form)


@app.route('/idea/view/<int:id>')
def view_idea(id):
    idea = Idea.query.filter_by(id=id, user_id=current_user.id).first()
    return render_template('view_idea.html', idea=idea)