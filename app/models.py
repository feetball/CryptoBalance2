# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class User(UserMixin, db.Model):
    """
    Create an User table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('Department.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('Role.id'))
    is_admin = db.Column(db.Boolean, default=False)
    wallets = db.relationship('Wallet', backref='User', lazy='dynamic')
    
    def count_wallets(self):
        """
        Count the number of wallets assigned to user
        """
        return len(self.wallets.all())
    
    @property
    def password(self):
        """
        Prevent password from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'Department'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='department',
                                lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)

class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'Role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='Role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)

class Coin(db.Model):
    __tablename__ = 'Coin'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    symbol = db.Column(db.String(10), nullable=False, unique=True)
    coin_api_id = db.Column(db.Integer, db.ForeignKey('CoinApi.id'))
    coin_prices = db.relationship('CoinPrice', backref='Coin', lazy='dynamic')
    wallets = db.relationship('Wallet', backref='Coin', lazy='dynamic')
    
    def count_prices(self):
        """
        Count the number of prices assigned to coin
        """
        return len(self.coin_prices.all())
    
    def __repr__(self):
        return '<Coin: {}>'.format(self.name)
        
class CoinPrice(db.Model):
    __tablename__ = 'CoinPrice'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price =  db.Column(db.Float)
    coin_id = db.Column(db.Integer, db.ForeignKey('Coin.id'), nullable=False)
    date = db.Column(db.DateTime)
        
    def __repr__(self):
        return '<Price: {}>'.format(self.price)

class CoinApi(db.Model):
    __tablename__ = 'CoinApi'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), unique=True)
    url = db.Column(db.String(200))
    qty_extract_format = db.Column(db.String(256))
    key = db.Column(db.String(100))
    coins = db.relationship('Coin', backref='CoinApi', lazy='dynamic')
    
    def __repr__(self):
        return '<CoinApi: {}>'.format(self.name)

class Wallet(db.Model):
    __tablename__ = 'Wallet'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    coin_id = db.Column(db.Integer, db.ForeignKey('Coin.id'), nullable=False)
    
    def __repr__(self):
        return '<Wallet: {}>'.format(self.address)

#################
# Misc DB Classes
#################
class Message(db.Model):
    __tablename__ = 'Message'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(200), nullable=False)
    text = db.Column(db.Unicode(200))
    date = db.Column(db.DateTime)
    
    def __repr__(self):
        return '<Message Text: {}>'.format(self.text)

#################
# NON-DB Classes
#################

class Balance(object):
    def __init__(self, coin_symbol, coin_price, address, num_coins, usd_value):
        self.coin_symbol = coin_symbol
        self.coin_price = coin_price
        self.address = address
        self.num_coins = num_coins
        self.usd_value = usd_value

