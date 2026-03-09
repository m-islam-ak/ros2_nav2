from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    teleop = Node(
        package="robo_world",
        executable="wasd_teleop.py",
        name="wasd_teleop",
        output="screen",
        emulate_tty=True,
        prefix=["xterm", "-e", "bash", "-lc"],  # important: use a shell
        parameters=[
            {"cmd_vel_topic": "/cmd_vel"},
            {"linear_speed": 0.25},
            {"angular_speed": 1.0},
            {"deadman_timeout": 0.25},
        ],
    )

    return LaunchDescription([
        # ... your existing gazebo/spawn nodes ...
        teleop,
    ])