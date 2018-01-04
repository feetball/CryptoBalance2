# app/admin/forms.py
import pdb

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.ext.dateutil.fields import DateTimeField
from ..models import Coin, CoinApi, CoinPrice, Wallet, User
from app import db

class CoinForm(FlaskForm):
    """
    Form for admin to add or edit a coin
    """
    name = StringField('Name', validators=[DataRequired()])
    symbol = StringField('Symbol', validators=[DataRequired()])
    coin_api = QuerySelectField(query_factory=lambda: CoinApi.query.all(), get_label="name")
    submit = SubmitField('Submit')
    
class CoinApiForm(FlaskForm):
    """
    Form for admin to add or edit a coin api
    """
    name = StringField('Name', validators=[DataRequired()])
    url = StringField('Url', validators=[DataRequired()])
    qty_extract_format = StringField('Extract Format')
    key = StringField('Key', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class PriceForm(FlaskForm):
    """
    Form for admin to add or edit a coin price
    """
    price = FloatField('Price', validators=[DataRequired()])
    date = DateTimeField('Date', validators=[DataRequired()])
    coin = QuerySelectField(query_factory=lambda: Coin.query.all(), get_label="name")
    submit = SubmitField('Submit')
    
class WalletForm(FlaskForm):
    """
    Form for admin to add or edit a wallet
    """
    address = FloatField('Address', validators=[DataRequired()])
    user = QuerySelectField(query_factory=lambda: User.query.all(), get_label="username")
    coin = QuerySelectField(query_factory=lambda: Coin.query.all(), get_label="name")
    submit = SubmitField('Submit')
    
class UserForm(FlaskForm):
    """
    Form for admin to add or edit a user
    """
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class MessageForm(FlaskForm):
    """
 0   Form for admin to edit or delete a message
    """
    name = StringField('Name', validators=[DataRequired()])
    text = StringField('Text', validators=[DataRequired()])
    date = DateTimeField('Date', validators=[DataRequired()])
    submit = SubmitField('Submit')