from flask import Flask, render_template, request, redirect, url_for, session, make_response
from forms import LoginForm, AdminAddProduct,RegisterForm
from product import Product
from mysql.connector import Error, errorcode
from db_conn import Conn_db


app = Flask(__name__)
app.config['SECRET_KEY']='DEV'


def user_exists(username, check_admin=False):
    with Conn_db() as conn:
        if check_admin:
            query = "SELECT username FROM Admin WHERE username=%s;"
        else:
            query = "SELECT username FROM User WHERE username=%s;"
        cursor = conn.cursor()
        cursor.execute(query, (username,))
        attr = cursor.fetchall() 
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
    """
        If username start with a '#' then its
        an admin account.
        
        TODO: Return relevant session data? such as if admin etc
    """
    try:
        username = session['username']
    except:
        return False
    check_admin = check_admin or username[0] == '#'
    if username[0] == '#':
        username = username[1:]
    return user_exists(username, check_admin)


def log_in(username, password, as_admin=False):
    with Conn_db() as conn:
        cursor = conn.cursor()
        if as_admin:
            lookup_query = 'SELECT username FROM Admin where username=%s and password=%s'
        else:
            lookup_query = 'SELECT username FROM User where username=%s and password=%s'
        cursor.execute(lookup_query, (username, password)) 

        if cursor.fetchone():
            return True
    return False
    

@app.route("/", methods=['GET', 'POST'])
def home():
    form = LoginForm()
    if is_logged_in():
        data=f'logged in as {session["username"]}'
        if 'admin' in session:
            return render_template("index.html", logged_in=True,admin=True, data=data, form=form)
        else:
            return render_template("index.html", logged_in=True, data=data, form=form)

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        response = make_response()
        if username[0]=='#':
            if log_in(username[1:], password, as_admin=True):
                session['admin'] = username
                session['username'] = username
        elif log_in(username, password): 
            session['username'] = username
        return redirect(url_for('home'))  
    return render_template("index.html", data='logged out', form=form)


@app.route("/about")
def about():
    return "Our incredible site!"

@app.route("/logout")
def logout():
    """
        Use post req instead?
        THIS DOES NOT PREVENT REPLAYING THE COOKIE
    """ 
    if is_logged_in():
        del session['username']
        if 'admin' in session:
            del session['admin']

    return redirect(url_for('home')) 

@app.route("/signup", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        if add_user_db(name, password):
            #session['username'] = name # Log in user auto...
            return redirect(url_for('home'))
        else:
            # Email already exists in DB!
            return render_template('register.html', form=form)
    else:
        return render_template('register.html', form=form)


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if not is_logged_in(check_admin=True):
        return redirect(url_for('home'))
    form = AdminAddProduct()
    if request.method == 'POST':
        if form.validate_on_submit():
            newProduct = Product()

    return render_template("adminpage.html", form=form)

if __name__ == "__main__":
    # Load local db_conf.json file
    Conn_db.load_conf()
    app.run(debug=True)
