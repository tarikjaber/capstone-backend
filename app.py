from flask import Flask
from elasticsearch import Elasticsearch

ES_CERT_PATH = "http_ca.crt"
INDEX_NAME = "imdb"

es = Elasticsearch(['https://localhost:9200'],
                   basic_auth=('elastic', 'n0jaL-CGa+YIznmEybmC'),
                   ca_certs=ES_CERT_PATH,
                   verify_certs=False)

app = Flask(__name__)

@app.route('/')
def hello_world():
    output = ""
    # Define your search query
    query_body = {
        "query": {
            "match": {
                "Series_Title": "Star Wars"
            }
        }
    }

    # Execute the search query
    response = es.search(index=INDEX_NAME, body=query_body)

    # Print the results
    for hit in response['hits']['hits']:
        output +="<p>" +  hit['_source']["Series_Title"] + "</p>"
        print(hit['_source']["Series_Title"])
    return output 

if __name__ == '__main__':
    app.run(debug=True)

