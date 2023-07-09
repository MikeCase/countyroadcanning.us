import os
from datetime import datetime

from flask import redirect, render_template, request, session, url_for, Blueprint
from flask_paypal_lib import Sandbox

from website.extensions import db, get_cart, get_cart_count
from website.blueprints.products.models import Product

from .models import Sales

payments_bp = Blueprint('payments_bp', __name__, template_folder='templates', static_folder='static', static_url_path='assets', url_prefix='/payments')

@payments_bp.route('/')
def index():
    # print('paypal payment processing..')
    # print(os.getenv('PP_URL'))
    cart = get_cart()
    total_items = get_cart_count()
    session['cart'] = []
    session.modified = True
    return render_template('payments/index.html', total_count=total_items, cart=cart)


@payments_bp.route('/process_payment', methods=['POST'])
def process_payment():
    """ This isn't ideal, more or less a prototype
        I don't like how it doesn't keep track of each item sold, just an overall total. 
        Plus this doesn't even pass off to paypal. """

    sale_items = []
    sale_sub_total = 0
    cases = 0
    jars = 0
    for product in session['cart']:
        item = Product.query.filter(Product.id == product["id"]).first()
        sale_items.append(item)

        # Determine if the item is being sold by the case or the jar
        if product['per_case'] == True:
            cases += product['qty']
        else:
            jars += product['qty']

            # if the number of jars sold makes a case, update the sale to show number of cases sold
            if jars >= 12:
                cases += 1
                jars = jars % 12

        sale_sub_total += product['price']

    tax_rate = 0.083
    taxes = sale_sub_total * tax_rate
    sale_total = sale_sub_total + taxes

    sale = Sales(sale_price=round(sale_total, 2), sale_date=datetime.now(
    ), sale_cases=cases, sale_jars=jars, product_id=sale_items)
    db.session.add(sale)
    db.session.commit()

    return redirect(url_for('payments_bp.index'))
