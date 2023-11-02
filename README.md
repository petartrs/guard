# guard

Repository related to ArUco based drone landing for DTIF GUARD project [![alt text]((https://theguardproject.com/about/) "Project Website")]

1. Install Ubuntu 20.04
2. Run $sudo apt-get update
3. Run $sudo apt-get upgrade
4. Download and Run script run_script.sh using $bash runscript.sh . NOTE do not run it as SUDO.  This will install ROS noetic, all necessary packages and SDK for FLIR camera and Inertial Labs INS, and update GCC compiler so you can install Guest 
5. Connect INS with the PC using USB-Serial converter
6. If working in a virtual machine e.g. VirtualBox, under Settings/USB add USB-Serial converter so it is visible in Ubuntu
7. Run $chmod -R 777 /dev/ttyUSB0 (or whatever USB port it is connected to. You can check that with $dmesg | grep tty ). This will allow for USB-Serial converter read/write permissions
