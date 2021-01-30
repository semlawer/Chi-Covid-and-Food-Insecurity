import sqlite3
import pandas as pd

connection = sqlite3.connect("course_information.sqlite3")
''' 
   Use the read_sql_query function to perform a query on a dataebase. 
   Pandas will automatically convert the list of tuples into a dataframe 
   for you when given a sqlite connection. 
'''
s0 = ''' SELECT lat, lon, building_code FROM gps WHERE building_code = "RY" '''
df = pd.read_sql_query(s0, connection)
print(df)
