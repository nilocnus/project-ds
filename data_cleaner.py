import numpy as np
import pandas as pd
import re
import sys

'''
This python script is meant to return cleaned dataframes for other files to use
It contains a getter function which returns cleaned dataframes for IMDB, Metacritic, and Rotten Tomatoes respectively
This script is not meant to aggregate the data of the 3 functions together, but it will need to cross reference them
'''

# Regular expression that separates the hour and minutes
extractor = re.compile(r'(?:(\d+)h)? (?:(\d+)m)?', re.IGNORECASE)

def runtime_converter(runtime):
    time = re.match(extractor, runtime)

    if time:
        result = 0
        if time.group(1):  # If hours are present, convert them to minutes
            result += int(time.group(1)) * 60
        if time.group(2):  # If minutes are present, add them
            result += int(time.group(2))
        return result
    return None # If there's no time

# Call this function to get all 4 dataframes
def get_dataframes(imdb, metacritic, rotten):
    
    imdb_df = pd.read_csv(imdb)
    metacritic_df = pd.read_csv(metacritic)
    rotten_df = pd.read_csv(rotten)

    imdb_drop = ['Description', 'Rank', 'Actors', 'Director']
    metacritic_drop = ['Description', 'Rank', 'Actors', 'Director', 'Revenue (Millions)']
    rotten_drop = ['movieId', 'movieURL', 'critic_sentiment', 'audience_sentiment', 'release_date_theaters', 'release_date_streaming', 'original_language', 'rating']

    # Remove unnecessary values from IMDB and Metacritic
    imdb_df.drop(columns=imdb_drop, inplace=True)
    metacritic_df.drop(columns=metacritic_drop, inplace=True)
    rotten_df.drop(columns=rotten_drop, inplace=True)

    # By zipping the Title and the Year, we then use set to find intersections between all 3 dataframes, and then place it in a list
    common_title_years = list(set(zip(imdb_df['Title'], imdb_df['Year'])).intersection(
        set(zip(metacritic_df['Title'], metacritic_df['Year']))
    ).intersection(
        set(zip(rotten_df['movieTitle'], rotten_df['movieYear']))
    ))

    # We can then apply a tuple on its first axis for the dataframes on their titles and years in order to filter through their common movies
    imdb_df = imdb_df[imdb_df[['Title', 'Year']].apply(tuple, axis=1).isin(common_title_years)]
    metacritic_df = metacritic_df[metacritic_df[['Title', 'Year']].apply(tuple, axis=1).isin(common_title_years)]
    rotten_df = rotten_df[rotten_df[['movieTitle', 'movieYear']].apply(tuple, axis=1).isin(common_title_years)]

    # Rotten Tomatoes has some duplicate entries which contains the same title and year but missing metadata. The last one is the real entry, so we'll keep those
    rotten_df.drop_duplicates(subset=['movieTitle', 'movieYear'], keep='last', inplace=True)

    # Rename the columns for consistency
    rotten_df = rotten_df.rename(columns={'movieTitle': 'Title', 'movieYear': 'Year'})
    imdb_df = imdb_df.rename(columns={'Runtime (Minutes)': 'runtime'})
    metacritic_df = metacritic_df.rename(columns={'Runtime (Minutes)': 'runtime', 'Metascore': 'Rating'})

    # Convert time to standardized minutes
    rotten_df['runtime'] = rotten_df['runtime'].apply(runtime_converter)

    # Reorder the columns to be consistent with one another
    imdb_df = imdb_df[['Title', 'Year', 'Genre', 'Rating', 'Votes', 'runtime', 'Revenue (Millions)']]
    metacritic_df = metacritic_df[['Title', 'Year', 'Genre', 'Rating', 'Votes', 'runtime']]
    rotten_df = rotten_df[['Title', 'Year', 'critic_score', 'audience_score', 'runtime']]

    # Standardize IMDB's ratings to be consistent with the other two
    imdb_df['Rating'] = imdb_df['Rating'] * 10

    # Sort all of the DF's by their Title's alphanumeric order
    imdb_df = imdb_df.sort_values(by='Title')
    metacritic_df = metacritic_df.sort_values(by='Title')
    rotten_df = rotten_df.sort_values(by='Title')

    # For debugging purposes
    # print(f'IMDB:\n{imdb_df}\nMeta:\n{metacritic_df}\nRotten:\n{rotten_df}\n')

    return imdb_df, metacritic_df, rotten_df

get_dataframes('imdb_movies.csv', 'metacritic_movies.csv', 'rt_movies.csv')