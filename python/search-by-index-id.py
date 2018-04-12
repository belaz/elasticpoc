import json
import requests

esconn = json.load(open('../esconn.json'))


r = requests.get("%s%s%s" % (esconn['uri'],'/node/profile/',278))
print(r.status_code, r.reason)
parsed = json.loads(r.content)
print (json.dumps(parsed, indent=4, sort_keys=True))

