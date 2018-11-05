import csv

class City:
    def __init__(self, cityname, x, y):
        self._cityname = cityname
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def setX(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def setY(self, y):
        self._y = y

    @property
    def cityname(self):
        return self._cityname

    @cityname.setter
    def setCityname(self, cityname):
        self._cityname = cityname

def readCities():
    cities = []
    with open('./tsp2.csv', newline='') as csvfile:
        citiesreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in citiesreader:
            cities.append(City(cityname = row[0],
                               x=int(row[1]),
                               y=int(row[2])))
    return cities