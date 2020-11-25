from flask import Flask, render_template, request, redirect, url_for, session
from forms import LoginForm, AdminAddProduct,RegisterForm
from product import Product
from mysql.connector import Error, errorcode
from db_conn import Conn_db


app = Flask(__name__)
app.config['SECRET_KEY']='DEV'


def user_exists(username, check_admin=False):
    with Conn_db() as conn:
        if check_admin:
            query = "SELECT name FROM Admin WHERE name=%s;"
        else:
            query = "SELECT name FROM User WHERE name=%s;"
        cursor = conn.cursor()
        cursor.execute(query, (username,))
        attr = cursor.fetchone() 
        cursor.close()
        # attr is 'None' if no user was found
        if attr:
            return True
    return False


def add_user_db(username, password):
    """
        Add a user to the 'User' table.
        If user already exists return False.
    """
    with Conn_db() as conn:
        conn.autocommit = False
        cursor = conn.cursor()
        lookup_query = 'SELECT username FROM User where username=%s'
        cursor.execute(lookup_query, (username,)) 

        if cursor.fetchone():
            conn.rollback() # Unsure about this rollback
            cursor.close()
            return False # User already exists.

        insert_query = 'INSERT INTO User(username, password) VALUES(%s, %s)'       
        cursor.execute(insert_query, (username, password))
        conn.commit()
        cursor.close()
    return True


def is_logged_in(check_admin=False):
    try:
        username = session['username']
    except:
        return False
    check_admin = check_admin or 'admin' in session
    return user_exists(username, check_admin)

def log_in(username, password):
    pass

@app.route("/", methods=['GET', 'POST'])
def home():
    form = LoginForm()
    if is_logged_in():
        return render_template("index.html", data='logged in', form=form)

    if form.validate_on_submit():
        # Check if creds are valid.
        if 
        session['username'] = form.username.data
        if form.username.data[0]=='#':
            #admin
            pass
        print(session)
        return redirect(url_for('home'))
    return render_template("index.html", data='logged out', form=form)


@app.route("/about")
def about():
    return "Our incredible site!"


@app.route("/signup", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        if add_user_db(name, password):
            session['username'] = name # Log in user auto...
            return redirect(url_for('home'))
        else:
            # Email already exists in DB!
            return render_template('register.html', form=form)
    else:
        return render_template('register.html', form=form)


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    #if not is_logged_in(check_admin=True):
    #    return redirect(url_for('home'))
    form = AdminAddProduct()
    if request.method == 'POST':
        if form.validate_on_submit():
            newProduct = Product()

    return render_template("adminpage.html", form=form)

if __name__ == "__main__":
    # Load local db_conf.json file
    Conn_db.load_conf()
    app.run(debug=False)
