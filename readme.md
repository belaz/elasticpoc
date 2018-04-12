To delete an index

curl  -XDELETE "192.168.91.114:9200/bank"

Data playground

Quickplay ->

Import the datasample.json file at the root of this project (bulk insert)

curl -H "Content-Type: application/json" -XPOST "192.168.91.114:9200/bank/_doc/_bulk?pretty&refresh" --data-binary "@datasample.json"

curl "192.168.91.114:9200/_cat/indices?v"

Realplay ->

generate some random json data here

https://www.json-generator.com/

Download and import the file (replace localhost by the elasticsearch ip)

curl -H "Content-Type: application/json" -XPOST "192.168.91.114:9200/bank/_doc/_bulk?pretty&refresh" --data-binary "@accounts.json"
curl "192.168.91.114:9200/_cat/indices?v"


Python bootstrap 

go to the python folder and execute this 2 times 

pip install --trusted-host pypi.python.org -r python-libs.txt
