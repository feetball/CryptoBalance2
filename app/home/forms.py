# app/home/forms.py

import pdb

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.ext.dateutil.fields import DateTimeField
from ..models import Coin, CoinApi, CoinPrice, Wallet, User
from app import db

class UserWalletForm(FlaskForm):
    """
    Form for admin to add or edit a wallet
    """
    address = StringField('Address', validators=[DataRequired()])
    coin = QuerySelectField(query_factory=lambda: Coin.query.all(), get_label="name")
    submit = SubmitField('Submit')
    
class AccountInfoForm(FlaskForm):
    """
    Form for user to edit their account info
    """
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField('Submit')