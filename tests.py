# tests.py

import pdb
import os
import unittest

from flask import abort, url_for
from flask_testing import TestCase


from app import create_app, db
from app.models import User, Coin, CoinApi, CoinPrice, Wallet

class TestBase(TestCase):

    def create_app(self):

        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql://cb_test:cb_tester@localhost/cryptobalance_test'
        )
        return app

    def setUp(self):
        """
        Will be called before every test
        """

        db.create_all()

        # create test admin user
        admin = User(username="admin", password="admin2016", is_admin=True)

        # create test non-admin user
        user = User(username="test_user", password="test2016")

        # save users to database
        db.session.add(admin)
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()


class TestModels(TestBase):

    def test_user_model(self):
        """
        Test number of records in User table
        """
        self.assertEqual(User.query.count(), 2)

    def test_Coin_model(self):
        """
        Test number of records in Coin table
        """

        # create test coin
        coin = Coin(name="BTC", symbol="BTC")

        # save coin to database
        db.session.add(coin)
        db.session.commit()

        self.assertEqual(Coin.query.count(), 1)

    def test_CoinApi_model(self):
        """
        Test number of records in CoinApi table
        """

        # create test CoinApi
        coin_api = CoinApi(name="Coin Market Cap", url="http://coinmarketcap.com", key="ABCDEF")

        # save coin api to database
        db.session.add(coin_api)
        db.session.commit()

        self.assertEqual(CoinApi.query.count(), 1)

    def test_CoinPrice_model(self):
        """
        Test number of records in CoinPrice table
        """

        # create test coin and get it's id
        coin = Coin(name="BTC", symbol="BTC")
        db.session.add(coin)
        db.session.commit()
        coin_id = Coin.query.all()[0].id

        # create test CoinPrice
        coin_price = CoinPrice(price=12.34, coin_id=coin_id, date="2001-01-01 01:01:01")

        # save coin price to database
        db.session.add(coin_price)
        db.session.commit()

        self.assertEqual(CoinPrice.query.count(), 1)

    def test_Wallet_model(self):
        """
        Test number of records in Wallet table
        """

        #create test user and coin and get thier ids
        user = User(username="test_user_wallet", password="test2017")
        coin = Coin(name="BTC", symbol="BTC")
        db.session.add(user)
        db.session.add(coin)
        db.session.commit()
        user_id = User.query.all()[0].id
        coin_id = Coin.query.all()[0].id

        # create test Wallet
        wallet = Wallet(address="ABCDEF", user_id=user_id, coin_id=coin_id)

        # save wallet to database
        db.session.add(wallet)
        db.session.commit()

        self.assertEqual(Wallet.query.count(), 1)

class TestViews(TestBase):

    def test_homepage_view(self):
        """
        Test that homepage is accessible without login
        """
        response = self.client.get(url_for('home.homepage'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        """
        Test that login page is accessible without login
        """
        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        """
        Test that logout link is inaccessible without login
        and redirects to login page then to logout
        """
        target_url = url_for('auth.logout')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_dashboard_view(self):
        """
        Test that dashboard is inaccessible without login
        and redirects to login page then to dashboard
        """
        target_url = url_for('home.dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_admin_dashboard_view(self):
        """
        Test that dashboard is inaccessible without login
        and redirects to login page then to dashboard
        """
        target_url = url_for('home.admin_dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_coins_view(self):
        """
        Test that coins page is inaccessible without login
        and redirects to login page then to coins page
        """
        target_url = url_for('admin.list_coins')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_coin_prices_view(self):
        """
        Test that coin_prices page is inaccessible without login
        and redirects to login page then to coin_prices page
        """
        target_url = url_for('admin.list_prices')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_users_view(self):
        """
        Test that users page is inaccessible without login
        and redirects to login page then to users page
        """
        target_url = url_for('admin.list_users')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_coin_apis_view(self):
        """
        Test that coin_apis page is inaccessible without login
        and redirects to login page then to coin_apis page
        """
        target_url = url_for('admin.list_coin_apis')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_wallet_view(self):
        """
        Test that wallets page is inaccessible without login
        and redirects to login page then to wallets page
        """
        target_url = url_for('admin.list_wallets')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

class TestErrorPages(TestBase):

    def test_403_forbidden(self):
        # create route to abort the request with the 403 Error
        @self.app.route('/403')
        def forbidden_error():
            abort(403)

        response = self.client.get('/403')
        self.assertEqual(response.status_code, 403)
        self.assertTrue("403 Error" in response.data)

    def test_404_not_found(self):
        response = self.client.get('/nothinghere')
        self.assertEqual(response.status_code, 404)
        self.assertTrue("404 Error" in response.data)

    def test_500_internal_server_error(self):
        # create route to abort the request with the 500 Error
        @self.app.route('/500')
        def internal_server_error():
            abort(500)

        response = self.client.get('/500')
        self.assertEqual(response.status_code, 500)
        self.assertTrue("500 Error" in response.data)

if __name__ == '__main__':
    unittest.main()