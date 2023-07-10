from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import fields, validators

from website.models import User


#Define login form (for flask-login)
class LoginForm(FlaskForm):
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
            raise validators.ValidationError('Invalid user')

    def get_user(self):
        # print(User.query.filter_by(username=self.login.data).first())
        return User.query.filter_by(username=self.login.data).first()


## Define form for the shopping cart items.
class ShoppingCartForm(FlaskForm):
    prod_id = fields.HiddenField("product_id")
    qty = fields.IntegerField("Quantity", validators=[validators.InputRequired()])
    per_case = fields.SelectField("Case")
    
    def update_cart(self):
        pass