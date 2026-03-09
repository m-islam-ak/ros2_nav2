import os
import xacro
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_path = get_package_share_directory('robot')
    xacro_file = os.path.join(pkg_path, 'urdf', 'robot_core.urdf.xacro')

    # This processes the xacro into a valid URDF string
    robot_description_config = xacro.process_file(xacro_file)
    robot_desc = robot_description_config.toxml()

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_desc}]
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            output='screen',
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            # Tip: Add an rviz config file path here to save your view settings
        ),
    ])