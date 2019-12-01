import os

from decimal import Decimal

from web3 import Web3

provider_url = os.environ.get("INFURA_URL")

provider = Web3.HTTPProvider(provider_url)

eth_client = Web3(provider)


def account_from_private_key(client, privkey):
    return client.eth.account.from_key(privkey)


def send_eth_from_to_amount(
    client, from_privkey: str, to_pubkey: str, amount: Decimal
) -> str:
    sender_account = account_from_private_key(client, from_privkey)
    params = {
        "to": to_pubkey,
        "from": sender_account.address,
        "nonce": client.eth.getTransactionCount(sender_account.address),
        "value": Web3.toWei(amount, "ether"),
        "gasPrice": client.eth.gasPrice,
    }
    gas = client.eth.estimateGas(params)
    params["gas"] = gas
    signed_tx = sender_account.signTransaction(params)
    tx_hash = client.eth.sendRawTransaction(signed_tx["rawTransaction"])
    return tx_hash.hex()
