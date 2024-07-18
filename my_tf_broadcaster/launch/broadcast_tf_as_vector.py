#!/usr/bin/env python3

import rospy
import tf2_ros
from geometry_msgs.msg import PoseStamped, TransformStamped, Vector3Stamped

# Known relative position of aruco_10 compared to aruco_26
RELATIVE_POSITION_ARUCO_10_TO_ARUCO_26 = {'x': 0, 'y': 0.155, 'z': 0}

def instance2_pose_callback(msg):
    # You can process the pose message here if needed, but you don't need to publish it.
    rospy.loginfo("Received /instance2/pose: %s", msg.pose)


def main():
    rospy.init_node('broadcast_tf_as_vector')
    tfBuffer = tf2_ros.Buffer(rospy.Duration(0.1))
    listener = tf2_ros.TransformListener(tfBuffer)
    vector_pub = rospy.Publisher('tf_vector', Vector3Stamped, queue_size=10)
    
     # Subscribe to the /instance1/pose/ and instance2/pose topics
    rospy.Subscriber('/instance2/pose', PoseStamped, instance2_pose_callback)
    rospy.Subscriber('/instance1/pose', PoseStamped, instance2_pose_callback)
  
    
    rate = rospy.Rate(10.0)  # 10 Hz

    while not rospy.is_shutdown():
        transform_acquired = False
        
        if tfBuffer.can_transform('imu_flat_yaw', 'aruco_26', rospy.Time(0), rospy.Duration(0.1)):
        
            try:
                transformStamped = tfBuffer.lookup_transform('imu_flat_yaw', 'aruco_26', rospy.Time(0))
                vector_msg = Vector3Stamped()
                vector_msg.header.stamp = rospy.Time.now()
                vector_msg.header.frame_id = 'imu_flat_yaw'
                # multiply by 10 to transform from metres to dm
                vector_msg.vector.x = transformStamped.transform.translation.x*10
                vector_msg.vector.y = transformStamped.transform.translation.y*10
                vector_msg.vector.z = transformStamped.transform.translation.z*10
                vector_pub.publish(vector_msg)
                transform_acquired = True

            except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
                rospy.logwarn(e)

        if not  transform_acquired and tfBuffer.can_transform('imu_flat_yaw', 'aruco_10', rospy.Time(0), rospy.Duration(0.1)):
            try:
                transformStamped = tfBuffer.lookup_transform('imu_flat_yaw', 'aruco_10', rospy.Time(0))
                vector_msg = Vector3Stamped()
                vector_msg.header.stamp = rospy.Time.now()
                vector_msg.header.frame_id = 'imu_flat_yaw'
                # multiply by 10 to transform from metres to dm
                vector_msg.vector.x = (transformStamped.transform.translation.x + RELATIVE_POSITION_ARUCO_10_TO_ARUCO_26['x'])*10
                vector_msg.vector.y = (transformStamped.transform.translation.y + RELATIVE_POSITION_ARUCO_10_TO_ARUCO_26['y'])*10
                vector_msg.vector.z = (transformStamped.transform.translation.z + RELATIVE_POSITION_ARUCO_10_TO_ARUCO_26['z'])*10
                vector_pub.publish(vector_msg)
                transform_acquired = True

            except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
                rospy.logwarn(e)
        if not transform_acquired:
            rospy.logwarn("Neither transform from imu_flat_yaw to aruco_26 nor aruco_10 available")        


        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
