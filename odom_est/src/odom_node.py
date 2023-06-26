#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from vesc_msgs.msg import VescStateStamped
import numpy as np
import tf
from geometry_msgs.msg import Quaternion, Pose, Point, Twist


initial_yaw_updated = False
yaw = 0.0
initial_yaw = 0.0
curr_speed = 0.0
speed_offset = 0
speed_gain = -4300.0
x = 0.0
y = 0.0
prev_time = 0.0

def imu_callback(data):
    global initial_yaw_updated, yaw ,x, y,prev_time, initial_yaw

    if not initial_yaw_updated:
        initial_yaw_updated = True
        orientation = data.orientation
        euler = tf.transformations.euler_from_quaternion([orientation.x, orientation.y, orientation.z, orientation.w])
        initial_yaw = euler[2]
        prev_time = rospy.Time.now()
        return
    
    orientation = data.orientation
    euler = tf.transformations.euler_from_quaternion([orientation.x, orientation.y, orientation.z, orientation.w])
    yaw = euler[2] - initial_yaw

    xdot = curr_speed * np.cos(yaw)
    ydot = curr_speed * np.sin(yaw)
    
    curr_time = rospy.Time.now()
    dt = (curr_time - prev_time).to_sec()
    prev_time = curr_time

    x += xdot*dt
    y += ydot*dt

    # Create a new Odometry message
    odom_msg = Odometry()

    # Set the header information
    odom_msg.header.stamp = rospy.Time.now()
    odom_msg.header.frame_id = "odom"
    odom_msg.child_frame_id = "base_link"

    # Set the position of the car
    odom_msg.pose.pose.position.x = np.round(x , decimals=4)
    odom_msg.pose.pose.position.y = np.round(x , decimals=4)
    odom_msg.pose.pose.position.z = 0.0

    # Convert the yaw angle to a Quaternion and set the orientation
    quaternion = Quaternion()
    quaternion.z = np.sin(yaw / 2.0)
    quaternion.w = np.cos(yaw / 2.0)
    odom_msg.pose.pose.orientation = quaternion

    # Set the linear and angular velocities
    odom_msg.twist.twist = Twist()

    # Publish the Odometry message
    odom_publisher.publish(odom_msg)

def vesc_callback(data):
    global curr_speed 
    # Get the speed from the VESC sensor/core data
    curr_speed = ( data.state.speed - speed_offset ) / speed_gain


if __name__ == '__main__':
    try:
        rospy.init_node('imu_to_odom', anonymous=True)

        # Create a subscriber for the IMU topic
        imu_subscriber = rospy.Subscriber('imu_data', Imu, imu_callback)

        # Create a subscriber to VESC topic
        vesc_subscriber = rospy.Subscriber('sensors/core', VescStateStamped, vesc_callback)


        # Create a publisher for the Odometry topic
        odom_publisher = rospy.Publisher('odom_est', Odometry, queue_size=10)

        # Start the main ROS loop
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
