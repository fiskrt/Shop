from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    make_response,
)
from forms import LoginForm, AdminAddProduct, RegisterForm, CommentForm
from product import Product
from db_conn import Conn_db
import database as db

app = Flask(__name__)
app.config["SECRET_KEY"] = "DEV"


def is_logged_in(check_admin=False, only_user=False):
    """
    If username start with a '#' then its
    an admin account.

    TODO: Return relevant session data? such as if admin etc
    """
    try:
        username = session["username"]
    except:
        return False
    check_admin = check_admin or username[0] == "#"
    if only_user:
        check_admin = False
    elif username[0] == "#":
        username = username[1:]
    return db.user_exists(username, check_admin)


@app.route("/", methods=["GET", "POST"])
@app.route("/<search>", methods=["GET", "POST"])
def home(search=None):
    form = LoginForm()
    products = db.get_products(search)
    for p in products:
        p["rating"] = int(db.get_star_rating(p["idProduct"]))

    if is_logged_in():
        data = f'logged in as {session["username"]}'
        if "admin" in session:
            return render_template(
                "index.html",
                products=products,
                logged_in=True,
                admin=True,
                data=data,
                form=form,
            )
        else:
            return render_template(
                "index.html", products=products, logged_in=True, data=data, form=form
            )

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        response = make_response()
        if username[0] == "#":
            if db.log_in(username[1:], password, as_admin=True):
                session["admin"] = username
                session["username"] = username
        elif db.log_in(username, password):
            session["username"] = username
        return redirect(url_for("home"))
    return render_template(
        "index.html", products=products, data="logged out", form=form
    )


@app.route("/product/<productId>", methods=["GET", "POST"])
def product(productId):
    logged_in = is_logged_in(only_user=True)
    if logged_in and request.method == "POST":
        if "add_basket" in request.form:
            if request.form["add_basket"]:
                db.add_to_basket(session["username"], 1, productId)
    form = CommentForm()
    product = db.get_product_by_id(productId)
    reviews = db.get_reviews(productId)
    if form.validate_on_submit() and logged_in:
        comment = form.comment.data
        rating = int(form.rating.data)
        db.add_review(session["username"], rating, comment, productId)
        reviews = db.get_reviews(productId)
        return render_template(
            "product.html",
            product=product,
            reviews=reviews,
            form=form,
            logged_in=True,
        )
    return render_template(
        "product.html", product=product, reviews=reviews, form=form, logged_in=logged_in
    )


@app.route("/basket", methods=["GET", "POST"])
def basket():
    if not is_logged_in(only_user=True):
        return redirect(url_for("home"))

    if request.method == "POST":
        try:
            quantity = int(request.form["quantity"])
            prod_id = int(request.form["idProduct"])
        except:
            print("Malformed input")
        else:
            db.set_basket_item_quantity(session["username"], prod_id, quantity)

    products = db.get_basket_products(session["username"])
    for p in products:
        p["rating"] = int(db.get_star_rating(p["idProduct"]))

    return render_template(
        "basket.html", products=products, basket=True, logged_in=True
    )

@app.route("/checkout")
def checkout():
    if not is_logged_in(only_user=True):
        return redirect(url_for("home"))
    if db.checkout(session['username']):
        return "tyvm for your purchase."
    else:
        return "Checkout <b>not</b> completed."


@app.route("/logout")
def logout():
    """
    Use post req instead?
    THIS DOES NOT PREVENT REPLAYING THE COOKIE
    """
    if is_logged_in():
        del session["username"]
        if "admin" in session:
            del session["admin"]

    return redirect(url_for("home"))


@app.route("/signup", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        if db.add_user_db(name, password):
            # session['username'] = name # Log in user auto...
            return redirect(url_for("home"))
        else:
            # Email already exists in DB!
            return render_template("register.html", form=form)
    else:
        return render_template("register.html", form=form)


@app.route("/adminpage", methods=["GET", "POST"])
def admin():
    if not is_logged_in(check_admin=True):
        return redirect(url_for("home"))
    form = AdminAddProduct()
    if form.validate_on_submit():
        name = form.name.data
        price = form.price.data
        description = form.description.data
        brand = form.brand.data
        path = "static/pictures/"
        prod_id = db.add_product(name, price, description, brand, path)
        if prod_id:
            image = form.image.data.save(path + str(prod_id) + ".jpg")

    return render_template("adminpage.html", form=form, admin=True)


if __name__ == "__main__":
    # Load local db_conf.json file
    Conn_db.load_conf()
    app.run(debug=True)
