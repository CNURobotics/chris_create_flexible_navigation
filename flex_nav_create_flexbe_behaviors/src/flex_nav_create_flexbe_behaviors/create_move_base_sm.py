#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flex_nav_flexbe_states.get_pose_state import GetPoseState
from flex_nav_flexbe_states.get_path_state import GetPathState
from flex_nav_flexbe_states.follow_path_state import FollowPathState
from flex_nav_flexbe_states.clear_costmaps_state import ClearCostmapsState
from flex_nav_flexbe_states.rotate_angle_state import RotateAngleState
from flexbe_states.operator_decision_state import OperatorDecisionState
from flexbe_states.log_state import LogState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Aug 19 2016
@author: Justin Willis
'''
class CreateMoveBaseSM(Behavior):
    '''
    A drop in replacement for move_base that works with CHRISLab Flexible Navigation system and iRobot Create
    '''


    def __init__(self):
        super(CreateMoveBaseSM, self).__init__()
        self.name = 'Create Move Base'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]

		# [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:175 y:115, x:629 y:210
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]

		# [/MANUAL_CREATE]


        with _state_machine:
            # x:56 y:20
            OperatableStateMachine.add('Get Pose',
                                        GetPoseState(topic='/move_base_simple/goal'),
                                        transitions={'done': 'Global Planner'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'goal': 'goal'})

            # x:52 y:155
            OperatableStateMachine.add('Global Planner',
                                        GetPathState(planner_topic='global_planner'),
                                        transitions={'planned': 'Local Planner', 'empty': 'Log Fail', 'failed': 'Log Fail'},
                                        autonomy={'planned': Autonomy.Off, 'empty': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'goal': 'goal', 'plan': 'plan'})

            # x:251 y:155
            OperatableStateMachine.add('Local Planner',
                                        FollowPathState(topic='local_planner'),
                                        transitions={'done': 'Continue', 'failed': 'Log Fail', 'preempted': 'Continue'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off, 'preempted': Autonomy.Off},
                                        remapping={'plan': 'plan'})

            # x:441 y:128
            OperatableStateMachine.add('Clear Costmaps',
                                        ClearCostmapsState(costmap_topics=['global_planner/clear_costmap','local_planner/clear_costmap']),
                                        transitions={'done': 'Rotate Recovery', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

            # x:448 y:28
            OperatableStateMachine.add('Rotate Recovery',
                                        RotateAngleState(target_time=5.0, cmd_topic='/create_node/cmd_vel', odometry_topic='/create_node/odom'),
                                        transitions={'done': 'Get Pose'},
                                        autonomy={'done': Autonomy.Off})

            # x:237 y:59
            OperatableStateMachine.add('Continue',
                                        OperatorDecisionState(outcomes=['yes', 'no'], hint=None, suggestion=None),
                                        transitions={'yes': 'Get Pose', 'no': 'finished'},
                                        autonomy={'yes': Autonomy.Off, 'no': Autonomy.Off})

            # x:167 y:270
            OperatableStateMachine.add('Log Fail',
                                        LogState(text='Navigation failed!', severity=Logger.logerr),
                                        transitions={'done': 'Autonomy'},
                                        autonomy={'done': Autonomy.Off})

            # x:437 y:272
            OperatableStateMachine.add('Autonomy',
                                        OperatorDecisionState(outcomes=['yes', 'no'], hint=None, suggestion='yes'),
                                        transitions={'yes': 'Clear Costmaps', 'no': 'failed'},
                                        autonomy={'yes': Autonomy.High, 'no': Autonomy.Off})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]

	# [/MANUAL_FUNC]
