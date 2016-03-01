from Adafruit_BNO055 import BNO055
import time
import threading
import os

class IMU:
  calibration_file_path = 'calibration.json'
  def __init__(self):
    self.imu = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)

  def boot(self):
    booted = self.imu.begin() 
    status, self_test, error = bno.get_system_status()
      
    if not(booted) or status == 0x01 or self_test != 0x0F:
      print('IMU error: {0}'.format(error)) 
    
    # BNO sensor axes remap values.  These are the parameters to the BNO.set_axis_remap
    # function.  Don't change these without consulting section 3.4 of the datasheet.
    # The default axes mapping below assumes the Adafruit BNO055 breakout is flat on
    # a table with the row of SDA, SCL, GND, VIN, etc pins facing away from you.

    self.imu.set_axis_remap(**{ 
      'x': BNO055.AXIS_REMAP_X,
      'y': BNO055.AXIS_REMAP_Z,
      'z': BNO055.AXIS_REMAP_Y,
      'x_sign': BNO055.AXIS_REMAP_POSITIVE,
      'y_sign': BNO055.AXIS_REMAP_POSITIVE,
      'z_sign': BNO055.AXIS_REMAP_NEGATIVE 
    })
    
    if os.path.exists(self.calibration_file_path):
      self.load_calibration()
    else:
      print "'{0}' not found, beginning calibration".format(self.calibration_file_path)
      self.calibrate()

  def calibrate(self):
    system_calibration, gyro_calibration, accelerometer_calibration, magnetometer_calibration = self.imu.get_calibration_status()

    while gyro_calibration != 3:
      print "Calibrating Gyroscope...{0}%\n".format(gyro_calibration*25)
      print "Please put the device down on a level surface.\n"
      time.sleep(0.5)
      system_calibration, gyro_calibration, accelerometer_calibration, magnetometer_calibration = self.imu.get_calibration_status()
      
    while magnetometer_calibration != 3:
      print "Calibrating Compass...{0}%\n".format(magnetometer_calibration*25)
      print "Please wave the device in Figure 8s.\n"
      time.sleep(0.5)
      system_calibration, gyro_calibration, accelerometer_calibration, magnetometer_calibration = self.imu.get_calibration_status()

    while accelerometer_calibration !=3:
      print "Calibrating Accelerometer...{0}%\n".format(accelerometer_calibration*25)
      print "Please move the device in a cube in the air.\n" 
      time.sleep(0.5)
      system_calibration, gyro_calibration, accelerometer_calibration, magnetometer_calibration = self.imu.get_calibration_status()

    while system_calibration != 3:
      print "Inertial Navigation Self-Calibrating...{0}%\n".format(system_calibration*25)
      print "Please wait."
      time.sleep(0.5)
      system_calibration, gyro_calibration, accelerometer_calibration, magnetometer_calibration = self.imu.get_calibration_status()
    
    store_calibration()

  def store_calibration(self):
    print "Storing calibration in {0}".format(self.calibration_file_path)
    with open(self.calibration_file_path, 'w') as calibration_file:
      json.dump(imu.get_calibration(), self.calibration_file_path)

  def load_calibration(self):
    print "Loading calibration from {0}".format(self.calibration_file_path)
    with open(self.calibration_file_path, 'r') as calibration_file:
      imu.set_calibration(json.load(self.calibration_file_path))

  def read(self):
    heading, roll, pitch = self.imu.read_euler() 
    x,y,z,w = self.imu.read_quaterion()

    temp_c = self.imu.read_temp() # in degrees C 
    x,y,z = self.imu.read_gyroscope() # in deg/sec

    x,y,z = self.imu.read_linear_acceleration() # in m/sec^2
    x,y,z = self.imu.read_gravity() # in m/sec^2
