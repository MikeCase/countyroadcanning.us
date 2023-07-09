import flask_login as login
from flask import redirect, request, url_for
from flask_admin import AdminIndexView, expose, helpers
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from website.forms import LoginForm



# Create customized model view class
class MyModelView(ModelView):

    def __init__(self, *args, **kwargs):
        super(MyModelView, self).__init__(*args, **kwargs)

    def is_accessible(self):
        return login.current_user.is_authenticated


class ProductView(MyModelView):

    def __init__(self, *args, **kwargs):
        super(ProductView, self).__init__(*args, **kwargs)

    can_view_details = True
    column_list = ['name', 'description', 'is_active',
                   'price', 'img_file', 'qty', 'bundles',]


class BundleView(MyModelView):

    def __init__(self, *args, **kwargs):
        super(BundleView, self).__init__(*args, **kwargs)

    can_view_details = True
    # column_list = ['name']


class PaymentView(MyModelView):

    def __init__(self, *args, **kwargs):
        super(PaymentView, self).__init__(*args, **kwargs)

    can_view_details = True
    column_list = ['sale_price', 'sale_date', 'product_id']


class FileView(FileAdmin):

    def __init__(self, *args, **kwargs):
        super(FileView, self).__init__(*args, **kwargs)

    can_view_details = True
    column_list = ['name', 'size', 'date']

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
