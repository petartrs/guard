# guard

Repository related to ArUco based drone landing for DTIF GUARD project [![alt text]((https://theguardproject.com/about/) "Project Website")]

1. Install Ubuntu 20.04
2. Download and Run script run_scipt.sh using $bash runscript.sh . NOTE do not run it as SUDO.  This will install ROS noetic, all necessary packages and SDK for FLIR camera and Inertial Labs INS, and update GCC compiler so you can install Guest 
3. Connect INS with the PC using USB-Serial converter
4. If working in a virtual machine e.g. VirtualBox, under Settings/USB add USB-Serial converter so it is visible in Ubuntu
5. Run $chmod -R 777 /dev/ttyUSB0 (or whatever USB port it is connected to. You can check that with $dmesg | grep tty ). This will allow for USB-Serial converter read/write permissions
