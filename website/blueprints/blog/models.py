from website.extensions import db


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    post = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime)
    date_updated = db.Column(db.DateTime)
    