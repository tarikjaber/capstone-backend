from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
import sys
import os
from dotenv import load_dotenv

ES_CERT_PATH = "http_ca.crt"
INDEX_NAME = "imdb"

load_dotenv()

ES_PASSWORD = os.getenv("ES_PASSWORD")

es = Elasticsearch(['https://localhost:9200'],
                   basic_auth=('elastic', ES_PASSWORD),
                   ca_certs=ES_CERT_PATH,
                   verify_certs=False)

app = Flask(__name__)

def query_field(field_name, field_value):
    query_body = {
        "query": {
            "match": {
                field_name: field_value
            }
        }
    }

    # Execute the search query
    response = es.search(index=INDEX_NAME, body=query_body)
    return response['hits']['hits']

def query_all_fields(field_value):
    query_body = {
        "query": {
            "query_string": {
                "query": field_value
            }
        }
    }

    # Execute the search query
    response = es.search(index=INDEX_NAME, body=query_body)
    return response['hits']['hits']

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/search')
def search_title():
    print(request.args)
    field = request.args.get('field')
    query = request.args.get('query')
    print("Field: " + field)
    print("Query: " + query)
    output = ""
    response = []
    if field == "all":
        response = query_all_fields(query)
    else:
        response = query_field(field, query)

    # Print the results
    for hit in response:
        output +="<p>" +  hit['_source']["Series_Title"] + "</p>"
        print(hit['_source']["Series_Title"])
    return output 

@app.route('/<query>')
def query_route(query):
    output = ""
    response = query_title(query)

    # Print the results
    for hit in response:
        output +="<p>" +  hit['_source']["Series_Title"] + "</p>"
        print(hit['_source']["Series_Title"])
    return output 

if __name__ == '__main__':
    app.run(debug=True)

