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
def home():
    return render_template('index.html', response=[])

@app.route('/search')
def search_title():
    field = request.args.get('field')
    query = request.args.get('query')
    if field and query:
        output = ""
        response = []
        if field == "all":
            response = query_all_fields(query)
        else:
            response = query_field(field, query)

        # Print the results
        return render_template('index.html', response=response, selected_field=field)
    else:
        return render_template('index.html', response=[])

def query_by_id(movie_id):
    try:
        response = es.get(index=INDEX_NAME, id=movie_id)
        return response['_source']
    except Exception as e:
        print(f"Error querying by ID: {e}")
        return None

@app.route('/movie/<movie_id>')
def movie_details_by_id(movie_id):
    movie = query_by_id(movie_id)
    if movie:
        return render_template('movie_details.html', movie=movie, movie_id=movie_id)
    return "Movie not found", 404

def query_similar_movies(movie_id):
    query_body = {
        "query": {
            "more_like_this": {
                "fields": ["Series_Title", "Genre", "Overview", "Director"],  # Fields to base the MLT query on
                "like": [
                    {
                        "_index": INDEX_NAME,
                        "_id": movie_id
                    }
                ],
                "min_term_freq": 1,
                "max_query_terms": 5
            }
        }
    }

    # Execute the search query
    response = es.search(index=INDEX_NAME, body=query_body)
    return response['hits']['hits']

@app.route('/similar/<movie_id>')
def get_similar_movies(movie_id):
    response = query_similar_movies(movie_id)

    output = ""
    for hit in response:
        movie = hit['_source']
        output += "<div class='result'>"
        output += "<img src='" + movie['Poster_Link'] + "'>"
        output += "<br>"
        output += "<a target='_blank' href='/movie/" + hit['_id'] + "'>" + hit['_source']['Series_Title'] + "</a>"
        output += "<p>Rating: " + movie['IMDB_Rating'] +  "</p>"
        output += "</div>"
    return output

if __name__ == '__main__':
    app.run(debug=True)

