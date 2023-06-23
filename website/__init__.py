import os.path as op
from flask import Flask
import flask_login as login
from .extensions import db, Admin, MyAdminIndexView, MyModelView
from .models import User, Product
from flask_admin.contrib.fileadmin import FileAdmin


app = Flask(__name__)

app.config['ENV'] = "prod"

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

init_login(app)
## init flask-admin
filespath = op.join(op.dirname(__file__), 'static/assets/product_images')

admin = Admin(app, name='CRC', index_view=MyAdminIndexView(), base_template='my_master.html', template_mode='bootstrap4')
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Product, db.session))
admin.add_view(FileAdmin(filespath, '/static/assets/product_images/', name='Images'))

import website.views