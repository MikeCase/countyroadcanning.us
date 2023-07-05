import os
import os.path as op
from flask import Flask
from dotenv import load_dotenv
import flask_login as login
from flask_migrate import Migrate
from .extensions import db, Admin, MyAdminIndexView, MyModelView, ProductView, BundleView, FileView
from .models import User, Product, Bundle
from website.cart import cart_bp
from website.bundles import bundle_bp
from werkzeug.security import generate_password_hash
from .initial_products import products
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config['ENV'] = os.getenv("ENV")

    if app.config['ENV'] == 'prod':
        app.config.from_object('conf.ProdConf')
    else:
        app.config.from_object('conf.DevConf')

    db.init_app(app)
    if not op.exists('instance/db.sqlite'):
        print('DB not found, creating it now.')
        with app.app_context():
            db.create_all()

    migrate = Migrate(app, db)

    init_login(app)
    ## init flask-admin
    filespath = op.join(op.dirname(__file__), 'static/assets/product_images')

    admin = Admin(app, name='CRC', index_view=MyAdminIndexView(), base_template='my_master.html', template_mode='bootstrap4')
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(ProductView(Product, db.session))
    admin.add_view(BundleView(Bundle, db.session))
    admin.add_view(FileView(filespath, '/static/assets/product_images/', name='Images'))
    
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(bundle_bp, url_prefix='/bundles')

    return app


## Utilities
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
        pwhash = generate_password_hash('pwd')

        try:
            user = User.query.filter(User.id == 0).first()
        except:
            user = User(username=username, email=email, pw_hash=pwhash)
            print(f'adding admin user @{username} to db.')
            db.session.add(user)
            for product in products:
                p = Product(**product)
                print(f'adding product {product["name"]} to the db.')
                db.session.add(p)

            print("Commiting changes.")
            db.session.commit()




app = create_app()



import website.routes