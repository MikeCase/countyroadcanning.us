from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from wtforms import form, fields, validators
from flask_admin import Admin, AdminIndexView
from flask_admin import helpers, expose
from flask_admin.contrib.sqla import ModelView
import flask_login as login
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.config.from_pyfile('conf.py')
# app.config['SECRET_KEY'] = 'Testing-Key1234ChangeMe'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = { "pool_pre_ping": True, }
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



## init SQLAlchemy
db = SQLAlchemy(app)


# Define Models

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(80), unique=True)
    # is_active = db.Column(db.Boolean(), default=True)
    pw_hash = db.Column(db.String(255))

    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    @property
    def get_id(self):
        return self.id
    
    @property
    def __unicode__(self):
        return self.username

class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(255))
    is_active = db.Column(db.Boolean(), default=True)
    price = db.Column(db.Double)
    img_file = db.Column(db.String(255))
    qty = db.Column(db.Integer, default=15)

    @property
    def get_qty(self):
        return self.qty
    
    @property
    def get_price(self):
        return self.price
    
    @property
    def get_id(self):
        return self.id


## Utilities
def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)


# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    login = fields.StringField(validators=[validators.InputRequired()])
    password = fields.PasswordField(validators=[validators.InputRequired()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.pw_hash, self.password.data):
        # to compare plain text passwords use
        # if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        # print(db.session.query(User).filter_by(username=self.login.data).first())
        return db.session.query(User).filter_by(username=self.login.data).first()


class RegistrationForm(form.Form):
    login = fields.StringField(validators=[validators.InputRequired()])
    email = fields.StringField()
    password = fields.PasswordField(validators=[validators.InputRequired()])

    def validate_login(self, field):
        if db.session.query(User).filter_by(username=self.login.data).count() > 0:
            raise validators.ValidationError('Duplicate username')
        

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
            print(user.id)
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        link = '<p>Don\'t have an account? Sorry, you can\'t be here then</p>'
        self._template_args['form'] = login_form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    # @expose('/register/', methods=('GET', 'POST'))
    # def register_view(self):
    #     register_form = RegistrationForm(request.form)
    #     if helpers.validate_form_on_submit(register_form):
    #         user = User()

    #         register_form.populate_obj(user)
    #         # we hash the users password to avoid saving it as plaintext in the db,
    #         # remove to use plain text:
    #         user.password = generate_password_hash(register_form.password.data)

    #         db.session.add(user)
    #         db.session.commit()

    #         login.login_user(user)
    #         return redirect(url_for('.index'))
    #     link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
    #     self._template_args['form'] = register_form
    #     self._template_args['link'] = link
    #     return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('home'))
# Views
@app.route('/')
def home():
    return render_template('home/home.html')

@app.route('/about')
def about_us():
    return render_template('about/about.html')

@app.route('/products')
def products():
    products = db.session.query(Product).filter_by(is_active=True).all()
    print(products)
    return render_template('products/products.html', products=products)

init_login()
## init flask-admin
admin = Admin(app, name='CRC', index_view=MyAdminIndexView(), base_template='my_master.html', template_mode='bootstrap4')
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Product, db.session))

# with app.app_context():
#     db.create_all()
#     default_user = User(username=app.config['ADMIN_USER'], pw_hash=generate_password_hash(app.config['ADMIN_PASS']))
#     db.session.add(default_user)

#     product = Product(name="Pear Moscato", description="Pear and Moscato Jelled", price=10.50, img_file="assets/pearmoscato.jpeg")
#     product1 = Product(name="Jalapeno Jelly", description="Spicy!", price=6.50, img_file="assets/Jalapeno.jpeg")
#     product2 = Product(name="Cranberry Pomegranet", description="Cranberry Pom yummyness!", price=6.25, img_file="assets/Cran.Pom.jpeg")
#     product3 = Product(name="Blueberry Jam", description="MMM MMM Blueberries!", price=6.25, img_file="assets/Blueberry.jpeg")
#     product4 = Product(name="Blackberry Merlot", description="Blackberry and merlot jam", price=7.50, img_file="assets/blackberrymerlot.jpeg")
#     product5 = Product(name="Peach Jelly", description="Delicious Peach Jelly", price=5.75, img_file="assets/Peach.jpeg")
#     product6 = Product(name="Pumpkin Pie Jam", description="Pumpkin Pie", price=6.50, img_file="assets/pumpkin_pie.jpg")
#     product7 = Product(name="Raspberry Jalapeno", description="Spicy Raspberries!", price=6.00, img_file="assets/raspberryjalapeno.jpeg")
#     db.session.add(product)
#     db.session.add(product1)
#     db.session.add(product2)
#     db.session.add(product3)
#     db.session.add(product4)
#     db.session.add(product5)
#     db.session.add(product6)
#     db.session.add(product7)

    
#     db.session.commit()


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')