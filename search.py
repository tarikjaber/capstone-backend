from elasticsearch import Elasticsearch
import sys
from dotenv import load_dotenv

ES_CERT_PATH = "http_ca.crt"
INDEX_NAME = "imdb"

load_dotenv()
ES_PASSWORD = os.getenv("ES_PASSWORD")

es = Elasticsearch(['https://localhost:9200'],
                   basic_auth=('elastic', 'SYud=s09Q-pFaN_8qKm3'),
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


