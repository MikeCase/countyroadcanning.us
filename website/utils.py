import flask_login as login
from website import db

## Utilities
def init_login(app_context):
    login_manager = login.LoginManager()
    login_manager.init_app(app_context)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(db.User).get(user_id)
    