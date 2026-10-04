"""Expand Xacro and display the robot with joint controls and TF in RViz."""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro


def generate_launch_description():
    package_path = get_package_share_directory('robot_description')
    model_path = os.path.join(package_path, 'urdf', 'robot.urdf.xacro')
    robot_xml = xacro.process_file(model_path).toxml()
    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{'robot_description': robot_xml}],
            output='screen',
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            parameters=[{'robot_description': robot_xml}],
            output='screen',
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', os.path.join(package_path, 'rviz', 'display.rviz')],
            output='screen',
        ),
    ])

