import sqlite3
import math

connection = sqlite3.connect("course_information.sqlite3")
c = connection.cursor()


def distance(x1, y1, x2, y2):
    sq1 = (x1-x2)*(x1-x2)
    sq2 = (y1-y2)*(y1-y2)
    return math.sqrt(sq1 + sq2)


connection.create_function("distance", 4, distance)

# distance from every building to Ryerson
# option 1

s1 = '''
       SELECT lon, lat, building_code FROM gps WHERE building_code = "RY"
     '''
args1 = []
(ry_lat, ry_lon, _), *rest = c.execute(s1, args1).fetchall()

s2 = '''
       SELECT a.building_code, distance(a.lon,a.lat,?,?) as distance
       FROM gps as a
       WHERE a.building_code != ?
       LIMIT 10
       '''
# order matters in arguments.
print("Option #1:")
print(c.execute(s2, [ry_lon, ry_lat, "RY"]).fetchall())

# distance from every building to Ryerson
# option 2: Better to use nested query instead of two separate queries
s3 = '''
       SELECT a.building_code, distance(a.lon,a.lat,b.lon,b.lat) as distance
       FROM gps as a JOIN (SELECT lon, lat, building_code FROM gps WHERE building_code = ?) as b
       WHERE a.building_code != b.building_code
       LIMIT 10
     '''
print("Option #2:")
print(c.execute(s3, ["RY"]).fetchall())
