#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import math
import time

current_direction = 0.0  # Initialize the current direction in radians
rotation_start= False  # To track the start time of rotation
desired_orienatation = 0.0 
rotation_done = False # Duration for the desired rotation
t0 = None
i = 0

def process_command(data):
    global current_direction, rotation_start, desired_orienatation, rotation_done,t0,i
    command = data.data.lower().split()
    
    if len(command) != 2:
        rospy.logwarn("Invalid command format")
        return

    direction, value = command[0], float(command[1])


    twist = Twist()
        
    twist.linear.x = 0
    twist.linear.y = 0
    twist.linear.z = 0
    twist.angular.x = 0
    twist.angular.y = 0
    twist.angular.z = 0 

    if direction =="forward":
        if i < value:
             i= i+0.01
        twist.linear.x = i
        pub.publish(twist) 

    elif direction == "backward":
        if i < value:
            i= i+0.01
        twist.linear.x = -i
        pub.publish(twist) 

    elif direction == "left":
        desired_orienatation = value*(3.1416/180)
        if rotation_start== False and rotation_done == False:
            rotation_start= True
            t0 = rospy.Time.now().to_sec()

        if current_direction < desired_orienatation:
            twist.angular.z = 0.174 
            pub.publish(twist)
            t1 = rospy.Time.now().to_sec()
            current_direction = twist.angular.z * (t1-t0)  
            rospy.loginfo(f"cd {current_direction}; do {desired_orienatation}")            

        if current_direction >= desired_orienatation :
                twist.angular.z = 0
                pub.publish(twist)
                rotation_done = True
                rospy.loginfo(f"rotation is done of {desired_orienatation} degrees")
 
    elif direction == "right":
        desired_orienatation = value*(3.1416/180)
        if rotation_start== False:
            rotation_start= True
            t0 = rospy.Time.now().to_sec()


        if current_direction < desired_orienatation:
            twist.angular.z = -0.174
            pub.publish(twist)

            t1 = rospy.Time.now().to_sec()
            current_direction = abs(twist.angular.z) * (t1-t0)  
            rospy.loginfo(f"cd {current_direction}; do {desired_orienatation}")

        if current_direction >= desired_orienatation :
                twist.angular.z = 0
                pub.publish(twist)
                rotation_done = True
                rospy.loginfo(f"rotation is done of {desired_orienatation} degrees") 

    elif direction == "stop":
        twist.linear.x = 0
        twist.linear.y = 0
        twist.linear.z = 0
        twist.angular.x = 0
        twist.angular.y = 0
        twist.angular.z = 0 
        t1 = 0
        rotation_done = False
        rotation_start = False
        current_direction = 0
        desired_orienatation = 0          
        pub.publish(twist)



if __name__ == '__main__':
    rospy.init_node('command_processor', anonymous=True)
    pub = rospy.Publisher('/, Twist, queue_size=10)
    rospy.Subscriber('/turtlebot_cmd_vel'command', String, process_command)
    rospy.spin()
