from website.extensions import get_cart_count, sort_products_by_image_size
from website.blueprints.products.models import Product

from flask import Blueprint, render_template

product_bp = Blueprint('product_bp', __name__, template_folder='templates')

@product_bp.route('/')
def products():
    products = Product.query.filter_by(is_active=True).all()

    img_dir = 'assets/product_images/'
    sorted_products = sort_products_by_image_size(products)
    total_items = get_cart_count()
    
    return render_template('products/products.html', products=sorted_products, img_dir=img_dir, total_count=total_items)


@product_bp.route('/view/<int:product_id>', methods=['GET'])
def product_view(product_id):
    product = Product.query.filter(Product.id == product_id).first()
    total_items = get_cart_count()

    if product:
        return render_template('products/product_page.html', product=product, total_count=total_items)
    else:
        return render_template('products/not_found.html', total_count=total_items)