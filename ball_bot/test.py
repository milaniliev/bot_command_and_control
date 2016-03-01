import imu
from motors import Motors

motor = Motors()
motor.boot()
motor.move('backward', 255)