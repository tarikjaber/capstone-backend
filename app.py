from flask import Flask, request
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
    return '''
        <html>
            <head>
                <script src="https://unpkg.com/htmx.org@1.9.6"></script>
            </head>
            <body>
                <form hx-get="/search" hx-target="#results" onsubmit="return false;">
                    <input type="text" name="query" placeholder="Enter movie title..."/>
                    <button type="submit">Search</button>
                </form>
                <div id="results"></div>
            </body>
        </html>
    '''

@app.route('/search')
def search_title():
    print("YOBA")
    print(request.url)
    query = request.args.get('query', '')
    output = ""
    response = query_title(query)

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

