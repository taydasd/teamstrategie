from DataModel import model
from Camera import Camera
from Constants import *
from datetime import datetime
import numpy as np
import cv2
import math
from Processing.ProcessFrame import processFrame
class State:
    IDLE = "IDLE"
    TRACKING = "TRACKING"
    PREDICTING = "PREDICTING"
    DEFENDING = "DEFENDING"
    HOMING = "HOMING"
    PLAYING_BACK = "PLAYING_BACK"


class RobotController:
    def __init__(self, sendMoveValues,updatePreCalculationUi, camera, calcData: dict = None):
        self.data = model
        self.state = State.IDLE
        self.sendMoveValues = sendMoveValues
        self.updatePreCalculationUi = updatePreCalculationUi
        self.camera = camera
        self.calc = calcData


    def update(self):
        if self.calc:
            x, y, radius, robotX, robotY, robotRadius, frame = (
                self.calc["x"],
                self.calc["y"],
                self.calc["radius"],
                self.calc["robotX"],
                self.calc["robotY"],
                self.calc["robotRadius"],
                self.calc["frame"]
            )

        if robotRadius < 10 or robotRadius > 50:
            robotX, robotY, robotRadius = -1, -1, -1

        self.currentPosition = (x, y)
        self.puckSpeed = self._calculateSpeed()
        frame = self.updatePreCalculationUi(
            frame, x, y, radius, robotX, robotY, robotRadius
        )
        self.isPuckGoingToRobot = self._isGoingToRobot()

        if self.state == State.IDLE:
            if self.isPuckGoingToRobot:
                self.state = State.PREDICTING
            if self._isAbleToAttack:
                self.state = State.PLAYING_BACK

        elif self.state == State.PREDICTING:
            self._resetPrediction()
            if self._makePrediction(frame):
                self.state = State.DEFENDING
            else:
                self.state = State.HOMING

        elif self.state == State.DEFENDING:
            self._moveToPredicted()
            if not self.isPuckGoingToRobot:
                self.state = State.HOMING

        elif self.state == State.HOMING:
            self._goHome()
            if self._atHome():
                self.state = State.IDLE

        elif self.state == State.PLAYING_BACK:
            self._playBack()
            self.state = State.HOMING

        self._saveState()
        return frame

    def _calculateSpeed(self):
        dx = self.data.currentPosition[0] - self.data.lastPosition[0]
        dy = self.data.currentPosition[1] - self.data.lastPosition[1]
        return math.sqrt(dx ** 2 + dy ** 2)

    def _isGoingToRobot(self):
        return self.data.currentPosition[1] < self.data.lastPosition[1] and abs(self.data.lastPosition[1] - self.data.currentPosition[1]) > 1

    def _isAbleToAttack(self):
        # logik falls puck sich im Bereich des Roboters befindet und sich so bewegt, dass Roboter angreifen kann
        return True

    def _resetPrediction(self):
        self.data.predictionMade = False
        self.data.savedPoints = []
        self.data.predictedPoints = []
        self.data.collisionPoints = []

    def _makePrediction(self, frame):
        # Deine Vorhersagelogik (gekürzt/eingekapselt)
        # Setze self.predictedPoint etc.
        return True  # Wenn Vorhersage erfolgreich


    def _moveToPredicted(self):
        if self.data.predictionMade and self.data.botActivated:
            moveX, moveY = self.mapCoordinates(
                self.data.predictedPoint[0],
                self.data.predictedPoint[1],
                CAMERA_FRAME_HEIGHT,
                CAMERA_FRAME_ROBOT_MAX_Y,
                TABLE_MAX_X,
                TABLE_MAX_Y,
            )
            moveX = TABLE_MAX_X - moveX
            self.sendMoveValues(int(moveX), int(moveY), "Defense")

    def _goHome(self):
        moveX, moveY = self.mapCoordinates(
            (CAMERA_FRAME_HEIGHT / 2),
            DEFENSIVE_LINE,
            CAMERA_FRAME_HEIGHT,
            CAMERA_FRAME_ROBOT_MAX_Y,
            TABLE_MAX_X,
            TABLE_MAX_Y,
        )
        if self.botActivated:
            self.sendMoveValues(int(moveX), int(moveY), "Homing")

    def _playBack(self):
        # Playback-Logik bei langsamem Puck in eigenem Feld
        pass

    def _playedBack(self):
        # Logik zur erkennung ob Puck zurückgespielt wurde
        # Fallback einbauen, falls Roboter Puck nicht getroffen hat
        # dieser soll dann zurück in PREDICTION FALLEN
        return False

    def _atHome(self):
        # Prüfen, ob Roboter am Ziel ist
        return True

    def _saveState(self):
        self.data.wasPuckGoingToRobot = self.data.isPuckGoingToRobot
        self.data.lastPosition = self.data.currentPosition
    
    
    


"""# schauen ob das so compiliert
def a():
    return True

def b():
    return True

# zum testen
controller = RobotController(a, b)
print(controller.state)
print(controller.data.targetPoint)
"""
