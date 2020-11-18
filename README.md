# Blockchain-python
In this project we will use the hd-wallet-derive command line tool to manage crypto assets by integrating this universal wallet and enabling non-standard derivation paths. We will use python to integrate the script into the backend. Ounce, this universal wallet is integrated, we will be able to manage billions of addresses accross more than three hundred coins. 
In this project, however, we will only need to get 2 coins working: Ethereum and Bitcoin Testnet.
## Dependencies
We need to have php installed in our operating system. We need the bit labrary and the web3.py Ethereum library then we will create a project directory called wallet and clone the hd-wallet-derive tool into this folder and install it using the instructions on its README.md.
After installing hd-wallet-derive, we will create a file called wallet.py which will be our universal wallet script. In a seperate file called constants, we will set the following: 
BTC = 'btc'
ETH = 'eth'
BTCTEST = 'btc-test'

In wallet.py, we will use these anytime we reference these strings, both in function calls, and in setting object keys. 
We will generate a new 12 word mnemonic using hd-wallet-derive and set this mnemonic as an environment variable:
mnemonic = os.getenv('MNEMONIC', 'insert mnemonic here').

## Deriving the wallet keys
We will use the subprocess library to call the ./derive script from Python. We will pass the following flags into the shell command as variables:

Mnemonic (--mnemonic) set from an environment variable, or default to a test mnemonic
Coin (--coin)
Numderive (--numderive) to set number of child keys generated
Set the --format=json flag, then parse the output into a JSON object using json.loads(output)
Then, we will wrap all of this into one function, called derive_wallets and create an object called coins that derives ETH and BTCTEST wallets with this function.

## Linhing the transaction signing libraries
Now, we will leverage the keys we've got in the coins object using bit and web3.py and create three more functions:
-priv_key_to_account -- this will convert the privkey string in a child key to an account object
that bit or web3.py can use to transact.

-create_tx -- this will create the raw, unsigned transaction that contains all metadata needed to transact.

-send_tx -- this will call create_tx, sign the transaction, then send it to the designated network.

## Send some transactions
We will now, fund these wallets using testnet faucets. We need to open up a new terminal window inside of wallet,
then run python. Within the Python shell, run from wallet import *, this will give us access to the functions interactively.
We will set the account with  priv_key_to_account and use send_tx to send transactions.

## Local PoA Ethereum transaction
-Here, let's add one of the ETH addresses to the pre-allocated accounts in our networkname.json.

-Delete the geth folder in each node, then re-initialize using geth --datadir nodeX init networkname.json.
This will create a new chain, and will pre-fund the new account.

-Add the following middleware
to web3.py to support the PoA algorithm:

from web3.middleware import geth_poa_middleware

w3.middleware_onion.inject(geth_poa_middleware, layer=0)

Due to a bug in web3.py, we will need to send a transaction or two with MyCrypto first, since the
w3.eth.generateGasPrice() function does not work with an empty chain. We can use one of the ETH address privkey,
or one of the node keystore files.

Send a transaction from the pre-funded address within the wallet to another.



















