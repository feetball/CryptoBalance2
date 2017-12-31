import requests, ast
import sqlalchemy
import time

import pdb

from ..models import CoinPrice, CoinApi, Coin, Message, Wallet
from .. import db
from datetime import datetime, timedelta
from flask import json
from sqlalchemy import desc

def get_coin_prices(start_time=None):
    try:
        if price_check_needed():
            coin_price_api = CoinApi.query.filter_by(name='CoinPrices').first_or_404()
            coin_price_response = requests.get(coin_price_api.url)
            coin_prices = json.loads(coin_price_response.text)

            coins = Coin.query.all()

            for coin in coins:
                coin_info = filter(lambda coin_price: coin_price['symbol'] == coin.symbol.upper(), coin_prices)[0]
                update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(coin_info['last_updated'])))

                if db.session.query(CoinPrice).join(CoinPrice.Coin).filter(Coin.symbol==coin_info['symbol'].upper(), CoinPrice.date==update_time).count() == 0:
                    coin_price = CoinPrice(price=float(coin_info['price_usd']),
                                           date=update_time,
                                           Coin=coin)
                    db.session.add(coin_price)

            exe_time = str(datetime.now() - start_time)
            message = Message(name='GET_COIN_PRICES', text='Execution Time: ' + exe_time, date=datetime.now())
            db.session.add(message)
            db.session.commit()
            #print 'Get Coin Prices Success! Execution Time: ' + str(datetime.now() - start_time)
            return 'Success! Execution Time: ' + str(datetime.now() - start_time)
        else:
            return 'No price check needed!'
    except Exception as e:
        temp = e.message
        return 'Error getting coin prices.  Error message: ' + temp
        
        
def get_last_price_check():
    try:
        return Message.query.filter_by(name='GET_COIN_PRICES').order_by(desc(Message.date)).first().date
    except Exception as e:
        return 'Error getting last price check.  Error Message: ' + e.message
        
def price_check_needed():
    last_price_check = get_last_price_check()
    print "time diff: " + str(((datetime.now() - last_price_check).seconds)/60)
    if ((datetime.now() - last_price_check).seconds)/300 > 1:
        return True
    else:
        return False
        
def get_latest_coin_price(coin_symbol):
    try:
        return db.session.query(CoinPrice).join(CoinPrice.Coin).filter(Coin.symbol==coin_symbol.upper()).order_by(desc(CoinPrice.date)).first().price
    except Exception as e:
        return 'Error getting last price.  Error Message: ' + e.message
        
def get_coin_qty(wallet):
    try: 
        db_url = wallet.Coin.CoinApi.url
        url = db_url.format(**{"symbol":wallet.Coin.symbol.lower(), "key":wallet.Coin.CoinApi.key, "address":wallet.address})
        url_response = requests.get(url)
        # next line will set coin quantity to coin_qty
        exec('coin_qty = ' + wallet.Coin.CoinApi.qty_extract_format)

        return coin_qty
        
    except Exception as e:
        return 'Error getting coin quantity.  Error Message: ' + e.message + 'Coin: ' + wallet.Coin.symbol