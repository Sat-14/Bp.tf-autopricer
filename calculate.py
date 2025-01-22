import requests
import json
import os
import pprint
import statistics
from sku.parser import Sku
import time
from Snapshot import *
import pkg_resources
from datetime import datetime, timedelta

def calculate_sell_price(name1):
    sku=Sku()
    
    dataout = get_snapshot(name1)
    data = dataout.get('listings', [])
    

    buy_intent = []
    sell_intent = []
    for _ in data:
        if _.get('intent') == 'sell':
            sell_intent.append(_)

    for entry in data:
        filtered_entry = {
            'userAgent': entry.get('userAgent'),
            'currencies': entry.get('currencies') or entry.get('currencies', {}).get('metal').get('keys'),
            'steamid': entry.get('steamid'),
            'item': entry.get('item'),
            'intent': entry.get('intent')
        }

        if entry.get('intent') == 'buy' and entry.get('userAgent', {}).get('client') == "Gladiator.tf - Rent your own bot from 6 keys per month" or "TF2Autobot - Run your own bot for free":
            buy_intent.append(filtered_entry)
        elif entry.get('intent') == 'sell' and entry.get('userAgent', {}).get('client') == "Gladiator.tf - Rent your own bot from 6 keys per month" or "TF2Autobot - Run your own bot for free":
            sell_intent.append(filtered_entry)

    sell_prices = []
    for entry in sell_intent:
        filtered_sell = {
            'currencies': entry.get('currencies', {}),
            'intent': entry.get('intent')
        }
        sell_prices.append(filtered_sell)

    complex_numbers = [complex(offer['currencies'].get('keys',0), offer['currencies'].get('metal',0)) for offer in sell_prices]

    clen = len(complex_numbers)
    complex_keys = []
    for i, _ in enumerate(complex_numbers):
        if _.real is not None:   
         complex_keys.append(_.real)
    print(complex_keys)     
        
    if len(complex_keys) > 0:
     mode_keys_price = statistics.mode(complex_keys)
    else:
     mode_keys_price = 0.0        
            
    

    complex_metal = []
    for i, _ in enumerate(complex_numbers):
        if _.real == mode_keys_price:
           if _.imag is not None: 
            complex_metal.append(_.imag)
    if len(complex_metal) > 0:
     median_metal_price = statistics.median(complex_metal)
    else:
     median_metal_price = 0.0              
    

    threshold = median_metal_price * 0.5
    

    In_threshold_prices_metal = [price for price in complex_metal if median_metal_price - threshold <= price <= median_metal_price + threshold]
    current_time=int(time.time())
    skunum=Sku.name_to_sku(name1)
    
    
    
    
    
    if In_threshold_prices_metal:
        sellpricefinal = {
        "sku":skunum,
        "name" : name1,
        "currency":None,
        "source":"bptf",
        "time":current_time,   
        "buy":{'keys':0.0,'metal':0.05},
        "sell":{'keys':mode_keys_price,'metal':min(In_threshold_prices_metal)}

        
        }
    else:
          sellpricefinal={
          "sku" : skunum,
          "name": name1,
          "currency": None,
          "source": "bptf",
          "time": current_time,
          "buy": {'keys': 0.0, 'metal': 0.05},
          "sell": {'keys': mode_keys_price, 'metal': 0.0}

            }
    return sellpricefinal

