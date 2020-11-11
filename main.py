from flask import Flask, render_template, request, redirect, url_for, session
from forms import LoginForm, AdminAddProduct
from product import Product

app = Flask(__name__)
app.config['SECRET_KEY']='DEV'

def is_logged_in():
    users = ['filip', 'max']
    for user in users:
        if user in session:
            return session[user]
    return False

@app.route("/", methods=['GET', 'POST'])
def home():
    form = LoginForm()
    if is_logged_in():
        return render_template("index.html", data='logged in', form=form)

    print(request.method)
    if request.method == 'POST':
        print('its a post!')
        if form.validate_on_submit():
            session[form.username.data] = True 
            print(session)
            return redirect(url_for('home'))
    return render_template("index.html", data='logged out', form=form)

@app.route("/about")
def about():
    return "Our incredible site!"

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    form = AdminAddProduct()
    if request.method == 'POST':
        if form.validate_on_submit():
            newProduct = Product()

    return render_template("AdminPage.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
