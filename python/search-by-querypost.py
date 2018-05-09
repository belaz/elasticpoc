import json
import requests
from datetime import date, datetime
from mysql.connector import (connection)

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from pprint import pprint
import os.path
import pandas as pd
import time


''' Module to make queries easier via python elasticsearch api. 
    All requestable fields are for now:
        "city", "country", "job", "goal","tag"
'''

def get_query_dict(conf, **kwargs):
    ''' construct full text query '''

    # get terms that shouldn't be used by fuzziness
    fuzziness_terms_to_exclude = conf['fuzziness_terms_to_exclude']

    query = {}
    # full text on job
    # if specific job is requested
    if "job" in kwargs.keys():
        # if several jobs are requested
        if isinstance(kwargs.get("job"), list):
            # prepare a should condition over all the jobs
            jobs = kwargs.get("job")
            query["bool"] = { "minimum_should_match": 1, "should": []}
            for ind_job in jobs:
                # individual job requested
                if ind_job in fuzziness_terms_to_exclude:
                    match_query = {"query": ind_job, "minimum_should_match": "2<75%"}
                else:
                    match_query = {"query": ind_job, "prefix_length": 3, "fuzziness": "AUTO", "minimum_should_match": "2<75%"}

                query["bool"]["should"].append({"match":{"job":match_query}})
        else:
            # individual job requested
            if kwargs.get("job") in fuzziness_terms_to_exclude:
                match_query = {"query": kwargs.get("job"), "minimum_should_match": "2<75%"}
            else:
                match_query = {"query": kwargs.get("job"), "prefix_length": 3, "fuzziness": "AUTO", "minimum_should_match": "2<75%"}

            query["match"] = {"job":match_query}

    else:
        # else match all
        query["match_all"] = {}
    return {"query": query}


def get_filter_dict(**kwargs):
    ''' construct filter query '''

    filt = {"filter": {"bool": {}}}
    logic_clauses = []
    # full text search field should be removed from kwargs
    for key, value in kwargs.items():
        # if the value is a list in a filter context, then we need to create a should
        if isinstance(value, list):
            should_dict = {"bool": {"minimum_should_match": 1, "should": []}}
            for elt in value:
                should_dict["bool"]["should"].append({"term" : {key: elt}})
            logic_clauses.append(should_dict)
        else:
            logic_clauses.append({"term": {key: value}})

    if len(logic_clauses) == 0:
        pass
    elif len(logic_clauses) > 1:
        filt["filter"]["bool"] = {"must": logic_clauses}
    else:
        # exactly one logic clause
        filt["filter"]["bool"] = {"must": logic_clauses[0]}
    return filt


def construct_body_query(conf, highlight, **kwargs):
    ''' construct complete es query '''

    if len(kwargs) == 0:
        print("no inputs")
        return False

    # final_dict = {"_source": ["fk_node_id"], "query": {"bool": {"must": {}}}}
    final_dict = {"query": {"bool": {"must": {}}}}

    params_dict = kwargs
    query_dict = get_query_dict(conf, **params_dict)
    if "job" in params_dict.keys(): 
        params_dict.pop("job")
        # add highlight information
        if highlight:
            final_dict["highlight"] = {"fields": {"job" : {}}}

    filter_dict = get_filter_dict(**params_dict)
    final_dict["query"]["bool"]["must"] = query_dict["query"]
    if len(filter_dict["filter"]["bool"]) > 0:
        final_dict["query"]["bool"]["filter"] = filter_dict["filter"]

    return final_dict


def elastic_search(es, index_name, doc_type_name, conf, highlight=False, debug=0, **kwargs):
    ''' specific function to query elasticsearch with custom parameters '''

    # construct json body query and request results
    body = construct_body_query(conf, highlight, **kwargs)
    res = es.search(index = index_name, doc_type = doc_type_name, size=10, body=body)

    if debug > 0:
        print("Query:")
        pprint(body)
        print("\nNumber of results: {}".format(str(res['hits']['total'])))
        pprint(res)
    return res['hits']['total']


def automatic_search(es, index_name, doc_type_name, file_scopes='', debug=0):
    ''' automatic research from a tsv file. please be sure to use the appropiate template '''

    # if file exists
    if not os.path.isfile(file_scopes):
        print("Error file: {} doesn't not exist.")
        return False

    start_time = time.time()
    df = pd.read_csv(file_scopes, sep='\t')

    errors = []
    nb_results = []
    print("Start processing file...\n")
    for id_row, row_dict in df.fillna('').T.to_dict().items():
        # print every 10% of treatments
        if id_row % (df.shape[0]/10) == 0:
            print("Processed {}%".format(str(id_row/df.shape[0]*100)))

        try:
            row_dict_drop_na = {}
            for k, v in row_dict.items():
                # if the field is empty
                if v != '':
                    # is it a list (not the best test)
                    if '[' in v:
                        row_dict_drop_na[k] = json.loads(v)
                    else:
                        row_dict_drop_na[k] = v

            nb_query_results = elastic_search(es, index_name=index_name, doc_type_name=doc_type_name, **row_dict_drop_na)
            nb_results.append(nb_query_results)
            errors.append(0)
        except:
            nb_results.append(-1)
            errors.append(1)
    # integrate results to tsv
    df["nb_results"] = nb_results
    df["errors"] = errors

    print("Processed {}%".format(str(100)))
    print("Done")
    print("--- %s seconds ---\n" % (time.time() - start_time))
    file_scopes_tokens = file_scopes.rsplit(".", 1)
    df.to_csv(file_scopes_tokens[0] + "_completed." + file_scopes_tokens[1], sep='\t')
    return True



# parameters
index_name = "node"
doc_type_name = "users"

# create elasticsearch object
es = Elasticsearch([{'host': "192.168.91.193", 'port': "9200"}])
# load configuration
with open('conf.json') as data_file:
    conf = json.load(data_file)

# construct json body query and request results on a SEPECIFIC SCOPE
res = elastic_search(es, debug=1, index_name=index_name, doc_type_name=doc_type_name, conf=conf, job="student", city="Paris")

