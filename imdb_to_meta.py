import numpy as np
import pandas as pd
import sys

'''
This python script is meant to split the imdb_uncleaned data into an imdb and metacritic csv file.
This needs to be done as the imdb dataset includes the ratings for both websites
'''

def main(in_directory):
    df = pd.read_csv(in_directory)
    # print(df)

    imdb = df.drop(columns='Metascore')
    metacritic = df.drop(columns='Rating')

    # print(imdb)
    # print(metacritic)
    imdb.to_csv('imdb_movies.csv', index=False)
    metacritic.to_csv('metacritic_movies.csv', index=False)

if __name__ == '__main__':
    # Input the file name of the uncleaned imdb data (should be 'imdb_uncleaned.csv')
    in_directory = sys.argv[1]
    main(in_directory)