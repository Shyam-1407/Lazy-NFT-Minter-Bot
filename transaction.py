from web3 import Web3
import json
import os
from dotenv import load_dotenv
load_dotenv()

def Transaction(metadata):
    w3 = Web3(
        Web3.HTTPProvider(
            "https://sepolia.infura.io/v3/17e9e4971b4d4aff9c6db5e65cca7eef")) 

    # Loading contract ABI
    with open('abi.txt', 'r') as f:
        contract_abi = json.loads(f.read())

    contract_address = "0xB5bfee21BB057Ddcf435707d7f99Fe2185D952aD"

    # contract instance
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    
    # minting adress details
    minter_address = "0xaBBAb4F74b85749b51599D65C2B8468B47870f53"
    private_key = os.getenv("PVT")

    metadata_uri = metadata

    nonce = w3.eth.get_transaction_count(minter_address)

    # current gas price
    gas_price = w3.eth.gas_price

    balance = w3.eth.get_balance(minter_address)
    required_funds = 0.01 + (300000 * w3.to_wei(50, 'gwei')) 
    if balance < required_funds:
        raise Exception(f"Insufficient funds. Balance: {w3.from_wei(balance, 'ether')} ETH")


    # Building the transaction for minting the NFT
    transaction_data = contract.functions.allowListMint(metadata_uri).build_transaction({
        'chainId': w3.eth.chain_id, 
        'gas': 300000, 
        'gasPrice': gas_price,
        'nonce': nonce,
        'from': minter_address,
        'value': w3.to_wei(0.0001, 'ether')
    })

    #signing the transaction and getting the receipt
    signed_txn = w3.eth.account.sign_transaction(transaction_data, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return tx_receipt, tx_hash.hex()
