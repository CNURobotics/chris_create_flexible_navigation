Chris Create Flexible Navigation
================================

CHRISLab specific implementations of the [ROS] and [FlexBE]-based [Flexible Navigation] ([Wiki]) for use with the iRobot Create.

This repository contains code that interfaces with the [CHRISLab iRobot Create] system, and the [FlexBE System] and new open-source CHRISLab [Flexible Navigation] system.

Installation and Setup
----------------------

This package has a number of dependencies.  The quickest, and easiest method to get a demonstration up and running, is to follow the [CHRISLab Installation] below.  This quickly sets up the entire CHRISLab system in a separate workspace.

1) Ensure that you are running a recent ROS version; this system is tested on `ros-kinetic-desktop-full`.  See [ROS Installation] for more information.

2) Follow the [CHRISLab Installation] guide
* This will install the entire system in a new workspace. Once you build, you can run the Gazebo simulation based demonstration described below.

3) Make sure the [FlexBE System], which will be installed as part of the [CHRISLab Installation], is properly set up.  

 This version presumes use of the [FlexBE App] for the user interface, which depends on states and behaviors that are exported as part of individual package.xml.

Operation
---------

`roscore`

`roslaunch chris_create_navigation gazebo_creech_world.launch`
 * This is a simple world with boxes and walls with the CHRISlab iRobot Create with a Hokuyo URG-04LX Lidar and a pair of web cameras

`rosrun rviz rviz`
 * Add the robot_description, maps, and laser scan as desired

`roslaunch flex_nav_create_flexbe_behaviors flex_nav_create_behavior_testing.launch`
 * This starts the FlexBE engine and FlexBE UI (Chromium App)
 * Load the `FlexPlanner` behavior

`roslaunch flex_nav_create_bringup flex.launch`
 * This starts the planning and mapping nodes.
 * This version uses a 3-layer planner as a demonstration.
  * Only a simple set of motion primitives is included in this version, and will be refined in the future.

After start up, all control is through the FlexBE UI.  Load the `FlexPlanner` behavior, and run.  The system asks for a 2D Nav Pose input via RViz, and then asks for confirmation of the initial global plan.  If the supervisor chooses to execute the plan, the state transitions to a concurrent node that uses an online multilayer planner to refine the plans as the robot moves, and also monitors the Create bumper status for collision.

[ROS]: http://www.ros.org
[FlexBE]: https://flexbe.github.io
[Flexible Navigation]: https://github.com/CNURobotics/flexible_navigation
[Wiki]: http://wiki.ros.org/flexible_navigation
[CHRISLab iRobot Create]: https://github.com/CNURobotics/chris_ros_create
[FlexBE System]: https://github.com/team-vigir/flexbe_behavior_engine
[CHRISLab Installation]: https://github.com/CNURobotics/chris_install
[FlexBE App Installation]: http://philserver.bplaced.net/fbe/download.php
[ROS Installation]: http://wiki.ros.org/kinetic/Installation
