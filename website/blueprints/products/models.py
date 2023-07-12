from website.extensions import db

product_bundle = db.Table('product_bundle',
                          db.Column('product_id', db.Integer,
                                    db.ForeignKey('products.id')),
                          db.Column('bundle_id', db.Integer,
                                    db.ForeignKey('bundles.id'))
                          )


class Product(db.Model):

    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(255))
    is_active = db.Column(db.Boolean(), default=True)
    price = db.Column(db.Double)
    img_file = db.Column(db.String(255))
    qty = db.Column(db.Integer, default=15)
    bundles = db.relationship('Bundle', secondary=product_bundle, backref='products')

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