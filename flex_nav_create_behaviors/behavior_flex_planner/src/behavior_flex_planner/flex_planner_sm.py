#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_flex_planner')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flex_nav_flexbe_states.get_pose_state import GetPoseState
from flex_nav_flexbe_states.get_path_state import GetPathState
from flexbe_states.operator_decision_state import OperatorDecisionState
from flex_nav_flexbe_states.follow_topic_state import FollowTopicState
from flex_nav_flexbe_states.follow_path_state import FollowPathState
from flex_nav_create_flexbe_states.create_status_state import CreateStatusState
from flexbe_states.log_state import LogState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jun 29 2016
@author: Justin Willis
'''
class FlexPlannerSM(Behavior):
	'''
	Generates a plan and executes it
	'''


	def __init__(self):
		super(FlexPlannerSM, self).__init__()
		self.name = 'Flex Planner'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]

		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:921 y:57, x:456 y:275
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.null_path = None

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]

		# [/MANUAL_CREATE]

		# x:433 y:240, x:533 y:40, x:733 y:40, x:433 y:190, x:433 y:290, x:333 y:40, x:157 y:40, x:333 y:390, x:133 y:390, x:686 y:592, x:533 y:390, x:737 y:611, x:752 y:572
		_sm_navigate_0 = ConcurrencyContainer(outcomes=['finished', 'failed', 'preempt'], input_keys=['plan', 'null_path'], conditions=[
										('finished', [('Start DWA', 'done')]),
										('finished', [('Execute Pure Pursuit', 'done')]),
										('finished', [('Start SBPL', 'done')]),
										('failed', [('Start DWA', 'failed')]),
										('preempt', [('Start DWA', 'preempted')]),
										('failed', [('Execute Pure Pursuit', 'failed')]),
										('preempt', [('Execute Pure Pursuit', 'preempted')]),
										('failed', [('Start SBPL', 'failed')]),
										('preempt', [('Start SBPL', 'preempted')]),
										('failed', [('Monitor Health', 'failed')])
										])

		with _sm_navigate_0:
			# x:187 y:178
			OperatableStateMachine.add('Execute Pure Pursuit',
										FollowTopicState(planner_topic='low_level_planner/DWAPlannerROS/local_plan', controller_topic='pure_pursuit'),
										transitions={'done': 'finished', 'failed': 'failed', 'preempted': 'preempt'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off, 'preempted': Autonomy.Off})

			# x:600 y:178
			OperatableStateMachine.add('Start DWA',
										FollowTopicState(planner_topic='mid_level_planner/SBPLLatticePlanner/plan', controller_topic='low_level_planner'),
										transitions={'done': 'finished', 'failed': 'failed', 'preempted': 'preempt'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off, 'preempted': Autonomy.Off})

			# x:201 y:263
			OperatableStateMachine.add('Start SBPL',
										FollowPathState(topic='mid_level_planner'),
										transitions={'done': 'finished', 'failed': 'failed', 'preempted': 'preempt'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off, 'preempted': Autonomy.Off},
										remapping={'plan': 'plan'})

			# x:597 y:278
			OperatableStateMachine.add('Monitor Health',
										CreateStatusState(),
										transitions={'failed': 'failed'},
										autonomy={'failed': Autonomy.Off})



		with _state_machine:
			# x:191 y:50
			OperatableStateMachine.add('Get Pose',
										GetPoseState(),
										transitions={'done': 'Get Path'},
										autonomy={'done': Autonomy.Off},
										remapping={'goal': 'goal'})

			# x:191 y:177
			OperatableStateMachine.add('Get Path',
										GetPathState(planner_topic='high_level_planner'),
										transitions={'planned': 'Execute', 'empty': 'Log Empty Path', 'failed': 'Log Fail'},
										autonomy={'planned': Autonomy.Off, 'empty': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'goal': 'goal', 'plan': 'plan'})

			# x:636 y:52
			OperatableStateMachine.add('Continue',
										OperatorDecisionState(outcomes=['yes', 'no'], hint=None, suggestion=None),
										transitions={'yes': 'Get Pose', 'no': 'finished'},
										autonomy={'yes': Autonomy.Off, 'no': Autonomy.Off})

			# x:646 y:174
			OperatableStateMachine.add('Navigate',
										_sm_navigate_0,
										transitions={'finished': 'Continue', 'failed': 'Log Rerouting', 'preempt': 'Get Pose'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'preempt': Autonomy.Inherit},
										remapping={'plan': 'plan', 'null_path': 'null_path'})

			# x:406 y:181
			OperatableStateMachine.add('Execute',
										OperatorDecisionState(outcomes=['yes', 'no'], hint=None, suggestion=None),
										transitions={'yes': 'Navigate', 'no': 'Continue'},
										autonomy={'yes': Autonomy.Off, 'no': Autonomy.Off})

			# x:20 y:177
			OperatableStateMachine.add('Log Empty Path',
										LogState(text='Empty path', severity=Logger.logerr),
										transitions={'done': 'Get Pose'},
										autonomy={'done': Autonomy.Off})

			# x:198 y:269
			OperatableStateMachine.add('Log Fail',
										LogState(text='Failed to generate a path', severity=Logger.logerr),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:656 y:273
			OperatableStateMachine.add('Try Again',
										GetPathState(planner_topic='high_level_planner'),
										transitions={'planned': 'Navigate', 'empty': 'Log Empty Path', 'failed': 'failed'},
										autonomy={'planned': Autonomy.High, 'empty': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'goal': 'goal', 'plan': 'plan'})

			# x:841 y:178
			OperatableStateMachine.add('Log Rerouting',
										LogState(text='Rerouting...', severity=Logger.logerr),
										transitions={'done': 'Try Again'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]

	# [/MANUAL_FUNC]
