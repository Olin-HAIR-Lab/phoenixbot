# Phoenixbot (Olin College's Sustainable Agricultural Robot Platform)

The Phoenixbot is [Olin College's](https://www.olin.edu/) first sustainable agricultural robot platform, developed my students and faculty. The robot platform is addressing the need for sustainable, ecological weed management strategies for healthier and more sustainable agriculture. It is designed on the [farm-ng Amiga micro tractor platform](https://farm-ng.com/products/la-maquina-amiga).

<img src="media/phoenixbot_demo.gif" width="1000">

<br>

## Repository Summary
- [```phoenixbot_description```](https://github.com/Olin-HAIR-Lab/phoenixbot/tree/main/phoenixbot_description): contains the URDF description files for the phoenixbot, sensors, etc.

- [```phoenixbot_gazebo```](https://github.com/Olin-HAIR-Lab/phoenixbot/tree/main/phoenixbot_gazebo): contains model, world, launch and configuration files to simulate the phoenixbot in Gazebo.

<br>

## Installation
This system was tested on Ubuntu 22.04 LTS and ROS2 Humble.

#### 1. Create your ROS2 workspace and clone the repository
```
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/Olin-HAIR-Lab/phoenixbot.git 
```

#### 2. Install all the relevant ROS dependencies
```
cd ~/ros2_ws
sudo rosdep init
rosdep update
rosdep install --from-paths src --ignore-src --rosdistro humble -r -y
```

#### 3. Source the ROS installation and workspace overlay (do only once)
```
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc

source ~/.bashrc
```

#### 3. Build the package(s)
```
# navigate to the root of the workspace and build the packages
cd ~/ros2_ws
colcon build --symlink-install
```

<br>

## How to Run

#### Start the Gazebo simulation
```
ros2 launch phoenixbot_gazebo gazebo_world.launch.py
```
NOTE: It may take a few minutes to come up the first time around, so please be patient.

If everything has been installed correctly, you should see Gazebo and Rviz windows open as below:

![bringup view](media/bringup.png)


#### Move the robot using keyboard teleoperation
```
# first, install the dependency
sudo apt install ros-humble-teleop-twist-keyboard

# run the command in a new terminal
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Control the robot with the keyboard keys as below:

![teleop keyboard keys](media/teleop_controls.png)



