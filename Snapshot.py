import os
import requests
import json
import time
from pprint import pprint
BPTF_TOKEN = ""



def get_snapshot(item_name: str) -> dict:
    url = "https://backpack.tf/api/classifieds/listings/snapshot"

    params = {
        "token": BPTF_TOKEN,
        "appid": "440", 
        "sku": item_name

    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        snapshot = response.json()
        data = json.loads(response.text)
        return data
    except requests.RequestException as e:
        raise Exception(f"Failed to get snapshot: {e}")


















    

    


    









