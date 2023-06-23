from flask_sqlalchemy import SQLAlchemy
from flask import redirect, url_for, request
from flask_admin import AdminIndexView, Admin
from flask_admin import helpers, expose
from flask_admin.contrib.sqla import ModelView
import flask_login as login


# Create DB instance.
db = SQLAlchemy()

from .forms import LoginForm
# Create customized model view class
class MyModelView(ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated
    
# Create customized index view class that handles login & registration
class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        login_form = LoginForm(request.form)
        if helpers.validate_form_on_submit(login_form):
            user = login_form.get_user()
            print(user)
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        link = '<p>Don\'t have an account? Sorry, you can\'t be here then</p>'
        self._template_args['form'] = login_form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('home'))