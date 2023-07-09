from website.extensions import db


class Bundle(db.Model):

    __tablename__ = 'bundles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))

    def __repr__(self):
        return self.name