import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["hcmut"]
doc = mydb["general"]
dict_entity={}

dict_entity['major_code']=doc.distinct('major_code')
dict_entity['major_name']=doc.distinct('major_name')
dict_entity['subject_group']=doc.distinct('subject_group')
dict_entity['point'] =doc.distinct('point')
dict_entity['type_edu']=doc.distinct('type_edu')
dict_entity['year'] = doc.distinct('year')
dict_entity['satify'] = doc.distinct('satify')
# dict_entity['university_name']=doc.distinct('university_name')
# dict_entity['university_code']=doc.distinct('university_code')
dict_entity['subject'] = doc.distinct('subject')
dict_entity['career'] = doc.distinct('career')
# dict_entity['typical_group'] = doc.distinct('typical_group')
# dict_entity['company'] = doc.distinct('company')
dict_entity['tuition_one_credit'] = doc.distinct('tuition_one_credit')
# dict_entity['tuition_avg_one_sem'] = doc.distinct('tuition_avg_one_sem')
# dict_entity['duration_std'] = doc.distinct('duration_std')
# dict_entity['credits'] = doc.distinct('credits')
# dict_entity['foreign_lang_min'] = doc.distinct('foreign_lang_min')
file_output=open('/home/taindp/PycharmProjects/thesis/data/db_entity_31dec.json','w')
list_final=[]
list_final.append(dict_entity)
dict_str=str(list_final)
dict_str=dict_str.replace(r"'",r'"')
# print(dict_str)
file_output.write(dict_str)


