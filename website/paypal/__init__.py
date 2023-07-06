from flask import Blueprint

paypal_bp = Blueprint('paypal_bp', __name__, template_folder='templates', static_folder='static', static_url_path='assets')

import website.paypal.routes