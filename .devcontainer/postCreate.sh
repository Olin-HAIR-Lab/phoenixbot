#!/bin/bash
# mkdir -p src
# cd /home/ros2_ws
sudo rosdep update
sudo rosdep install --from-paths /home/ros2_ws --ignore-src -y
sudo chown -R $(whoami) /home/ros2_ws/
cd /home/ros2_ws/ || exit
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
