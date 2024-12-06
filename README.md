# Movie Platforms Data Science Project

A **Data Science** project that performs statistical analysis on movie platforms to determine differences across various films.

This project will focus on three difference sources that displays metadata about films. We are interested in cleaning the data to standardize their values and comparing differences across each individual platform.

## Step 0.5 - Installing Prerequisites

Before running the script, ensure that you have the following prerequisites installed:

- **Python 3.0 or HIGHER**: Make sure you are using Python version 3.0 or higher.
- **Numpy**: Python module required as a dependency for pandas. It handles numerical computations and array operations.
- **Pandas**: Python module required for working with dataframes and data manipulation.
- **sklearn**: Python module required for machine learning analysis, providing various algorithms for analysis.
- **Matplotlib**: For data visualization and plotting graphs.
- **Seaborn**: A data visualization library based on Matplotlib for enhanced visuals.
- **Scipy**: For statistical tests and computations.
- **Statsmodels**: For statistical modeling, including tests like Tukey's HSD.

You can install these dependencies using `pip`:

```bash
pip install numpy pandas scikit-learn matplotlib seaborn scipy statsmodels


Addtionally, you may clone the repository onto your own directory. Make sure that both `rt_movies.csv` and `imdb_uncleaned.csv` are present, as they are the raw datasets that we're working with in this project.

## Step 1 - Splitting Dataset

We must first extract the `imdb_uncleaned.csv` file to two separate *csv's*. As the **imdb** website contains information about the ratings of both its own platform and metacritic's, we may separate these two through the `imdb_to_meta.py` file.

Run the file in the terminal with the argument of the csv file. If successful, it will generate two new csv files titled `imdb_movies.csv` and `metacritic_movies.csv` respectively.

To run the file, type `python3 imdb_to_meta.py imdb_uncleaned.csv` if you're using the Python interpreter. If you choose to use Anaconda, run `python imdb_to_meta.py imdb_uncleaned.csv` instead.

## Step 2 - Running Data Science Analysis

Now, there should be a total of 3 `.csv` files within the repository, and they should be named `imdb_movies.csv`, `metacritic_movies.csv` and `rt_movies.csv` respectively. We'll need these files to pass through the `data_cleaner.py` script in order for the other data analysis python files to work properly.

### Statistical Analysis

> [!IMPORTANT]
> Make sure all of the previous steps are completed properly! The following python script will rely on the `data_cleaner.py` script to process and return cleaned dataframes for use!

In this question, we hope to answer the following: ***Are there statistically significant differences in ratings between platforms like Rotten Tomatoes, IMDb, and Metacritic for the same movie?***

You may run the Statistical Analysis script to discover the results. Run `python3 stat_analysis.py` if you're using the default python interpreter or `python stat_analysis.py` if you're using Anaconda.
It will output the statistical analysis results, including the ANOVA test and p-values comparing ratings across platforms, along with post-hoc Tukey's HSD test results if significant differences are found. Additionally, t-tests will compare ratings between specific platforms, and graphical representations of the rating distributions will be displayed using box and bar plots.

### Machine Learning Analysis

In this question, we hope to answer the following: ***Do aggregated reviews from multiple sources provide a better predictor of a movie's overall success than individual platform scores?***

You may run the Machine Learning Analysis script to discover the results. Run `python3 ml_analysis.py` if you're using the default python interpreter or `python ml_analysis.py` if you're using Anaconda.
It will output prints of the accuracy scores of each model created for each platform, including an aggregated dataframe that averages all of the scores. The closer the value to `1`, the higher the accuracy as a predictor towards a movie's success.
