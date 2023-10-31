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
    return render_template('index.html', response=[], query_string = "", show_results = "hidden")

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
        return render_template('index.html', response=response, selected_field=field, query_string = query, show_results = "visible")
    else:
        return render_template('index.html', response=[], query_string = query, show_results = "visible")

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
    output += "<div class='responses'>"
    for hit in response:
        movie = hit['_source']
        
        output += "<a target='_blank' href='/movie/" + hit['_id'] + "'>"    
        output += "<div class='card'>"
        output += "<img class='card-img-top' src='" + movie['Poster_Link'] + "'>"
        output += "<hr/>"
        output += "<div class='card-body'>"
        output += "<h5 class='card-title' >"
        output += movie['Series_Title'] 
        output += "</h5>"
        output += "<p style='font-weight: 600; margin-bottom:0; margin-top:1.5rem;'>"
        output += "<i class='fa fa-star'></i>"
        output += movie['IMDB_Rating'] +  "</p>"
        output += "</div>"
        output += "</div>"
        output += "</a>"
    output += "</div>"
    return output

if __name__ == '__main__':
    app.run(debug=True)

