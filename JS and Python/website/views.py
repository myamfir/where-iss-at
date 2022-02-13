from curses.ascii import isspace
from flask import Blueprint, render_template, request
import urllib.request, json, datetime
import time
import json
from datetime import datetime, date, time, timedelta

#To initialize variables
issPeeps = []
timeArray = []
issLink = []
lat = []
lon = []
city = []
y = 0

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])

def main():

    #To make sure the function only execute if the request method is POST
    if request.method == 'POST':
        data = request.form.get('myDatetime')

        date_format = "%Y-%m-%dT%H:%M" 
        data = datetime.strptime(data, date_format)

        tentimes(data)

        getISSpeeps()

    #To return variables/arrays to the JavaScript to be displayed.
    return render_template("home.html", timeArray2=timeArray, lat2=lat, lon2=lon, city2=city, issLink2=issLink, issPeeps2=issPeeps)


#Retrieve data from json link (for ISS locations)
def getISS(ts):

    url = "https://api.wheretheiss.at/v1/satellites/25544/positions?timestamps=" + str(ts)
    response = urllib.request.urlopen(url)
    info = json.loads(response.read())

    lat1 = info[0]["latitude"]
    lon1 = info[0]["longitude"]

    issLink.append(url)
    lat.append(lat1)
    lon.append(lon1)

    url1 = "https://api.opencagedata.com/geocode/v1/json?q="+str(lat1)+"+"+str(lon1)+"&key=557c590f9bfb4a868d8c07f37c5ac3d8"
    response = urllib.request.urlopen(url1)
    info1 = json.loads(response.read())

    city1 = info1["results"][0]["formatted"]

    city.append(city1)

#Retrieve data from json link (for list of people in space currently)
def getISSpeeps(): 
    
    urlpeeps = "http://api.open-notify.org/astros.json"
    response = urllib.request.urlopen(urlpeeps)
    inf4 = json.loads(response.read())


    for i in inf4['people']:
        issPeeps1 = i['name']
        issPeeps.append(issPeeps1)

#Create 13 timestamps for retrieving 13 data
def tentimes(data):
    
    #Before
    time_choosed = data

    time_initiated = time_choosed - timedelta(minutes=60)

    for x in range(13):

        global m

        m = 10 * x

        time_add = time_initiated + timedelta(minutes=m)
        timeArray.append(str(time_add))

        timeEpoch = int(time_add.timestamp())
        getISS(timeEpoch)


"""
----------------------------------------------------------------------------------------------
-------------------------------------------> MAIN <-------------------------------------------
----------------------------------------------------------------------------------------------
"""
#Main


if __name__ == "__main__":
    main()