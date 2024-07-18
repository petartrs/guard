#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import CameraInfo

def camera_info_callback(msg):
    # Modify width and height fields
    modified_msg = msg
    modified_msg.binning_x = 1  # Set your desired width
    modified_msg.binning_y = 1  # Set your desired height

    # Publish the modified camera_info to a new topic
    pub.publish(modified_msg)

if __name__ == '__main__':
    # Initialize the ROS node
    rospy.init_node('camera_info_modifier_node')

    # Set the topic names
    camera_info_topic = 'camera_info'
    modified_camera_info_topic = 'camera_info2'

    # Subscribe to the original camera_info topic
    rospy.Subscriber(camera_info_topic, CameraInfo, camera_info_callback)

    # Create a publisher for the modified camera_info
    pub = rospy.Publisher(modified_camera_info_topic, CameraInfo, queue_size=10)

    # Spin to keep the node running
    rospy.spin()
