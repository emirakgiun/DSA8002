"""
DSA8002 Assignment file.
Task 2
Prepared by Emir Akgiun, student №40367624
"""
# Firstly, it is necessary to import the proper modules for the job at hand
import pandas as pd
import pandasql as sqldf
import sqlite3
"""In this task I´ve decided to generate SQL statements for table creation based on pandas dataframes"""
def Task2():
        # Firsly, it is necessary to wragle the data in the same way as in Task 1, so as to prepare it for being used for SQL statement generation
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
        genresDf  = genresDf.drop(labels = ["title"],axis = 1)
        moviesDf = moviesDf.fillna(value='None').drop(labels = ["genres"],axis = 1)
        # In order to properly generate string value to be inserted into the SQL table
        # it is necessary to wrap them in quotation marks
        def addQuotes(df):
                return f'"{df}"'
        # Selecting all the columns in dataframes containing string values
        moviesStringDf = moviesDf.select_dtypes(include='object')
        ratingsStringDf = ratingsDf.select_dtypes(include='object')
        tagsStringDf = tagsDf.select_dtypes(include='object')
        genresStringDf = genresDf.select_dtypes(include='object')
        # Applying the created function to our string columns
        moviesStringDf = moviesStringDf.applymap(addQuotes)
        ratingsStringDf = ratingsStringDf.applymap(addQuotes)
        tagsStringDf = tagsStringDf.applymap(addQuotes)
        genresStringDf = genresStringDf.applymap(addQuotes)
        # Updating the dataframes with columns containing edited strings
        moviesDf[moviesStringDf.columns] = moviesStringDf
        ratingsDf[ratingsStringDf.columns] = ratingsStringDf
        tagsDf[tagsStringDf.columns] = tagsStringDf
        genresDf[genresStringDf.columns] = genresStringDf
        print(moviesDf.head())
        print(ratingsDf.head())
        print(tagsDf.head())
        print(genresDf.head())
        # After preparing the dataframes, it is possible to  iterate through them, generating SQL tables
        def createSQL(dataFrame, tableName):
                # Obtaining the list of columns and data types  in the dataframe
                columns = []
                for col, dtype in zip(dataFrame.columns, dataFrame.dtypes):
                        if str(dtype) == 'object':
                                dtype = 'VARCHAR(255)'
                        elif 'int' in str(dtype):
                                dtype = 'INT'
                        elif 'float' in str(dtype):
                                dtype = 'FLOAT'
                        elif 'datetime' in str(dtype):
                                dtype = 'DATETIME'
                        # Creating a list of column names and the data types of values in it
                        columns.append(f"{col} {dtype}")

                # Creating the table
                columnStr = ", ".join(columns)
                createTable = f"CREATE TABLE {tableName} ({columnStr});"
                #  Finally, we can write the created strings into a .sql file
                with open(f'{tableName}.sql', 'wb') as f:
                        # Write the CREATE TABLE statement
                        f.write(createTable.encode('utf-8'))
                        # The string is binary to facilitate proper writing to the document
                        f.write(b'\n')
                        # Building and writing the INSERT INTO statements, looping  through the dataframe
                        for _, row in dataFrame.iterrows():
                                insert = f"INSERT INTO {tableName}({', '.join(dataFrame.columns)}) VALUES ({', '.join([str(x) for x in row])});"
                                f.write(insert.encode('utf-8'))
                                f.write(b'\n')
        # Saving created documents in variables
        moviesSQL = createSQL(moviesDf, "movies")
        ratingsSQL = createSQL(ratingsDf, "ratings")
        tagsSQL = createSQL(tagsDf, "tags")
        genresSQL = createSQL(genresDf, "genres")
        return [moviesSQL,ratingsSQL, tagsSQL,genresSQL]
#Executing the task function

""" Test for Task 2 """
"""Test Case 2: A database developer wants to fetch movie title and genre with moviedId set to 2  """
#It is necessary to  set up a local database in order to create SQL tables with our files
conn = sqlite3.connect("testdatabase.db")
cursor = conn.cursor()
#Executing our generated SQL files. !!! IF THE DATABASE FILE ALREADY EXISTS, COMMENT OUT THIS SECTION
# with open('movies.sql', 'r') as f:
#         sql1 = f.read()
#         cursor.executescript(sql1)
# with open('genres.sql', 'r') as f:
#         sql2 = f.read()
#         cursor.executescript(sql2)
# Commiting the changes to the database
conn.commit()
#END OF DATABASE CREATION!!!

# Selecting all data needed on movieId 2 into a dataframe"
testMoviesDf = pd.read_sql("SELECT title, genres FROM movies, genres WHERE movies.movieId == 2 AND genres.movieId == 2", conn)
print(testMoviesDf.head())
expectedOutput = pd.DataFrame({"title": ['Jumanji (1995)','Jumanji (1995)','Jumanji (1995)'], "genres": ["adventure", "children", "fantasy"]}, index=[0,1,2])
# Comparing to expected behaviour
if testMoviesDf.equals(expectedOutput):
        print("Test 2 passed successfully.")
else:
        print("Test 2 failed.")