import csv
import sys
import os
from elasticsearch import Elasticsearch, helpers
from dotenv import load_dotenv
import pandas as pd

ES_CERT_PATH = "http_ca.crt"
INDEX_NAME = "imdb"

load_dotenv()
ES_PASSWORD = os.getenv("ES_PASSWORD")

# Initialize Elasticsearch instance
es = Elasticsearch(['https://localhost:9200'], 
                 basic_auth=('elastic', ES_PASSWORD),
                 ca_certs=ES_CERT_PATH,
                 verify_certs=False)

# Read CSV records
csv_file_path = "updated_movie_data.csv"

upload_list = [] # list of items for upload

# Load all csv data
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    data_list = []

    csv_data = csv.reader(csvfile)
    for row in csv_data:
        data_list.append(row)

    # separate out the headers from the main data 
    headers = data_list[0]
    # drop headers from data_list
    data_list.pop(0)

    for item in data_list: # iterate over each row/item in the csv

        item_dict = {}

        # match a column header to the row data for an item
        i = 0
        for header in headers:
            item_dict[header] = item[i]
            i = i+1

        # add the transformed item/row to a list of dicts
        upload_list += [item_dict]

# using helper library's Bulk API to index list of Elasticsearch docs
try:
    resp = helpers.bulk(
        es,
        upload_list,
        index=INDEX_NAME
    )
    msg = "helpers.bulk() RESPONSE: " + str(resp)
    print(msg) # print the response returned by Elasticsearch
except Exception as err:
    msg = "Elasticsearch helpers.bulk() ERROR: " + str(err)
    print(msg)
    sys.exit(1)

print("CSV uploaded to Elasticsearch!")

