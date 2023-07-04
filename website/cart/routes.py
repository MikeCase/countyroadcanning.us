from flask import session, redirect, url_for, request, render_template
from website.models import Product
from .cart import cart_bp

# Main route, Cart homepage
@cart_bp.route('/')
def list():
    if 'cart' not in session:
        return render_template('cart/no_items.html')

    return render_template('cart/index.html', items=session['cart'])


# Add an item to the cart.
@cart_bp.route('/add', methods=['POST'])
def add_item_to_cart():
    if 'cart' not in session:
        session['cart'] = []

    product_id = request.form.get('product_id')
    product = Product.query.filter(Product.id == product_id).first()
    session['cart'].append({'id': product.id, 'name': product.name, 'price': product.price, 'desc': product.description, 'qty': 1, 'per_case': False})

    ## we are setting modified attribute to True because without it Flask will not send the updated session cookie to the client.
    ## @ https://overiq.com/flask-101/sessions-in-flask/
    session.modified = True

    return redirect(url_for('cart_bp.list'))

# Checkout pass off to paypal.
@cart_bp.route('/checkout')
def checkout():
    pass

# Clear the entire cart.
@cart_bp.route('/clear')
def clear_cart():
    if 'cart' in session:
        session['cart'] = []
        return redirect(url_for('cart_bp.list'))

# Remove one item from the cart
@cart_bp.route('/remove_item/<int:product_id>', methods=['GET'])
def rem_item(product_id):
    for item in session['cart']:
        if item['id'] == product_id:
            session['cart'].remove(item)
            session.modified = True
    return redirect(url_for('cart_bp.list'))

# Update an item in the cart.
@cart_bp.route('/update_cart', methods=['POST'])
def update_cart():
    # Get all form values for item being updated
    product_id = int(request.form.get('prod_id'))
    purchase_qty = int(request.form.get('qty'))
    purchase_case = request.form.get('per_case')

    # pull the product from the database by way of the product id
    product = Product.query.filter(Product.id==product_id).first()

    # Just some cleanup.
    jars_per_case = 9

    if purchase_case == None:
        purchase_case = False
    else:
        purchase_case = True

    # Go through each item in the cart(should never honestly be many.)
    for item in session['cart']:
        if item['id'] == product_id:
            item_idx = session['cart'].index(item)
            session['cart'][item_idx].update({'qty': purchase_qty})
            session['cart'][item_idx].update({'per_case': purchase_case})
            if purchase_case == True:
                session['cart'][item_idx].update({'price': (product.price * jars_per_case) * purchase_qty})
            else:
                session['cart'][item_idx].update({'price': (product.price * purchase_qty)})

            session.modified = True
            if purchase_qty <= 0:
                rem_item(product_id)

    return redirect(url_for('cart_bp.list'))