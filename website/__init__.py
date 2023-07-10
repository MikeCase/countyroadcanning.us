import dotenv
import flask_login as login

import os
import os.path as op

from flask import Flask, render_template
from flask_admin import Admin
from werkzeug.security import generate_password_hash

from website.blueprints.bundles.routes import bundle_bp
from website.blueprints.bundles.models import Bundle
from website.blueprints.cart.routes import cart_bp
from website.blueprints.payments.routes import payments_bp
from website.blueprints.payments.models import Sales
from website.blueprints.products.routes import product_bp
from website.blueprints.products.models import Product

from website.admin_viewmodels import (BundleView, FileView, MyAdminIndexView,
                               MyModelView, PaymentView, ProductView)
from website.extensions import db, get_cart_count
from website.initial_products import bundles, products
from website.models import User

dotfile = dotenv.find_dotenv()
dotenv.load_dotenv(dotfile)

def init_login(app_context):
    login_manager = login.LoginManager()
    login_manager.init_app(app_context)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)


def first_run(app):
    """ on the first run of the app the database will be initialized with some default values. """
    with app.app_context():
        username = os.getenv('ADMINUSER')
        email = os.getenv('ADMINEMAIL')
        pwd = os.getenv('ADMINPWD')
        pwhash = generate_password_hash(pwd)

        user = User.query.filter(User.id == 0).first()

        if user == None:
            user = User(username=username, email=email, pw_hash=pwhash)
            print(f'adding admin user @{username} to db.')
            db.session.add(user)
            for product in products:
                p = Product(**product)
                print(f'adding product {product["name"]} to the db.')
                db.session.add(p)
            for bundle in bundles:
                b = Bundle(**bundle)
                print(f'Adding bundle {b.name} to DB.')
                db.session.add(b)

            print("Commiting changes.")
            db.session.commit()



def create_app():
    app = Flask(__name__)
    app.config['ENV'] = int(os.getenv("ENV"))

    if app.config['ENV'] == 1:
        app.config.from_object('conf.ProdConf')
    else:
        app.config.from_object('conf.DevConf')

    db.init_app(app)
    
    if not op.exists('instance/db.sqlite'):
        print('DB not found, creating it now.')
        with app.app_context():
            db.create_all()


    # Check to see if this is the first run of the app.
    if dotenv.get_key(dotfile, key_to_get='FIRSTRUN') == "True":
        first_run(app)
        dotenv.set_key(dotfile, key_to_set='FIRSTRUN', value_to_set="False")
    else:
        print("DB already available. Lets run this puppy!")

    
    init_login(app)

    # init flask-admin
    filespath = op.join(op.dirname(__file__), 'static/assets/product_images')

    admin = Admin(app, name='CRC', index_view=MyAdminIndexView(),
                  base_template='my_master.html', template_mode='bootstrap4')
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(ProductView(Product, db.session))
    admin.add_view(BundleView(Bundle, db.session))
    admin.add_view(PaymentView(Sales, db.session))
    admin.add_view(FileView(filespath, '/static/assets/product_images/', name='Images'))
    
    # register any blueprints the app has.
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(bundle_bp, url_prefix='/bundles')
    app.register_blueprint(payments_bp, url_prefix="/payments")
    app.register_blueprint(product_bp, url_prefix="/products")

    return app






app = create_app()


# Views
@app.route('/')
def home():
    products = Product.query.all()
    img_dir = 'assets/product_images/'
    total_items = get_cart_count()

    return render_template('home/home.html', products=products, img_dir=img_dir, total_count=total_items)


@app.route('/about')
def about_us():
    total_items = get_cart_count()
    return render_template('about/about.html', total_count=total_items)

@app.context_processor
def custom_context():
    return dict(get_cart_count=get_cart_count())