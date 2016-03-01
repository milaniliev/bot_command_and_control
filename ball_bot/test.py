from inertial_navigation import InertialNavigation 
from motors import Motors
import time

# motor = Motors()
# motor.boot()
# motor.move('backward', 255)

nav = InertialNavigation()
nav.boot()

while True:
  print 'POS: {0}'.format(nav.get_current_position()['position'])
  print 'VEL: {0}'.format(nav.get_current_position()['velocity'])
  print 'ACC: {0}'.format(nav.get_current_position()['acceleration'])
  print 'HED: {0}'.format(nav.get_current_position()['heading'])
  time.sleep(2)