from flask import render_template, url_for, request, redirect
from website.models import Bundle
from . import bundle_bp

@bundle_bp.route('/')
def bundle_index():
    return render_template('bundles/index.html')


