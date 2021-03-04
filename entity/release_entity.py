import pymongo
client = pymongo.MongoClient("mongodb://taindp:chatbot2020@thesis-shard-00-00.bdisf.mongodb.net:27017,thesis-shard-00-01.bdisf.mongodb.net:27017,thesis-shard-00-02.bdisf.mongodb.net:27017/hcmut?ssl=true&replicaSet=atlas-12fynb-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.hcmut
# collection = db['general'].find({})
# collection = db['general']
database = db['general']
dict_entity={}
list_keys = []
for item in database.find({}):
    list_keys = list(dict(item).keys())
for key in list_keys:
    if key != '_id':
        dict_entity[key] = database.distinct(key)
# print(dict_entity)
file_output=open('../data/db_entity_feb20.json','w')
list_final=[]
list_final.append(dict_entity)
dict_str=str(list_final)
dict_str=dict_str.replace(r"'",r'"')
# print(dict_str)
file_output.write(dict_str)


