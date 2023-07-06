from . import app
# from .extensions import db
from PIL import Image
from flask import render_template, url_for
from .models import Product


def sort_products_by_image_size(products):

    sorted_products = []
    for product in products:
        ## Sort images by size, put all long images in the rear.
        cur_product = product
        cur_im = Image.open(f'website/static/{cur_product.img_file}')
        cur_w, cur_h = cur_im.size

        # Fairly simple sort, if the images are wider than they are tall
        # then we insert the product in the front, otherwise we append it
        # at the end.
        if cur_w > cur_h:
            sorted_products.insert(0, cur_product)
        elif cur_h > cur_w:
            sorted_products.append(cur_product)

    return sorted_products


# Views
@app.route('/')
def home():
    # print('home')
    products = Product.query.all()
    return render_template('home/home.html', products=products)

@app.route('/about')
def about_us():
    return render_template('about/about.html')

@app.route('/products')
def products():
    products = Product.query.filter_by(is_active=True).all()

    sorted_products = sort_products_by_image_size(products)

    return render_template('products/products.html', products=sorted_products)
