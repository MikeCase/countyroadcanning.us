from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('home/home.html')

@app.route("/products")
def products():
    return render_template('products/products.html')

@app.route("/about")
def about_us():
    return render_template('about/about.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)