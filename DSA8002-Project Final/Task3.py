"""
DSA8002 Assignment file.
Task 3(a,b)
Prepared by Emir Akgiun, student №40367624
"""
# Firstly, it is necessary to import the proper modules for the job at hand
import pandas as pd
from pandasql import sqldf
def Task3(test = False, testInput = 0):
        #  And for one more time, let us import the datasources in csv files, wrangle them and prepare
        # them for being used for SQL statements
        moviesDf = pd.read_csv("movies.csv")
        ratingsDf = pd.read_csv("ratings.csv")
        tagsDf = pd.read_csv("tags.csv")
        moviesDf = moviesDf.drop_duplicates(subset=["movieId", "title"])
        ratingsDf = ratingsDf.drop_duplicates(subset=["movieId", "userId"])
        tagsDf = tagsDf.drop_duplicates()
        moviesDf = moviesDf.dropna()
        ratingsDf = ratingsDf.dropna()
        tagsDf = tagsDf.dropna()
        allMovieId = moviesDf["movieId"]
        ratingsDf = ratingsDf.loc[ratingsDf["movieId"].isin(allMovieId)]
        tagsDf = tagsDf.loc[tagsDf["movieId"].isin(allMovieId)]
        splitCol = moviesDf['genres']
        splitCol = splitCol.str.lower()
        splitCol = splitCol.str.split('|')
        moviesDf['genres'] = splitCol
        genresDf = moviesDf.explode('genres')
        genresDf = genresDf.drop(labels=["title"], axis=1)
        moviesDf = moviesDf.fillna(value='None').drop(labels=["genres"], axis=1)
        """ Section A - SQL Queries for Similar Movie Retrieval"""
        allMovieId = moviesDf["movieId"]
        allMovieId = allMovieId.tolist()
        selectedId = -1
        while (selectedId not in allMovieId) == True:
                if test == False:
                        print('Enter the Movie Id: ')
                        selectedId = int(input('> '))

                else:
                        print('Testing mode. Input predefined. ')
                        selectedId = int(testInput)
        # The SQL query starts here. It operates over the dataframes thanks to pandasql

        query = f"SELECT DISTINCT m.movieId, m.title FROM moviesDf m JOIN ratingsDf r ON m.movieId = r.movieId JOIN genresDf g ON m.movieId =  g.movieId WHERE r.rating IN (SELECT DISTINCT rating from ratingsDf r WHERE r.movieId = {selectedId}) AND g.genres IN (SELECT DISTINCT genres  FROM genresDf g WHERE g.movieId = {selectedId}) AND m.movieId != {selectedId};"

        similarMovies = sqldf(query)

        """ Section B - SQL Query for tag-based Enhanced Movie Retrieval"""
        # In this section I've decided to also include tags in the query, so tag similarity is also
        # taken into account when fetching a result
        queryEnhanced = f"SELECT DISTINCT m.movieId, m.title FROM moviesDf m JOIN ratingsDf r ON m.movieId = r.movieId JOIN genresDf g ON m.movieId =  g.movieId JOIN tagsDf t ON m.movieId = t.movieId WHERE r.rating IN (SELECT DISTINCT rating from ratingsDf r WHERE r.movieId = {selectedId}) AND g.genres IN (SELECT DISTINCT genres  FROM genresDf g WHERE g.movieId = {selectedId}) AND t.tag IN (SELECT DISTINCT tag  FROM tagsDf t WHERE t.movieId = {selectedId}) AND m.movieId != {selectedId};"
        similarMoviesEnhanced = sqldf(queryEnhanced)
        print(f"You've selected movie named {moviesDf['title'].loc[moviesDf['movieId'] == selectedId].values.tolist()}. Here are the similarly tagged movies of similar ratings and genres")
        print(similarMoviesEnhanced)
        return similarMoviesEnhanced
Task3()
""" Test for Task 3 """
"""Test Case 3: A user aims to find a similar movie to the one with ID 2. """
expectedOutput = pd.DataFrame({"movieId": [4993, 7153, 46972, 59501, 80834, 106489], "title": ["Lord of the Rings: The Fellowship of the Ring, The (2001)","Lord of the Rings: The Return of the King, The (2003)","Night at the Museum (2006)","Chronicles of Narnia: Prince Caspian, The (2008)", "Sintel (2010)", "Hobbit: The Desolation of Smaug, The (2013)"]}, index=[0,1,2,3,4,5])
testOutput = Task3(test = True, testInput= 2)
if testOutput.equals(expectedOutput):
        print("Test 3 passed successfully.")
else:
        print("Test 3 failed.")