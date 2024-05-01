# Copyright 2019 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Demo for spawn_entity.
Launches Gazebo and spawns a model
"""
# A bunch of software packages that are needed to launch ROS2
import os
import xacro
from launch_ros.descriptions import ParameterValue
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir,LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory, get_package_prefix

def generate_launch_description():

    pkg_prefix = 'phoenixbot'
    pkg_gazebo = pkg_prefix + '_gazebo'
    pkg_description = pkg_prefix + '_description'
    robot_urdf_file = 'urdf/groundbot/phoenixbot.xacro'

    use_sim_time = LaunchConfiguration('use_sim_time', default='True')

    # Use xacro to process the file
    xacro_file = os.path.join(get_package_share_directory(pkg_description),robot_urdf_file)
    robot_description_raw = xacro.process_file(xacro_file).toxml()
    pkg_path = FindPackageShare(package=pkg_description).find(pkg_description)
    urdf_model_path = os.path.join(pkg_path, robot_urdf_file)


    world_file_name = 'farm.world'

    pkg_gazebo_dir = get_package_share_directory(pkg_gazebo)
    pkg_gazebo_install_dir = get_package_prefix(pkg_gazebo)

    pkg_description_dir = get_package_share_directory(pkg_description)
    pkg_description_install_dir = get_package_prefix(pkg_description)

    # Set the GAZEBO_MODEL_PATH to include the packages's model directory
    world_models_path = os.path.join(pkg_gazebo_dir, 'models')
    robot_model_path = os.path.join(pkg_description_dir, 'models')

    if 'GAZEBO_MODEL_PATH' in os.environ:
        os.environ['GAZEBO_MODEL_PATH'] = os.environ['GAZEBO_MODEL_PATH'] + ':' + pkg_gazebo_install_dir + '/share' + ':' + world_models_path
        os.environ['GAZEBO_MODEL_PATH'] = os.environ['GAZEBO_MODEL_PATH'] + ':' + pkg_description_install_dir + '/share' + ':' + robot_model_path
    else:
        os.environ['GAZEBO_MODEL_PATH'] = pkg_gazebo_install_dir + '/share' + ':' + world_models_path
        os.environ['GAZEBO_MODEL_PATH'] = os.environ['GAZEBO_MODEL_PATH'] + ':' + pkg_description_install_dir + '/share' + ':' + robot_model_path


    print("GAZEBO_MODEL_PATH=="+str(os.environ["GAZEBO_MODEL_PATH"]))


    world = os.path.join(pkg_gazebo_dir, 'worlds', world_file_name)
    launch_file_dir = os.path.join(pkg_gazebo_dir, 'launch')

    start_gazebo = ExecuteProcess(
            cmd=['gazebo', '--verbose', world, '-s', 'libgazebo_ros_init.so', 
            '-s', 'libgazebo_ros_factory.so'],
            output='screen')


    robot_description_config = ParameterValue(Command(['xacro ', urdf_model_path, ' sim_mode:=', use_sim_time]), value_type=str)
    params = {'robot_description': robot_description_config, 'use_sim_time': use_sim_time}

    start_robot_state_pub =  Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[params]
    )
    
    
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        output='screen',
        arguments=['-topic', 'robot_description',
                   '-entity', pkg_prefix,
                   '-x', '7.03', '-y', '-1.40', '-z', '0.0',
                   '-Y', '-3.04']
    )

    start_rviz = Node(
        package='rviz2',
        namespace='',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', [os.path.join(pkg_gazebo_dir, 'config', 'rviz/config.rviz')]]
    )

    return LaunchDescription([
        start_gazebo,
        start_robot_state_pub,
        spawn_entity,
        start_rviz
    ])