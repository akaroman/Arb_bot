#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 15:58:51 2022

@author: ith
"""
import pancake
import time
from sys import exit
import config

web3 = pancake.web3

def buy(amount, slippage, routerContract, tokenAaddr, tokenBaddr, gas, gaslimit, chainid):
    
    if (float(amount) > pancake.tokenB_bal):
         print("Insufficient balance")
         exit()
        
    tokenValue = int(amount * (10 ** pancake.decB))
    
    print(f"Swapping {amount} {pancake.sym_B} for {pancake.sym_A} ")
    
    amountout = routerContract.functions.getAmountsOut(tokenValue, [tokenBaddr, tokenAaddr]).call()
    
    readable = float(web3.fromWei(amountout[1],'ether'))
    readable = readable - (readable*slippage)
    
    amountOutMin = int(readable * (10 ** pancake.decA)) 
    
    pancakeswap2_txn = routerContract.functions.swapExactTokensForTokens(
                             tokenValue,
                             amountOutMin,
                             [tokenBaddr,tokenAaddr],
                             pancake.sender_address,
                             (int(time.time()) + 1000000)
            
                             ).buildTransaction({
                             'from': pancake.sender_address,
                             'chainId': chainid,
                             'gas': gaslimit,
                             'gasPrice': web3.toWei(gas, 'gwei'),
                             'nonce': web3.eth.get_transaction_count(pancake.sender_address),
                     })

    signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=config.private)
    tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt  = web3.eth.wait_for_transaction_receipt(web3.toHex(tx_token))
          
    if(receipt['status'] == 1):
         print(f'TXN SUCCESS!!! {web3.toHex(tx_token)}')
    else:
         print('FAILED!!!  {web3.toHex(tx_token)}')  
      
    
def sell(amount, slippage, routerContract, tokenAaddr, tokenBaddr, gas, gaslimit, chainid):
    
   if (float(amount) > pancake.tokenA_bal):
         print("Insufficient balance")
         exit()
        
   tokenValue = int(amount * (10 ** pancake.decB))
   
   print(f"Swapping {amount} {pancake.sym_A} for {pancake.sym_B} ")
   
   amountout = routerContract.functions.getAmountsOut(tokenValue, [tokenAaddr, tokenBaddr]).call()

   readable = float(web3.fromWei(amountout[1],'ether'))
   readable = readable - (readable*slippage)

   amountOutMin = int(readable * (10 ** pancake.decA)) 
   
   pancakeswap2_txn = routerContract.functions.swapExactTokensForTokens(
                    tokenValue,
                    amountOutMin,
                    [tokenAaddr,tokenBaddr],
                    pancake.sender_address,
                    (int(time.time()) + 1000000)

                    ).buildTransaction({
                    'from': pancake.sender_address,
                    'chainId': chainid,
                    'gas': gaslimit,
                    'gasPrice': web3.toWei(gas, 'gwei'),
                    'nonce': web3.eth.get_transaction_count(pancake.sender_address),
                    })

   signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=config.private)
   tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
   receipt  = web3.eth.wait_for_transaction_receipt(web3.toHex(tx_token))
  
   if(receipt['status'] == 1):
      print(f'TXN SUCCESS!!! {web3.toHex(tx_token)}')
   else:
      print('FAILED!!!  {web3.toHex(tx_token)}')  
  