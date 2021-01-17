import pymongo
import re
import numpy as np
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["hcmut"]
mycol = mydb["general"]
# data=mycol.find({
#   "$and": [
#     {
#     "$or":[
#   {"major_name": {"$all": [re.compile("máy tính")]}},
#   {"major_name": {"$all": [re.compile("kỹ thuật hóa")]}}
#     ]},
#   {"type_edu": {"$all": [re.compile("chất lượng cao")]}}
#   ]
# })
def gen_query(key,values):
  or_list = []
  final_list = []
  or_dict = {}
  if key != 'point':
    if len(values) > 1:
      for value in values:
        all_dict = {}
        all_dict[key] = {"$all":[re.compile(value)]}
        or_list.append(all_dict)
      or_dict["$or"] = or_list
      final_list.append(or_dict)
    else:
      all_dict = {}
      all_dict[key] = {"$all":[re.compile(values[0])]}
      final_list.append(all_dict)
  else:
    all_dict = {}
    all_dict["point"] = {"$gte":values[0],"$lte":values[1]}
    final_list.append(all_dict)
  return final_list[0]


def convert_constraint(constr):
  """
   input dict các thực thể theo từng slot {entity_slot:[entity_mess]}
   return câu query mongodb
   form của câu query: { "$and": [{entity_slot:{"$all":[re.compile("entity_mess")]}},{},{}] }
  """
  listkeys = list(constr.keys())
  and_list = []
  and_dict = {}
  for key in listkeys:
    values = constr[key]
    and_list.append(gen_query(key,values))
  and_dict["$and"] = and_list
  return and_dict

if __name__ == '__main__':
  constr = {'major_name': ['kỹ thuật hóa', 'điện tử'], 'year': ['2019','2020'], 'point': [0.0, 25]}
  data=mycol.find(convert_constraint(constr))
  for x in data:
    print(x['major_name'])
