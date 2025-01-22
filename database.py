import pymongo
from calculate import *
from key import *

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol=mydb['Pricelist']
'''items=["Mann Co. Supply Crate Key","Prohibition Opposition","The Head Prize","Strange Killstreak Australium Grenade Launcher","Strange Killstreak Your Eternal Reward"]

data = [calculate_sell_price(item) for item in items]

try:
    mycol.insert_many(data)
    print("Data inserted successfully")
except Exception as e:
    print(f"Error inserting data: {e}")'''

        
        

        
            
      
def update_database():
    
    for _ in mycol.find({},{"name":1,"_id":0}):
     name = _["name"]
     if name == "Mann Co. Supply Crate Key":
        new_p=calculate_buy_sell_price(name)
        new_priceb=new_p.get("buy", 0.0)
        new_prices=new_p.get("sell",0.0)
        mycol.update_one({"name": name}, {"$set": {"buy": new_priceb,"sell":new_prices,"time":int(time.time())}})
        
     else:

        new_p = calculate_sell_price(name)
        new_priceb=new_p.get("buy", 0.0)
        new_prices=new_p.get("sell",0.0)
        mycol.update_one({"name": name}, {"$set": {"buy": new_priceb,"sell":new_prices,"time":int(time.time())}})
        


