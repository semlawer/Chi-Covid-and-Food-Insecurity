import sqlite3

# Opens a sqlite database for querying
connection = sqlite3.connect("course_information.sqlite3")
c = connection.cursor()

# Retrive all the courses inside the courses table
# No need for a ; after the statment like in the sqlite3 terminal
s = ''' SELECT * FROM courses LIMIT 10 '''

# To perform the query then we call the execute() method with the query strinng
c.execute(s)

# We can "fetch" the result table by callinng the fetchall method on the cursor object.
# Calling a fetchall() will return a list of tuples where each tuple is a row in the table returned.
table = c.fetchall()

# We can print the result table.
print(table)

# Note: We can combine the fetchall() and execute() into a single line as follows
# c.execute(s).fetchall()
