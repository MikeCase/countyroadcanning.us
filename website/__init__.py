import os.path as op
from flask import Flask
import flask_login as login
# from .cart import cart_bp
from .extensions import db, Admin, MyAdminIndexView, MyModelView, ProductView, BundleView, FileView
from .models import User, Product, Bundle
# from flask_admin.contrib.fileadmin import FileAdmin
from website.cart.cart import cart_bp
from werkzeug.security import generate_password_hash

app = Flask(__name__)

app.config['ENV'] = "dev"

if app.config['ENV'] == 'prod':
    app.config.from_object('conf.ProdConf')
else:
    app.config.from_object('conf.DevConf')

db.init_app(app)



## Utilities
def init_login(app_context):
    login_manager = login.LoginManager()
    login_manager.init_app(app_context)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)
    
def create_admin_user():
    user = User(username='splaq', email='mike@mikescave.us', pw_hash=generate_password_hash('553rtb63'))
    db.session.add(user)
    db.session.commit()

init_login(app)
## init flask-admin
filespath = op.join(op.dirname(__file__), 'static/assets/product_images')

admin = Admin(app, name='CRC', index_view=MyAdminIndexView(), base_template='my_master.html', template_mode='bootstrap4')
admin.add_view(MyModelView(User, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(BundleView(Bundle, db.session))
admin.add_view(FileView(filespath, '/static/assets/product_images/', name='Images'))

app.register_blueprint(cart_bp, url_prefix='/cart')
import website.routes