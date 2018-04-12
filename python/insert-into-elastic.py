from mysql.connector import (connection)
import json
import requests

mysqlconn = json.load(open('../mysqlconn.json'))
esconn = json.load(open('../esconn.json'))

cnx = connection.MySQLConnection(**mysqlconn)
cursor = cnx.cursor()

query = ("SELECT fk_node_id,username from node_human limit 1")


cursor.execute(query)

result = dict(zip(cursor.column_names, cursor.fetchone()))
jsonResult = json.dumps( result, indent=4, sort_keys=True)
print (jsonResult)

cursor.close()
cnx.close()

print (result["fk_node_id"])
r = requests.put("%s%s%s" % (esconn['uri'],'/node/profile/',result["fk_node_id"]), data=jsonResult)
print(r.status_code, r.reason)
parsed = json.loads(r.content)
print (json.dumps(parsed, indent=4, sort_keys=True))

