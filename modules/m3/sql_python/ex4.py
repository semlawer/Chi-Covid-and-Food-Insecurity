import sqlite3
import math

connection = sqlite3.connect("course_information.sqlite3")
c = connection.cursor()


def distance(x1, y1, x2, y2):
    sq1 = (x1-x2)*(x1-x2)
    sq2 = (y1-y2)*(y1-y2)
    return math.sqrt(sq1 + sq2)


connection.create_function("distance", 4, distance)

s1 = ''' 
    SELECT a.building_code, b.building_code, distance(a.lon,a.lat,b.lon,b.lat) as distance
    FROM gps as a JOIN gps as b
    WHERE a.building_code != b.building_code
    LIMIT 10
    '''
print(c.execute(s1, []).fetchall())
