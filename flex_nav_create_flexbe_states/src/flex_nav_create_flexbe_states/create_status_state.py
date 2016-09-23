#!/usr/bin/env python

###############################################################################
#  Copyright (c) 2016
#  Capable Humanitarian Robotics and Intelligent Systems Lab (CHRISLab)
#  Christopher Newport University
#
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#    3. Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
#       THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#       "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#       LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#       FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#       COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#       INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
#       BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#       LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#       CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#       LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
#       WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#       POSSIBILITY OF SUCH DAMAGE.
###############################################################################

import rospy

from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxySubscriberCached

from chris_create_node.msg import CreateSensorState

class CreateStatusState(EventState):
    """
    The state monitors the iRobot Create bumper status, and stops and returns a
    failed outcome if a bumper is activated.

    <= failed    A bumper was activated prior to completion
    """

    def __init__(self):
        super(CreateStatusState, self).__init__(outcomes = ['failed'])

        self._sensor_topic = '/create_node/sensor_state'
        self._sensor_sub   = ProxySubscriberCached({self._sensor_topic: CreateSensorState})

    def execute(self, userdata):
        if (self._sensor_sub.has_msg(self._sensor_topic)):
            sensors = self._sub.get_last_msg(self._sensor_topic)
            if ((sensors.bumps_wheeldrops > 0) or sensors.cliff_left or sensors.cliff_front_left or sensors.cliff_front_right or sensors.cliff_right):
                Logger.logwarn('Bumper contact = %d  cliff: left=%d %d %d %d = right ' %
                        (sensors.bumps_wheeldrops, sensors.cliff_left, sensors.cliff_front_left,sensors.cliff_front_right, sensors.cliff_right))
                return 'failed'
