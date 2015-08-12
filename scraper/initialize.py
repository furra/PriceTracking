from pymongo import MongoClient

print 'Connecting to mongo db...'
client = MongoClient('0.0.0.0', 27017)
print 'Done.\nChecking if there are stores...'
db = client.price_tracking
stores = db.stores

if not stores.find_one({"code": "falabella"}):
  print "falabella store doesn't exist"
  stores.insert({"code": "falabella", "name": "Falabella"})
  print "Created falabella store"
  print stores.find_one({"code": "falabella"})
else:
  print "falabella store exists"

print "Finished."





