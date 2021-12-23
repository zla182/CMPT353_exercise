import sys
import pandas as pd
import difflib

movie_list = sys.argv[1]
movie_ratings = sys.argv[2]
output = sys.argv[3]

movies = open(movie_list).readlines()
ratings = pd.read_csv(movie_ratings)
ratings['title'] = ratings['title'].apply(lambda x: difflib.get_close_matches(x,movies))
ratings['title'] = ratings["title"].str.get(0)
ratings = ratings.groupby(by=["title"], dropna=True).mean()
ratings['rating'] = ratings['rating'].round(2)
ratings.to_csv(output)
