import pymongo
client = pymongo.MongoClient("mongodb://taindp:chatbot2020@thesis-shard-00-00.bdisf.mongodb.net:27017,thesis-shard-00-01.bdisf.mongodb.net:27017,thesis-shard-00-02.bdisf.mongodb.net:27017/hcmut?ssl=true&replicaSet=atlas-12fynb-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.hcmut
# collection = db['general'].find({})
# collection = db['general']
database = db['general']
# database = []
# for item in collection:
#     database.append(item)
dict_entity={}
# dict_entity['_id'] = database.distinct('_id')
dict_entity['major_code']=database.distinct('major_code')
dict_entity['major_name']=database.distinct('major_name')
dict_entity['subject_group']=database.distinct('subject_group')
dict_entity['point'] = database.distinct('point')
dict_entity['type_edu']= database.distinct('type_edu')
dict_entity['year'] = database.distinct('year')
dict_entity['satisfy'] = database.distinct('satisfy')

dict_entity['subject'] = database.distinct('subject')
dict_entity['career'] = database.distinct('career')
dict_entity['tuition'] = database.distinct('tuition')

file_output=open('../data/db_entity_jan23.json','w')
list_final=[]
list_final.append(dict_entity)
dict_str=str(list_final)
dict_str=dict_str.replace(r"'",r'"')
# print(dict_str)
file_output.write(dict_str)


