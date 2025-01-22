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
def calculate_buy_sell_price(name):
    sku = Sku()
    dataout = get_snapshot(name)
    data = dataout.get('listings', [])

    buy_intent = []
    sell_intent = []
    for _ in data:
        if _.get('intent') == 'buy':
            buy_intent.append(_)
        elif _.get('intent') == 'sell':
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

    buy_prices = []
    for entry in buy_intent:
        filtered_buy = {
            'currencies': entry.get('currencies', {}),
            'intent': entry.get('intent')
        }
        buy_prices.append(filtered_buy)

    sell_prices = []
    for entry in sell_intent:
        filtered_sell = {
            'currencies': entry.get('currencies', {}),
            'intent': entry.get('intent')
        }
        sell_prices.append(filtered_sell)

    complex_buy_numbers = [complex(offer['currencies'].get('keys', 0), offer['currencies'].get('metal', 0)) for offer in buy_prices]
    complex_sell_numbers = [complex(offer['currencies'].get('keys', 0), offer['currencies'].get('metal', 0)) for offer in sell_prices]

    

    complex_metal_sell = []
    for i, _ in enumerate(complex_sell_numbers):
        
            complex_metal_sell.append(_.imag)
    mean_metal_price_sell = statistics.median(complex_metal_sell)

    threshold_sell = mean_metal_price_sell*0.1 
    print(threshold_sell)

    

    complex_metal_buy = []
    for i, _ in enumerate(complex_buy_numbers):
        
            complex_metal_buy.append(_.imag)
    mean_metal_price_buy = statistics.mean(complex_metal_buy)
    
   


    threshold_buy = mean_metal_price_buy * 3
    In_threshold_prices_metal_buy = [price for price in complex_metal_buy if mean_metal_price_buy - threshold_buy <= price <= mean_metal_price_buy + threshold_buy]
    In_threshold_prices_metal_sell = [price for price in complex_metal_sell if mean_metal_price_sell - threshold_sell <= price <= mean_metal_price_sell + threshold_sell]
    print(In_threshold_prices_metal_buy)
    print(In_threshold_prices_metal_sell)
    if max(In_threshold_prices_metal_buy) < min(In_threshold_prices_metal_sell):
        threshold_price = max(In_threshold_prices_metal_buy)
    else:
        threshold_price = max([x for x in In_threshold_prices_metal_buy if x < min(In_threshold_prices_metal_sell)])

    key_price = {
           'sku':"5021;6",
            'name':"Mann Co. Supply Crate Key",
            'currency':None,
            'source':"bptf",
            'time':int(time.time()),
            'buy': {
            'keys': 0.0,
            'metal':threshold_price
        },
        'sell': {
            'keys': 0.0,
            'metal': min(In_threshold_prices_metal_sell)
        }
    }
    return key_price