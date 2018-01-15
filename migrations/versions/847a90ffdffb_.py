"""empty message

Revision ID: 847a90ffdffb
Revises:
Create Date: 2018-01-12 09:20:49.999847

"""
from alembic import op
import sqlalchemy as sa
from werkzeug.security import generate_password_hash

# revision identifiers, used by Alembic.
revision = '847a90ffdffb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    CoinApi_table = op.create_table('CoinApi',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=25), nullable=True),
    sa.Column('url', sa.String(length=200), nullable=True),
    sa.Column('qty_extract_format', sa.String(length=256), nullable=True),
    sa.Column('key', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('Department',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('Message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=200), nullable=False),
    sa.Column('text', sa.Unicode(length=200), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    Coin_table = op.create_table('Coin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('symbol', sa.String(length=10), nullable=False),
    sa.Column('coin_api_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['coin_api_id'], ['CoinApi.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('symbol')
    )
    User_table = op.create_table('User',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=True),
    sa.Column('username', sa.String(length=60), nullable=True),
    sa.Column('first_name', sa.String(length=60), nullable=True),
    sa.Column('last_name', sa.String(length=60), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('department_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['department_id'], ['Department.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['Role.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('CoinPrice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('coin_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['coin_id'], ['Coin.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    Wallet_table = op.create_table('Wallet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=128), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('coin_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['coin_id'], ['Coin.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###

    ##############################
    # ### db Seed Data ###
    ##############################
    op.bulk_insert(
        CoinApi_table,
        [
            {'id':1, 'name':'default', 'url':'default', 'qty_extract_format':'default', 'key':'default'},
            {'id':2, 'name':'CryptoID', 'url':'https://chainz.cryptoid.info/{symbol}/api.dws?q=getbalance&key={key}&a={address}', 'qty_extract_format':'float(url_response.text)', 'key':'1a29b449d778'},
            {'id':3, 'name':'Etherscan.io', 'url':'https://api.etherscan.io/api?module=account&action=balance&tag=latest&apikey={key}&address={address}', 'qty_extract_format':"float(ast.literal_eval(url_response.text)['result'])/10e17", 'key':'UUS5UI9VIRY8N5CARUWJTT1IQ5FT4F2UYR'},
            {'id':4, 'name':'Ripple.com', 'url':'https://data.ripple.com/v2/accounts/{address}/stats/value?limit=1&descending=true', 'qty_extract_format':"float(ast.literal_eval(url_response.text)['rows'][0]['account_value'])", 'key':'n/a'},
            {'id':5, 'name':'Zcha.in (Z-Cash)', 'url':'https://api.zcha.in/v2/mainnet/accounts/{address}', 'qty_extract_format':"float(ast.literal_eval(url_response.text)['balance'])", 'key':'n/a'},
            {'id':6, 'name':'Decred.org', 'url':'https://mainnet.decred.org/api/addr/{address}/?noTxList=1', 'qty_extract_format':"float(ast.literal_eval(url_response.text)['balance'])", 'key':'n/a'},
            {'id':7, 'name':'CoinPrices', 'url':'https://api.coinmarketcap.com/v1/ticker/', 'qty_extract_format':'default', 'key':'n/a'}
        ]
    )

    op.bulk_insert(
        Coin_table,
        [
            {'id':1, 'name':'Litecoin', 'symbol':'LTC', 'coin_api_id':2},
            {'id':2, 'name':'Bitcoin', 'symbol':'BTC', 'coin_api_id':2},
            {'id':3, 'name':'Ethereum', 'symbol':'ETH', 'coin_api_id':3},
            {'id':4, 'name':'Z-Cash', 'symbol':'ZEC', 'coin_api_id':5},
            {'id':5, 'name':'Decred', 'symbol':'DCR', 'coin_api_id':6},
            {'id':6, 'name':'Ripple', 'symbol':'XRP', 'coin_api_id':4}
        ]
    )

    op.bulk_insert(
        User_table,
        [
            {'id':1, 'email':'daniel@kuecker.net', 'username':'dkuecker', 'first_name':'d', 'last_name':'k', 'is_admin':1, 'password_hash':generate_password_hash('temp')}
        ]
    )

    op.bulk_insert(
        Wallet_table,
        [
            {'address':'33VKBmdsykMZ6Yd3LzKEDoZ7BaN8VCS67b', 'user_id':1, 'coin_id':2},
            {'address':'0x216E2887C0bdDCe42Ef94AEDA49bA57333Bd77F6', 'user_id':1, 'coin_id':3},
            {'address':'r9ayPXR8R2VnNgxSmaJAvTXAfGin3K3oED', 'user_id':1, 'coin_id':6},
            {'address':'MGNcrwA1FG2hSBg6A1FPrKoFcjN4k1JByV', 'user_id':1, 'coin_id':1},
            {'address':'t1bk26TjvuxEUQ4jMThxZKkuSeXu23oHTvB', 'user_id':1, 'coin_id':4}
        ]
    )

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Wallet')
    op.drop_table('CoinPrice')
    op.drop_index(op.f('ix_User_username'), table_name='User')
    op.drop_index(op.f('ix_User_last_name'), table_name='User')
    op.drop_index(op.f('ix_User_first_name'), table_name='User')
    op.drop_index(op.f('ix_User_email'), table_name='User')
    op.drop_table('User')
    op.drop_table('Coin')
    op.drop_table('Role')
    op.drop_table('Message')
    op.drop_table('Department')
    op.drop_table('CoinApi')
    # ### end Alembic commands ###