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

    cart = relationship("Cart", back_populates="userId")

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Product(db.Model):

    __tablename__ = 'product'

    productId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(100), nullable=False)

    cart = relationship("Cart", back_populates="productId")

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Cart(db.Model):

    __tablename__ = 'cart'

    orderId = db.Column(db.Integer, primary_key=True)

    userId = db.Column(db.Integer, db.ForeignKey("user.userId"))
    productId = db.Column(db.Integer, db.ForeignKey("product.productId"))

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# db.create_all()