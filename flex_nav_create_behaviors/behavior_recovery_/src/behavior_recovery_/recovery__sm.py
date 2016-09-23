#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_recovery_')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flex_nav_flexbe_states.move_distance_state import MoveDistanceState
from flex_nav_flexbe_states.clear_costmaps_state import ClearCostmapsState
from flex_nav_flexbe_states.rotate_angle_state import RotateAngleState
from flex_nav_create_flexbe_states.create_status_state import CreateStatusState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jul 25 2016
@author: John Wesley Hayhurst
'''
class RecoverySM(Behavior):
	'''
	A recovery behavior for the flex nav system
	'''


	def __init__(self):
		super(RecoverySM, self).__init__()
		self.name = 'Recovery '

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:30 y:365, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:585 y:71, x:130 y:365
		_sm_recovery_steps_0 = OperatableStateMachine(outcomes=['finished', 'failed'])

		with _sm_recovery_steps_0:
			# x:94 y:63
			OperatableStateMachine.add('Backup',
										MoveDistanceState(target_time=3, distance=-1, cmd_topic='/create_node/cmd_vel', odometry_topic='/create_node/odom'),
										transitions={'done': 'Clear Costmaps', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:241 y:70
			OperatableStateMachine.add('Clear Costmaps',
										ClearCostmapsState(costmap_topics=['/high_level_planner/clear_costmap', '/mid_level_planner/clear_costmap', '/low_level_planner/clear_costmap']),
										transitions={'done': 'Full Rotation', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:398 y:63
			OperatableStateMachine.add('Full Rotation',
										RotateAngleState(target_time=5, cmd_topic='/create_node/cmd_vel', odometry_topic='/create_node/odom'),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:792 y:148, x:130 y:365, x:230 y:365, x:330 y:365, x:430 y:365
		_sm_recovery_statemachine_1 = ConcurrencyContainer(outcomes=['finished', 'failed'], conditions=[
										('failed', [('Bumper State', 'failed')]),
										('failed', [('Recovery steps', 'failed')]),
										('finished', [('Recovery steps', 'finished')])
										])

		with _sm_recovery_statemachine_1:
			# x:294 y:72
			OperatableStateMachine.add('Recovery steps',
										_sm_recovery_steps_0,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:73 y:193
			OperatableStateMachine.add('Bumper State',
										CreateStatusState(),
										transitions={'failed': 'failed'},
										autonomy={'failed': Autonomy.Off})



		with _state_machine:
			# x:92 y:51
			OperatableStateMachine.add('Recovery Statemachine',
										_sm_recovery_statemachine_1,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
