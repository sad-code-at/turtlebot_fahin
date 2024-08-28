#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

def command_input():
    rospy.init_node('command_node', anonymous=True)
    pub = rospy.Publisher('/turtlebot_command', String, queue_size=1)
    
    def shutdown_hook():
        rospy.loginfo("Node is shutting down. Publishing 'stop 0' message.")
        pub.publish("stop 0")
        rospy.sleep(1)  # Give time to publish the message before shutdown

    rospy.on_shutdown(shutdown_hook)

    rate = rospy.Rate(10)
    command = input("Enter command (e.g., 'Move 5', 'Left 1'): ")
    
    while not rospy.is_shutdown():
        pub.publish(command)
        rate.sleep()

if __name__ == '__main__':
    try:
        command_input()
    except rospy.ROSInterruptException:
        pass
