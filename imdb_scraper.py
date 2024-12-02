import requests
from bs4 import BeautifulSoup
import json
import time
import pandas as pd

# Credits to Dawan17 on Reddit for helping with up-to-date scraper logic

url = 'https://www.imdb.com/search/title/?title_type=feature&count=250' # Adjust as needed
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}
result = requests.get(url, headers=headers)

soup = BeautifulSoup(result.content, 'html.parser')
movieData = soup.find('script', id='__NEXT_DATA__')

# print(movieData) Debugging purposes

movieName = []
movieYear = []
rating = []
metacritic_scores = []
runtimes = []
number_of_ratings = []

# Function to parse a single page
def parse_page(url):
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.content, 'html.parser')

    # print(soup) Debugging purposes
    
    # Extract JSON data from the script tag
    movie_data = soup.find('script', id='__NEXT_DATA__')
    if not movie_data:
        print("No movie data found!")
        return False  # Stop pagination
    
    json_data = json.loads(movie_data.string)
    title_results = json_data.get('props', {}).get('pageProps', {}).get('searchResults', {}).get('titleResults', {}).get('titleListItems', [])
    
    if not title_results:
        print("No more titles found!")
        return False  # Stop pagination

    print(title_results)
    # Extract data
    for item in title_results:
        movieName.append(item.get('titleText', 'Unknown'))
        movieYear.append(item.get('releaseYear', 'Unknown'))
        rating.append(item.get('ratingSummary', {}).get('aggregateRating', 'Unknown'))
        metacritic_scores.append(item.get('metascore', 'Unknown'))
        runtime = item.get('runtime', 'Unknown')
        if isinstance(runtime, int):  # If runtime is an integer (seconds)
            runtime_minutes = runtime // 60
        else:
            runtime_minutes = runtime  # Keep 'N/A' if it's not available
        runtimes.append(runtime_minutes)
        number_of_ratings.append(item.get('ratingSummary', {}).get('voteCount', 'Unknown'))
    
    return True  # Continue pagination

'''
WARNING: Pagination is currently broken on IMDB. You're currently only able to scrape at most 250 entries on any given page

# Pagination logic
start = 1
max_pages = 1  # Adjust as needed

for _ in range(max_pages):
    print(f"Processing page starting at {start}...")
    url = f"{url}&start={start}"
    if not parse_page(url):
        break
    start += 250  # Adjust based on IMDb's pagination (e.g., 50 results per page)
    time.sleep(0.1)  # To avoid overwhelming the server
'''

parse_page(url)

for name, year, rate, score, run, num in zip(movieName, movieYear, rating, metacritic_scores, runtimes, number_of_ratings):
    print(f"Title: {name}, Year: {year}, Rating: {rate}, Metascore: {score}, Runtime: {run}, Number of Ratings: {num}")

df = pd.DataFrame({
    'Title': movieName,
    'Year': movieYear,
    'Rating': rating,
    'MetaScore': metacritic_scores,
    'Runtime': runtimes,
    'Votes': number_of_ratings
})

# print(df) Debugging purposes

df.to_csv('imdb.csv', index=False)

print(f'{len(movieName)} titles have been saved successsfully!')