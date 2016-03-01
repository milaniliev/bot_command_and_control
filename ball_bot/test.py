from imu    import IMU 
from motors import Motors

# motor = Motors()
# motor.boot()
# motor.move('backward', 255)

imu = IMU()
imu.boot()

print '{0}'.format(imu.read())