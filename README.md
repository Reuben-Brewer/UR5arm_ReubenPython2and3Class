###########################

UR5arm_ReubenPython2and3Class

Code (including ability to hook to Tkinter GUI) to control Universal Robotics UR5 robot arm (with Controller Box 2 or 3).
Code has NOT been tested on the newer "E"-series UR5e.
However, the code should work for the most part on other sizes of arm (e.g. UR10, UR16, etc.)

Reuben Brewer, Ph.D.

reuben.brewer@gmail.com

www.reubotics.com

Apache 2 License

Software Revision E, 05/10/2023

UR5arm_ReubenPython2and3Class.py, test_program_for_UR5arm_ReubenPython2and3Class.py, and Teleop_UR5arm.py verified working on:

Python 3.8.

Windows 8.1, 10 64-bit

Ubuntu 20.04

Raspberry Pi Buster 

(no Mac testing yet)

NOTE: When commanding position in Tool/cartesian space via the function PositionControl_ServoJ_MoveThroughListOfPoses (using "PoseIsInToolSpaceFlag" = 1),
the UR5 is performing inverse-kinematics internally. If the desired TCP pose is one where the arm could achieve it via multiple sets of joint-angles
(like "elbow-left" vs "elbow-right"), then the arm would normally feak-out and attempt to make a sudden, large motion as it tries to switch between different joint-angle configurations.
For now, I allow the user to specify a maximum joint-angle-distance to travel in a given step, and the arm will refuse to move if it's going to exceed that max distance.
In the future, I plan to add the ability for the user to specify "elbow-left" vs "elbow-right".
When commanding only joint-angles via PositionControl_ServoJ_MoveThroughListOfPoses (using "PoseIsInToolSpaceFlag" = 0), this isn't an issue.

###########################

########################### Python module installation instructions, all OS's

-----

UR5arm_ReubenPython2and3Class, ListOfModuleDependencies: ['future.builtins', 'numpy', 'scipy.spatial.transform']
UR5arm_ReubenPython2and3Class, ListOfModuleDependencies_TestProgram: ['MyPrint_ReubenPython2and3Class']
UR5arm_ReubenPython2and3Class, ListOfModuleDependencies_NestedLayers: ['future.builtins']
UR5arm_ReubenPython2and3Class, ListOfModuleDependencies_All:['future.builtins', 'MyPrint_ReubenPython2and3Class', 'numpy', 'scipy.spatial.transform']

-----

-----

Teleop_UR5arm.py run via command:

sudo ./Launch_Teleop_UR5arm_Admin.sh

(if this script fails, then try "sudo chmod 777 Launch_Teleop_UR5arm_Admin.sh" and "sudo dos2unix Launch_Teleop_UR5arm_Admin.sh")

or

sudo python Teleop_UR5arm.py "software_launch_method":"BATfile"

(In Ubuntu, may need to run as sudo to get the keyboard module to work properly. Definitely need to run as sudo to get the ftd2xx module to work.)

Teleop_UR5arm.py, ListOfModuleDependencies: ['ArucoTagDetectionFromCameraFeed_ReubenPython3Class', 'GetPIDsByProcessEnglishNameAndOptionallyKill_ReubenPython2and3', 'JoystickHID_ReubenPython2and3Class', 'keyboard', 'LowPassFilter_ReubenPython2and3Class', 'MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class', 'MyPrint_ReubenPython2and3Class', 'numpy', 'RobotiqGripper2F85_ReubenPython2and3Class', 'scipy.spatial.transform', 'SharedGlobals_Teleop_UR5arm', 'UR5arm_ReubenPython2and3Class', 'ZEDasHandController_ReubenPython2and3Class']

Teleop_UR5arm.py, ListOfModuleDependencies_TestProgram: []

Teleop_UR5arm.py, ListOfModuleDependencies_NestedLayers: ['CameraStreamerClass_ReubenPython2and3Class', 'cv2', 'ftd2xx', 'future.builtins', 'Joystick2DdotDisplay_ReubenPython2and3Class', 'LowPassFilter_ReubenPython2and3Class', 'LowPassFilterForDictsOfLists_ReubenPython2and3Class', 'numpy', 'pexpect', 'psutil', 'pygame', 'pyzed.sl', 'scipy.spatial.transform', 'serial', 'serial.tools']

Teleop_UR5arm.py, ListOfModuleDependencies_All:['ArucoTagDetectionFromCameraFeed_ReubenPython3Class', 'CameraStreamerClass_ReubenPython2and3Class', 'cv2', 'ftd2xx', 'future.builtins', 'GetPIDsByProcessEnglishNameAndOptionallyKill_ReubenPython2and3', 'Joystick2DdotDisplay_ReubenPython2and3Class', 'JoystickHID_ReubenPython2and3Class', 'keyboard', 'LowPassFilter_ReubenPython2and3Class', 'LowPassFilterForDictsOfLists_ReubenPython2and3Class', 'MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class', 'MyPrint_ReubenPython2and3Class', 'numpy', 'pexpect', 'psutil', 'pygame', 'pyzed.sl', 'RobotiqGripper2F85_ReubenPython2and3Class', 'scipy.spatial.transform', 'serial', 'serial.tools', 'SharedGlobals_Teleop_UR5arm', 'UR5arm_ReubenPython2and3Class', 'ZEDasHandController_ReubenPython2and3Class']

sudo apt-get install python3-tk (only if there's an error about tkinter not being found)

pip install pygame

pip install keyboard

pip install pyserial

pip install ftd2xx #PROBABLY SKIP THIS IN UBUNTU AS IT'S VERY PAINFUL AND BUGGY

-- Install pyzed module

Ubuntu: cd "/usr/local/zed/"

Windows: cd "C:\Program Files (x86)\ZED SDK\"

Make sure you have admin access to run it in the Program Files folder, otherwise, you will have a Permission denied error.

You can still copy the file into another location to run it without permissions.

python get_python_api.py

--

-----

-----

ExcelPlot_CSVfileForTrajectoryData.py, ListOfModuleDependencies_All:['pandas', 'win32com.client', 'xlrd', 'xlsxwriter', 'xlutils.copy', 'xlwt']

-----


###########################

########################### ftd2xx installation instructions on Ubuntu (a very painful and buggy process which you might want to skip)

https://ftdichip.com/wp-content/uploads/2020/08/AN_220_FTDI_Drivers_Installation_Guide_for_Linux-1.pdf

https://ftdichip.com/drivers/d2xx-drivers/

https://ftdichip.com/wp-content/uploads/2022/07/libftd2xx-x86_64-1.4.27.tgz

sudo rmmod ftdi_sio #MIGHT HAVE TO DO THIS AFTER REBOOT

sudo rmmod usbserial #MIGHT HAVE TO DO THIS AFTER REBOOT

extract libftd2xx-x86_64-1.4.27.tgz #will put "release" folder onto the Desktop

sudo chmod 777 -R ~/Desktop/

sudo cp release/build/lib* /usr/local/lib

cd /usr/local/lib

sudo ln -s libftd2xx.so.1.4.27 libftd2xx.so

sudo chmod 0755 libftd2xx.so.1.4.27

sudo ldconfig #otherwise can’t find libftd2xx.so

check for cable: lsusb -v | grep "FT"

NOTE: CURRENTLY YOU HAVE TO USE SUDO FOR FTD2XX

###########################
