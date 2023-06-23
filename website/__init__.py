from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_login as login
from .extensions import db
from .models import User, Product
from . import admin_viewmodels as vm

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
admin = vm.Admin(app, name='CRC', index_view=vm.MyAdminIndexView(), base_template='my_master.html', template_mode='bootstrap4')
admin.add_view(vm.MyModelView(User, db.session))
admin.add_view(vm.MyModelView(Product, db.session))

import website.views