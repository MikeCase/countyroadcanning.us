from flask import render_template, redirect, url_for, request
from flask_paypal_lib import Sandbox
from website.models import Product
from . import paypal_bp

@paypal_bp.route('/')
def index():
    print('paypal payment processing..')
    return render_template('paypal/index.html')


@paypal_bp.route('/process_payment')
def process_payment():
    
    print('processing payment')
    return redirect(url_for('paypal_bp.index'))