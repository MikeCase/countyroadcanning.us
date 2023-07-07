from .extensions import db


product_bundle = db.Table('product_bundle',
                          db.Column('product_id', db.Integer, db.ForeignKey('products.id')),
                          db.Column('bundle_id', db.Integer, db.ForeignKey('bundles.id'))
                          )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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

    def get_id(self):
        return self.id

    @property
    def __unicode__(self):
        return self.username

class Product(db.Model):

    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(255))
    is_active = db.Column(db.Boolean(), default=True)
    price = db.Column(db.Double)
    img_file = db.Column(db.String(255))
    qty = db.Column(db.Integer, default=15)
    bundles = db.relationship('Bundle', secondary=product_bundle, backref=db.backref('products', lazy='select'))
    

    @property
    def get_qty(self):
        return self.qty

    @property
    def get_price(self):
        return self.price

    # @property
    # def get_bundles(self):
    #     return self.bundles

    def get_id(self):
        return self.id

    def __repr__(self):
        return self.name

class Bundle(db.Model):

    __tablename__ = 'bundles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))

    def __repr__(self):
        return self.name
