import json
from pprint import pprint
json_data=open('c:/1.json',encoding="utf8")

data = json.load(json_data)
#data.encode('ascii', 'ignore')
print(data)
json_data.close()