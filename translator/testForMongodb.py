import pymongo

client = pymongo.MongoClient(
    "mongodb://DONGMING:12345QWERT@cluster0-shard-00-00-xooxj.azure.mongodb.net:27017,cluster0-shard-00-01-xooxj.azure.mongodb.net:27017,cluster0-shard-00-02-xooxj.azure.mongodb.net:27017/test?replicaSet=Cluster0-shard-0&ssl=true&authSource=admin")
db = client.TranslatedInfo

collection = db.TranslatedText
profile = db.UserInfo

UserName = input('enter username: ')
Password = input('enter password: ')

if profile.find_one({'_id': UserName}) is None:
    print('user name does not exist. ')
elif profile.find_one({'_id': UserName, 'password': Password}):
    print('login in successfully. ')
else:
    print('password is wrong. ')
