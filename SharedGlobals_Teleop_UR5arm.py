# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision D, 09/21/2022

Verified working on: Python 3.8 for Windows 10 64-bit, Ubuntu 20.04, and Raspberry Pi Buster (no Mac testing yet).
'''

__author__ = 'reuben.brewer'

#################################################
#################################################
import os
import sys
import time
#################################################
#################################################

#################################################
#################################################
try:
    #https://stackoverflow.com/questions/5286210/is-there-a-way-to-access-parent-modules-in-python/45895490
    ParentModuleName = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__'].__file__
    print("@@@@@@@@@@ ParentModuleName: " + str(ParentModuleName) + " is importing SharedGlobals_Teleop_UR5 @@@@@@@@@@")
except:
    pass
#################################################
#################################################

#################################################
#################################################

#################################################
global EXIT_PROGRAM_FLAG
EXIT_PROGRAM_FLAG = 0
#################################################

#################################################
global UR5arm_MostRecentDict_JointAngleList_Rad
UR5arm_MostRecentDict_JointAngleList_Rad = [-11111.0] * 6

global UR5arm_MostRecentDict_JointAngleList_Deg
UR5arm_MostRecentDict_JointAngleList_Deg = [-11111.0] * 6

global UR5arm_MostRecentDict_ToolVectorActual
UR5arm_MostRecentDict_ToolVectorActual = [-11111.0] * 6
#################################################

#################################################
global DedicatedKeyboardListeningThread_StillRunningFlag
DedicatedKeyboardListeningThread_StillRunningFlag = 0

global CurrentTime_CalculatedFromDedicatedKeyboardListeningThread
CurrentTime_CalculatedFromDedicatedKeyboardListeningThread = -11111.0

global StartingTime_CalculatedFromDedicatedKeyboardListeningThread
StartingTime_CalculatedFromDedicatedKeyboardListeningThread = -11111.0

global LastTime_CalculatedFromDedicatedKeyboardListeningThread
LastTime_CalculatedFromDedicatedKeyboardListeningThread = -11111.0

global DataStreamingFrequency_CalculatedFromDedicatedKeyboardListeningThread
DataStreamingFrequency_CalculatedFromDedicatedKeyboardListeningThread = -11111.0

global DataStreamingDeltaT_CalculatedFromDedicatedKeyboardListeningThread
DataStreamingDeltaT_CalculatedFromDedicatedKeyboardListeningThread = -11111.0

global DedicatedKeyboardListeningThread_TimeToSleepEachLoop
DedicatedKeyboardListeningThread_TimeToSleepEachLoop = 0.020

global BeepNeedsToBePlayedFlag_RecordNewWaypoint_JointSpace
BeepNeedsToBePlayedFlag_RecordNewWaypoint_JointSpace = 0

global BeepNeedsToBePlayedFlag_RecordNewWaypoint_CartesianSpace
BeepNeedsToBePlayedFlag_RecordNewWaypoint_CartesianSpace = 0

global KeyPressResponse_ZEDcontrolClutch_State
KeyPressResponse_ZEDcontrolClutch_State = 0

global KeyPressResponse_IncrementURtoolTipInX_NeedsToBeChangedFlag
KeyPressResponse_IncrementURtoolTipInX_NeedsToBeChangedFlag = 0

global KeyPressResponse_DecrementURtoolTipInX_NeedsToBeChangedFlag
KeyPressResponse_DecrementURtoolTipInX_NeedsToBeChangedFlag = 0

global KeyPressResponse_IncrementURtoolTipInY_NeedsToBeChangedFlag
KeyPressResponse_IncrementURtoolTipInY_NeedsToBeChangedFlag = 0

global KeyPressResponse_DecrementURtoolTipInY_NeedsToBeChangedFlag
KeyPressResponse_DecrementURtoolTipInY_NeedsToBeChangedFlag = 0

global KeyPressResponse_IncrementURtoolTipInZ_NeedsToBeChangedFlag
KeyPressResponse_IncrementURtoolTipInZ_NeedsToBeChangedFlag = 0

global KeyPressResponse_DecrementURtoolTipInZ_NeedsToBeChangedFlag
KeyPressResponse_DecrementURtoolTipInZ_NeedsToBeChangedFlag = 0

global Keyboard_AddToUR5armCurrentPositionList
Keyboard_AddToUR5armCurrentPositionList = [-11111.0]*6

global KeyPressResponse_OpenRobotiqGripper2F85_NeedsToBeChangedFlag
KeyPressResponse_OpenRobotiqGripper2F85_NeedsToBeChangedFlag = 0

global KeyPressResponse_CloseRobotiqGripper2F85_NeedsToBeChangedFlag
KeyPressResponse_CloseRobotiqGripper2F85_NeedsToBeChangedFlag = 0

global Keyboard_KeysToTeleopControlsMapping_DictOfDicts
Keyboard_KeysToTeleopControlsMapping_DictOfDicts = dict()
#################################################

print("SharedGlobals_Teleop_UR5arm.py, finished loading!")
time.sleep(0.5)
#################################################
#################################################

#######################################################################################################################
#######################################################################################################################
if __name__ == '__main__':
    pass
#######################################################################################################################
#######################################################################################################################