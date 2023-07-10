from website import app
from flask import render_template
from .extensions import get_cart_count
from .blueprints.products.models import Product

# Views
@app.route('/')
def home():
    products = Product.query.all()
    img_dir = 'assets/product_images/'
    total_items = get_cart_count()

    return render_template('home/home.html', products=products, img_dir=img_dir, total_count=total_items)


@app.route('/about')
def about_us():
    total_items = get_cart_count()
    return render_template('about/about.html', total_count=total_items)
