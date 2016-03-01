from Adafruit_MotorHAT import Adafruit_MotorHAT
import atexit

class Motors(object):
  left_motor_id = 1
  right_motor_id = 2
  
  left_motor_trim = 0
  right_motor_trim = 0
  
  def __init__(self, motor_controller_i2c_address = 0x60):
    self.motor_controller = AdafruitMotorHAT(motor_controller_i2c_address)
    self.left_motor = self.motor_controller.getMotor(self.class.left_motor_id)
    self.right_motor = self.motor_controller.getMotor(self.class.right_motor_id)
    
  def boot():
    # stop both motors
    self.all_stop()
  
    atexit.register(self.all_stop())
  
  def all_stop(self):
    self.left_motor.run(Adafruit_MotorHAT.RELEASE)
    self.righ_motor.run(Adafruit_MotorHAT.RELEASE)  

  def move(self, direction, speed, for_seconds=None):
    self.left_motor.setSpeed  max(0, min(speed + self.left_motor_trim, 255))
    self.right_motor.setSpeed max(0, min(speed + self.right_motor_trim, 255)) 

    motor_directions = {
      ' forward': {'left': Adafruit_MotorHAT.FORWARD,  'right': Adafruit_MotorHAT.FORWARD },  
      'backward': {'left': Adafruit_MotorHAT.BACKWARD, 'right': Adafruit_MotorHAT.BACKWARD}, 
          'left': {'left': Adafruit_MotorHAT.BACKWARD, 'right': Adafruit_MotorHAT.FORWARD },  
         'right': {'left': Adafruit_MotorHAT.FORWARD,  'right': Adafruit_MotorHAT.BACKWARD},  
    }[direction]

    self.left_motor.run(motor_directions['left'])
    self.righ_motor.run(motor_directions['right'])
    
    if for_seconds is not None:
      time.sleep(for_seconds)
      self.all_stop()
    
    
    