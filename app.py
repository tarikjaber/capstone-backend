from flask import Flask
from elasticsearch import Elasticsearch
import sys
import os
from dotenv import load_dotenv
# test

ES_CERT_PATH = "http_ca.crt"
INDEX_NAME = "imdb"

load_dotenv()
ES_PASSWORD = os.getenv("ES_PASSWORD")

es = Elasticsearch(['https://localhost:9200'],
                   basic_auth=('elastic', ES_PASSWORD),
                   ca_certs=ES_CERT_PATH,
                   verify_certs=False)

app = Flask(__name__)

def query_title(series_title):
    query_body = {
        "query": {
            "match": {
                "Series_Title": series_title
            }
        }
    }

    # Execute the search query
    response = es.search(index=INDEX_NAME, body=query_body)
    return response['hits']['hits']

@app.route('/')
def hello_world():
    output = ""

    response = query_title("Star Wars")

    # Print the results
    for hit in response:
        output +="<p>" +  hit['_source']["Series_Title"] + "</p>"
        print(hit['_source']["Series_Title"])
    return output 

@app.route('/<query>')
def search_title(query):
    output = ""
    response = query_title(query)

    # Print the results
    for hit in response:
        output +="<p>" +  hit['_source']["Series_Title"] + "</p>"
        print(hit['_source']["Series_Title"])
    return output 

if __name__ == '__main__':
    app.run(debug=True)

