# app/home/views.py
import pdb

import datetime

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import home
from forms import UserWalletForm, AccountInfoForm
from .. import db
from ..models import User, Wallet, Balance
from tasks import get_coin_prices, get_latest_coin_price, get_coin_qty

def check_user(user_id):
    """
    Prevent users from accessing another user
    """
    if not current_user.id == user_id:
        abort(403)

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")

@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    get_coin_prices(start_time=datetime.datetime.now())
    
    wallets = User.query.get_or_404(current_user.id).wallets

    balances = []
    total_value = 0.00

    for wallet in wallets:
        price = get_latest_coin_price(wallet.Coin.symbol)
        qty_coins = get_coin_qty(wallet)

        balance = Balance(coin_symbol = wallet.Coin.symbol, 
                          coin_price = price,
                          address = wallet.address,
                          num_coins = qty_coins,
                          usd_value = price * qty_coins)
        balances.append(balance)
        total_value += price*qty_coins
        
    return render_template('home/dashboard.html', balances=balances, total_value=total_value, title="Dashboard")


@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")

##################
# Account Info Views
##################
@home.route('/account_info')
@login_required
def list_account_info():
    """
    List user
    """
    check_user(current_user.id)

    user = User.query.get_or_404(current_user.id)
    wallets = User.query.get_or_404(current_user.id).wallets
    return render_template('home/account_info/account_info.html',
                           user=user, wallets=wallets, title='Account Info')

@home.route('/account_info/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_account_info(id):
    """
    Edit user
    """
    check_user(id)

    add_user = False

    user = User.query.get_or_404(id)
    form = AccountInfoForm(obj=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        db.session.add(user)
        db.session.commit()
        flash('You have successfully edited your user account.')

        # redirect to the users page
        return redirect(url_for('home.list_account_info'))

    form.email.data = user.email
    form.username.data = user.username
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    return render_template('home/account_info/edit_account_info.html', edit_account_info=edit_account_info,
                           form=form, title="Edit Account Info")
                          
######################
# User Wallet Views
######################
@home.route('/user_wallet/add', methods=['GET', 'POST'])
@login_required
def add_user_wallet():
    """
    Add a wallet for the user to the database
    """
    
    check_user(current_user.id)

    add_user_wallet = True
    
    user = current_user

    form = UserWalletForm()
    if form.validate_on_submit():
        wallet = Wallet(address=form.address.data,
                    User= user,
                    Coin=form.coin.data)

        try:
            # add user's wallet to the database
            db.session.add(wallet)
            db.session.commit()
            flash('You have successfully added a new wallet.')
        except:
            # in case wallet name already exists
            flash('Error: Wallet address already exists.')

        # redirect to the wallets page
        return redirect(url_for('home.list_account_info'))

    # load wallet template
    return render_template('home/user_wallets/add_user_wallet.html', add_user_wallet=add_user_wallet,
                           form=form, title='Add Wallet')


@home.route('/user_wallets/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user_wallet(id):
    """
    Edit a user wallet
    """
    add_user_wallet = False

    wallet = Wallet.query.get_or_404(id)
    
    check_user(wallet.user_id)
    
    user = User.query.get_or_404(id)
    form = UserWalletForm(obj=wallet)
    if form.validate_on_submit():
        wallet.address = form.address.data
        wallet.Coin = form.coin.data
        wallet.User = user
        db.session.add(wallet)
        db.session.commit()
        flash('You have successfully edited the wallet.')

        # redirect to the wallets page
        return redirect(url_for('home.list_account_info'))

    form.address.data = wallet.address
    form.user.data = wallet.User
    form.coin.data = wallet.Coin
    return render_template('home/user_wallets/add_user_wallet.html', add_user_wallet=add_user_wallet,
                           form=form, title="Edit Wallet")

@home.route('/user_wallets/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user_wallet(id):
    """
    Delete a user's wallet from the database
    """
    wallet = Wallet.query.get_or_404(id)

    check_user(wallet.user_id)
    
    db.session.delete(wallet)
    db.session.commit()
    flash('You have successfully deleted the wallet.')

    # redirect to the wallets page
    return redirect(url_for('home.list_account_info'))

    return render_template(title="Delete Wallet")


