import pymongo
import pandas as pd
import json
client=pymongo.MongoClient('localhost',27017)

db=client['benchmark']

col=db['common']
data=col.distinct('university_meta')
data=pd.DataFrame(data)
data.columns=['url','university_code','university_name']
wr=data[['university_code','university_name']]
res=wr.values.tolist()
res=str(res)
with open('name_univ.txt','w') as f:
  f.write(res)
print(type(res))
