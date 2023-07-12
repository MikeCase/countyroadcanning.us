from flask import Blueprint, render_template

blog_bp = Blueprint("blog_bp", __name__, static_folder='static', template_folder='templates', static_url_path='assets', url_prefix='/blog')

@blog_bp.route("/")
def index():
    return render_template('blog/blog.html')