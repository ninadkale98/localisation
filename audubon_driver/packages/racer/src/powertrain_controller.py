#!/usr/bin/env python3

# Imports
import rospy
import math
from std_msgs.msg import String, Bool, Float64
from ackermann_msgs.msg import AckermannDriveStamped


gear_ratio = rospy.get_param("car_gear_ratio") # set as a rosparam
tire_circumference = rospy.get_param("tire_circumference")
max_servo_pos_in_radians = rospy.get_param("max_servo_pos_in_radians")

class MotorDriver:

    def __init__(self) -> None:
        self.wheel_radius = rospy.get_param('car_wheel_radius') # set as a rosparam
    
        self.drive_sub = rospy.Subscriber(rospy.get_param('drive_topic'), AckermannDriveStamped, self.drive_callback, queue_size=1)
        self.servo_pub = rospy.Publisher(rospy.get_param("set_servo_topic"),Float64,queue_size=1)
        self.rpm_pub = rospy.Publisher(rospy.get_param("set_rpm_topic"),Float64,queue_size=1)


    # if estop then just publish 0 speed else publish the desired rpm and servo
    def drive_callback(self, msg):
        speed = msg.drive.speed
        steer = msg.drive.steering_angle
        self.publish_rpm_and_servo(speed, -1*steer) # multiplied with -1 to follow positive CCW convention
        return


    #  takes speed and steering then converts and publishes
    def publish_rpm_and_servo(self, speed,steer):
        # make rpm and servo msg and publish
        rpm_msg = Float64()
        rpm_msg.data = speed_to_RPM(speed)
        servo_msg = Float64()
        # setting steer b/w 0 and 1
        # servo_msg.data = steer_position
        servo_msg.data = min(max(0,steer_to_servo(steer)),1)
        self.rpm_pub.publish(rpm_msg)
        self.servo_pub.publish(servo_msg)
        return

def speed_to_RPM(speed):
    wheelRPM = (speed/tire_circumference) * 60 * gear_ratio
    return wheelRPM

def steer_to_servo(steer):
    # (steer / ( max servo position in radians) )*0.5 (conver mapping -1 to 1 into -0.5 to 0.5) + 0.5 (-0.5 to 0.5 into 0 to 1)
    return (steer/max_servo_pos_in_radians)*0.5 + 0.5


if __name__ == "__main__":
    rospy.init_node("Powertrain",  anonymous=True)
    c = MotorDriver()
    rospy.spin()