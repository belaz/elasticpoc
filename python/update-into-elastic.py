import json
import requests

esconn = json.load(open('../esconn.json'))


r = requests.post("%s%s" % (esconn['uri'],'/node/profile/278/_update?pretty'),
json={
        "doc": {
            "uri": "pitoune"
        }
    })
print(r.status_code, r.reason)
parsed = json.loads(r.content)
print (json.dumps(parsed, indent=4, sort_keys=True))







