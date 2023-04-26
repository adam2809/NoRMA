#!/usr/bin/env python3
# license removed for brevity

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from math import radians, degrees
from actionlib_msgs.msg import *
from geometry_msgs.msg import PoseStamped,Point

class Navigator:
    def __init__(self):
        rospy.init_node("navigator")
        self.moveToGoal()

    def moveToGoal(self):
        xGoal = 0
        yGoal = 0

        ac = actionlib.SimpleActionClient("/move_base", MoveBaseAction)

        #wait for the action server to come up
        while(not ac.wait_for_server(rospy.Duration.from_sec(5.0))):
                rospy.loginfo("Waiting for the move_base action server to come up")


        goal = MoveBaseGoal()

        #set up the frame parameters
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()

        # moving towards the goal*/

        goal.target_pose.pose.position =  Point(xGoal,yGoal,0)
        goal.target_pose.pose.orientation.x = 0.0
        goal.target_pose.pose.orientation.y = 0.0
        goal.target_pose.pose.orientation.z = 0.0
        goal.target_pose.pose.orientation.w = 1.0

        rospy.loginfo("Sending goal location ...")
        ac.send_goal(goal)

        rospy.loginfo("Moving to goal")
        ac.wait_for_result(rospy.Duration(60))

        if(ac.get_state() ==  GoalStatus.SUCCEEDED):
                rospy.loginfo("You have reached the destination")
                return True

        else:
                rospy.loginfo("The robot failed to reach the destination")
                return False

if __name__ == '__main__':
    try:
        myNav = Navigator()
        rospy.spin()
    except rospy.ROSInterruptException:
       print('killed process')

