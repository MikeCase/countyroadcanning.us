from . import app
from PIL import Image
from flask import render_template, url_for
from .models import Product


def sort_products_by_image_size(products):

    sorted_products = []
    for product in products:
        ## Sort images by size, put all long images in the rear.
        cur_product = product
        cur_im = Image.open(f'website/static/assets/product_images/{cur_product.img_file}')
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
    img_dir = 'assets/product_images/'
    return render_template('home/home.html', products=products, img_dir=img_dir)

@app.route('/about')
def about_us():
    return render_template('about/about.html')

@app.route('/products')
def products():
    products = Product.query.filter_by(is_active=True).all()

    img_dir = 'assets/product_images/'
    sorted_products = sort_products_by_image_size(products)

    return render_template('products/products.html', products=sorted_products, img_dir=img_dir)
