from flask_sqlalchemy import SQLAlchemy # type: ignore
from sqlalchemy import MetaData # type: ignore
from sqlalchemy.orm import validates # type: ignore
from sqlalchemy_serializer import SerializerMixin # type: ignore

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    # Relationship
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='restaurant', cascade='all, delete-orphan')

    # Serialization rules
    serialize_rules = ('-restaurant_pizzas.pizza.restaurant_pizzas',)

    def __repr__(self):
        return f'<Restaurant {self.name}>'

class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)

    # Relationship
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='pizza')

    # Serialization rules
    serialize_rules = ('-restaurant_pizzas.restaurant',)

    def __repr__(self):
        return f'<Pizza {self.name}, {self.ingredients}>'

class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # Relationships
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas')
    pizza = db.relationship('Pizza', back_populates='restaurant_pizzas')

    # Serialization rules
    serialize_rules = ('-restaurant.restaurant_pizzas', '-pizza.restaurant_pizzas')

    @validates('price')
    def validate_price(self, key, price):
        if not (1 <= price <= 30):
            raise ValueError("Price must be between 1 and 30.")
        return price

    def __repr__(self):
        return f'<RestaurantPizza ${self.price}>'
