from flask import Blueprint

bundle_bp = Blueprint('bundle_bp', __name__, template_folder='templates', static_folder='static', static_url_path='assets')


import website.bundles.routes