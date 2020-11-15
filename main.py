from flask import Flask, render_template, request, redirect, url_for, session
from forms import LoginForm, AdminAddProduct
from product import Product
from mysql.connector import errorcode
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

def is_logged_in(check_admin=False):
    try:
        username = session['username']
    except:
        return False
    return user_exists(username, check_admin)

@app.route("/", methods=['GET', 'POST'])
def home():
    form = LoginForm()
    if is_logged_in():
        return render_template("index.html", data='logged in', form=form)

    if request.method == 'POST':
        if form.validate_on_submit():
            session['username'] = form.username.data
            print(session)
            return redirect(url_for('home'))
    return render_template("index.html", data='logged out', form=form)


@app.route("/about")
def about():
    return "Our incredible site!"

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if not is_logged_in(check_admin=True):
        return redirect(url_for('home'))
    form = AdminAddProduct()
    if request.method == 'POST':
        if form.validate_on_submit():
            newProduct = Product()

    return render_template("AdminPage.html", form=form)

if __name__ == "__main__":
    Conn_db.load_conf()
    app.run(debug=False)
