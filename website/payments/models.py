from website.extensions import db
from website.models import Product, Bundle

class SoldProduct(db.Model):

    __tablename__ = 'soldproducts'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    sales_id = db.relationship('Product', back_populates='Product.sales_id')
    sale_price = db.Column(db.Double)
    sale_date = db.Column(db.DateTime)
    sale_qty = db.Column(db.Integer)


    def __repr__(self):
        return "Sales Item"