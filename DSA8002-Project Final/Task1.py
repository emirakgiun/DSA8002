"""
DSA8002 Assignment file.
Task 1(a,b,c)
Prepared by Emir Akgiun, student №40367624
"""

# Firstly, it is necessary to import the proper modules for the job at hand
import pandas as pd

# Afterwards, it in necessary to read the data provided in CSV files into Pandas dataframes
# As long as the CSV files are in the same directory as this script, it is not necessary to
# specify a full path to the files, so I stick to simply using the file names as arguments
# to pandas.read_csv()
def Task1(test = False, testInput = 1):
        """ Section A - Import"""
        moviesDf = pd.read_csv("movies.csv")
        ratingsDf = pd.read_csv("ratings.csv")
        tagsDf = pd.read_csv("tags.csv")
        print(f"{tagsDf.shape}")
        print(f"{ratingsDf.shape}")

        # Next up, using the dataframes created it is necessary to perform some  data cleaning
        # Dropping duplicates
        moviesDf = moviesDf.drop_duplicates(subset=["movieId", "title"])
        ratingsDf = ratingsDf.drop_duplicates(subset=["movieId", "userId"])
        tagsDf = tagsDf.drop_duplicates()

        # Checking if there are no duplicate entries anymore
        print(f"The number of duplicates in the Movies table: {moviesDf.duplicated().sum()}")
        print(f"The number of duplicates in the Ratings table: {ratingsDf.duplicated().sum()}")
        print(f"The number of duplicates in the Tags table: {tagsDf.duplicated().sum()}")

        # Checking if there are no duplicate entries anymore
        print(f"NA values to remove: {moviesDf.isna().sum().sum()+ratingsDf.isna().sum().sum()+tagsDf.isna().sum().sum()}")
        moviesDf = moviesDf.dropna()
        ratingsDf = ratingsDf.dropna()
        tagsDf = tagsDf.dropna()
        # Lastly, filtering out entries in Ratings, Tags  that  do NOT pertain to any entries in Movies
        allMovieId = moviesDf["movieId"]
        # A test variable "someMovieId" was used to check that proper reviews and tags are, in fact, being filtered.
        # someMovieId = allMovieId.loc[1:12]
        ratingsDf = ratingsDf.loc[ratingsDf["movieId"].isin(allMovieId)]
        tagsDf = tagsDf.loc[tagsDf["movieId"].isin(allMovieId)]
        """ Section B - Similar Movies Retrieval"""
        # Merging the ratings, tags dataframes with movies in order to be able to fetch ratings and tags
        mergedDf = moviesDf.merge(ratingsDf[["movieId", "rating"]], on='movieId', how='left')
        mergedDf = mergedDf.merge(tagsDf[["movieId", "tag"]], on='movieId', how='left')
        mergedDf = mergedDf.fillna(value='None')

        # Splitting genres into a list of strings and setting them to lower-case, in order to ensure the retrieval
        # algorithm is case agnostic
        splitCol = mergedDf['genres']
        splitCol = splitCol.str.lower()
        splitCol = splitCol.str.split('|')
        mergedDf['genres'] = splitCol
        moviesDf = mergedDf
        # Now, it is time to group all the rows with repeating  movie IDs that exploded after joins previously,
        # putting all the proper ratings and tags into separate lists for every movie.
        moviesRatingDf = moviesDf.groupby('movieId')['rating'].apply(list)
        moviesRatingDf = moviesRatingDf.to_frame()
        moviesRatingDf = moviesRatingDf.rename(columns={0: 'movieId', 1: 'rating'})
        moviesRatingDf = moviesRatingDf.reset_index()
        moviesTagsDf = moviesDf.groupby('movieId')['tag'].apply(list)
        moviesTagsDf = moviesTagsDf.to_frame()
        moviesTagsDf = moviesTagsDf.rename(columns={0: 'movieId', 1: 'tag'})
        moviesTagsDf = moviesTagsDf.reset_index()
        moviesDf = moviesDf.drop_duplicates(subset = "movieId")
        moviesDf = moviesDf.reset_index()
        moviesDf = moviesDf.drop(['index', 'rating', 'tag'], axis = 1)
        moviesDf['rating'] = pd.DataFrame(moviesRatingDf['rating'])
        moviesDf['tag'] = pd.DataFrame(moviesTagsDf['tag'])
        moviesDf = moviesDf.fillna(value='None')

        # Prompting the user to enter a valid Movie ID and put the accordingly retrieved data into variables
        allMovieId = allMovieId.tolist()
        selectedId = -1
        while (selectedId not in allMovieId) == True:
                if test == False:
                        print('Enter the Movie Id: ')
                        selectedId = int(input('> '))

                else:
                        print('Testing mode. Input predefined. ')
                        selectedId = int(testInput)
        # Saving the values of columns pertaining to the chosen movie
        selectedMovie = moviesDf['title'].loc[moviesDf['movieId'] == selectedId].values.tolist()
        selectedGenre = moviesDf['genres'].loc[moviesDf['movieId'] == selectedId].values
        selectedRatings = moviesDf['rating'].loc[moviesDf['movieId'] == selectedId].values
        selectedTags = moviesDf['tag'].loc[moviesDf['movieId'] == selectedId].values
        print(f"You have chosen {selectedMovie[0]}, which is a(n) {str(selectedGenre[0])} movie"
        f", with Id {selectedId}."
        f"\nHere are the movies of the same genre(s) and possessing similar ratings: ")
        # Back  to merged dataframe with exploded genres to facilitate easier filtering
        selectedGenre = list(selectedGenre)[0]
        selectedRatings = list(selectedRatings)[0]
        mergedDf = mergedDf.explode('genres')
        mergedDf = mergedDf.drop_duplicates(subset=["genres", "rating", "tag"])
        # Fetching movies with matching ratings and genres, dropping all the duplicate rows and  unnecessary columns
        similarMovies = mergedDf[mergedDf["movieId"] != selectedId]
        similarMovies = similarMovies[similarMovies['genres'].isin(selectedGenre)&similarMovies['rating'].isin(selectedRatings)]
        similarMoviesFinal = similarMovies.drop_duplicates(subset = ["movieId", "title"]).drop(labels = ["rating", "genres", "tag"],axis = 1)
        print(similarMoviesFinal)
        """ Section C - Enhancing Similar Movies Retrieval"""
        # Removing duplicate tags and preparing the list of tags
        selectedTags = list(selectedTags)[0]
        selectedTags = set(selectedTags)
        selectedTags = list(selectedTags)
        # Preparing the movies dataset in a similar way to Task1(b)
        print(f"Now, let's enhance the search and show a subset  of  movies with most common tags as your selected movie - {selectedMovie[0]}."
                f"\nThe tags users assigned to this movie are: {selectedTags} ")
        similarMovies = mergedDf[mergedDf['tag'].isin(selectedTags)]
        similarMovies = similarMovies[similarMovies["movieId"] != selectedId]
        similarMoviesEnhanced = similarMovies[similarMovies['genres'].isin(selectedGenre) & similarMovies['rating'].isin(selectedRatings)]
        # Creating a dataframe containing the number of instances of each tag being  used on every movie
        similarMoviesFreq = similarMoviesEnhanced.groupby(['movieId','tag']).size()
        #If for some reason no dataframe is created, it is necessary to change that object's type
        if not isinstance(similarMoviesFreq, pd.DataFrame):
                similarMoviesFreq = similarMoviesFreq.to_frame()
        # Mutating the dataframes in an appropriate way
        similarMoviesFreq = similarMoviesFreq.reset_index()
        similarMoviesFreq = similarMoviesFreq.rename(columns={0: 'tag frequency'})
        similarMoviesEnhanced = similarMoviesEnhanced.drop_duplicates(subset=["tag"]).drop(labels = ["rating", "genres"],axis = 1)
        similarMoviesEnhanced =  similarMoviesEnhanced.reset_index()
        # Checking whether any similar tag frequencies were added and append them to the dataframe/sort the frequencies
        if not similarMoviesFreq.empty:
                similarMoviesEnhanced = similarMoviesEnhanced.join(similarMoviesFreq['tag frequency'])
                similarMoviesEnhanced= similarMoviesEnhanced.sort_values('tag frequency', ascending=False)
        # Final output of the function, the tag-coincidence rate and a skimmed best-matching movies dataframe
        if similarMoviesEnhanced.empty:
                print(f"No movies of similar genre and rating share same tags as the movie you chose :( ")
                similarMoviesEnhancedFinal  = None
        else:
                print(f"Here are the matching movies of the same genre(s) and similar ratings, sorted  by common tag frequency: ")
                print(similarMoviesEnhanced)
                print(f"Finally, just the best matching movies: ")
                similarMoviesEnhancedFinal = similarMoviesEnhanced.drop_duplicates(subset=["movieId", "title"]).drop(labels=["tag", "tag frequency","index"], axis=1)
                print(similarMoviesEnhancedFinal)
        return similarMoviesEnhancedFinal

# The function that performs the algorithm is called here
Task1()

""" Test for Task 1 """
"""Test Case 1: A user tries to find a similar movie to the one with ID 1231 "The Right Stuff". The output should contain a movie titled "Apollo 13", which has an ID of 150"""
testValue = 1231
expectedOutput = pd.DataFrame({"movieId": 150, "title": "Apollo 13 (1995)"}, index=[0])
testOutput =  Task1(test = True, testInput = testValue)
if testOutput.equals(expectedOutput):
        print("Test 1 passed successfully.")
else:
        print("Test 1 failed.")
