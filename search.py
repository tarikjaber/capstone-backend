from elasticsearch import Elasticsearch

ES_CERT_PATH = "http_ca.crt"
INDEX_NAME = "imdb"

es = Elasticsearch(['https://localhost:9200'],
                   basic_auth=('elastic', 'n0jaL-CGa+YIznmEybmC'),
                   ca_certs=ES_CERT_PATH,
                   verify_certs=False)

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
    print(hit['_source']["Series_Title"])


