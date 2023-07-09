from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import fields, form, validators

from website.models import User


#Define login form (for flask-login)
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
        # print(User.query.filter_by(username=self.login.data).first())
        return User.query.filter_by(username=self.login.data).first()
