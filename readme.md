# STARTER PACK

**Tools:**

http://cmder.net/  (console)

https://chocolatey.org/  (packages)

https://code.visualstudio.com/ (IDE)

https://www.python.org/ftp/python/3.6.5/python-3.6.5-amd64-webinstall.exe (PYTHON)

https://nodejs.org/en/ (nodejs)

https://www.json-generator.com/ (generate json sample datas)

**Config:**

Install curl with chocolatey (in administrator console)

`chocolatey install curl`

Install python libs (go to the project python folder and execute this 2 times)

`pip install --trusted-host pypi.python.org -r python-libs.txt`

install node modules (go to the project node folder and execute this)

`node install`

**Where to start:**

PS : if you have docker, you can go on a free ride on elasticsearch/mysql with the command
`docker-compose up -d`

Test the project with this commands :

`
cd node;
node insert-into-elastic.js`

`cd python;
py insert-into-elastic.py`

# USEFUL COMMANDS

**Delete an index**

`curl  -XDELETE "192.168.91.114:9200/bank"`

**List all indexes**

`curl "192.168.91.114:9200/_cat/indices?v"`

**Bulk insert**

`curl -H "Content-Type: application/json" -XPOST "192.168.91.114:9200/bank/_doc/_bulk?pretty&refresh" --data-binary "@datasample.json"`
