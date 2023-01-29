"""
DSA8002 Assignment file.
Task 4
Prepared by Emir Akgiun, student №40367624
The snippets below are each run in their own respective task file, this particular script should NOT be run
"""
# Importing all the modules, that were used throughout the previous scripts
import pandas as pd
import pandasql as sqldf
import sqlite3

""" Test for Task 1 """
"""Test Case 1: A user tries to find a similar movie to the one with ID 1231 "The Right Stuff". The output should contain a movie titled "Apollo 13", which has an ID of 150"""
from Task1 import Task1
testValue = 1231
expectedOutput = pd.DataFrame({"movieId": 150, "title": "Apollo 13 (1995)"}, index=[0])
testOutput =  Task1(test = True, testInput = testValue)
if testOutput.equals(expectedOutput):
        print("Test 1 passed successfully.")
else:
        print("Test 1 failed.")


""" Test for Task 2 """
"""Test Case 2: A database developer wants to fetch movie title and genre with moviedId set to 2  """
#It is necessary to  set up a local database in order to create SQL tables with our files
conn = sqlite3.connect("testdatabase.db")
cursor = conn.cursor()
#Executing our generated SQL files. !!! IF DATABASE ALREADY EXISTS, COMMENT OUT THIS SECTION
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


""" Test for Task 3 """
"""Test Case 3: A user aims to find a similar movie to the one with ID 2. """
expectedOutput = pd.DataFrame({"movieId": [4993, 7153, 46972, 59501, 80834, 106489], "title": ["Lord of the Rings: The Fellowship of the Ring, The (2001)","Lord of the Rings: The Return of the King, The (2003)","Night at the Museum (2006)","Chronicles of Narnia: Prince Caspian, The (2008)", "Sintel (2010)", "Hobbit: The Desolation of Smaug, The (2013)"]}, index=[0,1,2,3,4,5])
testOutput = Task3(test = True, testInput= 2)
if testOutput.equals(expectedOutput):
        print("Test 3 passed successfully.")
else:
        print("Test 3 failed.")