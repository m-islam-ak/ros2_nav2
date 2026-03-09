#!/usr/bin/env python3
import sys
import select
import termios
import tty

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


HELP = """
WASD Teleop (ROS 2)
-------------------
W: Forward
S: Backward
A: Turn Left
D: Turn Right

R/F : Increase/Decrease Linear Speed
T/G : Increase/Decrease Angular Speed

SPACE or X : Stop
CTRL+C : Quit
"""


class WASDTeleop(Node):

    def __init__(self):
        super().__init__('wasd_teleop')

        # Parameters
        self.declare_parameter('cmd_vel_topic', '/cmd_vel')
        self.declare_parameter('linear_speed', 0.3)
        self.declare_parameter('angular_speed', 1.0)
        self.declare_parameter('linear_step', 0.05)
        self.declare_parameter('angular_step', 0.1)
        self.declare_parameter('publish_rate', 20.0)

        self.cmd_topic = self.get_parameter('cmd_vel_topic').value
        self.linear_speed = self.get_parameter('linear_speed').value
        self.angular_speed = self.get_parameter('angular_speed').value
        self.linear_step = self.get_parameter('linear_step').value
        self.angular_step = self.get_parameter('angular_step').value
        self.rate = self.get_parameter('publish_rate').value

        self.publisher = self.create_publisher(Twist, self.cmd_topic, 10)

        self.vx = 0.0
        self.wz = 0.0

        self.timer = self.create_timer(1.0 / self.rate, self.publish_cmd)

        self.get_logger().info(f"Publishing to {self.cmd_topic}")
        self.get_logger().info(HELP)
        self.print_speeds()

    def publish_cmd(self):
        msg = Twist()
        msg.linear.x = float(self.vx)
        msg.angular.z = float(self.wz)
        self.publisher.publish(msg)

    def print_speeds(self):
        self.get_logger().info(
            f"Current Speeds -> Linear: {self.linear_speed:.2f} m/s | "
            f"Angular: {self.angular_speed:.2f} rad/s"
        )

    def handle_key(self, key):

        # Movement
        if key in ['w', 'W']:
            self.vx = self.linear_speed
            self.wz = 0.0

        elif key in ['s', 'S']:
            self.vx = -self.linear_speed
            self.wz = 0.0

        elif key in ['a', 'A']:
            self.vx = 0.0
            self.wz = self.angular_speed

        elif key in ['d', 'D']:
            self.vx = 0.0
            self.wz = -self.angular_speed

        # Stop
        elif key in [' ', 'x', 'X']:
            self.vx = 0.0
            self.wz = 0.0

        # Linear speed adjust
        elif key in ['r', 'R']:
            self.linear_speed += self.linear_step
            self.print_speeds()

        elif key in ['f', 'F']:
            self.linear_speed = max(0.0, self.linear_speed - self.linear_step)
            self.print_speeds()

        # Angular speed adjust
        elif key in ['t', 'T']:
            self.angular_speed += self.angular_step
            self.print_speeds()

        elif key in ['g', 'G']:
            self.angular_speed = max(0.0, self.angular_speed - self.angular_step)
            self.print_speeds()

        elif key in ['h', 'H']:
            self.get_logger().info(HELP)


def get_key(timeout=0.05):
    dr, _, _ = select.select([sys.stdin], [], [], timeout)
    if dr:
        return sys.stdin.read(1)
    return ''


def main():
    settings = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin.fileno())

    rclpy.init()
    node = WASDTeleop()

    try:
        while rclpy.ok():
            key = get_key()
            if key == '\x03':
                break
            if key:
                node.handle_key(key)
            rclpy.spin_once(node, timeout_sec=0.0)

    finally:
        node.vx = 0.0
        node.wz = 0.0
        node.publish_cmd()

        node.destroy_node()
        rclpy.shutdown()
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)


if __name__ == '__main__':
    main()