from Adafruit_BNO055 import BNO055
import time
import threading
import os
import json

class InertialNavigation:
  calibration_file_path = 'calibration.json'
  update_interval = 0.1 # seconds
  
  def __init__(self):
    self.sensors = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)
    self.position = {'x': 0, 'y': 0, 'z': 0}
    self.velocity = {'x': 0, 'y': 0, 'z': 0}
    self.data_available = threading.Condition()

  def boot(self):
    booted = self.sensors.begin() 
    status, self_test, error = self.sensors.get_system_status()
      
    if not(booted) or status == 0x01 or self_test != 0x0F:
      print('Inertial Sensors error: {0}'.format(error)) 
    
    # BNO sensor axes remap values.  These are the parameters to the BNO.set_axis_remap
    # function.  Don't change these without consulting section 3.4 of the datasheet.
    # The default axes mapping below assumes the Adafruit BNO055 breakout is flat on
    # a table with the row of SDA, SCL, GND, VIN, etc pins facing away from you.

    self.sensors.set_axis_remap(**{ 
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
      
    self.start_position_recording()

  def calibrate(self):
    system_calibration, gyro_calibration, accelerometer_calibration, magnetometer_calibration = self.sensors.get_calibration_status()

    while gyro_calibration != 3:
      print "Calibrating Gyroscope...{0}%\n".format(gyro_calibration*25)
      print "Please put the device down on a level surface.\n"
      time.sleep(0.5)
      system_calibration, gyro_calibration, accelerometer_calibration, magnetometer_calibration = self.sensors.get_calibration_status()
      
    while magnetometer_calibration != 3:
      print "Calibrating Compass...{0}%\n".format(magnetometer_calibration*25)
      print "Please wave the device in Figure 8s.\n"
      time.sleep(0.5)
      system_calibration, gyro_calibration, accelerometer_calibration, magnetometer_calibration = self.sensors.get_calibration_status()

    while accelerometer_calibration !=3:
      print "Calibrating Accelerometer...{0}%\n".format(accelerometer_calibration*25)
      print "Please move the device in a cube in the air.\n" 
      time.sleep(0.5)
      system_calibration, gyro_calibration, accelerometer_calibration, magnetometer_calibration = self.sensors.get_calibration_status()

    while system_calibration != 3:
      print "Inertial Navigation Self-Calibrating...{0}%\n".format(system_calibration*25)
      print "Please wait."
      time.sleep(0.5)
      system_calibration, gyro_calibration, accelerometer_calibration, magnetometer_calibration = self.sensors.get_calibration_status()
    
    self.store_calibration()

  def store_calibration(self):
    print "Storing calibration in {0}".format(self.calibration_file_path)
    with open(self.calibration_file_path, 'w') as calibration_file:
      json.dump(self.sensors.get_calibration(), calibration_file)

  def load_calibration(self):
    print "Loading calibration from {0}".format(self.calibration_file_path)
    with open(self.calibration_file_path, 'r') as calibration_file:
      self.sensors.set_calibration(json.load(calibration_file))
      
  def get_current_position(self):
    
    data = {}

    with self.data_available:
      x,y,z,w = self.sensors.read_quaternion()
      data['heading'] = {
        'x': x,
        'y': y,
        'z': z,
        'w': w,
      }
      
      x,y,z = self.sensors.read_gravity() # in m/sec^2
      data['gravity'] = {
        'x': x,
        'y': y,
        'z': z,
      }
      
      x,y,z = self.sensors.read_gyroscope() # in deg/sec
      data['rotation'] = {
        'x': x,
        'y': y,
        'z': z,
      }
      
      data['temp'] = self.sensors.read_temp() # in degrees C
        
      data['position'] = self.position
      data['velocity'] = self.velocity
    
    return data
  
  def start_position_recording(self):
    self.position_thread = threading.Thread(target=self.record_position)
    self.position_thread.daemon = True
    self.position_thread.start()
  
  def record_position(self):
    while True:
      with self.data_available:
        acceleration = {}
        acceleration['x'], acceleration['y'], acceleration['z'] = self.sensors.read_linear_acceleration() # in m/sec^2
        
        # update current velocity, in m/sec
        self.velocity['x'] += acceleration['x'] * self.update_interval
        self.velocity['y'] += acceleration['y'] * self.update_interval
        self.velocity['z'] += acceleration['z'] * self.update_interval
        
        # update current position, in m from origin
        self.position['x'] += velocity['x'] * self.update_interval
        self.position['y'] += velocity['y'] * self.update_interval
        self.position['z'] += velocity['z'] * self.update_interval
        
        self.data_available.notifyAll()
        
      time.sleep(self.update_interval)
      
