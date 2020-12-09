from flask import Flask, render_template, request, redirect, url_for, session, make_response
from forms import LoginForm, AdminAddProduct, RegisterForm
from product import Product
from db_conn import Conn_db
import database as db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'DEV'


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
    return db.user_exists(username, check_admin)


@app.route("/", methods=['GET', 'POST'])
def home():
    form = LoginForm()

    products = db.get_products()
    for p in products:
        p['rating'] = int(db.get_star_rating(p['idProduct']))

    if is_logged_in():
        data = f'logged in as {session["username"]}'
        if 'admin' in session:
            return render_template("index.html", products=products, logged_in=True, admin=True, data=data, form=form)
        else:
            return render_template("index.html", products=products, logged_in=True, data=data, form=form)

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        response = make_response()
        if username[0] == '#':
            if db.log_in(username[1:], password, as_admin=True):
                session['admin'] = username
                session['username'] = username
        elif db.log_in(username, password):
            session['username'] = username
        return redirect(url_for('home'))
    return render_template("index.html", products=products, data='logged out', form=form)


@app.route("/about")
def about():
    return "Our incredible site!"


@app.route("/product/<productId>")
def product(productId):
    lookup_query = 'SELECT picture FROM Product where idProduct=productId'
    reviews = db.get_reviews(productId)
    return render_template('product.html', productName="hej", description="Det här är en tomat")
                           #reviews=reviews)


@app.route("/basket")
def basket():
    if not is_logged_in():
        return redirect(url_for('home'))

    products = db.get_basket_products(session['username'])
    for p in products:
        p['rating'] = int(db.get_star_rating(p['idProduct']))

    print(products)
    return render_template('basket.html', products=products)


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
        if db.add_user_db(name, password):
            # session['username'] = name # Log in user auto...
            return redirect(url_for('home'))
        else:
            # Email already exists in DB!
            return render_template('register.html', form=form)
    else:
        return render_template('register.html', form=form)


@app.route("/adminpage", methods=['GET', 'POST'])
def admin():
    if not is_logged_in(check_admin=True):
        return redirect(url_for('home'))
    form = AdminAddProduct()
    if form.validate_on_submit():
        pid = form.productID.data
        stock = form.stock.data
        description = form.description.data
        price = form.price.data
        brand = form.brand.data
        db.addProduct(pid, stock, description, price, brand)

    return render_template("adminpage.html", form=form)


if __name__ == "__main__":
    # Load local db_conf.json file
    Conn_db.load_conf()
    app.run(debug=True)
