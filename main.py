from flask import Flask, render_template, request, redirect, url_for
from forms import LoginForm, AdminAddProduct
from product import Product

app = Flask(__name__)
app.config['SECRET_KEY']='DEV'

@app.route("/", methods=['GET', 'POST'])
def home():
    print(request.method)
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            print(request.form)
            return redirect(url_for('home'))
    return render_template("index.html", data='test', form=form)

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
