import json
import requests
from datetime import date, datetime
from mysql.connector import (connection)

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, streaming_bulk


def set_mapping(es, **kwargs):
    """ Create index in elasticsearch with specific mapping """

    shaprPro_mapping = {"properties": {
        "fk_node_id": {"type": "keyword"},
        "lastactivity_at": {"type": "date"},
        "lat": {"type": "float"},
        "long": {"type": "float"},
        "city": {"type": "keyword"},
        "country": {"type": "keyword"},
        "job": {"type": "text"},
        "company": {"type": "text"},
        "tag": {"type": "keyword"},
        "goal": {"type": "keyword"}}}
    body = {}
    body["settings"] = {"number_of_shards": 5, "number_of_replicas": 0}
    body["mappings"] = {}
    body["mappings"][kwargs.get('doc_type_name')] = shaprPro_mapping

    # delete index if exists
    if es.indices.exists(kwargs.get('index_name')):
        es.indices.delete(index= kwargs.get('index_name'))
    # create index
    create_index = es.indices.create(index=kwargs.get('index_name'), ignore=400, body=body)
    # sanity check
    if (create_index["acknowledged"] != True):
        print("Index creation failed...")


def es_formating_row(row, **kwargs):
    """ format row to match with the specific mapping employed """

    d = {
        "_index": kwargs.get('index_name'),
        "_type": kwargs.get('doc_type_name'),
        "_source": {
            "fk_node_id": row[0],
            "lastactivity_at": str(row[1].date()) if (row[1] is not None) else None,
            "lat": row[2],
            "long": row[3],
            "city": row[4],
            "country": row[5],
            "job": row[6],
            "company": row[7],
            "tag": row[8].split(";") if (row[8] is not None) else None,
            "goal": row[9].split(";") if (row[9] is not None) else None
        }
    }
    return d
    

def set_data(cursor, **kwargs):
    """ insert data into elasticsearch """

    while True:
        row = cursor.fetchone()
        if row == None:
            break
        yield es_formating_row(row, **kwargs)


def load_batch(es, cursor, **kwargs):
    """ launch the bulk process """

    success, _ = bulk(es, set_data(cursor, **kwargs))
    return success

def load(es, step=20000, max_iter=100, **kwargs):
    
    # database connection
    mysql_connection = '../mysqlconn.json'
    # id of the chunck inserted
    i = 0

    # sql connection
    mysqlconn = json.load(open(mysql_connection))
    cnx = connection.MySQLConnection(**mysqlconn)
    cursor = cnx.cursor()

    while True:   
        i = i + 1
        # max step security
        if i > max_iter:
            print("Number of steps exceeded.")
            break

        print("Inserting chunk {} ...".format(str(i)))
        cursor.callproc('rw.view_elasticsearch', [1 + (i-1)*step, i*step])
        # get the number of documents to be inserted
        mysql_generator = list(cursor.stored_results())[0]
        nb_chunk_results = mysql_generator.rowcount

        # if no document to be inserted 
        if nb_chunk_results == 0:
            print("Done")
            break

        success = load_batch(es, mysql_generator, index_name=kwargs.get('index_name'), doc_type_name=kwargs.get('doc_type_name'))
        print("Done.".format(str(i)))

    cursor.close()
    cnx.close()
    # sanity check
    print("\nNumber of documents correctly inserted: {}".format(str(es.count(index=kwargs.get('index_name')))))


if __name__ == "__main__":
    # parameters
    index_name = "node"
    doc_type_name = "users"

    # database connection
    mysql_connection = '../mysqlconn.json'
    es_connection = '../esconn.json'

    # load data into elasticsearch
    es = Elasticsearch([{'host': "192.168.91.193", 'port': "9200"}], timeout=5000)

    set_mapping(es, index_name=index_name, doc_type_name=doc_type_name)
    load(es, index_name=index_name, doc_type_name=doc_type_name)
