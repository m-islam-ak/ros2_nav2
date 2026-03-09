cmake_minimum_required(VERSION 3.8)
project(robo_world)

find_package(ament_cmake REQUIRED)

# (Optional but good) dependencies for package management
find_package(rclpy REQUIRED)
find_package(geometry_msgs REQUIRED)

# Install share resources
install(
  DIRECTORY urdf launch worlds config
  DESTINATION share/${PROJECT_NAME}
)

# Install Python executable script
install(PROGRAMS
  scripts/wasd_teleop.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()