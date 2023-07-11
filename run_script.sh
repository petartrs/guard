#!/bin/bash
sudo apt update
sudo apt upgrade -y
sudo apt install net-tools -y
sudo apt install terminator -y

#Install and setup ROS
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
echo "source /opt/ros/noetic/setup.bash" >> /home/$USER/.bashrc
echo "source ~/catkin_ws/devel/setup.bash" >> /home/$USER/.bashrc
echo "source ~/catkin_ws/devel_isolated/setup.bash" >> /home/$USER/.bashrc
sudo apt install curl
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
sudo apt update
sudo apt install ros-noetic-desktop-full -y
source ~/.bashrc
sudo apt install python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential -y
sudo rosdep init
rosdep update
mkdir -p $HOME/catkin_ws/src
(cd $HOME/catkin_ws && catkin_make)

#Install standard ROS packages
sudo apt install ros-noetic-image-proc -y
sudo apt install ros-noetic-aruco-ros -y

#Install SDKs and non standard ROS packages from my GIT Repo
(cd $HOME/Downloads && git clone https://github.com/petartrs/guard.git)
(cd $HOME/Downloads/guard/spinnaker-3.1.0.79-amd64 && sudo sh install_spinnaker.sh)
