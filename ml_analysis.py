import numpy as np
import pandas as pd
import data_cleaner
import sys

from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
# from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
# from sklearn.preprocessing import StandardScaler

def success(x):
    return 'positive' if x>=60 else 'negative'

def determine_consensus(row):
    votes = [
        row['rating_imdb'],
        row['rating_metacritic'],
        row['rating_rotten_critic'],
        row['rating_rotten_audience']
    ]
    positive = votes.count('positive')
    negative = votes.count('negative')

    if positive > 2:
        return 'positive'
    if negative > 2:
        return 'negative'
    else:
        return 'mixed'

def compute_average_accuracy(X, y, n):
    scores = []
    for i in range(n):
        X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.3)
        
        model = make_pipeline(
            RandomForestClassifier()
        )

        model.fit(X_train, y_train)
        scores.append(model.score(X_valid, y_valid))
    
    return np.median(scores)

def main():
    imdb, metacritic, rotten = data_cleaner.get_dataframes('imdb_movies.csv', 'metacritic_movies.csv', 'rt_movies.csv')

    # Reset indices
    imdb.reset_index(drop=True, inplace=True)
    metacritic.reset_index(drop=True, inplace=True)
    rotten.reset_index(drop=True, inplace=True)

    # We'll split rotten into two dataframes, one for critic scores, and one for audience scores
    rotten_critic = rotten.drop(columns='audience_score')
    rotten_audience = rotten.drop(columns='critic_score')

    # We'll add a new column to each dataframe for their own movie success based off their own ratings
    imdb['rating_imdb'] = imdb['Rating'].apply(success)
    metacritic['rating_metacritic'] = metacritic['Rating'].apply(success)
    rotten_critic['rating_rotten_critic'] = rotten_critic['critic_score'].apply(success)
    rotten_audience['rating_rotten_audience'] = rotten_audience['audience_score'].apply(success)

    # We'll created a merged df
    merged = imdb.merge(metacritic, on=['Title', 'Year', 'Genre', 'Votes', 'runtime'])
    merged = merged.merge(rotten_critic, on=['Title', 'Year'])
    merged = merged.merge(rotten_audience, on=['Title', 'Year'])

    # Perform the determine_consensus function to return a more "objective" rating of success for every movie
    # And then give that consensus row to every dataframe
    merged['Consensus'] = merged.apply(determine_consensus, axis=1)
    imdb['Consensus'] = merged['Consensus']
    metacritic['Consensus'] = merged['Consensus']
    rotten_critic['Consensus'] = merged['Consensus']
    rotten_audience['Consensus'] = merged['Consensus']

    # In the merged df, we'll make a new column for a new rating and then select relevant data
    merged['Average'] = merged[['Rating_x', 'Rating_y', 'critic_score', 'audience_score']].mean(axis=1)

    # We'll only select the relevant data
    imdb = imdb[['Title', 'Year', 'Rating', 'rating_imdb', 'Consensus']]
    metacritic = metacritic[['Title', 'Year', 'Rating', 'rating_metacritic', 'Consensus']]
    rotten_critic = rotten_critic[['Title', 'Year', 'critic_score', 'rating_rotten_critic', 'Consensus']]
    rotten_audience = rotten_audience[['Title', 'Year', 'audience_score', 'rating_rotten_audience', 'Consensus']]
    merged = merged[['Title', 'Year', 'Average', 'Consensus']]

    # Remove NaN rows
    imdb.dropna(inplace=True)
    metacritic.dropna(inplace=True)
    rotten.dropna(inplace=True)
    merged.dropna(inplace=True)

    # For debugging purposes
    # print(f'IMDB:\n{imdb}\nMeta:\n{metacritic}\nRotten Critic:\n{rotten_critic}\nRotten Audience:\n{rotten_audience}\nMerged:\n{merged}\n')

    # We'll run these tests 100 times to ensure a consistent accuracy
    n = 50

    print(f'Please wait. Each model will be tested {n} times.\n')

    # First up we'll do IMDB
    X = imdb[['Year', 'Rating']].values
    y = imdb['Consensus'].values
    imdb_avg_score = compute_average_accuracy(X, y, n)
    print(f"IMDB Average Accuracy Score: {imdb_avg_score:.4f}")

    # Next up is Metacritic
    X = metacritic[['Year', 'Rating']].values
    y = metacritic['Consensus'].values
    metacritic_avg_score = compute_average_accuracy(X, y, n)
    print(f"Metacritic Average Accuracy Score: {metacritic_avg_score:.4f}")

    # Then Rotten (Critics)
    X = rotten_critic[['Year', 'critic_score']].values
    y = rotten_critic['Consensus'].values
    rotten_critic_avg_score = compute_average_accuracy(X, y, n)
    print(f"Rotten Critics Average Accuracy Score: {rotten_critic_avg_score:.4f}")

    # Then the Rotten (Audience)
    X = rotten_audience[['Year', 'audience_score']].values
    y = rotten_audience['Consensus'].values
    rotten_audience_avg_score = compute_average_accuracy(X, y, n)
    print(f"Rotten Audience Average Accuracy Score: {rotten_audience_avg_score:.4f}")

    # Finally, the merged or aggregated averages of all platforms
    X = merged[['Year', 'Average']].values
    y = merged['Consensus'].values
    merged_avg_score = compute_average_accuracy(X, y, n)
    print(f"Merged/Aggregated Average Accuracy Score: {merged_avg_score:.4f}")

if __name__ == '__main__':
    main()