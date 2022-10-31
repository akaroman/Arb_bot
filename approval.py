#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 14:11:38 2022

@author: ith
"""
from web3 import Web3
import config

# added with key........REMEMBER


def approve(sender_address, key, panRouterContractAddress, tokenContract, gas, chainid, url):
    url = url
    web3 = Web3(Web3.HTTPProvider(url))
    al_value = tokenContract.functions.allowance(sender_address ,panRouterContractAddress).call()
    ap_quan = tokenContract.functions.balanceOf(sender_address).call()
        
    if int(al_value) <= int(ap_quan):
        approve = tokenContract.functions.approve(panRouterContractAddress, 9600000000000000000000).buildTransaction({
                'from': sender_address,
                'chainId': chainid,
                'gas': 100000,
                'gasPrice': web3.toWei(gas,'gwei'),
                'nonce': web3.eth.get_transaction_count(sender_address),
                })
        signed_txn = web3.eth.account.sign_transaction(approve, private_key=key)
        tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        al_value = tokenContract.functions.allowance(sender_address ,panRouterContractAddress).call()
        print(web3.toHex(tx_token) , al_value)
    else:
        print('Already Approved')
       
 