from flask import Blueprint

payments_bp = Blueprint('payments_bp', __name__, template_folder='templates', static_folder='static', static_url_path='assets')

import website.payments.routes