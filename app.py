import secrets, os
from datetime import datetime
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from flask_login import LoginManager, UserMixin
from PIL import Image

app = Flask(__name__)

# import secrets
# secrets.token_hex(16)
app.config['SECRET_KEY'] = 'e94305dcd6e2a80c903dd5d81bd69849'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'



# comments = db.Table('comments',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('comment_id', db.Integer, db.ForeignKey('comment.id'))
# )


# notes = db.Table('notes',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('note_id', db.Integer, db.ForeignKey('note.id'))
# )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    address1 = db.Column(db.String(120))
    address2 = db.Column(db.String(120))
    city = db.Column(db.String(60))
    state = db.Column(db.String(60))
    postal_code = db.Column(db.String(15))
    country = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    role = db.Column(db.Integer, nullable=False, default=0)
    profile_image = db.Column(db.String(20), nullable=False, default='default.jpg')
    nda = db.Column(db.Integer, nullable=False, default=0)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ideas = db.relationship('Idea', backref='inventor', lazy=True)


    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.id}')"

class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(64), nullable=False)
    company = db.Column(db.String(64), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    featured_image = db.Column(db.String(20), nullable=False, default='default_image.jpg')
    secondary_image = db.Column(db.String(20), nullable=False, default='default_image.jpg')
    primary_document = db.Column(db.String(20))
    secondary_document = db.Column(db.String(20))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # comments = db.relationship('Comment', secondary=comments, 
    #     backref=db.backref('idea_comments', lazy='dynamic'))
    # notes = db.relationship('Note', secondary=notes, 
    #     backref=db.backref('idea_notes', lazy='dynamic'))

    def __repr__(self):
        return f"Idea('{self.title}', '{self.id}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Comment('{self.comment}', '{self.id}')"


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Note('{self.note}', '{self.id}')"


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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('home.html', ideas=ideas)


@app.route('/about')
def about():
    return render_template('about.html', title="About")


@app.route('/terms')
def terms():
    return render_template('terms.html')


@app.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('home'))

    return render_template('register.html', form=form, title='Register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Welcome back {user.first_name}', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check your email and pasword', 'danger')
    return render_template('login.html', form=form, title='Login')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    #resize the image 
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    # form_picture.save()

    return picture_fn

if __name__ == '__main__':
    app.run(debug=True)
