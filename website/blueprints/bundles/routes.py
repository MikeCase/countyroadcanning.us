from flask import redirect, render_template, request, url_for, Blueprint

from website.extensions import get_cart_count
from website.blueprints.bundles.models import Bundle


bundle_bp = Blueprint('bundle_bp', __name__, template_folder='templates', static_folder='static', static_url_path='assets', url_prefix="/bundles")

@bundle_bp.route('/')
def bundle_index():
    bundle = Bundle.query.all()
    return render_template('bundles/index.html', bundles=bundle)


@bundle_bp.route("/view/<int:bundle_id>")
def bundle_view(bundle_id):
    bundle = Bundle.query.filter(Bundle.id == bundle_id).first()
    return render_template('bundles/bundle_page.html', bundle=bundle)
