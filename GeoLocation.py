import math
import redis

#Constants
MIN_LAT = math.radians(-90)
MAX_LAT = math.radians(90)
MIN_LON = math.radians(-180)
MAX_LON = math.radians(180)
E_R = 6378.1 #km #earth radius

#redis connection
re = redis.Redis()

#Function to calculate the bound within the given radius from user location
def GetBound(deg_lat,deg_long,radius):
    '''
    Calculate the max_lat, max_lon, min_lat, min_lon 
    within the radius
    PARAMETER: 
    -deg_lat: USER LATITUDE in DEGREES
    -deg_long: USER LONGITUDE in DEGREES
    -radius: SEARCH RADIUS in KM
    '''
    a = {}
    angular_rad = radius / E_R
    
    rad_lat = math.radians(deg_lat)
    rad_long = math.radians(deg_long)

    min_lat = rad_lat - angular_rad
    max_lat = rad_lat + angular_rad

    delta_long = math.asin(math.sin(angular_rad) / math.cos(rad_lat))

    if min_lat > MIN_LAT and MAX_LAT > max_lat:
        min_lon = rad_long - delta_long
        if min_lon < MIN_LON:
            min_lon += 2 * math.pi

        max_lon = rad_long + delta_long
        if max_lon > MAX_LON:
            max_lon -= 2 * math.pi

    else:
        min_lat = max(min_lat,MIN_LAT)
        max_lat = max(max_lat,MAX_LAT)
        min_lon = MIN_LON
        max_lon = MAX_LON

    a['min_lat'] = math.degrees(min_lat)
    a['max_lat'] = math.degrees(max_lat)
    a['min_lon'] = math.degrees(min_lon)
    a['max_lon'] = math.degrees(max_lon)
    return a

#Sample input users with locations
user1 = {'user':1,'name':'goku','lat':1,'long':1}
re.hmset('user1',user1)
user2 = {'user':2,'name':'vegetta','lat':2,'long':2}
re.hmset('user2',user2)
user3 = {'user':3,'name':'krillin','lat':3,'long':3}
re.hmset('user3',user3)
user4 = {'user':4,'name':'Piccolo','lat':4,'long':4}
re.hmset('user4',user4)

#Calculate the bound, within 300 km from the user location (0,0)
a = GetBound(0,0,300) 
min_lat = a['min_lat']
max_lat = a['max_lat']
min_lon = a['min_lon']
max_lon = a['max_lon']

result = []

#Query to get all users within 300km -radius from user location (0,0)
for i in re.keys():

    if (min_lat <= float(re.hgetall(i).get('lat')) <= max_lat) and (min_lon <= float(re.hgetall(i).get('long')) <= max_lon) and (:
        result.append(re.hgetall(i))

print result 
# Result should be 
# [
#   {'lat': '2', 'user': '2', 'long': '2', 'name': 'vegetta'}, 
#   {'lat': '1', 'user': '1', 'long': '1', 'name': 'goku'}
# ]





