from .extensions import db


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
    
    def get_id(self):
        return self.id