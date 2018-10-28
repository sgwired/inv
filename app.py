from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'e94305dcd6e2a80c903dd5d81bd69849'
# import secrets
# secrets.token_hex(16)

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
