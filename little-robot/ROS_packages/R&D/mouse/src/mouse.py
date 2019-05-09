#!/usr/bin/env python

"""
    telemetry movement with a pc mouse
    NB: run the code on a linux os with the super user right
"""

import struct
import rospy
from geometry_msgs.msg import Point
from std_msgs.msg import Bool

# choose the setting depending the mouse to have distance in cm
#SETTING_MOUSE = 1 # std
SETTING_MOUSE = 1/394.5 # ecam mouse

dist = [0,0,0]

def mouse_listener():
    rospy.init_node('mouse_reset', anonymous=True)
    rospy.Subscriber('curry_arrived', Bool, mouse_reset)
    rospy.spin()

def mouse_reset():
    if data.data:
        global dist
        dist = [0, 0, 0]

def mouse_talker():
    pub = rospy.Publisher('mouse_position', Point, queue_size=10)
    rospy.init_node('mouse', anonymous=True)
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        # read bites in file /dev/input/mice
        with open("/dev/input/mice","rb") as fd:
            while True:
                # unpack data to have x and y
                y,x = struct.unpack("xbb",fd.read(3))
                # correct the values with the mouse setting
                x *= SETTING_MOUSE
                y *= SETTING_MOUSE
                global dist
                # update the position of the mouse
                dist[0] += x
                dist[1] += y
                pub.publish(Point(dist[0], dist[1], dist[2]))
                rate.sleep()

if __name__ == '__main__':
    try:
        mouse_talker()
        mouse_listener()
    except rospy.ROSInterruptException:
	pass
