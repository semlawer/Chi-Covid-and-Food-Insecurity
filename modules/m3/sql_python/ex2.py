import sqlite3

connection = sqlite3.connect("course_information.sqlite3")
c = connection.cursor()

''' 
Parameterized queries 
    Database will check values provided for parameters to verify that they
    are not operations that will destroy the data
'''

# Use ''' quotes to allow for escape characters and multiline queries
# wrong...
s0s = ''' SELECT lat, lon FROM gps WHERE building = RY '''

# right
s0 = ''' SELECT lat, lon, building_code 
         FROM gps 
         WHERE building_code = "RY" '''


# parameterize building. Use a '?' to indicate where an argument should be
s1 = ''' SELECT lat,lon FROM gps WHERE building_code = ? '''
args1 = ["RY"]

print(c.execute(s1, args1).fetchall())
