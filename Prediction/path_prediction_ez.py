from Constants import constants

class PathPredictionEz:
    yMin = 0
    yMax = constants.FIELD_HEIGHT
    xMin = 0
    xMax = constants.FIELD_WIDTH
    def __init__(self):
        yMin = 0
        yMax = constants.FIELD_HEIGHT
        xMin = 0
        xMax = constants.FIELD_WIDTH


    def getCollision(self, startingPointX, startingPointY, m):

        b = float(startingPointY) - (float(m) * float(startingPointX))

        if (m > 0): #Puck bewegt sich nach unten (y = yMin = 0)
            intersectionPointX = (float(self.yMin) - float(b)) / float(m)
            nextStartingPointY = self.yMin
        elif (m < 0):#Puck bewegt sich nach oben (y = yMax = fieldheight)
            intersectionPointX = (float(self.yMax) - float(b)) / float(m)
            nextStartingPointY = self.yMax
        else:#steigung = 0 -> y position bleibt gleich und collision mit roboter ohne wandcollision garantiert
            return float(startingPointY)

        if (intersectionPointX < 0): #collision mit Bande wäre hinter roboter
            return float(b) #b aus geradengleichung ist schnittpunkt mit y achse und somit unser y
        else:
            nextStartingPointX = intersectionPointX
            return float(self.getCollision(nextStartingPointX, nextStartingPointY, -m))

    def calculate_arrival_point(self, point1, point2):

        #
        #               --------------- <- constants.FIELD_HEIGHT
        #               |             |
        # Roboter(y) -> |             |
        #               |             |
        #      (0,0) -> ---------------
        #  width (x) -> <             >

        # y = mx + t


        deltax = float(point2[0]) - float(point1[0])
        deltay = float(point2[1]) - float(point1[1])

        if(deltax>0):
            #wenn puck nach rechts geht, fahre in die mitte(Y WERT)
            arrivalPoint = (0, constants.FIELD_HEIGHT / 2)
            return arrivalPoint

        m = deltay / deltax

        startingPointX = float(point2[0])
        startingPointY = float(point2[1])

        value = self.getCollision(startingPointX, startingPointY, m)
        arrivalPoint = (0, value)
        return arrivalPoint



