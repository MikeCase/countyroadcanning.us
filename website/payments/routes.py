import os
from flask import render_template, redirect, url_for, request
from flask_paypal_lib import Sandbox
from .models import SoldProduct
from . import payments_bp

@payments_bp.route('/')
def index():
    print('paypal payment processing..')
    print(os.getenv('PP_URL'))
    print(SoldProduct.query.all())
    return render_template('payments/index.html')


@payments_bp.route('/process_payment')
def process_payment():

    print('processing payment')
    return redirect(url_for('payments_bp.index'))