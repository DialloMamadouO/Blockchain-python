import subprocess
import json 
import os 
from dotenv import load_dotenv
load_dotenv()
from constants import *
from bit import Key, PrivateKey, PrivateKeyTestnet
from bit.network import NetworkAPI
from bit import *
from web3 import Web3
from pathlib import Path
from bit import wif_to_key
from getpass import getpass
from web3.auto.gethdev import w3                                            
from web3.middleware import geth_poa_middleware
from eth_account import Account
enable PoA middleware
w3.middleware_stack.inject(geth_poa_middleware, layer=0)

#including a mnemonic with prefunded test tokens for testing
mnemonic = os.getenv('MNEMONIC')
print(mnemonic)
depth = 3
# php hd-wallet-derive/hd-wallet-derive.php -g --mnemonic='leg off pipe leg hub kiwi answer legal change board rude visual' --coin=eth --numderive=3 --format=json

# Creating a derive_wallets function
def derive_wallets(mnemonic, coin, depth=3):
    command = f"php hd-wallet-derive/hd-wallet-derive.php -g --mnemonic='{mnemonic}' --coin={coin} --numderive={depth} --format=json"
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    keys = json.loads(output)
    return print(keys)

defineConstants = {
    BTC = 'btc',
    ETH = 'eth',
    BTCTEST = 'btc-test'}

    keys = {}
coins = {ETH: derive_wallets(mnemonic, coin='eth', depth=3), BTCTEST: derive_wallets(mnemonic, coin='btc-test', depth=3)}
print(coins)
derive_wallets(mnemonic, coin='eth', depth=3)

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))


# Let's create private keys object 
eth_priv_key = keys["eth"][0]['priv_key']
btc_priv_key = keys["btc-test"][0]['priv_key']

print(json.dumps(eth_priv_key, indent=4, sort_keys=True))
print(json.dumps(btc_priv_key, indent=4, sort_keys=True))
print(json.dumps(keys, indent=4, sort_keys=True))

# Converting private key string in a child key to an account object that bit or web3.py can use to transact

def priv_key_to_account(coin, priv_key):
    print(coin)
    print(priv_key)
    if coin == ETH:
        return Account.PrivateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)

eth_acc = priv_key_to_account(ETH, eth_priv_key)
btc_acc = priv_key_to_account(BTCTEST, btc_priv_key)

# Creating Transaction
def create_raw_tx(coin, account, recipient, amount):
    if coin == ETH:
        gasEstimate = w3.eth.estimateGas(
        {"from": account.address, "to": recipient, "value": amount}
        )
        return {
       "from": account.address,
        "to": recipient,
        "value": amount,
        "gasPrice": w3.eth.gasPrice,
        "gas": gasEstimate,
        "nonce": w3.eth.getTransactionCount(account.address),
        }

    else: 
        return {
        PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, BTC)])
        }
# Sending Transaction
def send_tx(coin, account, recipient, amount):
    tx = create_raw_tx(coin, account, recipient, amount)

    if coin == ETH:
        signed_tx = eth_acc.sign_transaction(tx)
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(result.hex())
        return result.hex()

    else: 
        tx_btctest = create_raw_tx(coin, account, recipient, amount)
        signed_tx_btctest = account.sign_transaction(tx_btctest)
        return NetworkAPI.broadcast_tx_testnet(signed_tx_btctest)

    create_raw_tx(BTCTEST, "mpeUjwo1oWZVSPUqoSPnfDdrBrrXM9NFq9", 0.1)
    send_tx(BTCTEST, "mpeUjwo1oWZVSPUqoSPnfDdrBrrXM9NFq9", 0.1)

    print(eth_priv_key.get_transactions())
    print(btc_priv_key.get_transactions())
    Collapse










