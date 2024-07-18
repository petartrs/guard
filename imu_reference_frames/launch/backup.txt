#!/usr/bin/env python3  
import rospy
import tf2_ros
import geometry_msgs.msg
import math
from sensor_msgs.msg import Imu
from fiducial_msgs.msg import FiducialTransformArray
from geometry_msgs.msg import Transform
from tf.transformations import euler_from_quaternion
from tf.transformations import quaternion_from_euler
from math import degrees, radians
global quaternion_imu 

quaternion_imu = [0, 0, 0, 0]


def create_transform(parent_frame_id, child_frame_id, translation, rotation):
	t = geometry_msgs.msg.TransformStamped()
	t.header.stamp = rospy.Time.now()
	t.header.frame_id = parent_frame_id
	t.child_frame_id = child_frame_id
	t.transform.translation.x = translation[0]
	t.transform.translation.y = translation[1]
	t.transform.translation.z = translation[2]
	t.transform.rotation.x = rotation[0]
	t.transform.rotation.y = rotation[1]
	t.transform.rotation.z = rotation[2]
	t.transform.rotation.w = rotation[3]
	return t


def imu_callback(data, br):
	rotation = data.orientation
	global quaternion_imu

	
	#extract quaternion from imu measurements
	quaternion = (rotation.x, rotation.y, rotation.z, rotation.w)
	quaternion_imu = quaternion
	
	#convert the imu quaternion to roll, pitch and yaw between imu and earth
	roll, pitch, yaw = euler_from_quaternion(quaternion_imu)
	
	#calculate back quaternion that is used for dynamic rotation just around the yaw axis (z-axis)
	roll_degrees = 0
	pitch_degrees = 0
	yaw_degrees = degrees(yaw)
	quaternion_yaw = quaternion_from_euler(radians(roll_degrees), radians(pitch_degrees), radians(yaw_degrees))
	
	#Dynamic transformations between the frames. 
	#First we create imu frame which is child of imu_flat frame.
	#Then camera frame is created which is child of imu frame.
	#Finally we created another frame which is in roll and pitch always flat but it rotates around yaw axis 
	transform1 = create_transform("imu_flat", "imu", [0, 0.0, 0.0], [quaternion_imu[0], quaternion_imu[1], quaternion_imu[2],quaternion_imu[3]])
	br.sendTransform(transform1)
	
	transform2 = create_transform("imu", "camera_right", [0.055, 0.0, 0.0], [0, 0, 0.707, 0.707])
	br.sendTransform(transform2)

	transform3 = create_transform("imu_flat", "imu_flat_yaw", [0.0, 0.0, 0.0], [quaternion_yaw[0], quaternion_yaw[1], quaternion_yaw[2],quaternion_yaw[3]])
	br.sendTransform(transform3)
	
	transform4 = create_transform("imu_flat_yaw", "CGT50", [-0.5, 0.0, -0.3], [0,0,0,1])
	br.sendTransform(transform4)
	
    
	
def imu_transform_broadcaster():
	rospy.init_node('imu_transform_broadcaster', anonymous=True)
	br = tf2_ros.TransformBroadcaster()
	rospy.Subscriber("vectornav/IMU", Imu, imu_callback, br)
	rospy.spin()

if __name__ == '__main__':
    try:
        imu_transform_broadcaster()
    except rospy.ROSInterruptException:
        pass
