from imu    import IMU 
from motors import Motors
import time

# motor = Motors()
# motor.boot()
# motor.move('backward', 255)

imu = IMU()
imu.boot()

while True:
  print '{0}'.format(imu.read())
  time.sleep(0.5)