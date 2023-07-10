from flask import session
from flask_sqlalchemy import SQLAlchemy
from PIL import Image

# Create DB instance.
db = SQLAlchemy()

def sort_products_by_image_size(products):

    sorted_products = []
    for product in products:
        # Sort images by size, put all long images in the rear.
        cur_product = product
        cur_im = Image.open(
            f'website/static/assets/product_images/{cur_product.img_file}'
        )
        cur_w, cur_h = cur_im.size

        # Fairly simple sort, if the images are wider than they are tall
        # then we insert the product in the front, otherwise we append it
        # at the end.
        if cur_w > cur_h:
            sorted_products.insert(0, cur_product)
        elif cur_h > cur_w:
            sorted_products.append(cur_product)

    return sorted_products

## Used to add a badge at the top of the base template displaying the shopping cart count.
def get_cart_count():
    if 'cart' not in session:
        session['cart'] = []
        return 0
    else:
        total_count = len(session['cart']) or 0
        return total_count

## Get the contents of the shopping cart.
def get_cart():
    if 'cart' not in session:
        session['cart'] = []
        return session['cart']
    else:
        return session['cart']