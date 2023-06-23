from . import app
from .extensions import db
from flask import render_template
from .models import Product

# Views
@app.route('/')
def home():
    print('home')
    return render_template('home/home.html')

@app.route('/about')
def about_us():
    return render_template('about/about.html')

@app.route('/products')
def products():
    products = db.session.query(Product).filter_by(is_active=True).all()
    print(products)
    return render_template('products/products.html', products=products)
