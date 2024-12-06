# Movie Platforms Data Science Project

A **Data Science** project that performs statistical analysis on movie platforms to determine differences across various films.

This project will focus on three difference sources that displays metadata about films. We are interested in cleaning the data to standardize their values and comparing differences across each individual platform.

## Step 0.5 - Installing Prerequisites

- **Python 3.0 or HIGHER**
- **Numpy** - Python module required as a dependency for pandas
- **Pandas** - Python module required for dataframe work

Addtionally, you may clone the repository onto your own directory. Make sure that both `rt_movies.csv` and `imdb_uncleaned.csv` are present, as they are the raw datasets that we're working with in this project.

## Step 1 - Splitting Dataset

We must first extract the `imdb_uncleaned.csv` file to two separate *csv's*. As the **imdb** website contains information about the ratings of both its own platform and metacritic's, we may separate these two through the `imdb_to_meta.py` file.

Run the file in the terminal with the argument of the csv file. If successful, it will generate two new csv files titled `imdb_movies.csv` and `metacritic_movies.csv` respectively.

To run the file, type `python3 imdb_to_meta.py imdb_uncleaned.csv` if you're using the Python interpreter. If you choose to use Anaconda, run `python imdb_to_meta.py imdb_uncleaned.csv` instead.

## Step 2 - Running Data Science Analysis

Now, there should be a total of 3 `.csv` files within the repository, and they should be named `imdb_movies.csv`, `metacritic_movies.csv` and `rt_movies.csv` respectively. We'll need these files to pass through the `data_cleaner.py` script in order for the other data analysis python files to work properly.
