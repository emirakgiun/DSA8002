#Coursework assignment submission: DSA8002
##Prepared by Emir Akgiun (student number 40367624)
###Description
This ZIP archive contains all files pertaining to my submission to the assignment. The files contain code, descriptions and solution to the tasks.
###Files and contents
-*Report-EmirAkgiun-40367624.pdf* - the report on coursework completion in the PDF format, compiled using LaTeX. Contains explanations and source code snippets,
subdivided into sections and subsections.
-*README.txt* - the readme file of the assignment project
-*Task1.py* - python script, containing all Python code produced in order to complete Task1 (a,b,c), alongside code for running a test.
-*Task2.py* - python script, containing all Python code produced in order to complete Task2, alongside code for running a test.
-*Task3.py* - python script, containing all Python code produced in order to complete Task3 (a,b), alongside code for running a test.
-*Task4.py* - python script, containing code snippets of all 3 Test Cases used throughout the task. This file should not be run and serves as a
summary of all code output for Task4. All the test cases are executed in their proper code files.
-*movies.csv* - task sourcefile, containing data on movies in .csv format. It is read into a dataframe in Task1.py 
-*ratings.csv* - task sourcefile, containing data on movie ratings in .csv format. It is read into a dataframe in Task1.py 
-*tags.csv* - task sourcefile, containing data on movies in .csv format. It is read into a dataframe in Task1.py 
-*movies.sql* - task output file, containing SQL statements to create a table with movies data
-*ratings.sql* - task output file, containing SQL statements to create a table with ratings data
-*tags.sql* - task output file, containing SQL statements to create a table with taags data
-*genres.sql* - task output file, containing SQL statements to create a table with genres data
###Dependencies
- python  3.(9)
- pandas
- pandasql
- .sql files were tested on their ability to generate proper tables in SQLite
###How to Run
Files should be checked in the same order they appear in the assignment.

Task 1 and Task 3 both solicit user console input, which could be disabled by passing arguments **test = True** and  **testInput**
to be equal to an integer, referring to the movieId. These task scripts also print out 
The task function inside the scripts should output a pandas Dataframe with all movies that were selected according to the Task 1(c) and Task3(c) respectively.

Task2.py will generate files of .sql format, which will in their turn generate SQL  script files with appropriate SQL statements, as wellas SQL tables when run. 
They are also used in Task3.py It also runs the Test Case 2. 


Task4.py should NOT be executed, as  it is simply a showcase of 3 test cases used  within the aforementioned scripts, one for each task.