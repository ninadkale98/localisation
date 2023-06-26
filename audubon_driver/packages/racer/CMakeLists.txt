cmake_minimum_required(VERSION 3.0.2)
project(racer)


set(CMAKE_CXX_STANDARD 14)
set(vesc_ackermann_DIR ../../install/share/vesc_ackermann/cmake)
set(vesc_msgs_DIR ../../install/share/vesc_msgs/cmake)
set(vesc_driver_DIR ../../install/share/vesc_driver/cmake)

find_package(catkin REQUIRED COMPONENTS
        roscpp
        ackermann_msgs
        geometry_msgs
        nav_msgs
        std_msgs
        tf
        vesc_msgs
        vesc_ackermann
        vesc_driver
        )

catkin_package(
        CATKIN_DEPENDS
        roscpp
        ackermann_msgs
        geometry_msgs
        nav_msgs
        std_msgs
        tf
        vesc_msgs
        vesc_ackermann
        vesc_driver
)

include_directories(include ${catkin_INCLUDE_DIRS})

# add_library(racer_libs
#         src/robot_core/control/PID/controller.h
#         src/robot_core/control/PID/controller.cpp
#         src/robot_core/control/core/motor_driver.cpp
#         src/robot_core/control/core/motor_driver.h
#         src/robot_core/control/core/power_accumulator.cpp
#         src/robot_core/control/core/power_accumulator.h
#         )

# add_executable(
#         rmotor_driver
#         src/motor_driver.cpp
# )
# add_executable(
#         controller
#         src/controller.cpp
# )


