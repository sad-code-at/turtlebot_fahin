#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

def process_command(data):
    command = data.data.lower().split()
    
    if len(command) != 2:
        rospy.logwarn("Invalid command format")
        return

    direction, speed = command[0], float(command[1])
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

    twist = Twist()

    if direction =="forward":
        twist.linear.x = speed
    elif direction == "backward":
        twist.linear.x = -speed
    elif direction == "left":
        twist.linear.y = speed
    elif direction == "right":
        twist.linear.y = -speed
    elif direction == "stop":
        twist.linear.x = 0
        twist.linear.y = 0

    pub.publish(twist)

def listener():
    rospy.init_node('command_processor', anonymous=True)
    rospy.Subscriber('/turtlebot_command', String, process_command)
    rospy.spin()

if __name__ == '__main__':
    listener()
