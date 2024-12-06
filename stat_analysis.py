import numpy as np
import pandas as pd
import data_cleaner
import matplotlib.pyplot as plt
import scipy.stats as stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import seaborn as sns

def clean_data(imdb, metacritic, rotten):
    # normalize title names (lowercase) for matching
    imdb['Title'] = imdb['Title'].str.lower()
    metacritic['Title'] = metacritic['Title'].str.lower()
    rotten['Title'] = rotten['Title'].str.lower()
    
    # merge rotten tomatoes data: average of critic and audience score
    rotten['average_score'] = (rotten['critic_score'] + rotten['audience_score']) / 2
    
    # merge the data on 'Title' and 'Year' 
    merged_data = pd.merge(imdb[['Title', 'Year', 'Rating']], 
                           metacritic[['Title', 'Year', 'Rating']], 
                           on=['Title', 'Year'], 
                           how='outer', 
                           suffixes=('_imdb', '_meta'))
    merged_data = pd.merge(merged_data, 
                           rotten[['Title', 'Year', 'average_score']], 
                           on=['Title', 'Year'], 
                           how='outer')
    
    return merged_data

def perform_statistical_tests(merged_data):
    ratings_data = merged_data[['Rating_imdb', 'Rating_meta', 'average_score']].dropna()

    # ANOVA Test
    f_stat, p_value = stats.f_oneway(ratings_data['Rating_imdb'], 
                                      ratings_data['Rating_meta'], 
                                      ratings_data['average_score'])

    print(f'ANOVA Test: F-statistic = {f_stat}, P-value = {p_value}')
    
    if p_value < 0.05:
        print("There is a statistically significant difference in ratings between the platforms.\n")
        
        # Post hoc test (Tukey's HSD)
        ratings_melted = ratings_data.melt(var_name='Platform', value_name='Rating')
        tukey_result = pairwise_tukeyhsd(ratings_melted['Rating'], ratings_melted['Platform'], alpha=0.05)
        print(tukey_result)
    else:
        print("There is no statistically significant difference in ratings between the platforms.")
    
    # T-test for IMDB vs Metacritic
    t_stat_imdb_meta, p_value_imdb_meta = stats.ttest_ind(ratings_data['Rating_imdb'], ratings_data['Rating_meta'])
    print(f'T-test (IMDB vs Metacritic): T-statistic = {t_stat_imdb_meta}, P-value = {p_value_imdb_meta}')
    
    if p_value_imdb_meta < 0.05:
        print("There is a statistically significant difference in ratings between IMDB and Metacritic (T-test).\n")
    else:
        print("There is no statistically significant difference in ratings between IMDB and Metacritic (T-test).")
    
    # T-test for IMDB vs Rotten Tomatoes
    t_stat_imdb_rt, p_value_imdb_rt = stats.ttest_ind(ratings_data['Rating_imdb'], ratings_data['average_score'])
    print(f'T-test (IMDB vs Rotten Tomatoes): T-statistic = {t_stat_imdb_rt}, P-value = {p_value_imdb_rt}')
    
    if p_value_imdb_rt < 0.05:
        print("There is a statistically significant difference in ratings between IMDB and Rotten Tomatoes (T-test).\n")
    else:
        print("There is no statistically significant difference in ratings between IMDB and Rotten Tomatoes (T-test).")
    
    # T-test for Metacritic vs Rotten Tomatoes
    t_stat_meta_rt, p_value_meta_rt = stats.ttest_ind(ratings_data['Rating_meta'], ratings_data['average_score'])
    print(f'T-test (Metacritic vs Rotten Tomatoes): T-statistic = {t_stat_meta_rt}, P-value = {p_value_meta_rt}')
    
    if p_value_meta_rt < 0.05:
        print("There is a statistically significant difference in ratings between Metacritic and Rotten Tomatoes (T-test).\n")
    else:
        print("There is no statistically significant difference in ratings between Metacritic and Rotten Tomatoes (T-test).")

def plot_ratings_distribution(merged_data):
    ratings_data = merged_data[['Rating_imdb', 'Rating_meta', 'average_score']].dropna()
    ratings_melted = ratings_data.melt(var_name='Platform', value_name='Rating')
    
    platform_names = {
        'Rating_imdb': 'IMDB',
        'Rating_meta': 'Metacritic',
        'average_score': 'Rotten Tomatoes'
    }
    ratings_melted['Platform'] = ratings_melted['Platform'].replace(platform_names)
    
    # box plot
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Platform', y='Rating', data=ratings_melted, hue='Platform', showfliers=True)
    plt.title('Rating Distribution by Review Platform', fontsize=16)
    plt.xlabel('Review Platform', fontsize=12)
    plt.ylabel('Rating Score', fontsize=12)
    
    # bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Platform', y='Rating', data=ratings_melted, errorbar='sd', hue='Platform', estimator='mean', palette='Set2')
    plt.title('Average Rating by Review Platform', fontsize=16)
    plt.xlabel('Review Platform', fontsize=12)
    plt.ylabel('Average Rating Score', fontsize=12)
    
    plt.tight_layout()
    plt.show()


def main():
    imdb, metacritic, rotten = data_cleaner.get_dataframes('imdb_movies.csv', 'metacritic_movies.csv', 'rt_movies.csv')
    merged_data = clean_data(imdb, metacritic, rotten)
    
    perform_statistical_tests(merged_data)
    plot_ratings_distribution(merged_data)


if __name__ == '__main__':
    main()
