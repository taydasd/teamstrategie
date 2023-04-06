from StepperController.StepperController import StepperController
from Camera.Camera import Camera
controller = StepperController("COM4", 115200)
controller.calibrate()
camera = Camera(0)

