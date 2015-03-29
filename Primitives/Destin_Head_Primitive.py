'''
 Deplacemnt of the head Poppy to contact
 
 Author : H. Guermoule
'''
from __future__ import division
import pypot.primitive

class Sound_Detect_Motion(pypot.primitive.Primitive):
    '''
     primitive to make Poppy will return to contact
    '''
    def setup(self): 
        for m in self.robot.motors:
            m.moving_speed = 50.0
  	    #m.compliant_behavior = 'safe'
	    #m.goto_behavior = 'minjerk'

    def run(self):
	pres_head_z_pos = self.robot.head_z.present_position
	if (self.which_side == 'Left_Side'):
		Go_head_z_pos = pres_head_z_pos + 45
	elif (self.which_side == 'Right_Side') :
		Go_head_z_pos = pres_head_z_pos - 45
	elif (self.which_side == 'Center') :
		Go_head_z_pos = pres_head_z_pos
	# do Action
	self.robot.head_y.goal_position = 10
	self.robot.head_z.goal_position = Go_head_z_pos
	#self.robot.head_z.goto_position(Go_head_z_pos, 2, control = 'minjerk', wait=True)
    
    def teardown(self):
	self.robot.power_up()
