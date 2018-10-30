from datetime import datetime
from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

# import secrets
# secrets.token_hex(16)
app.config['SECRET_KEY'] = 'e94305dcd6e2a80c903dd5d81bd69849'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


comments = db.Table('comments',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('comment_id', db.Integer, db.ForeignKey('comment.id'))
)


notes = db.Table('notes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('note_id', db.Integer, db.ForeignKey('note.id'))
)


class User(db.Model):
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
    comments = db.relationship('Comment', secondary='comments', backref=db.backref('idea_comments', lazy='dynamic'))
    notes = db.relationship('Note', secondary='notes', backref=db.backref('idea_notes', lazy='dynamic'))

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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.first_name.data} {form.last_name.data}', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', form=form, title='Register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your email and password', 'danger')

    return render_template('login.html', form=form, title='Login')


if __name__ == '__main__':
    app.run(debug=True)
