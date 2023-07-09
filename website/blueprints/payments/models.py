from website.extensions import db


product_sales = db.Table('product_sales', 
                         db.Column('product_id', db.Integer, db.ForeignKey('products.id')),
                         db.Column('sales_id', db.Integer, db.ForeignKey('productsales.id'))
                         )

class Sales(db.Model):

    __tablename__ = 'productsales'

    id = db.Column(db.Integer, primary_key=True)
    sale_price = db.Column(db.Double)
    sale_date = db.Column(db.DateTime)
    sale_jars = db.Column(db.Integer, default=1)
    sale_cases = db.Column(db.Integer, default=0)
    product_id = db.relationship('Product', secondary=product_sales)



    def __repr__(self):
        return f"Sale Item {self.id}"