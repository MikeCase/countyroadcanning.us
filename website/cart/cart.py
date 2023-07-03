from flask import Blueprint


cart_bp = Blueprint('cart_bp', __name__, template_folder='templates', static_folder='static', static_url_path='assets')


import website.cart.routes

    