import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("TMDB_API_KEY")
base_url = "https://api.themoviedb.org/3"
# Load the CSV file
df = pd.read_csv('imdb_top_1000.csv')
print(api_key)

def get_movie_poster(movie_name):
    # Search for the movie by name
    search_url = f"{base_url}/search/movie?api_key={api_key}&query={movie_name}"
    search_response = requests.get(search_url)
    search_results = search_response.json()
    print(search_results)

    # Check if there are any results
    if search_results['results']:
        first_result = search_results['results'][0]
        movie_id = first_result['id']
        poster_path = first_result['poster_path']

        # Construct the full URL for the poster image
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        return poster_url
    else:
        return "No poster found."

# Update Poster_Link in the dataframe
for index, row in df.iterrows():
    movie_name = row['Series_Title']
    poster_url = get_movie_poster(movie_name)
    df.at[index, 'Poster_Link'] = poster_url

# Save the updated dataframe to a new CSV file
df.to_csv('updated_movie_data.csv', index=False)
