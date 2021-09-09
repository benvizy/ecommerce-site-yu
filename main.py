from flask import Flask, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DecimalField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL

## Initialize App and Bootstrap
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfF66vla43SihBXav7C0sKR6b'
Bootstrap(app)


## Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecom.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##Cafe TABLE Configuration
class User(db.Model):

    __tablename__ = 'user'

    userId = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    address1 = db.Column(db.String(75), nullable=False)
    address2 = db.Column(db.String(75), nullable=True)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    cart = relationship("Cart", back_populates="user")

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Product(db.Model):

    __tablename__ = 'product'

    productId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(100), nullable=False)

    cart = relationship("Cart", back_populates="product")

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Cart(db.Model):

    __tablename__ = 'cart'

    orderId = db.Column(db.Integer, primary_key=True)

    userId = db.Column(db.Integer, db.ForeignKey("user.userId"))
    productId = db.Column(db.Integer, db.ForeignKey("product.productId"))
    user = relationship("User", back_populates="cart")
    product = relationship("Product", back_populates="cart")

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# db.create_all()

# Add some Products
# product1 = Product(
#     name="Japanese Tapestry",
#     price=30,
#     description="2401 Kanji laid out in a colorful grid for you to memorize",
#     image='tapestry.png')
#
# product2 = Product(
#     name="New Idaho",
#     price=20,
#     description="A novel set 30 years into the future, analyzing the consequences of Augmented Reality",
#     image='new-idaho.png')
#
# product3 = Product(
#     name="Japanese Pokemon Encyclopedia",
#     price=50,
#     description="A Pokemon encyclopedia in Japanese",
#     image='pokemon.png')
#
# db.session.add(product1)
# db.session.add(product2)
# db.session.add(product3)
# db.session.commit()



# Create a User Login Form






## Back-End Direction!

@app.route('/')
def home():
    products = db.session.query(Product).all()
    try:
        print(products[0].name)
    except:
        print('product list empty')
    return render_template('home.html', products=products)




if __name__ == "__main__":
    app.run(debug=True)