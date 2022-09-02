########################

UR5arm_ReubenPython2and3Class

Code (including ability to hook to Tkinter GUI) to control Universal Robotics UR5 robot arm (with Controller Box 2 or 3).
Code has NOT been tested on the newer "E"-series UR5e.
However, the code should work for the most part on other sizes of arm (e.g. UR10, UR16, etc.)

Reuben Brewer, Ph.D.

reuben.brewer@gmail.com

www.reubotics.com

Apache 2 License

Software Revision C, 08/29/2022

Verified working on: 
Python 2.7, 3.8.
Windows 8.1, 10 64-bit
Raspberry Pi Buster 
(no Mac testing yet)

NOTE: When commanding position in Tool/cartesian space via the function PositionControl_ServoJ_MoveThroughListOfPoses (using "PoseIsInToolSpaceFlag" = 1),
the UR5 is performing inverse-kinematics internally. If the desired TCP pose is one where the arm could achieve it via multuple sets of joint-angles
(like "elbow-left" vs "elbow-right"), then the arm may feak-out and attempt to make a sudden, large motion as it tries to switch between different joint-angle configurations.
In the future, I plan to perform the inverse kinematics within this class so that the user can specify "elbow-left" vs "elbow-right" to prevent those freak-outs.
For now, make sure to operate the arm in a portion of the workspace where there's only a single-joint-angle-configuration that could satisfy a commanded TCP pose.
Of course, if you command only joint-angles via PositionControl_ServoJ_MoveThroughListOfPoses (using "PoseIsInToolSpaceFlag" = 0), then none of these problems will arise.

########################  

########################### Python module installation instructions, all OS's

UR5arm_ReubenPython2and3Class, ListOfModuleDependencies: ['future.builtins']
UR5arm_ReubenPython2and3Class, ListOfModuleDependencies_TestProgram: ['MyPrint_ReubenPython2and3Class']
UR5arm_ReubenPython2and3Class, ListOfModuleDependencies_NestedLayers: ['future.builtins']
UR5arm_ReubenPython2and3Class, ListOfModuleDependencies_All: ['future.builtins', 'MyPrint_ReubenPython2and3Class']

Note: Additional dependencies may exist for helper files beyond the files UR5arm_ReubenPython2and3Class.py and test_program_for_UR5arm_ReubenPython2and3Class.py.

###########################