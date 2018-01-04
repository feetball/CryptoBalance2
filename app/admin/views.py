# app/admin/views.py

from datetime import datetime, timedelta
import pdb

from flask import jsonify, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import CoinForm, CoinApiForm, PriceForm, WalletForm, UserForm, MessageForm
from .. import db
from ..models import Coin, CoinApi, CoinPrice, Wallet, User, Message

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

@admin.route('/get_coin_prices', methods=['GET', 'POST'])
@login_required
def get_coin_prices():
    """
    Get prices for all coins
    """
    check_admin()

    return render_template('admin/tasks/execute_task.html',
                           status=ret, title="Execute Task")


#############
# Coin Views
#############
@admin.route('/coins', methods=['GET', 'POST'])
@login_required
def list_coins():
    """
    List all coins
    """
    check_admin()

    coins = Coin.query.all()

    return render_template('admin/coins/coins.html',
                           coins=coins, title="Coins")

@admin.route('/coins/add', methods=['GET', 'POST'])
@login_required
def add_coin():
    """
    Add a coin to the database
    """
    check_admin()

    add_coin = True

    form = CoinForm()
    if form.validate_on_submit():
        coin = Coin(name=form.name.data, symbol=form.symbol.data, CoinApi=form.coin_api.data)
        try:
            # add coin to the database
            db.session.add(coin)
            db.session.commit()
            flash('You have successfully added a new coin.')
        except:
            # in case coin name already exists
            flash('Error: coin symbol already exists.')

        # redirect to coins page
        return redirect(url_for('admin.list_coins'))

    # load coin template
    return render_template('admin/coins/coin.html', action="Add",
                           add_coin=add_coin, form=form,
                           title="Add Coin")

@admin.route('/coins/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_coin(id):
    """
    Edit a coin
    """
    check_admin()

    add_coin = False

    coin = Coin.query.get_or_404(id)
    form = CoinForm(obj=coin)
    if form.validate_on_submit():
        coin.name = form.name.data
        coin.symbol = form.symbol.data
        coin.CoinApi = form.coin_api.data
        db.session.commit()
        flash('You have successfully edited the coin.')

        # redirect to the coins page
        return redirect(url_for('admin.list_coins'))

    form.symbol.data = coin.symbol
    form.name.data = coin.name
    return render_template('admin/coins/coin.html', action="Edit",
                           add_coin=add_coin, form=form,
                           coin=coin, title="Edit Coin")

@admin.route('/coin/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_coin(id):
    """
    Delete a coin from the database
    """
    check_admin()

    coin = Coin.query.get_or_404(id)
    db.session.delete(coin)
    db.session.commit()
    flash('You have successfully deleted the coin.')

    # redirect to the coins page
    return redirect(url_for('admin.list_coins'))

    return render_template(title="Delete Coin")

#################
# Coin Api Views
#################
@admin.route('/coin_apis')
@login_required
def list_coin_apis():
    check_admin()
    """
    List all coin_apis
    """
    coin_apis = CoinApi.query.all()
    return render_template('admin/coin_apis/coin_apis.html',
                           coin_apis=coin_apis, title='Coin Apis')

@admin.route('/coin_apis/add', methods=['GET', 'POST'])
@login_required
def add_coin_api():
    """
    Add a coin_api to the database
    """
    check_admin()

    add_coin_api = True

    form = CoinApiForm()
    if form.validate_on_submit():
        coin_api = CoinApi(name=form.name.data,
                    url=form.url.data,
                    key=form.key.data,
                    qty_extract_format=form.qty_extract_format.data)

        try:
            # add coin_api to the database
            db.session.add(coin_api)
            db.session.commit()
            flash('You have successfully added a new coin api.')
        except:
            # in case coin_api name already exists
            flash('Error: coin api name already exists.')

        # redirect to the coin_api page
        return redirect(url_for('admin.list_coin_apis'))

    # load coin_api template
    return render_template('admin/coin_apis/coin_api.html', add_coin_api=add_coin_api,
                           form=form, title='Add Coin Api')

@admin.route('/coin_apis/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_coin_api(id):
    """
    Edit a coin_api
    """
    check_admin()

    add_coin_api = False

    coin_api = CoinApi.query.get_or_404(id)
    form = CoinApiForm(obj=coin_api)
    if form.validate_on_submit():
        coin_api.name = form.name.data
        coin_api.url = form.url.data
        coin_api.key = form.key.data
        coin_api.qty_extract_format = form.qty_extract_format.data
        db.session.add(coin_api)
        db.session.commit()
        flash('You have successfully edited the coin api.')

        # redirect to the coin_apis page
        return redirect(url_for('admin.list_coin_apis'))

    form.url.data = coin_api.url
    form.name.data = coin_api.name
    form.key.data = coin_api.key
    form.qty_extract_format.data = coin_api.qty_extract_format
    return render_template('admin/coin_apis/coin_api.html', add_coin_api=add_coin_api,
                           form=form, title="Edit Coin Api")

@admin.route('/coin_apis/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_coin_api(id):
    """
    Delete a coin_api from the database
    """
    check_admin()

    coin_api = CoinApi.query.get_or_404(id)
    db.session.delete(coin_api)
    db.session.commit()
    flash('You have successfully deleted the coin api.')

    # redirect to the coin_apis page
    return redirect(url_for('admin.list_coin_apis'))

    return render_template(title="Delete Coin Api")

###############
#Users Views
###############
@admin.route('/users')
@login_required
def list_users():
    """
    List all users
    """
    check_admin()

    users = User.query.all()
    return render_template('admin/users/users.html',
                           users=users, title='Users')

@admin.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    """
    Add a user to the database
    """
    check_admin()

    add_user = True

    form = UserForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    is_admin=form.is_admin.data)
        try:
            # add user to the database
            db.session.add(user)
            db.session.commit()
            flash('You have successfully added a new user.')
        except:
            # in case user name already exists
            flash('Error: User already exists.')

        # redirect to the users page
        return redirect(url_for('admin.list_users'))

    # load user template
    return render_template('admin/users/user.html', add_user=add_user,

                           form=form, title='Add User Price')


@admin.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    """
    Edit a user
    """
    check_admin()

    add_user = False

    user = User.query.get_or_404(id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        db.session.add(user)
        db.session.commit()
        flash('You have successfully edited the user.')

        # redirect to the users page
        return redirect(url_for('admin.list_users'))

    form.email.data = user.email
    form.username.data = user.username
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    return render_template('admin/users/user.html', add_user=add_user,
                           form=form, title="Edit User")

@admin.route('/users/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    """
    Delete a user from the database
    """
    check_admin()

    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('You have successfully deleted the user.')

    # redirect to the users page
    return redirect(url_for('admin.list_users'))

    return render_template(title="Delete User")


################
# Prices Views
################
@admin.route('/prices')
@login_required
def list_prices():
    check_admin()
    """
    List all prices
    """
    prices = CoinPrice.query.all()
    return render_template('admin/prices/prices.html',
                           prices=prices, title='Prices')

@admin.route('/prices/add', methods=['GET', 'POST'])
@login_required
def add_price():
    """
    Add a price to the database
    """
    check_admin()

    add_price = True

    form = PriceForm()
    if form.validate_on_submit():
        price = CoinPrice(price=form.price.data,
                    date=form.date.data,
                    Coin=form.coin.data)

        try:
            # add price to the database
            db.session.add(price)
            db.session.commit()
            flash('You have successfully added a new coin price.')
        except:
            # in case price name already exists
            flash('Error: coin price already exists.')

        # redirect to the prices page
        return redirect(url_for('admin.list_prices'))

    # load price template
    return render_template('admin/prices/price.html', add_price=add_price,
                           form=form, title='Add Coin Price')

@admin.route('/prices/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_price(id):
    """
    Edit a price
    """
    check_admin()

    add_price = False

    price = CoinPrice.query.get_or_404(id)
    form = PriceForm(obj=price)
    if form.validate_on_submit():
        price.price = form.price.data
        price.date = form.date.data
        price.Coin = form.coin.data
        db.session.add(price)
        db.session.commit()
        flash('You have successfully edited the coin price.')

        # redirect to the prices page
        return redirect(url_for('admin.list_prices'))

    form.price.data = price.price
    form.date.data = price.date
    form.coin.data = price.Coin
    return render_template('admin/prices/price.html', add_price=add_price,
                           form=form, title="Edit Coin Price")

@admin.route('/prices/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_price(id):
    """
    Delete a price from the database
    """
    check_admin()

    price = CoinPrice.query.get_or_404(id)
    db.session.delete(price)
    db.session.commit()
    flash('You have successfully deleted the coin price.')

    # redirect to the prices page
    return redirect(url_for('admin.list_prices'))

    return render_template(title="Delete Coin Price")


######################
# Wallet Views
######################
@admin.route('/wallets')
@login_required
def list_wallets():
    check_admin()
    """
    List all wallets
    """
    wallets = Wallet.query.all()
    return render_template('admin/wallets/wallets.html',
                           wallets=wallets, title='Wallets')

@admin.route('/wallets/add', methods=['GET', 'POST'])
@login_required
def add_wallet():
    """
    Add a wallet to the database
    """
    check_admin()

    add_wallet = True

    form = WalletForm()
    if form.validate_on_submit():
        wallet = Wallet(address=form.address.data,
                    User=form.user.data,
                    Coin=form.coin.data)

        try:
            # add wallet to the database
            db.session.add(wallet)
            db.session.commit()
            flash('You have successfully added a new wallet.')
        except:
            # in case wallet name already exists
            flash('Error: Wallet already exists.')

        # redirect to the wallets page
        return redirect(url_for('admin.list_wallets'))

    # load wallet template
    return render_template('admin/wallets/wallet.html', add_wallet=add_wallet,

                           form=form, title='Add Wallet Price')


@admin.route('/wallets/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_wallet(id):
    """
    Edit a wallet
    """
    check_admin()

    add_wallet = False

    wallet = Wallet.query.get_or_404(id)
    form = WalletForm(obj=wallet)
    if form.validate_on_submit():
        wallet.address = form.address.data
        wallet.Coin = form.coin.data
        wallet.User = form.user.data
        db.session.add(wallet)
        db.session.commit()
        flash('You have successfully edited the wallet.')

        # redirect to the wallets page
        return redirect(url_for('admin.list_wallets'))

    form.address.data = wallet.address
    form.user.data = wallet.User
    form.coin.data = wallet.Coin
    return render_template('admin/wallets/wallet.html', add_wallet=add_wallet,
                           form=form, title="Edit Wallet")

@admin.route('/wallets/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_wallet(id):
    """
    Delete a wallet from the database
    """
    check_admin()

    wallet = Wallet.query.get_or_404(id)
    db.session.delete(wallet)
    db.session.commit()
    flash('You have successfully deleted the wallet.')

    # redirect to the wallets page
    return redirect(url_for('admin.list_wallets'))

    return render_template(title="Delete Wallet")

##############
# Message Views
##############
@admin.route('/messages/')
def list_messages():
    messages = Message.query.all()
    return render_template('admin/messages/messages.html',
                           messages=messages, title="Messages")

@admin.route('/messages/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_message(id):
    """
    Edit a message
    """
    check_admin()

    add_message = False

    message = Message.query.get_or_404(id)
    form = MessageForm(obj=message)
    if form.validate_on_submit():
        message.name = form.name.data
        message.text = form.text.data
        message.date = form.date.data
        db.session.add(message)
        db.session.commit()
        flash('You have successfully edited the message.')

        # redirect to the messages page
        return redirect(url_for('admin.list_messages'))

    form.name.data = message.name
    form.text.data = message.text
    form.date.data = message.date
    return render_template('admin/messages/message.html', add_message=add_message,
                           form=form, title="Edit Message")

@admin.route('/messages/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_message(id):
    """
    Delete a message from the database
    """
    check_admin()

    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    flash('You have successfully deleted the message.')

    # redirect to the messages page
    return redirect(url_for('admin.list_messages'))

    return render_template(title="Delete Message")
