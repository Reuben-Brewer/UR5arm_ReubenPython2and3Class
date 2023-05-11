# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision E, 05/10/2023

Verified working on: Python 3.8 for Windows 10 64-bit, Ubuntu 20.04, and Raspberry Pi Buster (no Mac testing yet).
'''

__author__ = 'reuben.brewer'

#########################################################
import os
import sys
import platform
import time
import datetime
import multiprocessing
import math
import collections
from copy import * #for deepcopy of dicts
import inspect #To enable 'TellWhichFileWereIn'
import threading
import traceback
import socket
import select
import struct
import string
import types #Required for 'ListFunctionNamesInClass'
import numpy
from scipy.spatial.transform import Rotation
#########################################################

#########################################################
if sys.version_info[0] < 3:
    from Tkinter import * #Python 2
    import tkFont
    import ttk
else:
    from tkinter import * #Python 3
    import tkinter.font as tkFont #Python 3
    from tkinter import ttk
#########################################################

#########################################################
if sys.version_info[0] < 3:
    import Queue  # Python 2
else:
    import queue as Queue  # Python 3
#########################################################

#########################################################
if sys.version_info[0] < 3:
    from builtins import raw_input as input
else:
    from future.builtins import input as input
######################################################### "sudo pip3 install future" (Python 3) AND "sudo pip install future" (Python 2)

#########################################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
#########################################################

#########################################################
import platform
if platform.system() == "Windows":
    import winsound
#########################################################

class UR5arm_ReubenPython2and3Class(Frame): #Subclass the Tkinter Frame

    ##########################################################################################################
    ##########################################################################################################
    def __init__(self, setup_dict): #Subclass the Tkinter Frame

        print("#################### UR5arm_ReubenPython2and3Class __init__ starting at " + str(self.getPreciseSecondsTimeStampString()) + " ####################")

        self.StartMultiprocessingProcess(setup_dict)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StartMultiprocessingProcess(self, setup_dict):

        if sys.version_info[0] >= 3:

            try: #MUST PUT IN TRY TO PREVENT ERROR, "raise RuntimeError('context has already been set')"
                multiprocessing_StartMethod = multiprocessing.get_start_method()
                print("UR5arm_ReubenPython2and3Class __init__: multiprocessing.get_start_method(): " + str(multiprocessing_StartMethod))
                if multiprocessing_StartMethod != "spawn":
                    print("UR5arm_ReubenPython2and3Class __init__: Issuing multiprocessing.set_start_method('spawn', force=True).")
                    multiprocessing.set_start_method('spawn', force=True) #'spawn' is required for all Linux flavors, with 'force=True' required specicially by Ubuntu (not Raspberry Pi).
            except:
                exceptions = sys.exc_info()[0]
                print("UR5arm_ReubenPython2and3Class __init__: multiprocessing.set_start_method('spawn', force=True) Exceptions: %s" % exceptions)

        '''
        From: https://docs.python.org/3/library/multiprocessing.html#multiprocessing-programming
        spawn
        The parent process starts a fresh python interpreter process.
        The child process will only inherit those resources necessary to run the process object’s run() method.
        In particular, unnecessary file descriptors and handles from the parent process will not be inherited.
        Starting a process using this method is rather slow compared to using fork or forkserver.
        Available on Unix and Windows. The default on Windows and macOS.
        '''

        self.MultiprocessingQueue_Rx = multiprocessing.Queue() #NOT a regular Queue.queue
        self.MultiprocessingQueue_Tx = multiprocessing.Queue() #NOT a regular Queue.queue
        self.job_for_another_core = multiprocessing.Process(target=self.StandAloneProcess,args=(self.MultiprocessingQueue_Rx, self.MultiprocessingQueue_Tx, setup_dict))
        self.job_for_another_core.start() #unicorn
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def StandAloneProcess(self, MultiprocessingQueue_Rx_Local, MultiprocessingQueue_Tx_Local, setup_dict):

        ##########################################################################################################
        ##########################################################################################################
        print("Entering UR5arm_ReubenPython2and3Class StandAloneProcess at " + str(self.getPreciseSecondsTimeStampString()))

        self.ProcessSetupDictInitializeVariablesAndStartThreads(setup_dict)

        self.LastTime_CalculatedFromStandAloneProcess = self.getPreciseSecondsTimeStampString()

        self.StandAloneProcess_ReadyForWritingFlag = 1
        ##########################################################################################################
        ##########################################################################################################

        ########################################################################################################## unicorn dragon
        ##########################################################################################################
        self.StandAloneProcess_DictOfFunctions = dict([("MoveSafelyToStartingPoseViaMultipointSequence", self.MoveSafelyToStartingPoseViaMultipointSequence),
                                                       ("PositionControl_ServoJ_MoveThroughListOfPoses_SafeReturnToStartingPoseFromAnywhere", self.PositionControl_ServoJ_MoveThroughListOfPoses_SafeReturnToStartingPoseFromAnywhere),
                                                       ("PositionControl_ServoJ_MoveThroughListOfPoses", self.PositionControl_ServoJ_MoveThroughListOfPoses),
                                                       ("PositionControl_ServoC_MoveThroughListOfPoses", self.PositionControl_ServoC_MoveThroughListOfPoses),
                                                       ("TestFunctionWithMultipleArguments", self.TestFunctionWithMultipleArguments),
                                                       ("ExitProgram_Callback", self.ExitProgram_Callback),
                                                       ("KickWatchdogButDoNothing", self.KickWatchdogButDoNothing),
                                                       ("SetWatchdogTimerEnableState", self.SetWatchdogTimerEnableState),
                                                       ("StopMotion_JointSpace", self.StopMotion_JointSpace),
                                                       ("ForceControl", self.ForceControl),
                                                       ("DisplayPopupMessage", self.DisplayPopupMessage)])
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0: #unicorn

            try:

                ##########################################################################################################
                self.WatchdogTimerCheck()
                ##########################################################################################################

                ##########################################################################################################
                while not MultiprocessingQueue_Rx_Local.empty():
                    try:

                        #########################################################
                        self.WatchdogTimerCheck()
                        #########################################################

                        #########################################################
                        self.CurrentTime_CalculatedFromStandAloneProcess = self.getPreciseSecondsTimeStampString()
                        self.UpdateFrequencyCalculation_CalculatedFromStandAloneProcess()
                        #########################################################

                        #########################################################
                        inputDict = MultiprocessingQueue_Rx_Local.get(FALSE)  #for queue, non-blocking with "FALSE" argument, could also use MultiprocessingQueue_Rx_Local.get_nowait() for non-blocking
                        #########################################################

                        #########################################################
                        for DictKey_IsFunctionNameString in inputDict:

                            if DictKey_IsFunctionNameString in self.StandAloneProcess_DictOfFunctions:
                                #print("StandAloneProcess found a valid DictKey_IsFunctionNameString: " + DictKey_IsFunctionNameString)

                                ListOfFunctionArguments = inputDict[DictKey_IsFunctionNameString]
                                FunctionToCall = self.StandAloneProcess_DictOfFunctions[DictKey_IsFunctionNameString]
                                FunctionToCall(*ListOfFunctionArguments) # "*" tells Python to unpack the list into separate argument-inputs to the function
                        #########################################################

                    except:
                        exceptions = sys.exc_info()[0]
                        print("UR5arm_ReubenPython2and3Class StandAloneProcess, exceptions: %s" % exceptions)
                        traceback.print_exc()
                ##########################################################################################################

                ##########################################################################################################
                self.LoadMostRecentDataDictIntoMultiprocessingQueueTx(self.MultiprocessingQueue_Tx, IgnoreNewDataIfQueueIsFullFlag = 1)
                ##########################################################################################################

                ##########################################################################################################
                time.sleep(self.StandAloneProcess_TimeToSleepEachLoop) #Without this sleep, the loop will jam your CPU (particularly on Raspberry Pi).
                ##########################################################################################################

            except:
                exceptions = sys.exc_info()[0]
                print("UR5arm_ReubenPython2and3Class, exceptions: %s" % exceptions)
                traceback.print_exc()

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        try: #Need the try/except for if the StandAloneProcess window is closed before that of its parent which is still communicating with it.

            ######################################################### Drain all remaining items in Queues OR ELSE THIS THREAD WON'T DRAIN.
            while not MultiprocessingQueue_Rx_Local.empty():
                DummyToDrainRemainingItemsInRxQueue = MultiprocessingQueue_Rx_Local.get(FALSE)
                #print("MultiprocessingQueue_Rx_Local.qsize()" + str(MultiprocessingQueue_Rx_Local.qsize()))
                time.sleep(0.001) #WITHOUT THIS SLEEP, THE PROGRAM WON'T TERMINATE CORRECTLY!

            while not MultiprocessingQueue_Tx_Local.empty():
                DummyToDrainRemainingItemsInTxQueue = MultiprocessingQueue_Tx_Local.get(FALSE)
                #print("MultiprocessingQueue_Tx_Local.qsize()" + str(MultiprocessingQueue_Tx_Local.qsize()))
                time.sleep(0.001) #WITHOUT THIS SLEEP, THE PROGRAM WON'T TERMINATE CORRECTLY!
            #########################################################

        except:
            pass

        ##########################################################################################################
        ##########################################################################################################

        print("Exited UR5arm_ReubenPython2and3Class.")
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ProcessSetupDictInitializeVariablesAndStartThreads(self, setup_dict):

        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0

        self.DedicatedRxThread_StillRunningFlag = 0
        self.DedicatedTxThread_StillRunningFlag = 0

        self.URarm_ConnectedFlag_CombinedRxAndTx = 0
        self.URarm_ConnectedFlag_DedicatedRx = 0
        self.URarm_ConnectedFlag_DedicatedTx = 0
        self.URarm_ConnectedFlag_DedicatedDashboardEStop = 0

        self.RxPacketsCounter_Total = 0
        self.RxPacketsCounter_WrongSize = 0
        self.RxPackets_PercentWrongSize = 0.0
        self.RxPacketCounter = 0

        self.EnableInternal_MyPrint_Flag = 0

        self.DedicatedTxThread_TxMessageToSend_Queue = Queue.Queue()
        self.TxDataToWrite = ""

        self.ServoJ_JointAngleDistance_Threshold_MinValue = 0.0
        self.ServoJ_JointAngleDistance_Threshold_MaxValue = 20.0
        self.ServoJ_JointAngleDistance_Threshold = 1.0

        self.Velocity_MinValue = 0.001
        self.Velocity_MaxValue = 1.5 # 1.5m/s or 1500 mm/s
        self.Acceleration_MinValue = 0.001
        self.Acceleration_MaxValue = 150.0  # 150m/s^2 or 150000mm/s^2

        self.JointAngleList_Rad = [0.0, -1.57, 0.0, -1.57, 0.0, 0.0] #[-11111.0] * 6 #NEED TO REPLACE 04/22/22
        #self.JointAngleList_Rad = [-11111.0] * 6
        self.JointAngleList_Deg = [-11111.0] * 6
        self.ToolVectorActual = [-11111.0]*6

        self.ToolTip_XYZ_Meters = [-11111.0]*3
        self.ToolTip_RotationEulerList_Radians = [-11111.0]*3
        self.ToolTip_RotationEulerList_Degrees = [-11111.0]*3

        self.ToolTipSpeedsCartestian_TCPspeedActual = [-11111.0] * 6
        self.ToolTipSpeedsCartestian_LinearXYZnorm_MetersPerMin = -11111.0
        self.ToolTipSpeedsCartestian_LinearXYZnorm_MetersPerSec = -11111.0

        self.MoveSafelyToStartingPoseViaMultipointSequence_State_NeedsToBeChangedFlag = 0
        self.MoveToStartingPose_State_NeedsToBeChangedFlag = 0 #START PROGRAM BY MOVING TO StartingPoseJointAngleList_Deg
        self.StopMotion_State_NeedsToBeChangedFlag = 0
        self.ClearProtectiveStop_State_NeedsToBeChangedFlag = 0
        self.RestartSafety_State_NeedsToBeChangedFlag = 0
        self.StartRobot_State_NeedsToBeChangedFlag = 0
        self.ResetTCPsockets_State_NeedsToBeChangedFlag = 0

        self.Freedrive_State = 0
        self.Freedrive_State_ToBeSet = 0
        self.Freedrive_State_NeedsToBeChangedFlag = 0

        self.WatchdogTimerEnableState = 0

        self.Payload_MassKG_ToBeCommanded = -11111.0
        self.Payload_CoGmetersList_ToBeCommanded = [-11111.0]*3

        self.JointAngleCommandIncrementDecrement_EntryLabelList = list()
        self.JointAngleCommandIncrementDecrement_EntryTextContentList = list()
        self.JointAngleCommandIncrementDecrement_EntryObject = list()
        self.JointAngleCommandIncrementDecrement_ValueList_ToBeSet = [0.0]*6
        self.JointAngleCommandIncrementDecrement_NeedsToBeChangedFlag = 0

        self.JointAngleCommandIncrement_ButtonObjectList = list()
        self.JointAngleCommandDecrement_ButtonObjectList = list()

        #########################################################
        self.CurrentTime_CalculatedFromDedicatedTxThread = -11111.0
        self.LastTime_CalculatedFromDedicatedTxThread = -11111.0
        self.StartingTime_CalculatedFromDedicatedTxThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromDedicatedTxThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromDedicatedTxThread = -11111.0

        self.CurrentTime_CalculatedFromDedicatedRxThread = -11111.0
        self.LastTime_CalculatedFromDedicatedRxThread = -11111.0
        self.StartingTime_CalculatedFromDedicatedRxThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromDedicatedRxThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromDedicatedRxThread = -11111.0

        self.CurrentTime_CalculatedFromGUIthread = -11111.0
        self.LastTime_CalculatedFromGUIthread = -11111.0
        self.LoopFrequency_CalculatedFromGUIthread = -11111.0
        self.LoopDeltaT_CalculatedFromGUIthread = -11111.0

        self.CurrentTime_CalculatedFromStandAloneProcess = -11111.0
        self.LastTime_CalculatedFromStandAloneProcess = -11111.0
        self.LoopFrequency_CalculatedFromStandAloneProcess = -11111.0
        self.LoopDeltaT_CalculatedFromStandAloneProcess = -11111.0

        self.StandAloneProcess_ReadyForWritingFlag = 0
        #########################################################

        #"<3.0", the spreadsheet says that it should be 764, but I swear it's 812, NumberOfValues should be 96 but is 102
        self.RealTimeClientInterfaceVersionHistoryNumberOfValuesAndBytesDict = dict([
            ("<3.0", dict([("NumberOfValues", 102),("NumberOfBytes", 812), ("LastValue", "Joint Modes")])), #pre 3.0            | NumberOfValues = 096, NumberOfBytes = 0764 (last item is "Joint Modes").
            ("3.0", dict([("NumberOfValues", 131), ("NumberOfBytes", 1044), ("LastValue", "V actual")])), #3.0-3.1             | NumberOfValues = 131, NumberOfBytes = 1044 (last item is "V actual").
            ("3.1", dict([("NumberOfValues", 131), ("NumberOfBytes", 1044), ("LastValue", "V actual")])), #3.0-3.1             | NumberOfValues = 131, NumberOfBytes = 1044 (last item is "V actual").
            ("3.2", dict([("NumberOfValues", 133), ("NumberOfBytes", 1060), ("LastValue", "Program State")])), #3.2-3.4        | NumberOfValues = 133, NumberOfBytes = 1060 (last item is "Program State").
            ("3.3", dict([("NumberOfValues", 133), ("NumberOfBytes", 1060), ("LastValue", "Program State")])), #3.2-3.4        | NumberOfValues = 133, NumberOfBytes = 1060 (last item is "Program State").
            ("3.4", dict([("NumberOfValues", 133), ("NumberOfBytes", 1060), ("LastValue", "Program State")])), #3.2-3.4        | NumberOfValues = 133, NumberOfBytes = 1060 (last item is "Program State").
            ("3.5", dict([("NumberOfValues", 139), ("NumberOfBytes", 1108), ("LastValue", "Elbow Velocity")])), #3.5           | NumberOfValues = 139, NumberOfBytes = 1108 (last item is "Elbow Velocity").
            ("3.6", dict([("NumberOfValues", 139), ("NumberOfBytes", 1108), ("LastValue", "Elbow Velocity")])), #3.6           | NumberOfValues = 139, NumberOfBytes = 1108 (last item is "Elbow Velocity").
            ("3.7", dict([("NumberOfValues", 139), ("NumberOfBytes", 1108), ("LastValue", "Elbow Velocity")])), #3.7-3.9       | NumberOfValues = 139, NumberOfBytes = 1108 (last item is "Elbow Velocity").
            ("3.8", dict([("NumberOfValues", 139), ("NumberOfBytes", 1108), ("LastValue", "Elbow Velocity")])), #3.7-3.9       | NumberOfValues = 139, NumberOfBytes = 1108 (last item is "Elbow Velocity").
            ("3.9", dict([("NumberOfValues", 139), ("NumberOfBytes", 1108), ("LastValue", "Elbow Velocity")])), #3.7-3.9       | NumberOfValues = 139, NumberOfBytes = 1108 (last item is "Elbow Velocity").
            ("3.10", dict([("NumberOfValues", 140), ("NumberOfBytes", 1116), ("LastValue", "Safety Status")])), #3.10-3.13     | NumberOfValues = 140, NumberOfBytes = 1116 (last item is "Safety Status").
            ("3.11", dict([("NumberOfValues", 140), ("NumberOfBytes", 1116), ("LastValue", "Safety Status")])), #3.10-3.13     | NumberOfValues = 140, NumberOfBytes = 1116 (last item is "Safety Status").
            ("3.12", dict([("NumberOfValues", 140), ("NumberOfBytes", 1116), ("LastValue", "Safety Status")])), #3.10-3.13     | NumberOfValues = 140, NumberOfBytes = 1116 (last item is "Safety Status").
            ("3.13", dict([("NumberOfValues", 140), ("NumberOfBytes", 1116), ("LastValue", "Safety Status")])), #3.10-3.13     | NumberOfValues = 140, NumberOfBytes = 1116 (last item is "Safety Status").
            ("3.14", dict([("NumberOfValues", 143), ("NumberOfBytes", 1140), ("LastValue", "InternalURuseOnly")])), #3.14-3.15 | NumberOfValues = 143, NumberOfBytes = 1140 (last item is "Used by Universal Robots software only").
            ("3.15", dict([("NumberOfValues", 143), ("NumberOfBytes", 1140), ("LastValue", "InternalURuseOnly")])), #3.14-3.15 | NumberOfValues = 143, NumberOfBytes = 1140 (last item is "Used by Universal Robots software only").
            ("5.0", dict([("NumberOfValues", 139), ("NumberOfBytes", 1108), ("LastValue", "Elbow Velocity")])), #5.0           | NumberOfValues = 139, NumberOfBytes = 1108 (last item is "Elbow Velocity").
            ("5.1", dict([("NumberOfValues", 139), ("NumberOfBytes", 1108), ("LastValue", "Elbow Velocity")])), #5.1-5.3       | NumberOfValues = 139, NumberOfBytes = 1108 (last item is "Elbow Velocity").
            ("5.2", dict([("NumberOfValues", 139), ("NumberOfBytes", 1108), ("LastValue", "Elbow Velocity")])), #5.1-5.3       | NumberOfValues = 139, NumberOfBytes = 1108 (last item is "Elbow Velocity").
            ("5.3", dict([("NumberOfValues", 139), ("NumberOfBytes", 1108), ("LastValue", "Elbow Velocity")])), #5.1-5.3       | NumberOfValues = 139, NumberOfBytes = 1108 (last item is "Elbow Velocity").
            ("5.4", dict([("NumberOfValues", 140), ("NumberOfBytes", 1116), ("LastValue", "Safety Status")])), #5.4-5.8        | NumberOfValues = 140, NumberOfBytes = 1116 (last item is "Safety Status").
            ("5.5", dict([("NumberOfValues", 140), ("NumberOfBytes", 1116), ("LastValue", "Safety Status")])), #5.4-5.8        | NumberOfValues = 140, NumberOfBytes = 1116 (last item is "Safety Status").
            ("5.6", dict([("NumberOfValues", 140), ("NumberOfBytes", 1116), ("LastValue", "Safety Status")])), #5.4-5.8        | NumberOfValues = 140, NumberOfBytes = 1116 (last item is "Safety Status").
            ("5.7", dict([("NumberOfValues", 140), ("NumberOfBytes", 1116), ("LastValue", "Safety Status")])), #5.4-5.8        | NumberOfValues = 140, NumberOfBytes = 1116 (last item is "Safety Status").
            ("5.8", dict([("NumberOfValues", 140), ("NumberOfBytes", 1116), ("LastValue", "Safety Status")])), #5.4-5.8        | NumberOfValues = 140, NumberOfBytes = 1116 (last item is "Safety Status").
            ("5.9", dict([("NumberOfValues", 143), ("NumberOfBytes", 1140), ("LastValue", "InternalURuseOnly")])), #5.9        | NumberOfValues = 143, NumberOfBytes = 1140 (last item is "Used by Universal Robots software only").
            ("5.10", dict([("NumberOfValues", 153),("NumberOfBytes", 1220), ("LastValue", "Payload Inertia")]))]) #5.10        | NumberOfValues = 153, NumberOfBytes = 1220 (last item is "Payload Inertia").

        #########################################################
        #########################################################
        if platform.system() == "Linux":

            if "raspberrypi" in platform.uname():  # os.uname() doesn't work in windows
                self.my_platform = "pi"
            else:
                self.my_platform = "linux"

        elif platform.system() == "Windows":
            self.my_platform = "windows"

        elif platform.system() == "Darwin":
            self.my_platform = "mac"

        else:
            self.my_platform = "other"

        print("UR5arm_ReubenPython2and3Class __init__: The OS platform is: " + self.my_platform)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "GUIparametersDict" in setup_dict:
            self.GUIparametersDict = setup_dict["GUIparametersDict"]

            #########################################################
            if "USE_GUI_FLAG" in self.GUIparametersDict:
                self.USE_GUI_FLAG = self.PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG", self.GUIparametersDict["USE_GUI_FLAG"])
            else:
                self.USE_GUI_FLAG = 0

            print("UR5arm_ReubenPython2and3Class __init__: USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))
            #########################################################

            #########################################################
            if "EnableInternal_MyPrint_Flag" in self.GUIparametersDict:
                self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", self.GUIparametersDict["EnableInternal_MyPrint_Flag"])
            else:
                self.EnableInternal_MyPrint_Flag = 0

            print("UR5arm_ReubenPython2and3Class __init__: EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
            #########################################################

            ##########################################
            if "GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents" in self.GUIparametersDict:
                self.GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents", self.GUIparametersDict["GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents"], 0.0, 1000.0))
            else:
                self.GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents = 30

            print("GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents = " + str(self.GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents))
            ##########################################

            #########################################################
            if "PrintToConsoleFlag" in self.GUIparametersDict:
                self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", self.GUIparametersDict["PrintToConsoleFlag"])
            else:
                self.PrintToConsoleFlag = 1

            print("UR5arm_ReubenPython2and3Class __init__: PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
            #########################################################

            #########################################################
            if "NumberOfPrintLines" in self.GUIparametersDict:
                self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", self.GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
            else:
                self.NumberOfPrintLines = 10

            print("UR5arm_ReubenPython2and3Class __init__: NumberOfPrintLines: " + str(self.NumberOfPrintLines))
            #########################################################

            #########################################################
            if "RootWindowWidth" in self.GUIparametersDict:
                self.RootWindowWidth = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("RootWindowWidth", self.GUIparametersDict["RootWindowWidth"], 0.0, 1920.0)
            else:
                self.RootWindowWidth = 1000.0

            print("UR5arm_ReubenPython2and3Class __init__: RootWindowWidth: " + str(self.RootWindowWidth))
            #########################################################

            #########################################################
            if "RootWindowHeight" in self.GUIparametersDict:
                self.RootWindowHeight = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("RootWindowHeight", self.GUIparametersDict["RootWindowHeight"], 0.0, 1080.0)
            else:
                self.RootWindowHeight = 1000.0

            print("UR5arm_ReubenPython2and3Class __init__: RootWindowHeight: " + str(self.RootWindowHeight))
            #########################################################

            #########################################################
            if "RootWindowStartingX" in self.GUIparametersDict:
                self.RootWindowStartingX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("RootWindowStartingX", self.GUIparametersDict["RootWindowStartingX"], 0.0, 1920.0))
            else:
                self.RootWindowStartingX = 50.0

            print("UR5arm_ReubenPython2and3Class __init__: RootWindowStartingX: " + str(self.RootWindowStartingX))
            #########################################################

            #########################################################
            if "RootWindowStartingY" in self.GUIparametersDict:
                self.RootWindowStartingY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("RootWindowStartingY", self.GUIparametersDict["RootWindowStartingY"], 0.0, 1080.0))
            else:
                self.RootWindowStartingY = 50.0

            print("UR5arm_ReubenPython2and3Class __init__: RootWindowStartingY: " + str(self.RootWindowStartingY))
            #########################################################

            #########################################################
            if "RootWindowTitle" in self.GUIparametersDict:
                self.RootWindowTitle = str(self.GUIparametersDict["RootWindowTitle"])
            else:
                self.RootWindowTitle = "UR5arm_ReubenPython2and3Class"

            print("UR5arm_ReubenPython2and3Class __init__: RootWindowTitle: " + self.RootWindowTitle)
            #########################################################

        else:
            self.GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("URarm_ReubenPython2and3Class __init__: No GUIparametersDict present, setting USE_GUI_FLAG = " + str(self.USE_GUI_FLAG))

        #print("UR5arm_ReubenPython2and3Class __init__: GUIparametersDict = " + str(self.GUIparametersDict))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "IPV4_address" in setup_dict:
            self.IPV4_address = str(setup_dict["IPV4_address"])

        else:
            print("UR5arm_ReubenPython2and3Class __init__: ERROR, Must pass in 'IPV4_address' argument.")
            exit() #return Doesn't work in multiprocessing situation, must use exit() instead.

        print("URarm_ReubenPython2and3Class __init__: IPV4_address: " + str(self.IPV4_address))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "ControllerBoxVersion" in setup_dict:
            try:
                self.ControllerBoxVersion = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("ControllerBoxVersion", setup_dict["ControllerBoxVersion"], 2.0, 3.0))

                if self.ControllerBoxVersion not in [2, 3]:
                    print("UR5arm_ReubenPython2and3Class __init__: ERROR, ControllerBoxVersion must be 2 or 3.")
                    exit() #return Doesn't work in multiprocessing situation, must use exit() instead.

            except:
                print("UR5arm_ReubenPython2and3Class __init__: ERROR, Must initialize object with 'ControllerBoxVersion' argument that is type 'int'.")
                exit() #return Doesn't work in multiprocessing situation, must use exit() instead.

        else:
            self.ControllerBoxVersion = 3

        print("URarm_ReubenPython2and3Class __init__: ControllerBoxVersion: " + str(self.ControllerBoxVersion))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "IPV4_TimeoutDurationSeconds" in setup_dict:
            try:
                self.IPV4_TimeoutDurationSeconds = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("IPV4_TimeoutDurationSeconds", setup_dict["IPV4_TimeoutDurationSeconds"], 0.0, 300.0)
            except:
                print("UR5arm_ReubenPython2and3Class __init__: ERROR, Must initialize object with 'IPV4_TimeoutDurationSeconds' argument that is type 'float'.")
                exit() #return Doesn't work in multiprocessing situation, must use exit() instead.

        else:
            self.IPV4_TimeoutDurationSeconds = 1.0

        print("URarm_ReubenPython2and3Class __init__: IPV4_TimeoutDurationSeconds: " + str(self.IPV4_TimeoutDurationSeconds))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "IPV4_NumberOfRxMessagesToBuffers" in setup_dict:
            try:
                self.IPV4_NumberOfRxMessagesToBuffers = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("IPV4_NumberOfRxMessagesToBuffers", setup_dict["IPV4_NumberOfRxMessagesToBuffers"], 1.0, 1000000000.0))
            except:
                print("UR5arm_ReubenPython2and3Class __init__: ERROR, Must initialize object with 'IPV4_NumberOfRxMessagesToBuffers' argument that is type 'float'.")
                exit() #return Doesn't work in multiprocessing situation, must use exit() instead.

        else:
            self.IPV4_NumberOfRxMessagesToBuffers = 64

        print("URarm_ReubenPython2and3Class __init__: IPV4_NumberOfRxMessagesToBuffers: " + str(self.IPV4_NumberOfRxMessagesToBuffers))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "NameToDisplay_UserSet" in setup_dict:
            self.NameToDisplay_UserSet = str(setup_dict["NameToDisplay_UserSet"])
        else:
            self.NameToDisplay_UserSet = ""

        print("URarm_ReubenPython2and3Class __init__: NameToDisplay_UserSet: " + str(self.NameToDisplay_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DedicatedRxThread_TimeToSleepEachLoop" in setup_dict:
            self.DedicatedRxThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("DedicatedRxThread_TimeToSleepEachLoop", setup_dict["DedicatedRxThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.DedicatedRxThread_TimeToSleepEachLoop = 0.005

        print("URarm_ReubenPython2and3Class __init__: DedicatedRxThread_TimeToSleepEachLoop: " + str(self.DedicatedRxThread_TimeToSleepEachLoop))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DedicatedTxThread_MaximumTxMessagesPerSecondFrequency" in setup_dict:
            self.DedicatedTxThread_MaximumTxMessagesPerSecondFrequency = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("DedicatedTxThread_MaximumTxMessagesPerSecondFrequency", setup_dict["DedicatedTxThread_MaximumTxMessagesPerSecondFrequency"], 0.001, 100000)

        else:
            self.DedicatedTxThread_MaximumTxMessagesPerSecondFrequency = 150.0

        print("URarm_ReubenPython2and3Class __init__: DedicatedTxThread_MaximumTxMessagesPerSecondFrequency: " + str(self.DedicatedTxThread_MaximumTxMessagesPerSecondFrequency))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DedicatedTxThread_TxMessageToSend_Queue_MaxSize" in setup_dict:
            self.DedicatedTxThread_TxMessageToSend_Queue_MaxSize = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("DedicatedTxThread_TxMessageToSend_Queue_MaxSize", setup_dict["DedicatedTxThread_TxMessageToSend_Queue_MaxSize"], 1.0, 100000.0))

        else:
            self.DedicatedTxThread_TxMessageToSend_Queue_MaxSize = 1

        print("URarm_ReubenPython2and3Class __init__: DedicatedTxThread_TxMessageToSend_Queue_MaxSize: " + str(self.DedicatedTxThread_TxMessageToSend_Queue_MaxSize))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "StandAloneProcess_TimeToSleepEachLoop" in setup_dict:
            self.StandAloneProcess_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("StandAloneProcess_TimeToSleepEachLoop", setup_dict["StandAloneProcess_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.StandAloneProcess_TimeToSleepEachLoop = 0.005

        print("URarm_ReubenPython2and3Class __init__: StandAloneProcess_TimeToSleepEachLoop: " + str(self.StandAloneProcess_TimeToSleepEachLoop))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "StartingPoseJointAngleList_Deg" in setup_dict:
            StartingPoseJointAngleList_Deg_TEMP = setup_dict["StartingPoseJointAngleList_Deg"]

            if self.IsInputListOfNumbers(StartingPoseJointAngleList_Deg_TEMP) == 1:
                if len(StartingPoseJointAngleList_Deg_TEMP) == 6:
                    self.StartingPoseJointAngleList_Deg = StartingPoseJointAngleList_Deg_TEMP

                else:
                    print("UR5arm_ReubenPython2and3Class __init__: ERROR, StartingPoseJointAngleList_Deg must be a list of 6 numbers.")
                    exit() #return Doesn't work in multiprocessing situation, must use exit() instead.

            else:
                print("UR5arm_ReubenPython2and3Class __init__: ERROR, StartingPoseJointAngleList_Deg must be a list of 6 numbers.")
                exit() #return Doesn't work in multiprocessing situation, must use exit() instead.

        else:
            self.StartingPoseJointAngleList_Deg = [0.0, -90.0, 0.0, -90.0, 0.0, 0.0] #Homing pose

        print("URarm_ReubenPython2and3Class __init__: StartingPoseJointAngleList_Deg: " + str(self.StartingPoseJointAngleList_Deg))

        self.StartingPoseJointAngleList_Rad = self.ConvertListOfValuesDegToRad(self.StartingPoseJointAngleList_Deg)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "PositionControl_ServoJ_MoveThroughListOfPoses_SafeReturnToStartingPoseFromAnywhere" in setup_dict:
            self.PositionControl_ServoJ_MoveThroughListOfPoses_SafeReturnToStartingPoseFromAnywhere = setup_dict["PositionControl_ServoJ_MoveThroughListOfPoses_SafeReturnToStartingPoseFromAnywhere"]

        else:
            self.PositionControl_ServoJ_MoveThroughListOfPoses_SafeReturnToStartingPoseFromAnywhere = list([])

        print("URarm_ReubenPython2and3Class __init__: PositionControl_ServoJ_MoveThroughListOfPoses_SafeReturnToStartingPoseFromAnywhere: " + str(self.PositionControl_ServoJ_MoveThroughListOfPoses_SafeReturnToStartingPoseFromAnywhere))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "Payload_MassKG_ToBeCommanded" in setup_dict:
            self.Payload_MassKG_ToBeCommanded = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("Payload_MassKG_ToBeCommanded", setup_dict["Payload_MassKG_ToBeCommanded"], 0.000, 16.0)

        else:
            self.Payload_MassKG_ToBeCommanded = 0.000

        print("URarm_ReubenPython2and3Class __init__: Payload_MassKG_ToBeCommanded: " + str(self.Payload_MassKG_ToBeCommanded))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "Payload_CoGmetersList_ToBeCommanded" in setup_dict:
            Payload_CoGmetersList_ToBeCommanded_TEMP = setup_dict["Payload_CoGmetersList_ToBeCommanded"]

            if self.IsInputListOfNumbers(Payload_CoGmetersList_ToBeCommanded_TEMP) == 1:
                if len(Payload_CoGmetersList_ToBeCommanded_TEMP) == 3:
                    self.Payload_CoGmetersList_ToBeCommanded = Payload_CoGmetersList_ToBeCommanded_TEMP

                else:
                    print("UR5arm_ReubenPython2and3Class __init__: ERROR, Payload_CoGmetersList_ToBeCommanded must be a list of 3 numbers.")
                    exit() #return Doesn't work in multiprocessing situation, must use exit() instead.

            else:
                print("UR5arm_ReubenPython2and3Class __init__: ERROR, Payload_CoGmetersList_ToBeCommanded must be a list of 3 numbers.")
                exit() #return Doesn't work in multiprocessing situation, must use exit() instead.

        else:
            self.Payload_CoGmetersList_ToBeCommanded = [0.0]*3

        print("URarm_ReubenPython2and3Class __init__: Payload_CoGmetersList_ToBeCommanded: " + str(self.Payload_CoGmetersList_ToBeCommanded))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "Acceleration" in setup_dict:
            self.Acceleration = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("Acceleration", setup_dict["Acceleration"], self.Acceleration_MinValue, self.Acceleration_MaxValue)

        else:
            self.Acceleration = 1000.0

        print("URarm_ReubenPython2and3Class __init__: Acceleration: " + str(self.Acceleration))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "Velocity" in setup_dict:
            self.Velocity = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("Velocity", setup_dict["Velocity"], self.Velocity_MinValue, self.Velocity_MaxValue)

        else:
            self.Velocity = 1.0

        print("URarm_ReubenPython2and3Class __init__: Velocity: " + str(self.Velocity))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "JointAngleCommandIncrementDecrement_ValueInDegrees" in setup_dict:
            self.JointAngleCommandIncrementDecrement_ValueInDegrees = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("JointAngleCommandIncrementDecrement_ValueInDegrees", setup_dict["JointAngleCommandIncrementDecrement_ValueInDegrees"], 0.000, 360.0)

        else:
            self.JointAngleCommandIncrementDecrement_ValueInDegrees = 1.0

        print("URarm_ReubenPython2and3Class __init__: JointAngleCommandIncrementDecrement_ValueInDegrees: " + str(self.JointAngleCommandIncrementDecrement_ValueInDegrees))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "JointAngleCommandIncrementDecrement_CustomEntryLabels_ListOfDicts" in setup_dict:
            JointAngleCommandIncrementDecrement_CustomEntryLabels_ListOfDicts_TEMP = setup_dict["JointAngleCommandIncrementDecrement_CustomEntryLabels_ListOfDicts"]

            if self.IsInputList(JointAngleCommandIncrementDecrement_CustomEntryLabels_ListOfDicts_TEMP) == 1:
                if len(JointAngleCommandIncrementDecrement_CustomEntryLabels_ListOfDicts_TEMP) == 6:
                    self.JointAngleCommandIncrementDecrement_CustomEntryLabels_ListOfDicts = []
                    for counter, JointLabelDict in enumerate(JointAngleCommandIncrementDecrement_CustomEntryLabels_ListOfDicts_TEMP):
                        if "IncrementLabel" in JointLabelDict and "DecrementLabel" in JointLabelDict:
                            self.JointAngleCommandIncrementDecrement_CustomEntryLabels_ListOfDicts.append(JointLabelDict)
                        else:
                            print("UR5arm_ReubenPython2and3Class __init__: ERROR, JointAngleCommandIncrementDecrement_CustomEntryLabels_ListOfDicts must be a list of 6 Dicts, each with 'IncrementLabel' and 'DecrementLabel'.")
                            exit() #return Doesn't work in multiprocessing situation, must use exit() instead.

                else:
                    print("UR5arm_ReubenPython2and3Class __init__: ERROR, JointAngleCommandIncrementDecrement_CustomEntryLabels_ListOfDicts must be a list of 6 Dicts.")
                    exit() #return Doesn't work in multiprocessing situation, must use exit() instead.

            else:
                print("UR5arm_ReubenPython2and3Class __init__: ERROR, JointAngleCommandIncrementDecrement_CustomEntryLabels_ListOfDicts must be a list of 6 Dicts.")
                exit() #return Doesn't work in multiprocessing situation, must use exit() instead.

        else:
            self.JointAngleCommandIncrementDecrement_CustomEntryLabels_ListOfDicts = [dict([("IncrementLabel", "Increment"), ("DecrementLabel", "Decrement")])]*6

        print("URarm_ReubenPython2and3Class __init__: JointAngleCommandIncrementDecrement_CustomEntryLabels_ListOfDicts: " + str(self.JointAngleCommandIncrementDecrement_CustomEntryLabels_ListOfDicts))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "RealTimeClientInterfaceVersionNumberString" in setup_dict:
            RealTimeClientInterfaceVersionNumberString_TEMP = str(setup_dict["RealTimeClientInterfaceVersionNumberString"])
            if RealTimeClientInterfaceVersionNumberString_TEMP not in self.RealTimeClientInterfaceVersionHistoryNumberOfValuesAndBytesDict:

                ############
                RealTimeClientInterfaceVersionNumberString_SetString = "["
                for key in self.RealTimeClientInterfaceVersionHistoryNumberOfValuesAndBytesDict:
                    RealTimeClientInterfaceVersionNumberString_SetString = RealTimeClientInterfaceVersionNumberString_SetString + key + ","
                RealTimeClientInterfaceVersionNumberString_SetString = RealTimeClientInterfaceVersionNumberString_SetString[:-2] + "]"
                ############

                print("UR5arm_ReubenPython2and3Class __init__: ERROR, 'RealTimeClientInterfaceVersionNumberString' must be in the set " + RealTimeClientInterfaceVersionNumberString_SetString)
                exit() #return Doesn't work in multiprocessing situation, must use exit() instead.

            self.RealTimeClientInterfaceVersionNumberString = RealTimeClientInterfaceVersionNumberString_TEMP

        else:
            self.RealTimeClientInterfaceVersionNumberString = "5.10"

        print("URarm_ReubenPython2and3Class __init__: RealTimeClientInterfaceVersionNumberString: " + str(self.RealTimeClientInterfaceVersionNumberString))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:
            if self.RealTimeClientInterfaceVersionNumberString == "<3.0":
                self.RealTimeClientInterfaceVersionNumberFloat = 2.9
            else:
                self.RealTimeClientInterfaceVersionNumberFloat = float(self.RealTimeClientInterfaceVersionNumberString)

            print("URarm_ReubenPython2and3Class __init__: self.RealTimeClientInterfaceVersionNumberFloat: " + str(self.RealTimeClientInterfaceVersionNumberFloat))
        except:
            exceptions = sys.exc_info()[0]
            print("URarm_ReubenPython2and3Class __init__: RealTimeClientInterfaceVersionNumberFloat could not be calculated, Exceptions: %s" % exceptions)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "ParentPID" in setup_dict:
            self.ParentPID = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("ParentPID", setup_dict["ParentPID"], 0.0, 100000000.0))
        else:
            self.ParentPID = -11111

        print("URarm_ReubenPython2and3Class __init__: ParentPID = " + str(self.ParentPID))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "WatchdogTimerDurationSeconds_ExpirationWillEndStandAloneProcess" in setup_dict:
            self.WatchdogTimerDurationSeconds_ExpirationWillEndStandAloneProcess = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("WatchdogTimerDurationSeconds_ExpirationWillEndStandAloneProcess", setup_dict["WatchdogTimerDurationSeconds_ExpirationWillEndStandAloneProcess"], 0.0, 1000.0)
        else:
            self.WatchdogTimerDurationSeconds_ExpirationWillEndStandAloneProcess = 0.0

        print("URarm_ReubenPython2and3Class __init__: WatchdogTimerDurationSeconds_ExpirationWillEndStandAloneProcess = " + str(self.WatchdogTimerDurationSeconds_ExpirationWillEndStandAloneProcess))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "MultiprocessingQueue_Rx_MaxSize" in setup_dict:
            self.MultiprocessingQueue_Rx_MaxSize = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("MultiprocessingQueue_Rx_MaxSize", setup_dict["MultiprocessingQueue_Rx_MaxSize"], 1.0, sys.float_info.max))

        else:
            self.MultiprocessingQueue_Rx_MaxSize = 2

        print("URarm_ReubenPython2and3Class __init__: MultiprocessingQueue_Rx_MaxSize: " + str(self.MultiprocessingQueue_Rx_MaxSize))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "MultiprocessingQueue_Tx_MaxSize" in setup_dict:
            self.MultiprocessingQueue_Tx_MaxSize = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("MultiprocessingQueue_Tx_MaxSize", setup_dict["MultiprocessingQueue_Tx_MaxSize"], 1.0, sys.float_info.max))

        else:
            self.MultiprocessingQueue_Tx_MaxSize = 2

        print("URarm_ReubenPython2and3Class __init__: MultiprocessingQueue_Tx_MaxSize: " + str(self.MultiprocessingQueue_Tx_MaxSize))
        #########################################################
        #########################################################

        ######################################################### dragon
        #########################################################
        if "EnableTx_State_AtStartupFlag" in setup_dict:
            self.EnableTx_State_AtStartupFlag = self.PassThrough0and1values_ExitProgramOtherwise("EnableTx_State_AtStartupFlag", setup_dict["EnableTx_State_AtStartupFlag"])
        else:
            self.EnableTx_State_AtStartupFlag = 1

        print("UR5arm_ReubenPython2and3Class __init__: EnableTx_State_AtStartupFlag: " + str(self.EnableTx_State_AtStartupFlag))

        self.EnableTx_State = self.EnableTx_State_AtStartupFlag
        #########################################################
        #########################################################

        #########################################################
        ######################################################### This doesn't always hold. For instance, I've used a UR5-CB3 arm with RealTimeClientInterface version 5.10!
        #if int(self.RealTimeClientInterfaceVersionNumberFloat) != int(self.ControllerBoxVersion): #To prevent someone from using older URscript protocol (like 1.8) with newer ControllerBox (like 3).
        #    print("URarm_ReubenPython2and3Class __init__: ERROR, Incompatible RealTimeClientInterfaceVersion (" + str(self.RealTimeClientInterfaceVersionNumberFloat) + ") and ControllerBoxVersion (" + str(self.ControllerBoxVersion) + ").")
        #    exit() #return Doesn't work in multiprocessing situation, must use exit() instead.
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if self.ControllerBoxVersion == 2:
            self.IPV4_RxPort = 30003
            self.IPV4_TxPort = 30003
        else:
            self.IPV4_RxPort = 30013
            self.IPV4_TxPort = 30003
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.PacketKeywordStringsList_UpToRealTimeClientInterfaceVersion_BelowVersion_3dot0 = ["MessageSize",
                                        "Time",
                                        "Qtarget_Joint1", "Qtarget_Joint2", "Qtarget_Joint3", "Qtarget_Joint4", "Qtarget_Joint5", "Qtarget_Joint6",
                                        "Qdtarget_Joint1", "Qdtarget_Joint2", "Qdtarget_Joint3", "Qdtarget_Joint4", "Qdtarget_Joint5", "Qdtarget_Joint6",
                                        "Qddtarget_Joint1", "Qddtarget_Joint2", "Qddtarget_Joint3", "Qddtarget_Joint4", "Qddtarget_Joint5", "Qddtarget_Joint6",
                                        "Itarget_Joint1", "Itarget_Joint2", "Itarget_Joint3", "Itarget_Joint4", "Itarget_Joint5", "Itarget_Joint6",
                                        "Mtarget_Joint1", "Mtarget_Joint2", "Mtarget_Joint3", "Mtarget_Joint4", "Mtarget_Joint5", "Mtarget_Joint6",
                                        "Qactual_Joint1", "Qactual_Joint2", "Qactual_Joint3", "Qactual_Joint4", "Qactual_Joint5", "Qactual_Joint6",
                                        "QDactual_Joint1", "QDactual_Joint2", "QDactual_Joint3", "QDactual_Joint4", "QDactual_Joint5", "QDactual_Joint6",
                                        "Iactual_Joint1", "Iactual_Joint2", "Iactual_Joint3", "Iactual_Joint4", "Iactual_Joint5", "Iactual_Joint6",
                                        "ToolAccelerometerX", "ToolAccelerometerY", "ToolAccelerometerZ",
                                        "Unused", "Unused", "Unused", "Unused", "Unused", "Unused", "Unused", "Unused", "Unused", "Unused", "Unused", "Unused", "Unused", "Unused", "Unused",
                                        "TCPforce_Joint1", "TCPforce_Joint2", "TCPforce_Joint3", "TCPforce_Joint4", "TCPforce_Joint5", "TCPforce_Joint6",
                                        "ToolXactual", "ToolYactual", "ToolZactual", "ToolRXactual", "ToolRYactual", "ToolRZactual",
                                        "TCPspeedActual_Joint1", "TCPspeedActual_Joint2", "TCPspeedActual_Joint3", "TCPspeedActual_Joint4", "TCPspeedActual_Joint5", "TCPspeedActual_Joint6",
                                        "DigitalInputBits",
                                        "MotorTemperature_Joint1", "MotorTemperature_Joint2", "MotorTemperature_Joint3", "MotorTemperature_Joint4", "MotorTemperature_Joint5", "MotorTemperature_Joint6",
                                        "ControllerTimer",
                                        "TestValue",
                                        "RobotMode",
                                        "JointMode_Joint1", "JointMode_Joint2", "JointMode_Joint3", "JointMode_Joint4", "JointMode_Joint5", "JointMode_Joint6"]

        #This list encompasses up to Real-Time Client Interface Version 5.10.
        self.PacketKeywordStringsList_UpToRealTimeClientInterfaceVersion_3dot0_to_5dot10 = ["MessageSize",
                                        "Time",
                                        "Qtarget_Joint1", "Qtarget_Joint2", "Qtarget_Joint3", "Qtarget_Joint4", "Qtarget_Joint5", "Qtarget_Joint6",
                                        "Qdtarget_Joint1", "Qdtarget_Joint2", "Qdtarget_Joint3", "Qdtarget_Joint4", "Qdtarget_Joint5", "Qdtarget_Joint6",
                                        "Qddtarget_Joint1", "Qddtarget_Joint2", "Qddtarget_Joint3", "Qddtarget_Joint4", "Qddtarget_Joint5", "Qddtarget_Joint6",
                                        "Itarget_Joint1", "Itarget_Joint2", "Itarget_Joint3", "Itarget_Joint4", "Itarget_Joint5", "Itarget_Joint6",
                                        "Mtarget_Joint1", "Mtarget_Joint2", "Mtarget_Joint3", "Mtarget_Joint4", "Mtarget_Joint5", "Mtarget_Joint6",
                                        "Qactual_Joint1", "Qactual_Joint2", "Qactual_Joint3", "Qactual_Joint4", "Qactual_Joint5", "Qactual_Joint6",
                                        "QDactual_Joint1", "QDactual_Joint2", "QDactual_Joint3", "QDactual_Joint4", "QDactual_Joint5", "QDactual_Joint6",
                                        "Iactual_Joint1", "Iactual_Joint2", "Iactual_Joint3", "Iactual_Joint4", "Iactual_Joint5", "Iactual_Joint6",
                                        "Icontrol_Joint1", "Icontrol_Joint2", "Icontrol_Joint3", "Icontrol_Joint4", "Icontrol_Joint5", "Icontrol_Joint6",
                                        "ToolXactual", "ToolYactual", "ToolZactual", "ToolRXactual", "ToolRYactual", "ToolRZactual",
                                        "TCPspeedActual_Joint1", "TCPspeedActual_Joint2", "TCPspeedActual_Joint3", "TCPspeedActual_Joint4", "TCPspeedActual_Joint5", "TCPspeedActual_Joint6",
                                        "TCPforce_Joint1", "TCPforce_Joint2", "TCPforce_Joint3", "TCPforce_Joint4", "TCPforce_Joint5", "TCPforce_Joint6",
                                        "ToolVectorTarget_Joint1", "ToolVectorTarget_Joint2", "ToolVectorTarget_Joint3", "ToolVectorTarget_Joint4", "ToolVectorTarget_Joint5", "ToolVectorTarget_Joint6",
                                        "TCPspeedTarget_Joint1", "TCPspeedTarget_Joint2", "TCPspeedTarget_Joint3", "TCPspeedTarget_Joint4", "TCPspeedTarget_Joint5", "TCPspeedTarget_Joint6",
                                        "DigitalInputBits",
                                        "MotorTemperature_Joint1", "MotorTemperature_Joint2", "MotorTemperature_Joint3", "MotorTemperature_Joint4", "MotorTemperature_Joint5", "MotorTemperature_Joint6",
                                        "ControllerTimer",
                                        "TestValue",
                                        "RobotMode",
                                        "JointMode_Joint1", "JointMode_Joint2", "JointMode_Joint3", "JointMode_Joint4", "JointMode_Joint5", "JointMode_Joint6",
                                        "SafetyMode",
                                        "InternalURuseOnly", "InternalURuseOnly", "InternalURuseOnly", "InternalURuseOnly", "InternalURuseOnly", "InternalURuseOnly",
                                        "ToolAccelerometer_X", "ToolAccelerometer_Y", "ToolAccelerometer_Z",
                                        "InternalURuseOnly", "InternalURuseOnly", "InternalURuseOnly", "InternalURuseOnly", "InternalURuseOnly", "InternalURuseOnly",
                                        "SpeedScaling",
                                        "LinearMomentumNorm",
                                        "InternalURuseOnly",
                                        "InternalURuseOnly",
                                        "Vmain",
                                        "Vrobot",
                                        "Irobot",
                                        "Vactual_Joint1", "Vactual_Joint2", "Vactual_Joint3", "Vactual_Joint4", "Vactual_Joint5", "Vactual_Joint6",
                                        "DigitalOutputs",
                                        "ProgramState",
                                        "ElbowPosition_X", "ElbowPosition_Y", "ElbowPosition_Z",
                                        "ElbowVelocity_X", "ElbowVelocity_Y", "ElbowVelocity_Z",
                                        "SafetyStatus",
                                        "InternalURuseOnly",
                                        "InternalURuseOnly",
                                        "InternalURuseOnly",
                                        "PayloadMass",
                                        "PayloadCog_X", "PayloadCog_Y", "PayloadCog_Z",
                                        "PayloadInertia_X", "PayloadInertia_Y", "PayloadInertia_Z", "PayloadInertia_RX", "PayloadInertia_RY", "PayloadInertia_RZ"]

        if self.RealTimeClientInterfaceVersionNumberString == "<3.0":
            self.PacketKeywordStringsList_ToUseNow = deepcopy(self.PacketKeywordStringsList_UpToRealTimeClientInterfaceVersion_BelowVersion_3dot0)
        else:
            self.PacketKeywordStringsList_ToUseNow = deepcopy(self.PacketKeywordStringsList_UpToRealTimeClientInterfaceVersion_3dot0_to_5dot10)

        self.RealTimeClientInterface_NumberOfBytesPerMessage = self.RealTimeClientInterfaceVersionHistoryNumberOfValuesAndBytesDict[self.RealTimeClientInterfaceVersionNumberString]["NumberOfBytes"]
        print("RealTimeClientInterface, NumberOfBytesPerMessage: " + str(self.RealTimeClientInterface_NumberOfBytesPerMessage))

        self.RealTimeClientInterface_NumberOfValuesPerMessage = self.RealTimeClientInterfaceVersionHistoryNumberOfValuesAndBytesDict[self.RealTimeClientInterfaceVersionNumberString]["NumberOfValues"]
        print("RealTimeClientInterface, NumberOfValuesPerMessage: " + str(self.RealTimeClientInterface_NumberOfValuesPerMessage))

        self.RealTimeClientInterface_LastValueInMessage = self.RealTimeClientInterfaceVersionHistoryNumberOfValuesAndBytesDict[self.RealTimeClientInterfaceVersionNumberString]["LastValue"]
        print("RealTimeClientInterface, LastValueInMessage: " + str(self.RealTimeClientInterface_LastValueInMessage))

        self.PacketKeywordStringsList = list(self.PacketKeywordStringsList_ToUseNow[:(self.RealTimeClientInterface_NumberOfValuesPerMessage)])
        print("Length of self.PacketKeywordStringsList = " + str(len(self.PacketKeywordStringsList)))
        print("Length of self.PacketKeywordStringsList_ToUseNow = " + str(len(self.PacketKeywordStringsList_ToUseNow)))

        self.PacketDict = dict()
        for KeywordString in self.PacketKeywordStringsList:
            self.PacketDict[KeywordString] = "-11111.0"
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.ToolTip6DOFpose_ToBeSet = [-11111.0]*6
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.JointControlModeListInt = [-1]*6
        self.JointControlModeListString = ["NotYetReceived"]*6

        self.JointControlModeListPossibilities = ["CONTROL_MODE_POSITION", #0, CONTROL_MODE_POSITION
                                                 "CONTROL_MODE_TEACH", #1, CONTROL_MODE_TEACH
                                                 "CONTROL_MODE_FORCE", #2, CONTROL_MODE_FORCE
                                                 "CONTROL_MODE_TORQUE"] #3, CONTROL_MODE_TORQUE

        # 255 = force
        # 253 = position
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.PrintToGui_Label_TextInputHistory_List = [" "] * self.NumberOfPrintLines
        self.PrintToGui_Label_TextInput_Str = ""
        self.GUI_ready_to_be_updated_flag = 0
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.MostRecentDataDict = dict()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.OpenTCPsocket_DedicatedDashboardEStop()
        self.OpenTCPsocket_RxAndTx()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if self.URarm_ConnectedFlag_DedicatedTx == 1:
            self.DedicatedTxThread_ThreadingObject = threading.Thread(target=self.DedicatedTxThread, args=())
            self.DedicatedTxThread_ThreadingObject.start()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if self.URarm_ConnectedFlag_DedicatedRx == 1:
            self.DedicatedRxThread_ThreadingObject = threading.Thread(target=self.DedicatedRxThread, args=())
            self.DedicatedRxThread_ThreadingObject.start()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if self.URarm_ConnectedFlag_DedicatedTx == 1 or self.URarm_ConnectedFlag_DedicatedRx == 1:

            ##########################################
            if self.USE_GUI_FLAG == 1:
                self.StartGUI()
            ##########################################

            ##########################################
            self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1
            ##########################################

        #########################################################
        #########################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __del__(self):
        pass
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def getPreciseSecondsTimeStampString(self):
        ts = time.time()

        return ts
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def PassThrough0and1values_ExitProgramOtherwise(self, InputNameString, InputNumber):

        try:
            InputNumber_ConvertedToFloat = float(InputNumber)
        except:
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()

        try:
            if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1:
                return InputNumber_ConvertedToFloat
            else:
                input("PassThrough0and1values_ExitProgramOtherwise Error. '" +
                          InputNameString +
                          "' must be 0 or 1 (value was " +
                          str(InputNumber_ConvertedToFloat) +
                          "). Press any key (and enter) to exit.")

                sys.exit()
        except:
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def PassThroughFloatValuesInRange_ExitProgramOtherwise(self, InputNameString, InputNumber, RangeMinValue, RangeMaxValue):
        try:
            InputNumber_ConvertedToFloat = float(InputNumber)
        except:
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()

        try:
            if InputNumber_ConvertedToFloat >= RangeMinValue and InputNumber_ConvertedToFloat <= RangeMaxValue:
                return InputNumber_ConvertedToFloat
            else:
                input("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" +
                          InputNameString +
                          "' must be in the range [" +
                          str(RangeMinValue) +
                          ", " +
                          str(RangeMaxValue) +
                          "] (value was " +
                          str(InputNumber_ConvertedToFloat) + "). Press any key (and enter) to exit.")

                sys.exit()
        except:
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()
    ##########################################################################################################
    ##########################################################################################################

    ###########################################################################################################
    ##########################################################################################################
    def LimitNumber_FloatOutputOnly(self, min_val, max_val, test_val):
        if test_val > max_val:
            test_val = max_val

        elif test_val < min_val:
            test_val = min_val

        else:
            test_val = test_val

        test_val = float(test_val)

        return test_val
    ##########################################################################################################
    ##########################################################################################################

    ###########################################################################################################
    ##########################################################################################################
    def ListFunctionNamesInClass(self, ClassToBeChecked, FilterFunctionNamesWithLeadingUnderscoresFlag = 1):
        FunctionListOfStrings_All = list()
        FunctionListOffFunctions_All = list()

        FunctionDictOfFunctions = dict()

        for FunctionName, Function in ClassToBeChecked.__dict__.items():
            if isinstance(Function, types.FunctionType):
                if FilterFunctionNamesWithLeadingUnderscoresFlag == 0:
                    print(type(Function))
                    FunctionListOfStrings_All.append(FunctionName)
                    FunctionListOffFunctions_All.append(Function)
                    FunctionDictOfFunctions[FunctionName] = Function
                else:
                    if FunctionName[0] != "_":
                        FunctionListOfStrings_All.append(FunctionName)
                        FunctionListOffFunctions_All.append(Function)
                        FunctionDictOfFunctions[FunctionName] = Function

        return FunctionDictOfFunctions
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TellWhichFileWereIn(self):

        #We used to use this method, but it gave us the root calling file, not the class calling file
        #absolute_file_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        #filename = absolute_file_path[absolute_file_path.rfind("\\") + 1:]

        frame = inspect.stack()[1]
        filename = frame[1][frame[1].rfind("\\") + 1:]
        filename = filename.replace(".py","")

        return filename
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ComputeListNorm(self, InputList):
        #print("ComputeListNorm: InputList = " + str(InputList))
    
        norm = -1
    
        try:
            ElementsSquaredSum = 0.0
            for InputElement in InputList:
                InputElement = float(InputElement)
                ElementsSquaredSum = ElementsSquaredSum + InputElement * InputElement
    
            norm = math.sqrt(ElementsSquaredSum)
    
        except:
            exceptions = sys.exc_info()[0]
            print("ComputeListNorm Error, Exceptions: %s" % exceptions)
    
        return norm
    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    def NormalizeListToUnitLength(self, InputList):
        OutputList = list(InputList)
    
        try:
            ElementsSquaredSum = 0.0
            for InputElement in InputList:
                InputElement = float(InputElement)
                ElementsSquaredSum = ElementsSquaredSum + InputElement * InputElement
    
            norm = math.sqrt(ElementsSquaredSum)
    
            for i, InputElement in enumerate(InputList):
                InputElement = float(InputElement)
                OutputList[i] = InputElement / norm
    
        except:
            exceptions = sys.exc_info()[0]
            print("NormalizeListToUnitLength Error, Exceptions: %s" % exceptions)
    
        return OutputList
    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    def MultiplyListOfNumbersByScalar(self, InputList, ScalarToMultiplyBy):
        OutputList = list(InputList)
    
        try:
            for i, OutputElement in enumerate(OutputList):
                OutputElementFloat = float(OutputElement)
                OutputList[i] = ScalarToMultiplyBy*OutputElementFloat
    
        except:
            exceptions = sys.exc_info()[0]
            print("MultiplyListOfNumbersByScalar Error, Exceptions: %s" % exceptions)
            return list()
    
        return OutputList
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def IsInputList(self, InputToCheck):

        result = isinstance(InputToCheck, list)
        return result
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def IsInputListOfNumbers(self, InputToCheck):

        if isinstance(InputToCheck, list) == 1:
            for element in InputToCheck:
                if isinstance(element, int) == 0 and isinstance(element, float) == 0:
                    return 0
        else:
            return 0

        return 1  # If InputToCheck was a list and no element failed to be a float or int, then return a success/1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ConvertListOfValuesDegToRad(self, ListOfValuesDegToRadToBeConverted):

        ListOfValuesRadToBeReturned = list()

        try:
            if self.IsInputList(ListOfValuesDegToRadToBeConverted) == 0:
                ListOfValuesDegToRadToBeConverted = list([ListOfValuesDegToRadToBeConverted])

            for index, value in enumerate(ListOfValuesDegToRadToBeConverted):
                ListOfValuesRadToBeReturned.append(value*math.pi/180.0)

            return ListOfValuesRadToBeReturned

        except:
            exceptions = sys.exc_info()[0]
            print("ConvertListOfValuesDegToRad Exceptions: %s" % exceptions)
            return ListOfValuesRadToBeReturned
            #traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def OpenTCPsocket_RxAndTx(self):

        ##########################################################################################################
        try:
            self.TCPsocketObject_DedicatedTx = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.TCPsocketObject_DedicatedTx.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) #Send immediately without waiting for buffer to fill. https://stackoverflow.com/questions/31826762/python-socket-send-immediately
            self.TCPsocketObject_DedicatedTx.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.TCPsocketObject_DedicatedTx.settimeout(self.IPV4_TimeoutDurationSeconds)
            self.TCPsocketObject_DedicatedTx.connect((self.IPV4_address, self.IPV4_TxPort))

            self.URarm_ConnectedFlag_DedicatedTx = 1

            print("OpenTCPsocket_RxAndTx succeeded on port " + str(self.IPV4_TxPort) + "!")

        except:
            self.URarm_ConnectedFlag_DedicatedTx = 0
            exceptions = sys.exc_info()[0]
            print("OpenTCPsocket_RxAndTx ERROR: Could not open Tx on port " + str(self.IPV4_TxPort) + ", Exceptions: %s" % exceptions)

            ########################
            for i in range(0, 10):
                print("@@@@@@@@@@ VERIFY NETWORK SETTINGS @@@@@@@@@@")
            ########################

            traceback.print_exc()
        ##########################################################################################################

        ##########################################################################################################
        try:
            self.TCPsocketObject_DedicatedRx = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.TCPsocketObject_DedicatedRx_BufferSizeInBytes = int(self.IPV4_NumberOfRxMessagesToBuffers*self.RealTimeClientInterface_NumberOfBytesPerMessage)
            self.TCPsocketObject_DedicatedRx.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.TCPsocketObject_DedicatedRx_BufferSizeInBytes)
            self.TCPsocketObject_DedicatedRx.settimeout(self.IPV4_TimeoutDurationSeconds)

            print("OpenTCPsocket_RxAndTx: Set IPV4_NumberOfRxMessagesToBuffers = " +
                    str(self.IPV4_NumberOfRxMessagesToBuffers) +
                    ", to give a buffer size of " +
                    str(self.TCPsocketObject_DedicatedRx_BufferSizeInBytes) +
                    " bytes.")
            ###################

            self.TCPsocketObject_DedicatedRx.connect((self.IPV4_address, self.IPV4_RxPort))

            self.URarm_ConnectedFlag_DedicatedRx = 1

            print("OpenTCPsocket_RxAndTx succeeded on port " + str(self.IPV4_RxPort) + "!")

        except:
            self.URarm_ConnectedFlag_DedicatedRx = 0
            exceptions = sys.exc_info()[0]
            print("OpenTCPsocket_RxAndTx ERROR: Could not open Rx on port " + str(self.IPV4_RxPort) + ", Exceptions: %s" % exceptions)

            ########################
            for i in range(0, 10):
                print("@@@@@@@@@@ VERIFY NETWORK SETTINGS @@@@@@@@@@")
            ########################

            traceback.print_exc()
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CloseTCPsocket_RxAndTx(self):

        try:
            self.TCPsocketObject_DedicatedRx.close()
            self.URarm_ConnectedFlag_DedicatedRx = 0
            self.RxPacketsCounter_Total = 0
            self.RxPacketsCounter_WrongSize = 0
            self.RxPackets_PercentWrongSize = 0.0

            self.TCPsocketObject_DedicatedTx.close()
            self.URarm_ConnectedFlag_DedicatedTx = 0
        except:
            exceptions = sys.exc_info()[0]
            print("CloseTCPsocket_RxAndTx, Exceptions: %s" % exceptions)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def OpenTCPsocket_DedicatedDashboardEStop(self):

        try:
            self.TCPsocketObject_DedicatedDashboardEStop = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self.TCPsocketObject_DedicatedDashboardEStop.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) #Send immediately without waiting for buffer to fill. https://stackoverflow.com/questions/31826762/python-socket-send-immediately
            self.TCPsocketObject_DedicatedDashboardEStop.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.TCPsocketObject_DedicatedDashboardEStop.settimeout(self.IPV4_TimeoutDurationSeconds)

            self.TCPsocketObject_DedicatedDashboardEStop.connect((self.IPV4_address, 29999))

            self.URarm_ConnectedFlag_DedicatedDashboardEStop = 1

            print("OpenTCPsocket_DedicatedDashboardEStop succeeded!")

        except:
            self.URarm_ConnectedFlag_DedicatedDashboardEStop = 0
            exceptions = sys.exc_info()[0]
            print("OpenTCPsocket_DedicatedDashboardEStop ERROR: Could not open TCPsocketObject_DedicatedDashboardEStop, Exceptions: %s" % exceptions)
            for i in range(0, 10):
                print("@@@@@@@@@@ VERIFY THAT CHECKPOINT IS NOT ON @@@@@@@@@@")

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CloseTCPsocket_DedicatedDashboardEStop(self):

        try:
            self.TCPsocketObject_DedicatedDashboardEStop.close()
            self.URarm_ConnectedFlag_DedicatedDashboardEStop = 0
        except:
            exceptions = sys.exc_info()[0]
            print("CloseTCPsocket_DedicatedDashboardEStop ERROR: Could not open TCPsocketObject_DedicatedDashboardEStop, Exceptions: %s" % exceptions)
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ResetTCPsockets(self):

        if self.URarm_ConnectedFlag_CombinedRxAndTx == 1:

            self.CloseTCPsocket_RxAndTx()
            time.sleep(0.25)
            self.OpenTCPsocket_RxAndTx()

        if self.URarm_ConnectedFlag_DedicatedDashboardEStop == 1:
            self.CloseTCPsocket_DedicatedDashboardEStop()
            time.sleep(0.25)
            self.OpenTCPsocket_DedicatedDashboardEStop()

        print("ResetTCPsockets event fired!")
    ##########################################################################################################
    ##########################################################################################################

    ###########################################################################################################
    ##########################################################################################################
    def SendTxMessage(self, MessageToSend, IgnoreNewDataIfQueueIsFullFlag = 1):

        if self.DedicatedTxThread_TxMessageToSend_Queue.qsize() < self.DedicatedTxThread_TxMessageToSend_Queue_MaxSize:
            self.DedicatedTxThread_TxMessageToSend_Queue.put(MessageToSend)
        else:
            #print("SendTxMessage queue is full!")
            if IgnoreNewDataIfQueueIsFullFlag != 1:
                dummy = self.DedicatedTxThread_TxMessageToSend_Queue.get() #makes room for one more message
                self.DedicatedTxThread_TxMessageToSend_Queue.put(MessageToSend) #backfills that message with new data
    
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ########################################################################################################## unicorn
    def LoadMostRecentDataDictIntoMultiprocessingQueueTx(self, MultiprocessingQueue_Tx_Local, IgnoreNewDataIfQueueIsFullFlag = 1):

        try:
            ##########################################################################################################
            # print("LoadMostRecentDataDictIntoMultiprocessingQueueTx event fired!")

            #deepcopy is required (beyond .copy()) as MostRecentDataDict contains lists.

            if MultiprocessingQueue_Tx_Local.qsize() < self.MultiprocessingQueue_Tx_MaxSize:
                MultiprocessingQueue_Tx_Local.put(deepcopy(self.MostRecentDataDict))

            else:
                if IgnoreNewDataIfQueueIsFullFlag != 1:
                    dummy = MultiprocessingQueue_Tx_Local.get()  # makes room for one more message
                    MultiprocessingQueue_Tx_Local.put(deepcopy(self.MostRecentDataDict))  # backfills that message with new data

            ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("LoadMostRecentDataDictIntoMultiprocessingQueueTx, Exceptions: %s" % exceptions)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentDataDict(self):

        try:
            if self.MultiprocessingQueue_Tx.empty() != 1:
                return self.MultiprocessingQueue_Tx.get(FALSE)
            else:
                return dict()
        except:
            exceptions = sys.exc_info()[0]
            #print("GetMostRecentDataDict, Exceptions: %s" % exceptions)
            return dict()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StopMotion_JointSpace(self, Acceleration = -11111.0):

        if Acceleration == -11111.0:
            Acceleration = self.Acceleration

        Message = "stopj(" + str(Acceleration) + ")\n"
        print("StopMotion_JointSpace issuing Message: '" + Message + "'")
        self.SendTxMessage(Message)
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ClearProtectiveStop(self):

        #MANUAL STATES: "The unlock protective stop command fails if less than 5 seconds has passed since the protective stop occurred."

        for i in range(0, 1):

            if self.RealTimeClientInterfaceVersionNumberFloat >= 1.6: #Only supported in URscript versions >= 1.6
                self.TCPsocketObject_DedicatedDashboardEStop.send("close popup\n".encode('utf-8')) #Python3 requires you to use '.encode('utf-8')' on strings before they can be sent to the socket.

            if self.RealTimeClientInterfaceVersionNumberFloat >= 3.1: #Only supported in URscript versions >= 3.1
                self.TCPsocketObject_DedicatedDashboardEStop.send("unlock protective stop\n".encode('utf-8')) #Python3 requires you to use '.encode('utf-8')' on strings before they can be sent to the socket.
                time.sleep(0.002)

        print("ClearProtectiveStop event fired!")
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ClearViolationOrFault_RestartSafety(self):

        for i in range(0, 1):
            if self.RealTimeClientInterfaceVersionNumberFloat >= 3.1:  # Only supported in URscript versions >= 3.1
                self.TCPsocketObject_DedicatedDashboardEStop.send("close safety popup\n".encode('utf-8'))
                time.sleep(0.25)

            if self.RealTimeClientInterfaceVersionNumberFloat >= 3.0:  # Only supported in URscript versions >= 3.0
                self.TCPsocketObject_DedicatedDashboardEStop.send("power on\n".encode('utf-8'))

        print("ClearViolationOrFault_RestartSafety event fired!")
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def RestartSafety(self):

        for i in range(0, 1):

            if self.RealTimeClientInterfaceVersionNumberFloat >= 3.1:  # Only supported in URscript versions >= 3.1
                self.TCPsocketObject_DedicatedDashboardEStop.send("close safety popup\n".encode('utf-8'))
                time.sleep(0.5)

            if self.RealTimeClientInterfaceVersionNumberFloat >= 3.7:  # Only supported in URscript versions >= 3.7
                self.TCPsocketObject_DedicatedDashboardEStop.send("restart safety\n".encode('utf-8')) #Python3 requires you to use '.encode('utf-8')' on strings before they can be sent to the socket.

        print("RestartSafety event fired!")
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StartRobot(self):

        for i in range(0, 1):

            if self.RealTimeClientInterfaceVersionNumberFloat >= 3.0:  # Only supported in URscript versions >= 3.0
                self.TCPsocketObject_DedicatedDashboardEStop.send("power on\n".encode('utf-8'))
                time.sleep(1.0)
                self.TCPsocketObject_DedicatedDashboardEStop.send("brake release\n".encode('utf-8'))

        print("StartRobot event fired!")
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def PositionControl_MoveJ_MoveThroughListOfPoses(self, ListOfDicts_Waypoints):

        #Input Format = dict([("JointAngleList_Rad", JointAngleList_Rad), ("Acceleration", Acceleration), ("Velocity", Velocity), ("TimeDurationSec", TimeDurationSec),("BlendRadiusMeters", BlendRadiusMeters)]))

        self.SendTxMessage(self.MoveJ_CreateMessage_ListOfDictsMoveJWaypoints(ListOfDicts_Waypoints))

        print("PositionControl_MoveJ_MoveThroughListOfPoses event fired for ListOfDicts_Waypoints: " + str(ListOfDicts_Waypoints))

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def PositionControl_ServoJ_MoveThroughListOfPoses(self, ListOfDicts_Waypoints):

        #Input Format = dict([("JointAngleList_Rad", JointAngleList_Rad), ("Acceleration", Acceleration), ("Velocity", Velocity), ("TimeDurationSec", TimeDurationSec),("BlendRadiusMeters", BlendRadiusMeters)]))

        self.SendTxMessage(self.ServoJ_CreateMessage_ListOfDictsMoveJWaypoints(ListOfDicts_Waypoints))

        #print("PositionControl_ServoJ_MoveThroughListOfPoses event fired for ListOfDicts_Waypoints: " + str(ListOfDicts_Waypoints))

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def PositionControl_ServoC_MoveThroughListOfPoses(self, ListOfDicts_Waypoints):
        #print("PositionControl_ServoC_MoveThroughListOfPoses, ListOfDicts_Waypoints: " + str(ListOfDicts_Waypoints) + ", Type: " + str(type(ListOfDicts_Waypoints)))

        #Input Format = dict([("ToolTip6DOFpose", ToolTip6DOFpose), ("Acceleration", Acceleration), ("Velocity", Velocity), ("TimeDurationSec", TimeDurationSec),("BlendRadiusMeters", BlendRadiusMeters)]))

        self.SendTxMessage(self.ServoC_CreateMessage_ListOfDictsMoveJWaypoints(ListOfDicts_Waypoints))

        #print("PositionControl_ServoC_MoveThroughListOfPoses event fired for ListOfDicts_Waypoints: " + str(ListOfDicts_Waypoints))

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def PositionControl_MoveL_MoveThroughListOfPoses(self, ListOfDicts_Waypoints):

        #Input Format = dict([("PoseCartesianCoordinates", PoseCartesianCoordinates), ("Acceleration", Acceleration), ("Velocity", Velocity), ("TimeDurationSec", TimeDurationSec),("BlendRadiusMeters", BlendRadiusMeters)]))

        self.SendTxMessage(self.MoveL_CreateMessage_ListOfDictsMoveLWaypoints(ListOfDicts_Waypoints))

        #print("PositionControl_MoveL_MoveThroughListOfPoses event fired for ListOfDicts_Waypoints: " + str(ListOfDicts_Waypoints))

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def MoveSafelyToStartingPoseViaMultipointSequence(self):

        #self.PositionControl_ServoJ_MoveThroughListOfPoses(self.PositionControl_ServoJ_MoveThroughListOfPoses_SafeReturnToStartingPoseFromAnywhere)
        self.PositionControl_MoveJ_MoveThroughListOfPoses(self.PositionControl_ServoJ_MoveThroughListOfPoses_SafeReturnToStartingPoseFromAnywhere)

        print("MoveSafelyToStartingPoseViaMultipointSequence EVENT FIRED!")
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def MoveToStartingPose(self):

        self.SendTxMessage(self.ServoJ_CreateMessage_ListOfDictsMoveJWaypoints(dict([("JointAngleList_Rad", self.StartingPoseJointAngleList_Rad),("Acceleration", self.Acceleration),("Velocity", self.Velocity), ("TimeDurationSec", 5.0)])))

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def MoveJ_CreateMessage_ListOfDictsMoveJWaypoints(self, ListOfDictsMoveJWaypoints, UserNotes=""):

        # $$$$ THE SYNTAX OF THIS FUNCTION IS SPECIFIC TO URscript SOFTWARE VERSION 1.8
        '''
        Move to position (linear in joint-space) When using this command, the
        robot must be at standstill or come from a movej og movel with a blend.
        The speed and acceleration parameters controls the trapezoid speed
        profile of the move. The $t$ parameters can be used in stead to set the
        time for this move. Time setting has priority over speed and acceleration
        settings. The blend radius can be set with the $r$ parameters, to avoid
        the robot stopping at the point. However, if he blend region of this mover
        overlaps with previous or following regions, this move will be skipped, and
        an ’Overlapping Blends’ warning message will be generated.
        Parameters
        q: joint positions (q can also be specified as a pose, then
        inverse kinematics is used to calculate the corresponding
        joint positions)
        a: joint acceleration of leading axis [rad/sˆ2]
        v: joint speed of leading axis [rad/s]
        t: time [S]
        r: blend radius [m]
        '''

        if self.IsInputList(ListOfDictsMoveJWaypoints) == 0:
            ListOfDictsMoveJWaypoints = list([ListOfDictsMoveJWaypoints])

        Message = ""
        ###################################
        for WaypointDict in ListOfDictsMoveJWaypoints:

            ####
            if "JointAngleList_Deg" not in WaypointDict and "JointAngleList_Rad" in WaypointDict:
                JointAngleList_Rad = WaypointDict["JointAngleList_Rad"]

            elif "JointAngleList_Deg" in WaypointDict and "JointAngleList_Rad" not in WaypointDict:
                JointAngleList_Rad = list(self.ConvertListOfValuesDegToRad(WaypointDict["JointAngleList_Deg"]))

            else:
                print("MoveJ_CreateMessage_ListOfDictsMoveJWaypoints ERROR: Must input EITHER JointAngleList_Deg OR JointAngleList_Rad.")
                return ""
            ####

            ####
            Message = Message + "movej(" + str(JointAngleList_Rad) \
            ####

            ####
            if "Acceleration" in WaypointDict:
                Acceleration = WaypointDict["Acceleration"]
            else:
                Acceleration = self.Acceleration #Go with what the class already has set for acceleration

            Acceleration = self.LimitNumber_FloatOutputOnly(self.Acceleration_MinValue, self.Acceleration_MaxValue, Acceleration)
            Message = Message + ",a=" + str(Acceleration)
            ####

            ####
            if "TimeDurationSec" not in WaypointDict: #Time setting has priority over speed and acceleration settings.

                if "Velocity" in WaypointDict:
                    Velocity = WaypointDict["Velocity"]
                else:
                    Velocity = self.Velocity #Go with what the class already has set for velocity

                Velocity = self.LimitNumber_FloatOutputOnly(self.Velocity_MinValue, self.Velocity_MaxValue, Velocity)
                Message = Message + ",v=" + str(Velocity) #Go with what the class already has set for velocity
            ####

            ####
            if "TimeDurationSec" in WaypointDict: #Time setting has priority over speed and acceleration settings.
                TimeDurationSec = WaypointDict["TimeDurationSec"]
                Message = Message + ",t=" + str(TimeDurationSec)
            ####

            ####
            if "BlendRadiusMeters" in WaypointDict:
                BlendRadiusMeters = WaypointDict["BlendRadiusMeters"]
                Message = Message + ",r=" + str(BlendRadiusMeters)
            ####

            ####
            Message = Message + ")\n"
            ####

        ###################################

        return Message
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ServoJ_CreateMessage_ListOfDictsMoveJWaypoints(self, ListOfDictsServoJWaypoints):

        '''
        if PoseIsInToolSpaceFlag == 1, then the message format will be:
        ****
        def servoj_custom():
            x = p[0.445, 0.191, 0.5303887773609804, -1.569, 0.033, 0.068]
            q = get_inverse_kin(x)
            servoj(q,a=0,v=0,t=0.01,lookahead_time=0.01,gain=200)
        end
        ****

        if PoseIsInToolSpaceFlag == 0, then the message format will be:
        ****
        def servoj_custom():
            servoj([3.141, -1.44, 1.64, -3.264, 0.023, -0.012],a=0,v=0,t=10.0,lookahead_time=0.01,gain=200)
        end
        ****
        '''

        #########################################################
        if self.IsInputList(ListOfDictsServoJWaypoints) == 0:
            ListOfDictsServoJWaypoints = list([ListOfDictsServoJWaypoints])
        #########################################################

        Message = "def servoj_custom():\n"

        for WaypointDict in ListOfDictsServoJWaypoints:

            #########################################################
            if "PoseIsInToolSpaceFlag" in WaypointDict:
                PoseIsInToolSpaceFlag = WaypointDict["PoseIsInToolSpaceFlag"]

            else:
                PoseIsInToolSpaceFlag = 0
            #########################################################

            #########################################################
            #########################################################
            if PoseIsInToolSpaceFlag == 0:

                #########################################################
                if "JointAngleList_Deg" not in WaypointDict and "JointAngleList_Rad" in WaypointDict:
                    JointAngleList_Rad = WaypointDict["JointAngleList_Rad"]

                elif "JointAngleList_Deg" in WaypointDict and "JointAngleList_Rad" not in WaypointDict:
                    JointAngleList_Rad = list(self.ConvertListOfValuesDegToRad(WaypointDict["JointAngleList_Deg"]))

                else:
                    print("ServoJ_CreateMessage_ListOfDictsServoJWaypoints ERROR: Must input EITHER JointAngleList_Deg OR JointAngleList_Rad.")
                    return ""
                #########################################################

                #########################################################
                Message = Message + "  servoj(" + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(JointAngleList_Rad, 0, 3)
                #########################################################

            else:

                #########################################################
                if "ToolTip6DOFpose" in WaypointDict:
                    ToolTip6DOFpose = WaypointDict["ToolTip6DOFpose"]
                else:
                    print("ServoJ_CreateMessage_ListOfDictsServoJWaypoints ERROR: Must input ToolTip6DOFpose if PoseIsInToolSpaceFlag = 1.")
                    return ""
                #########################################################

                #########################################################
                self.ToolTip6DOFpose_ToBeSet = ToolTip6DOFpose
                #########################################################

                #########################################################
                Message = Message + \
                                "  x_NextPoseCartesianSpace = p" + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(ToolTip6DOFpose, 0, 3) + "\n" +\
                                "  q_NextPoseJointSpace = get_inverse_kin(x_NextPoseCartesianSpace)\n" + \
                                "  q_CurrentPoseJointSpace = get_actual_joint_positions()\n" + \
                                "  MoveFlag = 1\n" + \
                                "  i = 0\n" + \
                                "  while i < 5:\n" + \
                                "    JointAngleDistance = norm(q_NextPoseJointSpace[i] - q_CurrentPoseJointSpace[i])\n" + \
                                "    if JointAngleDistance > " + str(self.ServoJ_JointAngleDistance_Threshold) + ":\n" + \
                                "        MoveFlag = 0\n" + \
                                "        popup(\"EXCEEDED THRESHOLD\", blocking=True)\n" + \
                                "    end\n" +\
                                "    i = i + 1\n" + \
                                "  end\n" + \
                                "  if MoveFlag == 1:\n" + \
                                "    servoj(q_NextPoseJointSpace"
                                #"    PopupMessageString = to_str(JointAngleDistance)\n" + \
                                #                                "    popup(PopupMessageString, blocking=True)\n" + \
                #########################################################

            #########################################################
            #########################################################

            #########################################################
            Message = Message + ",a=" + str(0) #a: NOT used in current version, so we're just sending 0
            #########################################################

            #########################################################
            Message = Message + ",v=" + str(0) #v: NOT used in current version, so we're just sending 0
            #########################################################

            #########################################################
            if "TimeDurationSec" in WaypointDict:
                TimeDurationSec = WaypointDict["TimeDurationSec"]
                Message = Message + ",t=" + str(TimeDurationSec)
            else:
                print("ServoJ_CreateMessage_ListOfDictsServoJWaypoints ERROR: Must specify 'TimeDurationSec'.")
                return ""
            #########################################################

            #########################################################
            #########################################################
            if self.ControllerBoxVersion >= 3:
                #########################################################
                if "lookahead_time" in WaypointDict:
                    lookahead_time = WaypointDict["lookahead_time"]
                else:
                    lookahead_time = 0.1  # Default value = 0.1

                Message = Message + ",lookahead_time=" + str(lookahead_time)
                #########################################################

                #########################################################
                if "gain" in WaypointDict:
                    gain = WaypointDict["gain"]
                else:
                    gain = 300  #Default value = 300

                Message = Message + ",gain=" + str(gain)
                #########################################################

            #########################################################
            #########################################################

            #########################################################
            Message = Message  + ")\n" + \
                      "    end\n" + \
                      "end\n"
            #########################################################

        #########################################################
        #########################################################

        #print("ServoJ_CreateMessage_ListOfDictsServoJWaypoints: " + str(Message))

        return Message
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ServoC_CreateMessage_ListOfDictsMoveJWaypoints(self, ListOfDictsServoCWaypoints):

        #$$$$ THE SYNTAX OF THIS FUNCTION IS SPECIFIC TO URscript SOFTWARE VERSION 1.8
        '''
        Servo Circular
        Servo to position (circular in tool-space). Accelerates to and moves with
        constant tool speed v.
        Parameters
        pose: target pose (pose can also be specified as joint
        positions, then forward kinematics is used to calculate
        the corresponding pose)
        a: tool acceleration [m/sˆ2]
        v: tool speed [m/s]
        r: blend radius (of target pose) [m]
        '''

        if self.IsInputList(ListOfDictsServoCWaypoints) == 0:
            ListOfDictsServoCWaypoints = list([ListOfDictsServoCWaypoints])

        ####
        Message = ""
        ####

        for WaypointDict in ListOfDictsServoCWaypoints:
            ####

            ###################################
            if "ToolTip6DOFpose" in WaypointDict:
                ToolTip6DOFpose = WaypointDict["ToolTip6DOFpose"]
                Message = Message + "servoc(p" + str(ToolTip6DOFpose)
            else:
                print("ServoC_CreateMessage_ListOfDictsMoveLWaypoints ERROR, ListOfDictsMoveLWaypoints must contain 'ToolTip6DOFpose'")
                return ""

            ####
            if "Acceleration" in WaypointDict: #MANUAL 5.11 SAYS THAT ACCELERATION ISN'T USED CURRENTLY
                Acceleration = WaypointDict["Acceleration"]
                Message = Message + ",a=" + str(Acceleration)
            ####

            ####
            if "Velocity" in WaypointDict: #MANUAL 5.11 SAYS THAT ACCELERATION ISN'T USED CURRENTLY
                Velocity = WaypointDict["Velocity"]
                Message = Message + ",v=" + str(Velocity)
            ####


            ####
            if "BlendRadiusMeters" in WaypointDict:
                BlendRadiusMeters = WaypointDict["BlendRadiusMeters"]
                Message = Message + ",r=" + str(BlendRadiusMeters) \
            ####

            ####
            Message = Message  + ")\n"
            ####

        ###################################

        #print("ServoC_CreateMessage_ListOfDictsServoCWaypoints: " + str(Message))

        return Message
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def MoveL_CreateMessage_ListOfDictsMoveLWaypoints(self, ListOfDictsMoveLWaypoints, UserNotes=""):

        '''
        Move to position (linear in tool-space)
        See movej.
        Parameters
        pose: target pose (pose can also be specified as joint
        positions, then forward kinematics is used to calculate
        the corresponding pose)
        a: tool acceleration [m/sˆ2]
        v: tool speed [m/s]
        t: time [S]
        r: blend radius [m]
        '''

        if self.IsInputList(ListOfDictsMoveLWaypoints) == 0:
            ListOfDictsMoveLWaypoints = list([ListOfDictsMoveLWaypoints])

        Message = ""

        ###################################
        for WaypointDict in ListOfDictsMoveLWaypoints:

            ####
            if "ToolTip6DOFpose" in WaypointDict:
                ToolTip6DOFpose = WaypointDict["ToolTip6DOFpose"]
                Message = Message + "movel(p" + str(ToolTip6DOFpose)
            else:
                print("MoveL_CreateMessage_ListOfDictsMoveLWaypoints ERROR, ListOfDictsMoveLWaypoints must contain 'ToolTip6DOFpose'")
                return ""
            ####

            ####
            if "Acceleration" in WaypointDict:
                Acceleration = WaypointDict["Acceleration"]
                Message = Message + ",a=" + str(Acceleration) \
            ####

            ####
            if "Velocity" in WaypointDict:
                Velocity = WaypointDict["Velocity"]
                Message = Message + ",v=" + str(Velocity) \
            ####

            ####
            if "TimeDurationSec" in WaypointDict:
                TimeDurationSec = WaypointDict["TimeDurationSec"]
                Message = Message + ",t=" + str(TimeDurationSec)
            ####

            ####
            if "BlendRadiusMeters" in WaypointDict:
                BlendRadiusMeters = WaypointDict["BlendRadiusMeters"]
                Message = Message + ",r=" + str(BlendRadiusMeters) \
            ####

            ####
            Message = Message + ")\n"
            ####
        ###################################

        print("MoveL_CreateMessage_ListOfDictsMoveLWaypoints: " + str(Message))

        return Message
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetPayload(self, Payload_MassKG_ToBeSet, Payload_CoGmetersList_ToBeSet = [0.0, 0.0, 0.0]):

        if isinstance(Payload_MassKG_ToBeSet, int) == 1 or isinstance(Payload_MassKG_ToBeSet, float) == 1:

            if self.IsInputListOfNumbers(Payload_CoGmetersList_ToBeSet) == 1:

                if len(Payload_CoGmetersList_ToBeSet) == 3:

                    message_set_payload_mode = "set_payload(" + str(Payload_MassKG_ToBeSet)  + ", " + str(Payload_CoGmetersList_ToBeSet) + ")\n"
                    #print("message_set_payload_mode: " + str(message_set_payload_mode))

                    self.SendTxMessage(message_set_payload_mode)

                else:
                    print("SetPayload ERROR: Payload_CoGmetersList_ToBeSet must be a list of 3 numbers.")

            else:
                print("SetPayload ERROR: Payload_CoGmetersList_ToBeSet must be a list of 3 numbers.")
        else:
            print("SetPayload ERROR: Payload_MassKG_ToBeSet must be an int or float2")
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DisplayPopupMessage(self, MessageString = "MessageString", TitleString = "TitleString", WarningBooleanInteger = 0, ErrorBooleanInteger = 0, BlockingBooleanInteger = 1):

        if WarningBooleanInteger not in [0, 1]:
            print("DisplayPopupMessage: ERROR, 'WarningBooleanInteger' must be 0 or 1.")
            return

        if ErrorBooleanInteger not in [0, 1]:
            print("DisplayPopupMessage: ERROR, 'ErrorBooleanInteger' must be 0 or 1.")
            return


        if BlockingBooleanInteger not in [0, 1]:
            print("DisplayPopupMessage: ERROR, 'BlockingBooleanInteger' must be 0 or 1.")
            return

        #popup(s, title=’Popup’, warning=False, error=False, blocking=False)
        #blocking: if True, program will be suspended until "continue" is pressed
        PopupMessageCommandToSend = "popup(" +\
                                    "\"" + str(MessageString) + "\"" +\
                                    ", title=\"" + str(TitleString) + "\"" +\
                                    ", warning=" + str(bool(WarningBooleanInteger)) +\
                                    ", error=" + str(bool(ErrorBooleanInteger)) +\
                                    ", blocking=" + str(bool(BlockingBooleanInteger)) +\
                                    ")\n"

        print("DisplayPopupMessage, PopupMessageCommandToSend: " + str(PopupMessageCommandToSend))
        self.SendTxMessage(PopupMessageCommandToSend)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetFreedriveState(self, FreedriveState_ToBeSet):

        message_enter_freedrive_mode = "def enter_freedrive_mode_function_reuben():\n" + \
                                       "  while(True):\n" + \
                                       "    freedrive_mode()\n" + \
                                       "    sleep(600)\n" + \
                                       "  end\n" + \
                                       "end\n"

        message_end_freedrive_mode = "def end_freedrive_mode_function_reuben():\n" + \
                                     "  end_freedrive_mode()\n" + \
                                     "end\n"

        #message_enter_freedrive_mode = "freedrive_mode()\n" #Simple commands don't stick on the arm (stops immediately).
        #message_end_freedrive_mode = "end_freedrive_mode()\n" #Simple commands don't stick on the arm (stops immediately).

        if self.RealTimeClientInterfaceVersionNumberFloat >= 3.0: #Available on all CB3 controllers
            if FreedriveState_ToBeSet == 1:
                self.SendTxMessage(message_enter_freedrive_mode)
            else:
                self.SendTxMessage(message_end_freedrive_mode)

        self.Freedrive_State = FreedriveState_ToBeSet
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ForceControl(self, Force_XYZlist, Speed_MagnitudeMetersPerSec, StoppingDecellerationMetersPerSecSquared, DurationForWhichToApplyForceInSeconds = -11111.0, ZeroForceReadingsBeforeMoveFlag = 0):

        try:
            print("ForceControl event fired!")
            #CHECK HERE THAT LISTS ARE LISTS AND ALL VALUES ARE WITHIN BOUNDS

            #########################
            Speed_NormalizedXYZlist = self.NormalizeListToUnitLength(list(Force_XYZlist))
            print("ForceControl, Speed_NormalizedXYZlist: " + str(Speed_NormalizedXYZlist))

            print("Speed_MagnitudeMetersPerSec: " + str(Speed_MagnitudeMetersPerSec))

            Speed_LimitXYZlist = self.MultiplyListOfNumbersByScalar(Speed_NormalizedXYZlist, Speed_MagnitudeMetersPerSec)
            Speed_LimitXYZlist[1] = Speed_LimitXYZlist[1] + 0.005 #Include epison to avoid Max Position Deviation Error.
            print("ForceControl, Speed_LimitXYZlist: " + str(Speed_LimitXYZlist))

            AngularSpeedLimit = 100.0 #Must be high to allow the Roll/Pitch/Yaw to move.

            SpeedMessage = "["
            for SpeedValue in Speed_LimitXYZlist:
                SpeedMessage = SpeedMessage + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(SpeedValue, 0, 3) + ", "
            for i in range(0, 3):
                SpeedMessage = SpeedMessage + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(AngularSpeedLimit, 0, 3)
                if i != 2:
                    SpeedMessage = SpeedMessage + ", "
                else:
                    SpeedMessage = SpeedMessage + "]"

            print("SpeedMessage: " + str(SpeedMessage))
            #########################

            #########################
            TorqueLimit = 0.0 #Don't allow Roll/Pitch/Yaw torques.

            ForceMessage = "["
            for ForceValue in Force_XYZlist:
                ForceMessage = ForceMessage + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(ForceValue, 0, 3) + ", "
            for i in range(0, 3):
                ForceMessage = ForceMessage + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(TorqueLimit, 0, 3)
                if i != 2:
                    ForceMessage = ForceMessage + ", "
                else:
                    ForceMessage = ForceMessage + "]"

            print("ForceMessage: " + str(ForceMessage))
            #########################

            #####
            SelectionVectorString = "[1, 1, 1, 0, 0, 0]"
            #####


            #########################
            IndentationStr = " " * 4

            Message = "def force_control_function_reuben():\n"

            if ZeroForceReadingsBeforeMoveFlag == 1:
                Message = Message + \
                        IndentationStr + "sleep(0.02)\n" +\
                        IndentationStr + "zero_ftsensor()\n"

            Message = Message + \
                      IndentationStr + "force_mode(p[0.0,0.0,0.0,0.0,0.0,0.0], " + SelectionVectorString + ", " + ForceMessage + ", 2, " + SpeedMessage + ")\n"

            if DurationForWhichToApplyForceInSeconds > 0.0:
                Message = Message + \
                          IndentationStr + "sleep(" + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DurationForWhichToApplyForceInSeconds, 0, 3) + ")\n" + \
                          IndentationStr + "stopl(" + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(StoppingDecellerationMetersPerSecSquared, 0, 3) + ")\n"

            Message = Message + "end\n"

            print(Message)
            self.SendTxMessage(Message)
            #########################

        except:
            exceptions = sys.exc_info()[0]
            print("ForceControl, %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_DedicatedTxThread(self):
    
        try:
            self.DataStreamingDeltaT_CalculatedFromDedicatedTxThread = self.CurrentTime_CalculatedFromDedicatedTxThread - self.LastTime_CalculatedFromDedicatedTxThread
    
            if self.DataStreamingDeltaT_CalculatedFromDedicatedTxThread != 0.0:
                self.DataStreamingFrequency_CalculatedFromDedicatedTxThread = 1.0/self.DataStreamingDeltaT_CalculatedFromDedicatedTxThread
    
            self.LastTime_CalculatedFromDedicatedTxThread = self.CurrentTime_CalculatedFromDedicatedTxThread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_DedicatedTxThread ERROR with Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_DedicatedRxThread(self):
    
        try:
            self.DataStreamingDeltaT_CalculatedFromDedicatedRxThread = self.CurrentTime_CalculatedFromDedicatedRxThread - self.LastTime_CalculatedFromDedicatedRxThread
    
            if self.DataStreamingDeltaT_CalculatedFromDedicatedRxThread != 0.0:
                self.DataStreamingFrequency_CalculatedFromDedicatedRxThread = 1.0/self.DataStreamingDeltaT_CalculatedFromDedicatedRxThread
    
            self.LastTime_CalculatedFromDedicatedRxThread = self.CurrentTime_CalculatedFromDedicatedRxThread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_DedicatedRxThread ERROR with Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_CalculatedFromStandAloneProcess(self):

        try:
            self.LoopDeltaT_CalculatedFromStandAloneProcess = self.CurrentTime_CalculatedFromStandAloneProcess - self.LastTime_CalculatedFromStandAloneProcess

            if self.LoopDeltaT_CalculatedFromStandAloneProcess != 0.0:
                self.LoopFrequency_CalculatedFromStandAloneProcess = 1.0/self.LoopDeltaT_CalculatedFromStandAloneProcess

            self.LastTime_CalculatedFromStandAloneProcess = self.CurrentTime_CalculatedFromStandAloneProcess
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_CalculatedFromStandAloneProcess ERROR, exceptions: %s" % exceptions)
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def KickWatchdogButDoNothing(self, OptionalUserNotesString = 0):

        if OptionalUserNotesString == 1:
            print("KickWatchdogButDoNothing event fired!")

        return
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetWatchdogTimerEnableState(self, WatchdogTimerEnableState):

        try:
            WatchdogTimerEnableState = int(WatchdogTimerEnableState)

            if WatchdogTimerEnableState in [0, 1]:
                self.WatchdogTimerEnableState = WatchdogTimerEnableState
                print("********** SetWatchdogTimerEnableState: Set WatchdogTimerEnableState to " + str(self.WatchdogTimerEnableState) + " **********")
            else:
                print("SetWatchdogTimerEnableState: WatchdogTimerEnableState must be 0 or 1.")

        except:
            exceptions = sys.exc_info()[0]
            print("SetWatchdogTimerEnableState Exceptions: %s" % exceptions)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def WatchdogTimerCheck(self):

        #############################################
        if self.WatchdogTimerEnableState == 1:
            if self.WatchdogTimerDurationSeconds_ExpirationWillEndStandAloneProcess > 0.0:
                if self.getPreciseSecondsTimeStampString() - self.LastTime_CalculatedFromStandAloneProcess >= self.WatchdogTimerDurationSeconds_ExpirationWillEndStandAloneProcess:
                    print("***** UR5arm_ReubenPython2and3Class, Watchdog fired! *****")
                    self.EXIT_PROGRAM_FLAG = 1
        #############################################

    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## unicorn
    ##########################################################################################################
    ##########################################################################################################
    def DedicatedTxThread(self):

        self.MyPrint_WithoutLogFile("Started DedicatedTxThread for UR5arm_ReubenPython2and3Class object at " + str(self.getPreciseSecondsTimeStampString()))
        self.DedicatedTxThread_StillRunningFlag = 1

        ###############################################
        for i in range(0, 5):
            self.SetPayload(self.Payload_MassKG_ToBeCommanded, self.Payload_CoGmetersList_ToBeCommanded)
            time.sleep(0.25)
        ###############################################

        self.StartingTime_CalculatedFromDedicatedTxThread = self.getPreciseSecondsTimeStampString()
        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ##########################################################################################################
            self.CurrentTime_CalculatedFromDedicatedTxThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromDedicatedTxThread
            ##########################################################################################################

            ##########################################################################################################
            if self.JointAngleCommandIncrementDecrement_NeedsToBeChangedFlag == 1:

                NewJointAngleListToSendDeg = list([0.0]*6)
                NewJointAngleListToSendRad = list([0.0] * 6)
                for JointNumber, JointAngleActualRad in enumerate(self.JointAngleList_Rad):
                    NewJointAngleListToSendRad[JointNumber] = JointAngleActualRad + self.JointAngleCommandIncrementDecrement_ValueList_ToBeSet[JointNumber]*math.pi/180.0

                NewWaypointToSendDict = dict([("JointAngleList_Rad", NewJointAngleListToSendRad),
                                          ("Acceleration", self.Acceleration),
                                          ("Velocity", self.Velocity)])

                NewWaypointToSendDict_ConvertedToStrMessage = self.MoveJ_CreateMessage_ListOfDictsMoveJWaypoints(NewWaypointToSendDict)

                #for i in range(0, 3): #For sending multiple times for redundancy
                self.SendTxMessage(NewWaypointToSendDict_ConvertedToStrMessage)

                self.JointAngleCommandIncrementDecrement_NeedsToBeChangedFlag = 0
            ##########################################################################################################

            ##########################################################################################################
            if self.Freedrive_State_NeedsToBeChangedFlag == 1:
                self.SetFreedriveState(self.Freedrive_State_ToBeSet)
                self.Freedrive_State_NeedsToBeChangedFlag = 0
            ##########################################################################################################

            ##########################################################################################################
            if self.ClearProtectiveStop_State_NeedsToBeChangedFlag == 1:
                self.ClearProtectiveStop()
                self.ClearProtectiveStop_State_NeedsToBeChangedFlag = 0
            ##########################################################################################################

            ##########################################################################################################
            if self.RestartSafety_State_NeedsToBeChangedFlag == 1:
                self.RestartSafety()
                self.RestartSafety_State_NeedsToBeChangedFlag = 0
            ##########################################################################################################

            ##########################################################################################################
            if self.StartRobot_State_NeedsToBeChangedFlag == 1:
                self.StartRobot()
                self.StartRobot_State_NeedsToBeChangedFlag = 0
            ##########################################################################################################

            ##########################################################################################################
            if self.ResetTCPsockets_State_NeedsToBeChangedFlag == 1:
                self.ResetTCPsockets()
                self.ResetTCPsockets_State_NeedsToBeChangedFlag = 0
            ##########################################################################################################

            ##########################################################################################################
            if self.StopMotion_State_NeedsToBeChangedFlag == 1:
                self.StopMotion_Acceleration = 10.0
                self.StopMotion_JointSpace(self.StopMotion_Acceleration)
                self.StopMotion_State_NeedsToBeChangedFlag = 0
            ##########################################################################################################

            ##########################################################################################################
            if self.MoveSafelyToStartingPoseViaMultipointSequence_State_NeedsToBeChangedFlag == 1:
                self.MoveSafelyToStartingPoseViaMultipointSequence()
                self.MoveSafelyToStartingPoseViaMultipointSequence_State_NeedsToBeChangedFlag = 0
            ##########################################################################################################

            ##########################################################################################################
            if self.MoveToStartingPose_State_NeedsToBeChangedFlag == 1:
                self.MoveToStartingPose()
                self.MoveToStartingPose_State_NeedsToBeChangedFlag = 0
            ##########################################################################################################

            ##########################################################################################################
            if self.DedicatedTxThread_TxMessageToSend_Queue.qsize() > 0:
                try:
                    self.TxDataToWrite = self.DedicatedTxThread_TxMessageToSend_Queue.get()

                    if len(self.TxDataToWrite) > 0:

                        ######
                        if self.TxDataToWrite[-1] != "\n":
                            self.TxDataToWrite = self.TxDataToWrite + "\n"
                        ######

                        ######
                        if self.EnableTx_State == 1:
                            self.TCPsocketObject_DedicatedTx.send(self.TxDataToWrite.encode('utf-8')) #Python3 requires you to use '.encode('utf-8')' on strings before they can be sent to the socket.
                        ######

                        #print("SENDING '" + str(self.TxDataToWrite.encode('utf-8')) + "'")
                except:
                    exceptions = sys.exc_info()[0]
                    print("DedicatedTxThread Exceptions: %s" % exceptions)
            ##########################################################################################################

            ########################################################################################################## USE THE TIME.SLEEP() TO SET THE LOOP FREQUENCY
            self.UpdateFrequencyCalculation_DedicatedTxThread()
            time.sleep((1.0/self.DedicatedTxThread_MaximumTxMessagesPerSecondFrequency) - 0.001) #The "- 0.001" corrects for slight deviation from intended frequency due to other functions being called.
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        self.CloseTCPsocket_RxAndTx()

        self.MyPrint_WithoutLogFile("Finished DedicatedTxThread for UR5arm_ReubenPython2and3Class object.")
        self.DedicatedTxThread_StillRunningFlag = 0
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## unicorn
    ##########################################################################################################
    ##########################################################################################################
    def DedicatedRxThread(self):

        self.MyPrint_WithoutLogFile("Started DedicatedRxThread for UR5arm_ReubenPython2and3Class object at " + str(self.getPreciseSecondsTimeStampString()))
        self.DedicatedRxThread_StillRunningFlag = 1

        self.StartingTime_CalculatedFromDedicatedRxThread = self.getPreciseSecondsTimeStampString()
        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ##########################################################################################################
            self.CurrentTime_CalculatedFromDedicatedRxThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromDedicatedRxThread
            ##########################################################################################################

            ##########################################################################################################
            self.ReceiveAndParseRxMessageFromURarm_RealTimeInterfaceClient()
            ##########################################################################################################

            ########################################################################################################## unicorn
            # DON'T USE DEEPCOPY AS IT SLOWS US FROM 125HZ TO 25HZ
            self.MostRecentDataDict = self.PacketDict.copy() #.copy() is MUCH faster then deepcopy (just make sure that you don't need deepcopy for making a fresh, independent copy)

            #Adding information that we did something special to (like extra processing or calculation)
            self.MostRecentDataDict["JointAngleList_Deg"] = self.JointAngleList_Deg
            self.MostRecentDataDict["JointAngleList_Rad"] = self.JointAngleList_Rad
            self.MostRecentDataDict["ToolVectorActual"] = self.ToolVectorActual

            self.MostRecentDataDict["ToolTip_XYZ_Meters"] = self.ToolTip_XYZ_Meters
            self.MostRecentDataDict["ToolTip_RotationEulerList_Radians"] = self.ToolTip_RotationEulerList_Radians
            self.MostRecentDataDict["ToolTip_RotationEulerList_Degrees"] = self.ToolTip_RotationEulerList_Degrees

            self.MostRecentDataDict["ToolTipSpeedsCartestian_TCPspeedActual"] = self.ToolTipSpeedsCartestian_TCPspeedActual
            self.MostRecentDataDict["ToolTipSpeedsCartestian_LinearXYZnorm_MetersPerSec"] = self.ToolTipSpeedsCartestian_LinearXYZnorm_MetersPerSec
            self.MostRecentDataDict["DataStreamingFrequency_CalculatedFromDedicatedRxThread"] = self.DataStreamingFrequency_CalculatedFromDedicatedRxThread
            self.MostRecentDataDict["Time"] = self.CurrentTime_CalculatedFromDedicatedRxThread
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        self.MyPrint_WithoutLogFile("Finished DedicatedRxThread for UR5arm_ReubenPython2and3Class object.")
        self.DedicatedRxThread_StillRunningFlag = 0
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## unicorn
    ##########################################################################################################
    def ReceiveAndParseRxMessageFromURarm_RealTimeInterfaceClient(self):

        if self.URarm_ConnectedFlag_DedicatedRx == 1:

            message_length = self.RealTimeClientInterface_NumberOfBytesPerMessage

            try:

                if self.RxPacketCounter == 0:
                    Packet_Temp = self.TCPsocketObject_DedicatedRx.recv(4)
                    if len(Packet_Temp) >= 4:
                        MessageSize_Temp = struct.unpack('!I', Packet_Temp)[0]
                        #print("MessageSize_Temp: " + str(MessageSize_Temp))

                        if MessageSize_Temp == message_length:
                            self.PacketDict[self.PacketKeywordStringsList[self.RxPacketCounter]] = MessageSize_Temp
                            self.RxPacketCounter = 1

                if self.RxPacketCounter > 0:
                    Packet_Temp = self.TCPsocketObject_DedicatedRx.recv(8)
                    #print("Packet_Temp: " + str(Packet_Temp))

                    if len(Packet_Temp) >= 8:
                        self.PacketDict[self.PacketKeywordStringsList[self.RxPacketCounter]] = struct.unpack('!d', Packet_Temp)[0]

                        if self.RxPacketCounter < len(self.PacketKeywordStringsList) - 1:
                            self.RxPacketCounter = self.RxPacketCounter + 1
                        else:
                            self.RxPacketCounter = 0

                            ##############################
                            self.JointAngleList_Rad = [self.PacketDict["Qactual_Joint1"],
                                                       self.PacketDict["Qactual_Joint2"],
                                                       self.PacketDict["Qactual_Joint3"],
                                                       self.PacketDict["Qactual_Joint4"],
                                                       self.PacketDict["Qactual_Joint5"],
                                                       self.PacketDict["Qactual_Joint6"]]

                            for index, value in enumerate(self.JointAngleList_Rad):
                                self.JointAngleList_Deg[index] = value * 180.0 / math.pi
                            ##############################

                            ##############################
                            self.ToolVectorActual = [self.PacketDict["ToolXactual"],
                                                     self.PacketDict["ToolYactual"],
                                                     self.PacketDict["ToolZactual"],
                                                     self.PacketDict["ToolRXactual"],
                                                     self.PacketDict["ToolRYactual"],
                                                     self.PacketDict["ToolRZactual"]]
                            ##############################

                            ##############################
                            self.ToolTip_XYZ_Meters = self.ToolVectorActual [0:3]

                            RotationObjectScipy = Rotation.from_rotvec(self.ToolVectorActual[-3:])
                            self.ToolTip_RotationEulerList_Radians = RotationObjectScipy.as_euler('xyz', degrees=False)
                            self.ToolTip_RotationEulerList_Degrees = numpy.array(numpy.rad2deg(numpy.array(self.ToolTip_RotationEulerList_Radians))).tolist()
                            ##############################

                            ##############################
                            # Actual speed of the tool given in Cartesian coordinates
                            self.ToolTipSpeedsCartestian_TCPspeedActual = [self.PacketDict["TCPspeedActual_Joint1"],
                                                                           self.PacketDict["TCPspeedActual_Joint2"],
                                                                           self.PacketDict["TCPspeedActual_Joint3"],
                                                                           self.PacketDict["TCPspeedActual_Joint4"],
                                                                           self.PacketDict["TCPspeedActual_Joint5"],
                                                                           self.PacketDict["TCPspeedActual_Joint6"]]

                            self.ToolTipSpeedsCartestian_LinearXYZnorm_MetersPerSec = self.ComputeListNorm(list([self.ToolTipSpeedsCartestian_TCPspeedActual[0],
                                                                                                                    self.ToolTipSpeedsCartestian_TCPspeedActual[1],
                                                                                                                    self.ToolTipSpeedsCartestian_TCPspeedActual[2]]))

                            self.ToolTipSpeedsCartestian_LinearXYZnorm_MetersPerMin = self.ToolTipSpeedsCartestian_LinearXYZnorm_MetersPerSec * 60.0
                            ##############################

                            ##############################
                            self.JointControlModeListInt = [int(self.PacketDict["JointMode_Joint1"]), int(self.PacketDict["JointMode_Joint2"]), int(self.PacketDict["JointMode_Joint3"]), int(self.PacketDict["JointMode_Joint4"]), int(self.PacketDict["JointMode_Joint5"]), int(self.PacketDict["JointMode_Joint6"])]
                            # 255 = force
                            # 253 = position
                            ##############################

                            ############################################### USE THE TIME.SLEEP() TO SET THE LOOP FREQUENCY
                            ###############################################
                            ###############################################
                            self.UpdateFrequencyCalculation_DedicatedRxThread()

                            if self.DedicatedRxThread_TimeToSleepEachLoop > 0.0:
                                time.sleep(self.DedicatedRxThread_TimeToSleepEachLoop)
                            ###############################################
                            ###############################################
                            ###############################################

                            #print(self.PacketDict)

            except:
                exceptions = sys.exc_info()[0]
                print("ReceiveAndParseRxMessageFromURarm_RealTimeInterfaceClient ERROR with Exceptions: %s" % exceptions)
                #traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("UR5arm_ReubenPython2and3Class, ExitProgram_Callback event fired!")

        self.EXIT_PROGRAM_FLAG = 1

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TestFunctionWithMultipleArguments(self, a=100, b=101, c=102, d=103):
        print(locals().keys())
        print("a: " + str(a) + ", b: " + str(b) + ", c: " + str(c) + ", d: " + str(d))

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def FunctionCallToStandAloneProcess(self, FunctionName, ListOfFunctionArguments, MultiprocessingQueue_Rx_MaxSize_Local = 1, IgnoreNewDataIfQueueIsFullFlag = 1):

        try:
            if self.MultiprocessingQueue_Rx.qsize() < MultiprocessingQueue_Rx_MaxSize_Local:
                self.MultiprocessingQueue_Rx.put(dict([(FunctionName, ListOfFunctionArguments)]))

                #print("FunctionCallToStandAloneProcess event fired!")
            else:
                if IgnoreNewDataIfQueueIsFullFlag != 1:
                    print("FunctionCallToStandAloneProcess: self.MultiprocessingQueue_Rx is full, making room...")
                    dummy = self.MultiprocessingQueue_Rx.get()  # makes room for one more message
                    self.MultiprocessingQueue_Rx.put(dict([(FunctionName, ListOfFunctionArguments)]))  # backfills that message with new data
        except:
            pass

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StartGUI(self):

        self.GUI_Thread_ThreadingObject = threading.Thread(target=self.GUI_Thread, args=())
        self.GUI_Thread_ThreadingObject.setDaemon(True) #Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
        self.GUI_Thread_ThreadingObject.start()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_Thread(self):

        print("Starting the GUI_Thread for URarm_ReubenPython2and3Class object.")

        ###################################################
        self.UseBorderAroundThisGuiObjectFlag = 0
        self.GUI_ROW = 0
        self.GUI_COLUMN = 0
        self.GUI_PADX = 1
        self.GUI_PADY = 1
        self.GUI_ROWSPAN = 1
        self.GUI_COLUMNSPAN = 1
        self.GUI_STICKY = "w"
        ###################################################

        ###################################################
        self.root = Tk()
        ##################################################

        ###################################################
        ###################################################
        self.root.title(self.RootWindowTitle)
        self.root.after(self.GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents, self.__GUI_update_clock)
        self.root.protocol("WM_DELETE_WINDOW", self.ExitProgram_Callback)  # Set the callback function for when the window's closed.
        self.root.geometry('%dx%d+%d+%d' % (self.RootWindowWidth, self.RootWindowHeight, self.RootWindowStartingX, self.RootWindowStartingY))
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.TabControlObject = ttk.Notebook(self.root)

        self.Tab_MainControls = ttk.Frame(self.TabControlObject)
        self.TabControlObject.add(self.Tab_MainControls, text='  Main Controls  ')

        self.Tab_PrintAllMostRecentDataDict = ttk.Frame(self.TabControlObject)
        self.TabControlObject.add(self.Tab_PrintAllMostRecentDataDict, text='  MostRecentDataDict  ')

        self.TabControlObject.pack(expand=1, fill="both") #CANNOT MIX PACK AND GRID IN THE SAME FRAME/TAB, SO ALL .GRID'S MUST BE CONTAINED WITHIN THEIR OWN FRAME/TAB.

        ############# #Set the tab header font
        self.TabStyle = ttk.Style()
        self.TabStyle.configure('TNotebook.Tab', font=('Helvetica', '12', 'bold'))
        #############

        ###################################################
        ###################################################

        ###################################################
        self.myFrame = Frame(self.Tab_MainControls)
    
        if self.UseBorderAroundThisGuiObjectFlag == 1:
            self.myFrame["borderwidth"] = 2
            self.myFrame["relief"] = "ridge"

        self.myFrame.grid(row=self.GUI_ROW,
                          column=self.GUI_COLUMN,
                          padx=self.GUI_PADX,
                          pady=self.GUI_PADY,
                          rowspan=self.GUI_ROWSPAN,
                          columnspan=self.GUI_COLUMNSPAN,
                          sticky = self.GUI_STICKY)
        ###################################################
    
        ###################################################
        self.TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150)  # RGB
        self.TKinter_LightBlueColor = '#%02x%02x%02x' % (150, 150, 255)  # RGB
        self.TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150)  # RGB
        self.TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
        self.TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
        self.Tkinter_TextLabelWidth = 150
        self.Tkinter_EntryWidth = 10
        self.Tkinter_ButtonWidth = 20
        self.Tkinter_Scalelength = 250
        ###################################################

        #################################################
        self.DeviceInfo_Label = Label(self.myFrame, text="Device Info", width=self.Tkinter_TextLabelWidth)
        self.DeviceInfo_Label["text"] = self.NameToDisplay_UserSet
        self.DeviceInfo_Label.grid(row=0, column=0, padx=1, pady=10, columnspan=1, rowspan=1)
        #################################################

        #################################################
        self.DedicatedTxThread_Label = Label(self.myFrame, text="DedicatedTxThread_Label", width=self.Tkinter_TextLabelWidth)
        self.DedicatedTxThread_Label.grid(row=1, column=0, padx=10, pady=1, columnspan=1, rowspan=1)
        #################################################

        #################################################
        self.DedicatedRxThread_Label = Label(self.myFrame, text="DedicatedRxThread_Label", width=self.Tkinter_TextLabelWidth)
        self.DedicatedRxThread_Label.grid(row=2, column=0, padx=10, pady=1, columnspan=1, rowspan=1)
        #################################################

        #################################################
        self.PrintAllMostRecentDataDict_Label = Label(self.Tab_PrintAllMostRecentDataDict, text="PrintAllMostRecentDataDict_Label", width=self.Tkinter_TextLabelWidth)
        self.PrintAllMostRecentDataDict_Label.grid(row=0, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        #################################################

        #################################################
        self.JointAngleCommandIncrementDecrement_Frame = Frame(self.myFrame)
        self.JointAngleCommandIncrementDecrement_Frame.grid(row=3, column=0, padx=1, pady=10, rowspan=1, columnspan=1)
        #################################################

        ####################################################
        self.JointAngleCommandIncrementDecrement_EntryRowInt = 0
        for JointNumber in range(0, 6):

            self.JointAngleCommandIncrementDecrement_EntryLabelPrefixesList = ["Base", "Shoulder", "Elbow", "Wrist Pitch", "Wrist Roll", "Gripper Roll"]
            self.JointAngleCommandIncrementDecrement_EntryLabelList.append(Label(self.JointAngleCommandIncrementDecrement_Frame, text=self.JointAngleCommandIncrementDecrement_EntryLabelPrefixesList[JointNumber] + ", Inc/Decrement Joint " + str(JointNumber), width=40, font=("Helvetica", int(12))))
            self.JointAngleCommandIncrementDecrement_EntryLabelList[JointNumber].grid(row=self.JointAngleCommandIncrementDecrement_EntryRowInt+JointNumber, column=0, padx=1, pady=1, columnspan=1, rowspan=1)

            self.JointAngleCommandIncrementDecrement_EntryTextContentList.append(StringVar())
            self.JointAngleCommandIncrementDecrement_EntryTextContentList[JointNumber].set(self.JointAngleCommandIncrementDecrement_ValueInDegrees)

            self.JointAngleCommandIncrementDecrement_EntryObject.append(Entry(self.JointAngleCommandIncrementDecrement_Frame,
                                                font=("Helvetica", int(12)),
                                                state="normal",
                                                width=self.Tkinter_EntryWidth,
                                                textvariable=self.JointAngleCommandIncrementDecrement_EntryTextContentList[JointNumber],
                                                justify='center'))

            self.JointAngleCommandIncrementDecrement_EntryObject[JointNumber].grid(row=self.JointAngleCommandIncrementDecrement_EntryRowInt+JointNumber, column=1, padx=0, pady=0, columnspan=1, rowspan=1)
            self.JointAngleCommandIncrementDecrement_EntryObject[JointNumber].bind('<Return>', lambda event, JointNumberOfEvent=JointNumber: self.JointAngleCommandIncrementDecrement_EntryEventResponse(event, JointNumberOfEvent))
            self.JointAngleCommandIncrementDecrement_EntryObject[JointNumber].bind('<Leave>', lambda event, JointNumberOfEvent=JointNumber: self.JointAngleCommandIncrementDecrement_EntryEventResponse(event, JointNumberOfEvent))

            IncrementLabelText = self.JointAngleCommandIncrementDecrement_CustomEntryLabels_ListOfDicts[JointNumber]["IncrementLabel"]
            self.JointAngleCommandIncrement_ButtonObjectList.append(Button(self.JointAngleCommandIncrementDecrement_Frame, text=IncrementLabelText, state="normal", width=self.Tkinter_ButtonWidth, command=lambda JointNumberOfEvent=JointNumber: self.JointAngleCommandIncrement_ButtonObjectResponse(JointNumberOfEvent)))
            self.JointAngleCommandIncrement_ButtonObjectList[JointNumber].grid(row=self.JointAngleCommandIncrementDecrement_EntryRowInt+JointNumber, column=2, padx=0, pady=0, columnspan=1, rowspan=1)

            DecrementLabelText = self.JointAngleCommandIncrementDecrement_CustomEntryLabels_ListOfDicts[JointNumber]["DecrementLabel"]
            self.JointAngleCommandDecrement_ButtonObjectList.append(Button(self.JointAngleCommandIncrementDecrement_Frame, text=DecrementLabelText, state="normal", width=self.Tkinter_ButtonWidth, command=lambda JointNumberOfEvent=JointNumber: self.JointAngleCommandDecrement_ButtonObjectResponse(JointNumberOfEvent)))
            self.JointAngleCommandDecrement_ButtonObjectList[JointNumber].grid(row=self.JointAngleCommandIncrementDecrement_EntryRowInt+JointNumber, column=3, padx=0, pady=0, columnspan=1, rowspan=1)

        ###################################################

        #################################################
        self.AdditionalControls_Frame = Frame(self.myFrame)
        self.AdditionalControls_Frame.grid(row=4, column=0, padx=1, pady=10, rowspan=1, columnspan=1)
        #################################################

        #################################################
        self.MostRecentDataDict_Button = Button(self.AdditionalControls_Frame, text="Snapshot DataDict", state="normal", width=self.Tkinter_ButtonWidth, command=lambda: self.MostRecentDataDict_ButtonResponse())
        self.MostRecentDataDict_Button.grid(row=0, column=1, padx=1, pady=1, columnspan=1, rowspan=1)
        #################################################
        
        #################################################
        self.ToggleEnableTx_Button = Button(self.AdditionalControls_Frame, text="EnableTx", state="normal", width=self.Tkinter_ButtonWidth, command=lambda: self.ToggleEnableTx_ButtonResponse())
        self.ToggleEnableTx_Button.grid(row=0, column=2, padx=1, pady=1, columnspan=1, rowspan=1)
        #################################################

        #################################################
        self.MoveToStartingPose_Button = Button(self.AdditionalControls_Frame, text="Move To Starting Pose", state="normal", width=self.Tkinter_ButtonWidth, command=lambda: self.MoveToStartingPose_ButtonResponse())
        self.MoveToStartingPose_Button.grid(row=0, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        #################################################

        #################################################
        MoveSafelyToStartingPoseViaMultipointSequence_Button = Button(self.AdditionalControls_Frame, text='Safe Sequence', state="normal", width=self.Tkinter_ButtonWidth, bg=self.TKinter_LightGreenColor, command=lambda i=1: self.MoveSafelyToStartingPoseViaMultipointSequence_ButtonResponse())
        if len(self.PositionControl_ServoJ_MoveThroughListOfPoses_SafeReturnToStartingPoseFromAnywhere) == 0:
            MoveSafelyToStartingPoseViaMultipointSequence_Button["state"] = "disabled"
        MoveSafelyToStartingPoseViaMultipointSequence_Button.grid(row=1, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        #################################################

        #################################################
        self.StopMotion_Button = Button(self.AdditionalControls_Frame, text="Stop Motion", state="normal", width=self.Tkinter_ButtonWidth, bg=self.TKinter_LightRedColor, command=lambda: self.StopMotion_ButtonResponse())
        self.StopMotion_Button.grid(row=2, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        #################################################

        #################################################
        self.Freedrive_Button = Button(self.AdditionalControls_Frame, text="Freedrive", state="normal", width=self.Tkinter_ButtonWidth, bg=self.TKinter_LightYellowColor, command=lambda: self.Freedrive_ButtonResponse())
        if self.RealTimeClientInterfaceVersionNumberFloat >= 3.0:
            self.Freedrive_Button.grid(row=3, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        #################################################

        #################################################
        if self.RealTimeClientInterfaceVersionNumberFloat >= 1.6 and self.RealTimeClientInterfaceVersionNumberFloat < 3.1:
            self.ClearProtectiveStop_Button_TextToDisplay = "Close Popup"
            self.ClearProtectiveStop_Button_DisplayButtonFlag = 1
        elif self.RealTimeClientInterfaceVersionNumberFloat >= 3.1:
            self.ClearProtectiveStop_Button_TextToDisplay = "Clear Errors"
            self.ClearProtectiveStop_Button_DisplayButtonFlag = 1
        else:
            self.ClearProtectiveStop_Button_TextToDisplay = ""
            self.ClearProtectiveStop_Button_DisplayButtonFlag = 0

        self.ClearProtectiveStop_Button = Button(self.AdditionalControls_Frame, text=self.ClearProtectiveStop_Button_TextToDisplay, state="normal", width=self.Tkinter_ButtonWidth, command=lambda: self.ClearProtectiveStop_ButtonResponse())
        if self.ClearProtectiveStop_Button_DisplayButtonFlag == 1:
            self.ClearProtectiveStop_Button.grid(row=4, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        #################################################

        #################################################
        if self.RealTimeClientInterfaceVersionNumberFloat >= 3.1 and self.RealTimeClientInterfaceVersionNumberFloat < 3.7:
            self.RestartSafety_Button_TextToDisplay = "Close Safety Popup"
            self.RestartSafety_Button_DisplayButtonFlag = 1
        elif self.RealTimeClientInterfaceVersionNumberFloat >= 3.7:
            self.RestartSafety_Button_TextToDisplay = "Restart Safety"
            self.RestartSafety_Button_DisplayButtonFlag = 1
        else:
            self.RestartSafety_Button_TextToDisplay = ""
            self.RestartSafety_Button_DisplayButtonFlag = 0

        self.RestartSafety_Button = Button(self.AdditionalControls_Frame, text=self.RestartSafety_Button_TextToDisplay, state="normal", width=self.Tkinter_ButtonWidth, command=lambda: self.RestartSafety_ButtonResponse())
        if self.RestartSafety_Button_DisplayButtonFlag == 1:
            self.RestartSafety_Button.grid(row=5, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        #################################################

        #################################################
        self.StartRobot_Button = Button(self.AdditionalControls_Frame, text="Start Robot", state="normal", width=self.Tkinter_ButtonWidth, command=lambda: self.StartRobot_ButtonResponse())
        if self.RealTimeClientInterfaceVersionNumberFloat >= 3.0:
            self.StartRobot_Button.grid(row=6, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        #################################################

        #################################################
        self.ResetTCPsockets_Button = Button(self.AdditionalControls_Frame, text="ResetTCPsockets", state="normal", width=self.Tkinter_ButtonWidth, command=lambda: self.ResetTCPsockets_ButtonResponse())
        self.ResetTCPsockets_Button.grid(row=7, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        #################################################

        #################################################
        self.Velocity_Slider_DoubleVar = DoubleVar()

        self.Velocity_Slider = Scale(self.AdditionalControls_Frame,
                                                       label = "Velocity",
                                                       state="normal",
                                                       from_ = self.Velocity_MinValue,
                                                       to = self.Velocity_MaxValue,
                                                       tickinterval = (self.Velocity_MaxValue - self.Velocity_MinValue)/5.0,
                                                       orient=HORIZONTAL,
                                                       showvalue=True,
                                                       width = 10,
                                                       length = self.Tkinter_Scalelength,
                                                       resolution = 0.01,
                                                       variable = self.Velocity_Slider_DoubleVar)
        self.Velocity_Slider.bind('<Button-1>', lambda event, name="Velocity_Slider": self.Velocity_Slider_Response(event, name))
        self.Velocity_Slider.bind('<B1-Motion>', lambda event, name="Velocity_Slider": self.Velocity_Slider_Response(event, name))
        self.Velocity_Slider.bind('<ButtonRelease-1>', lambda event, name="Velocity_Slider": self.Velocity_Slider_Response(event, name))
        self.Velocity_Slider.set(self.Velocity)
        self.Velocity_Slider.grid(row=1, column=1, padx=1, pady=10, columnspan=2, rowspan=1)
        #################################################

        #################################################
        self.ServoJ_JointAngleDistance_Threshold_Slider_DoubleVar = DoubleVar()

        self.ServoJ_JointAngleDistance_Threshold_Slider = Scale(self.AdditionalControls_Frame,
                                                       label = "ServoJ_JointAngleDistance_Threshold",
                                                       state="normal",
                                                       from_ = self.ServoJ_JointAngleDistance_Threshold_MinValue,
                                                       to = self.ServoJ_JointAngleDistance_Threshold_MaxValue,
                                                       tickinterval = (self.ServoJ_JointAngleDistance_Threshold_MaxValue - self.ServoJ_JointAngleDistance_Threshold_MinValue)/5.0,
                                                       orient=HORIZONTAL,
                                                       showvalue=True,
                                                       width = 10,
                                                       length = self.Tkinter_Scalelength,
                                                       resolution = 0.01,
                                                       variable = self.ServoJ_JointAngleDistance_Threshold_Slider_DoubleVar)
        self.ServoJ_JointAngleDistance_Threshold_Slider.bind('<Button-1>', lambda event, name="ServoJ_JointAngleDistance_Threshold_Slider": self.ServoJ_JointAngleDistance_Threshold_Slider_Response(event, name))
        self.ServoJ_JointAngleDistance_Threshold_Slider.bind('<B1-Motion>', lambda event, name="ServoJ_JointAngleDistance_Threshold_Slider": self.ServoJ_JointAngleDistance_Threshold_Slider_Response(event, name))
        self.ServoJ_JointAngleDistance_Threshold_Slider.bind('<ButtonRelease-1>', lambda event, name="ServoJ_JointAngleDistance_Threshold_Slider": self.ServoJ_JointAngleDistance_Threshold_Slider_Response(event, name))
        self.ServoJ_JointAngleDistance_Threshold_Slider.set(self.ServoJ_JointAngleDistance_Threshold)
        self.ServoJ_JointAngleDistance_Threshold_Slider.grid(row=1, column=3, padx=1, pady=10, columnspan=2, rowspan=1)
        #################################################

        #################################################
        self.Acceleration_Slider_DoubleVar = DoubleVar()

        self.Acceleration_Slider = Scale(self.AdditionalControls_Frame,
                                                       label = "Acceleration",
                                                       state="normal",
                                                       from_ = self.Acceleration_MinValue,
                                                       to = self.Acceleration_MaxValue,
                                                       tickinterval = (self.Acceleration_MaxValue - self.Acceleration_MinValue)/5.0,
                                                       orient=HORIZONTAL,
                                                       showvalue=True,
                                                       width = 10,
                                                       length = self.Tkinter_Scalelength,
                                                       resolution = 0.01,
                                                       variable = self.Acceleration_Slider_DoubleVar)
        self.Acceleration_Slider.bind('<Button-1>', lambda event, name="Acceleration_Slider": self.Acceleration_Slider_Response(event, name))
        self.Acceleration_Slider.bind('<B1-Motion>', lambda event, name="Acceleration_Slider": self.Acceleration_Slider_Response(event, name))
        self.Acceleration_Slider.bind('<ButtonRelease-1>', lambda event, name="Acceleration_Slider": self.Acceleration_Slider_Response(event, name))
        self.Acceleration_Slider.set(self.Acceleration)
        self.Acceleration_Slider.grid(row=2, column=1, padx=1, pady=10, columnspan=2, rowspan=1)
        #################################################

        #################################################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=self.Tkinter_TextLabelWidth)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=5, column=0, padx=1, pady=1, columnspan=10, rowspan=10)
        #################################################

        #################################################
        self.GUI_ready_to_be_updated_flag = 1
        #################################################

        #################################################
        self.root.mainloop() #THIS MUST BE THE LAST LINE IN THE GUI THREAD SETUP BECAUSE IT'S BLOCKING!!!!
        #################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def JointAngleCommandIncrementDecrement_EntryEventResponse(self, event, JointNumberOfEvent):

        ################################### Take away focus so that we're not continuing to tpye into entry when logging waypoints.
        self.myFrame.focus_set()
        ###################################

        try:
            pass
            '''
            for i in range(0, 6):
                if i == JointNumberOfEvent:
                    Value = float(self.JointAngleCommandIncrementDecrement_EntryTextContentList[i].get())
                    self.JointAngleCommandIncrementDecrement_ValueList_ToBeSet[i] = Value
                else:
                    self.JointAngleCommandIncrementDecrement_ValueList_ToBeSet[i] = 0.0

            self.JointAngleCommandIncrementDecrement_NeedsToBeChangedFlag = 1
            print("JointAngleCommandIncrementDecrement_EntryEventResponse event fired on JointNumberOfEvent " + str(JointNumberOfEvent) + " with value of " + str(Value))
            '''

        except:
            exceptions = sys.exc_info()[0]
            print("JointAngleCommandIncrementDecrement_EntryEventResponse ERROR: Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def JointAngleCommandIncrement_ButtonObjectResponse(self, JointNumberOfEvent):

        try:
            for i in range(0, 6):
                if i == JointNumberOfEvent:
                    Value = float(self.JointAngleCommandIncrementDecrement_EntryTextContentList[i].get())
                    self.JointAngleCommandIncrementDecrement_ValueList_ToBeSet[i] = Value
                else:
                    self.JointAngleCommandIncrementDecrement_ValueList_ToBeSet[i] = 0.0

            self.JointAngleCommandIncrementDecrement_NeedsToBeChangedFlag = 1
            #print("JointAngleCommandIncrement_ButtonObjectResponse event fired on JointNumberOfEvent " + str(JointNumberOfEvent) + " with value of " + str(Value))

        except:
            exceptions = sys.exc_info()[0]
            print("JointAngleCommandIncrement_ButtonObjectResponse ERROR: Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def JointAngleCommandDecrement_ButtonObjectResponse(self, JointNumberOfEvent):

        try:
            for i in range(0, 6):
                if i == JointNumberOfEvent:
                    Value = -1.0*float(self.JointAngleCommandIncrementDecrement_EntryTextContentList[i].get())
                    self.JointAngleCommandIncrementDecrement_ValueList_ToBeSet[i] = Value
                else:
                    self.JointAngleCommandIncrementDecrement_ValueList_ToBeSet[i] = 0.0

            self.JointAngleCommandIncrementDecrement_NeedsToBeChangedFlag = 1
            #print("JointAngleCommandDecrement_ButtonObjectResponse event fired on JointNumberOfEvent " + str(JointNumberOfEvent) + " with value of " + str(Value))

        except:
            exceptions = sys.exc_info()[0]
            print("JointAngleCommandDecrement_ButtonObjectResponse ERROR: Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Velocity_Slider_Response(self, event, name):

        self.Velocity = float(self.Velocity_Slider_DoubleVar.get())

        #print("Velocity_Slider_Response event fired, Velocity = " + str(self.Velocity))

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ServoJ_JointAngleDistance_Threshold_Slider_Response(self, event, name):

        self.ServoJ_JointAngleDistance_Threshold = float(self.ServoJ_JointAngleDistance_Threshold_Slider_DoubleVar.get())

        #print("ServoJ_JointAngleDistance_Threshold_Slider_Response event fired, Velocity = " + str(self.ServoJ_JointAngleDistance_Threshold))

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Acceleration_Slider_Response(self, event, name):

        self.Acceleration = float(self.Acceleration_Slider_DoubleVar.get())

        #print("Acceleration_Slider_Response event fired, Acceleration = " + str(self.Acceleration))

    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## unicorn
    ##########################################################################################################
    def __GUI_update_clock(self):

        #######################################################
        #######################################################
        #######################################################
        #######################################################
        if self.USE_GUI_FLAG == 1 and self.EXIT_PROGRAM_FLAG == 0:

            #######################################################
            #######################################################
            #######################################################
            if self.GUI_ready_to_be_updated_flag == 1:

                #######################################################
                #######################################################
                try:

                    #######################################################
                    self.ToggleEnableTx_Button["text"] = "EnableTx: " + str(self.EnableTx_State)
                    #######################################################

                    #######################################################
                    self.Freedrive_Button["text"] = "Freedrive State: " + str(self.Freedrive_State)
                    #######################################################

                    #######################################################
                    self.DeviceInfo_Label["text"] = "RealTimeClientInterfaceVersionNumberFloat: " + str(self.RealTimeClientInterfaceVersionNumberFloat) + \
                                                    "\nControllerBoxVersion: " + str(self.ControllerBoxVersion) + \
                                                    "\nURarm_ConnectedFlag_DedicatedDashboardEStop: " + str(self.URarm_ConnectedFlag_DedicatedDashboardEStop)
                    #######################################################

                    #######################################################
                    self.DedicatedTxThread_Label["text"] = "URarm_ConnectedFlag_DedicatedTx: " + str(self.URarm_ConnectedFlag_DedicatedTx) + \
                                                "\nTime: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.CurrentTime_CalculatedFromDedicatedTxThread, 0, 3) + \
                                                "\nTx Data Frequency: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_CalculatedFromDedicatedTxThread, 0, 3) + \
                                                "\nToolTip6DOFpose_ToBeSet: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.ToolTip6DOFpose_ToBeSet, 0, 5) # +\
                                                #"\nTxDataToWrite: " + str(self.TxDataToWrite)
                    #######################################################

                    #######################################################
                    self.DedicatedRxThread_Label["text"] = "URarm_ConnectedFlag_DedicatedRx: " + str(self.URarm_ConnectedFlag_DedicatedRx) + \
                                                "\nself.MultiprocessingQueue_Rx.qsize(): " + str(self.MultiprocessingQueue_Rx.qsize()) + \
                                                "\tself.MultiprocessingQueue_Tx.qsize(): " + str(self.MultiprocessingQueue_Tx.qsize()) + \
                                                "\nTime: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.CurrentTime_CalculatedFromDedicatedRxThread, 0, 3) + \
                                                "\nRx Data Frequency: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_CalculatedFromDedicatedRxThread, 0, 3) + \
                                                "\t\tTx Data Frequency: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_CalculatedFromDedicatedTxThread, 0, 3) + \
                                                "\nRxPacketsCounter_Total: " + str(self.RxPacketsCounter_Total) + ",\tWrongSize: "  + str(self.RxPacketsCounter_WrongSize) + "\t%WrongSize: " + str(self.RxPackets_PercentWrongSize) + \
                                                "\nToolVectorActual: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.ToolVectorActual, 0, 5) + \
                                                "\nToolTip_XYZ_Meters: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.ToolTip_XYZ_Meters, 0, 5) + \
                                                "\nToolTip_RotationEulerList_Radians: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.ToolTip_RotationEulerList_Radians, 0, 3) + \
                                                "\nToolTip_RotationEulerList_Degrees: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.ToolTip_RotationEulerList_Degrees, 0, 3) + \
                                                "\nToolTipSpeedsCartestian_TCPspeedActual: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.ToolTipSpeedsCartestian_TCPspeedActual, 0, 5) + \
                                                "\nToolTipSpeedsCartestian_LinearXYZnorm_MetersPerSec: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.ToolTipSpeedsCartestian_LinearXYZnorm_MetersPerSec, 0, 3) + \
                                                "\nToolTipSpeedsCartestian_LinearXYZnorm_MetersPerMin: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.ToolTipSpeedsCartestian_LinearXYZnorm_MetersPerMin, 0, 3) + \
                                                "\nJointAngleList_Rad: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.JointAngleList_Rad, 0, 5) + \
                                                "\nJointAngleList_Deg: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.JointAngleList_Deg, 0, 5) + \
                                                "\nJoint Control Modes: "  + str(self.JointControlModeListInt) + "--> " + str(self.JointControlModeListString)

                     #######################################################

                    #######################################################
                    self.PrintAllMostRecentDataDict_Label["text"] = self.ConvertDictToProperlyFormattedStringForPrinting(self.MostRecentDataDict, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 3, NumberOfTabsBetweenItems = 1)
                    #######################################################

                    #######################################################
                    self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                    #######################################################

                except:
                    exceptions = sys.exc_info()[0]
                    print("UR5arm_ReubenPython2and3Class __GUI_update_clock ERROR: Exceptions: %s" % exceptions)
                    traceback.print_exc()
                #######################################################
                #######################################################

                #######################################################
                #######################################################
                self.root.after(self.GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents, self.__GUI_update_clock)
                #######################################################
                #######################################################

            #######################################################
            #######################################################
            #######################################################

        #######################################################
        #######################################################
        #######################################################
        #######################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def MostRecentDataDict_ButtonResponse(self):

        MostRecentDataDict_ProperlyFormattedStringForPrinting = self.ConvertDictToProperlyFormattedStringForPrinting(self.MostRecentDataDict, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3)

        print("\nUR5arm_ReubenPython2and3Class: MostRecentDataDict_ButtonResponse, self.MostRecentDataDict:\n" + MostRecentDataDict_ProperlyFormattedStringForPrinting.replace("+","")  + "\n") #No leading +
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ToggleEnableTx_ButtonResponse(self):

        if self.EnableTx_State == 1:
            self.EnableTx_State = 0
        else:
            self.EnableTx_State = 1

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def MoveSafelyToStartingPoseViaMultipointSequence_ButtonResponse(self):

        self.MoveSafelyToStartingPoseViaMultipointSequence_State_NeedsToBeChangedFlag = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def MoveToStartingPose_ButtonResponse(self):

        self.MoveToStartingPose_State_NeedsToBeChangedFlag = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StopMotion_ButtonResponse(self):

        self.StopMotion_State_NeedsToBeChangedFlag = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Freedrive_ButtonResponse(self):

        if self.Freedrive_State == 0:
            self.Freedrive_State_ToBeSet = 1
        else:
            self.Freedrive_State_ToBeSet = 0

        self.Freedrive_State_NeedsToBeChangedFlag = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ClearProtectiveStop_ButtonResponse(self):

        self.ClearProtectiveStop_State_NeedsToBeChangedFlag = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def RestartSafety_ButtonResponse(self):

        self.RestartSafety_State_NeedsToBeChangedFlag = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StartRobot_ButtonResponse(self):

        self.StartRobot_State_NeedsToBeChangedFlag = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ResetTCPsockets_ButtonResponse(self):

        self.ResetTCPsockets_State_NeedsToBeChangedFlag = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def MyPrint_WithoutLogFile(self, input_string):

        input_string = str(input_string)

        if input_string != "":

            #input_string = input_string.replace("\n", "").replace("\r", "")

            ################################ Write to console
            # Some people said that print crashed for pyinstaller-built-applications and that sys.stdout.write fixed this.
            # http://stackoverflow.com/questions/13429924/pyinstaller-packaged-application-works-fine-in-console-mode-crashes-in-window-m
            if self.PrintToConsoleFlag == 1:
                sys.stdout.write(input_string + "\n")
            ################################

            ################################ Write to GUI
            self.PrintToGui_Label_TextInputHistory_List.append(self.PrintToGui_Label_TextInputHistory_List.pop(0)) #Shift the list
            self.PrintToGui_Label_TextInputHistory_List[-1] = str(input_string) #Add the latest value

            self.PrintToGui_Label_TextInput_Str = ""
            for Counter, Line in enumerate(self.PrintToGui_Label_TextInputHistory_List):
                self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + Line

                if Counter < len(self.PrintToGui_Label_TextInputHistory_List) - 1:
                    self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + "\n"
            ################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self, input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

        number_of_decimal_places = max(1, number_of_decimal_places) #Make sure we're above 1

        ListOfStringsToJoin = []

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if isinstance(input, str) == 1:
            ListOfStringsToJoin.append(input)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, int) == 1 or isinstance(input, float) == 1:
            element = float(input)
            prefix_string = "{:." + str(number_of_decimal_places) + "f}"
            element_as_string = prefix_string.format(element)

            ##########################################################################################################
            ##########################################################################################################
            if element >= 0:
                element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place
                element_as_string = "+" + element_as_string  # So that our strings always have either + or - signs to maintain the same string length
            else:
                element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1 + 1)  # +1 for sign, +1 for decimal place
            ##########################################################################################################
            ##########################################################################################################

            ListOfStringsToJoin.append(element_as_string)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, list) == 1:

            if len(input) > 0:
                for element in input: #RECURSION
                    ListOfStringsToJoin.append(self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a list() or []
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, tuple) == 1:

            if len(input) > 0:
                for element in input: #RECURSION
                    ListOfStringsToJoin.append("TUPLE" + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a list() or []
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, dict) == 1:

            if len(input) > 0:
                for Key in input: #RECURSION
                    ListOfStringsToJoin.append(str(Key) + ": " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a dict()
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        else:
            ListOfStringsToJoin.append(str(input))
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if len(ListOfStringsToJoin) > 1:

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            StringToReturn = ""
            for Index, StringToProcess in enumerate(ListOfStringsToJoin):

                ################################################
                if Index == 0: #The first element
                    if StringToProcess.find(":") != -1 and StringToProcess[0] != "{": #meaning that we're processing a dict()
                        StringToReturn = "{"
                    elif StringToProcess.find("TUPLE") != -1 and StringToProcess[0] != "(":  # meaning that we're processing a tuple
                        StringToReturn = "("
                    else:
                        StringToReturn = "["

                    StringToReturn = StringToReturn + StringToProcess.replace("TUPLE","") + ", "
                ################################################

                ################################################
                elif Index < len(ListOfStringsToJoin) - 1: #The middle elements
                    StringToReturn = StringToReturn + StringToProcess + ", "
                ################################################

                ################################################
                else: #The last element
                    StringToReturn = StringToReturn + StringToProcess

                    if StringToProcess.find(":") != -1 and StringToProcess[-1] != "}":  # meaning that we're processing a dict()
                        StringToReturn = StringToReturn + "}"
                    elif StringToProcess.find("TUPLE") != -1 and StringToProcess[-1] != ")":  # meaning that we're processing a tuple
                        StringToReturn = StringToReturn + ")"
                    else:
                        StringToReturn = StringToReturn + "]"

                ################################################

            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

        elif len(ListOfStringsToJoin) == 1:
            StringToReturn = ListOfStringsToJoin[0]

        else:
            StringToReturn = ListOfStringsToJoin

        return StringToReturn
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ConvertDictToProperlyFormattedStringForPrinting(self, DictToPrint, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3):

        ProperlyFormattedStringForPrinting = ""
        ItemsPerLineCounter = 0

        for Key in DictToPrint:

            ##########################################################################################################
            if isinstance(DictToPrint[Key], dict): #RECURSION
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     Key + ":\n" + \
                                                     self.ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key], NumberOfDecimalsPlaceToUse, NumberOfEntriesPerLine, NumberOfTabsBetweenItems)

            else:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     Key + ": " + \
                                                     self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key], 0, NumberOfDecimalsPlaceToUse)
            ##########################################################################################################

            ##########################################################################################################
            if ItemsPerLineCounter < NumberOfEntriesPerLine - 1:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\t"*NumberOfTabsBetweenItems
                ItemsPerLineCounter = ItemsPerLineCounter + 1
            else:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\n"
                ItemsPerLineCounter = 0
            ##########################################################################################################

        return ProperlyFormattedStringForPrinting
    ##########################################################################################################
    ##########################################################################################################
