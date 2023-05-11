# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision D, 05/10/2023

Verified working on: Python 2.7, 3.8 for Windows 8.1, 10 64-bit, Ubuntu 20.04, and Raspberry Pi Buster (no Mac testing yet).
'''

__author__ = 'reuben.brewer'

#########################################################
import os
import sys
import platform
import time
import datetime
import math
import collections
import inspect #To enable 'TellWhichFileWereIn'
import threading
import traceback
#########################################################

#########################################################

##########################
import serial #___IMPORTANT: pip install pyserial (NOT pip install serial).
from serial.tools import list_ports
##########################

##########################
global ftd2xx_IMPORTED_FLAG
ftd2xx_IMPORTED_FLAG = 0
try:
    import ftd2xx #https://pypi.org/project/ftd2xx/ 'pip install ftd2xx', current version is 1.3.1 as of 05/06/22. For SetAllFTDIdevicesLatencyTimer function
    ftd2xx_IMPORTED_FLAG = 1

except:
    exceptions = sys.exc_info()[0]
    print("**********")
    print("********** RobotiqGripper2F85_ReubenPython2and3Class __init__: ERROR, failed to import ftdtxx, Exceptions: %s" % exceptions + " ********** ")
    print("**********")
##########################

##########################
if sys.version_info[0] < 3:
    from builtins import bytes #Necessary to make bytes() function call work in Python 2.7
##########################

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
######################################################### #"sudo pip3 install future" (Python 3) AND "sudo pip install future" (Python 2)

#########################################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
#########################################################

class RobotiqGripper2F85_ReubenPython2and3Class(Frame): #Subclass the Tkinter Frame

    ##########################################################################################################
    ##########################################################################################################
    def __init__(self, setup_dict): #Subclass the Tkinter Frame

        print("#################### RobotiqGripper2F85_ReubenPython2and3Class __init__ starting. ####################")

        #########################################################
        #########################################################
        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
        self.EnableInternal_MyPrint_Flag = 0
        self.MainThread_still_running_flag = 0

        self.SerialBaudRate = 115200 #Standard baud rates are: 1200, 2400, 4800, 9600, 19200, 38400, 57600, and 115200
        self.SerialTimeoutSeconds = 0.5
        self.SerialParity = serial.PARITY_NONE
        self.SerialStopBits = serial.STOPBITS_ONE
        self.SerialByteSize = serial.EIGHTBITS
        self.SerialConnectedFlag = -11111
        self.SerialPortNameCorrespondingToCorrectSerialNumber = "default"

        self.CurrentTime_CalculatedFromMainThread = -11111.0
        self.StartingTime_CalculatedFromMainThread = -11111.0
        self.LastTime_CalculatedFromMainThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromMainThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromMainThread = -11111.0

        #When the slave ID of a gripper is different than 9,
        #the Robotiq User Interface cannot detect the gripper if you select Search for Devices.
        #If a gripper is not detected, check the with any slave ID box, and try searching for your device once again.
        self.SlaveIDmin = 1
        self.SlaveIDmax = 247
        self.SlaveIDreceivedFromGripper = -11111

        self.Position_Min = 0
        self.Position_Max = 255

        self.Speed_Min = 0
        self.Speed_Max = 255

        self.Force_Min = 0
        self.Force_Max = 255

        self.SendPositionSpeedForceCommandToGripper_Queue = Queue.Queue()

        self.MostRecentDataDict = dict()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if platform.system() == "Linux":

            if "raspberrypi" in platform.uname(): #os.uname() doesn't work in windows
                self.my_platform = "pi"
            else:
                self.my_platform = "linux"

        elif platform.system() == "Windows":
            self.my_platform = "windows"

        elif platform.system() == "Darwin":
            self.my_platform = "mac"

        else:
            self.my_platform = "other"

        print("RobotiqGripper2F85_ReubenPython2and3Class __init__: The OS platform is: " + self.my_platform)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "GUIparametersDict" in setup_dict:
            self.GUIparametersDict = setup_dict["GUIparametersDict"]

            #########################################################
            #########################################################
            if "USE_GUI_FLAG" in self.GUIparametersDict:
                self.USE_GUI_FLAG = self.PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG", self.GUIparametersDict["USE_GUI_FLAG"])
            else:
                self.USE_GUI_FLAG = 0

            print("RobotiqGripper2F85_ReubenPython2and3Class __init__: USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "root" in self.GUIparametersDict:
                self.root = self.GUIparametersDict["root"]
            else:
                print("RobotiqGripper2F85_ReubenPython2and3Class __init__: ERROR, must pass in 'root'")
                return
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "EnableInternal_MyPrint_Flag" in self.GUIparametersDict:
                self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", self.GUIparametersDict["EnableInternal_MyPrint_Flag"])
            else:
                self.EnableInternal_MyPrint_Flag = 0

            print("RobotiqGripper2F85_ReubenPython2and3Class __init__: EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "PrintToConsoleFlag" in self.GUIparametersDict:
                self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", self.GUIparametersDict["PrintToConsoleFlag"])
            else:
                self.PrintToConsoleFlag = 1

            print("RobotiqGripper2F85_ReubenPython2and3Class __init__: PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "NumberOfPrintLines" in self.GUIparametersDict:
                self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", self.GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
            else:
                self.NumberOfPrintLines = 10

            print("RobotiqGripper2F85_ReubenPython2and3Class __init__: NumberOfPrintLines: " + str(self.NumberOfPrintLines))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "UseBorderAroundThisGuiObjectFlag" in self.GUIparametersDict:
                self.UseBorderAroundThisGuiObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseBorderAroundThisGuiObjectFlag", self.GUIparametersDict["UseBorderAroundThisGuiObjectFlag"])
            else:
                self.UseBorderAroundThisGuiObjectFlag = 0

            print("RobotiqGripper2F85_ReubenPython2and3Class __init__: UseBorderAroundThisGuiObjectFlag: " + str(self.UseBorderAroundThisGuiObjectFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_ROW" in self.GUIparametersDict:
                self.GUI_ROW = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROW", self.GUIparametersDict["GUI_ROW"], 0.0, 1000.0))
            else:
                self.GUI_ROW = 0

            print("RobotiqGripper2F85_ReubenPython2and3Class __init__: GUI_ROW: " + str(self.GUI_ROW))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMN" in self.GUIparametersDict:
                self.GUI_COLUMN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMN", self.GUIparametersDict["GUI_COLUMN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMN = 0

            print("RobotiqGripper2F85_ReubenPython2and3Class __init__: GUI_COLUMN: " + str(self.GUI_COLUMN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADX" in self.GUIparametersDict:
                self.GUI_PADX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADX", self.GUIparametersDict["GUI_PADX"], 0.0, 1000.0))
            else:
                self.GUI_PADX = 0

            print("RobotiqGripper2F85_ReubenPython2and3Class __init__: GUI_PADX: " + str(self.GUI_PADX))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADY" in self.GUIparametersDict:
                self.GUI_PADY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADY", self.GUIparametersDict["GUI_PADY"], 0.0, 1000.0))
            else:
                self.GUI_PADY = 0

            print("RobotiqGripper2F85_ReubenPython2and3Class __init__: GUI_PADY: " + str(self.GUI_PADY))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_ROWSPAN" in self.GUIparametersDict:
                self.GUI_ROWSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROWSPAN", self.GUIparametersDict["GUI_ROWSPAN"], 0.0, 1000.0))
            else:
                self.GUI_ROWSPAN = 1

            print("RobotiqGripper2F85_ReubenPython2and3Class __init__: GUI_ROWSPAN: " + str(self.GUI_ROWSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMNSPAN" in self.GUIparametersDict:
                self.GUI_COLUMNSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMNSPAN", self.GUIparametersDict["GUI_COLUMNSPAN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMNSPAN = 1

            print("RobotiqGripper2F85_ReubenPython2and3Class __init__: GUI_COLUMNSPAN: " + str(self.GUI_COLUMNSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_STICKY" in self.GUIparametersDict:
                self.GUI_STICKY = str(self.GUIparametersDict["GUI_STICKY"])
            else:
                self.GUI_STICKY = "w"

            print("RobotiqGripper2F85_ReubenPython2and3Class __init__: GUI_STICKY: " + str(self.GUI_STICKY))
            #########################################################
            #########################################################

        else:
            self.GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("RobotiqGripper2F85_ReubenPython2and3Class __init__: No GUIparametersDict present, setting USE_GUI_FLAG = " + str(self.USE_GUI_FLAG))

        #print("RobotiqGripper2F85_ReubenPython2and3Class __init__: GUIparametersDict = " + str(self.GUIparametersDict))
        #########################################################
        #########################################################

        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DesiredSerialNumber" in setup_dict:
            self.DesiredSerialNumber = str(setup_dict["DesiredSerialNumber"])
        else:
            print("RobotiqGripper2F85_ReubenPython2and3Class ERROR: Must initialize object with 'DesiredSerialNumber' argument.")
            return

        print("RobotiqGripper2F85_ReubenPython2and3Class __init__: DesiredSerialNumber: " + str(self.DesiredSerialNumber))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DesiredSlaveID" in setup_dict:
            try:
                self.DesiredSlaveID = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("DesiredSlaveID", setup_dict["DesiredSlaveID"], self.SlaveIDmin, self.SlaveIDmax))

            except:
                print("RobotiqGripper2F85_ReubenPython2and3Class __init__: ERROR, DesiredSlaveID invalid.")
        else:
            self.DesiredSlaveID = 9 #Default for gripper

        print("RobotiqGripper2F85_ReubenPython2and3Class __init__: DesiredSlaveID: " + str(self.DesiredSlaveID))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "NameToDisplay_UserSet" in setup_dict:
            self.NameToDisplay_UserSet = str(setup_dict["NameToDisplay_UserSet"])
        else:
            self.NameToDisplay_UserSet = ""

        print("RobotiqGripper2F85_ReubenPython2and3Class __init__: NameToDisplay_UserSet: " + str(self.NameToDisplay_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "MainThread_TimeToSleepEachLoop" in setup_dict:
            self.MainThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("MainThread_TimeToSleepEachLoop", setup_dict["MainThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.MainThread_TimeToSleepEachLoop = 0.005

        print("RobotiqGripper2F85_ReubenPython2and3Class __init__: MainThread_TimeToSleepEachLoop: " + str(self.MainThread_TimeToSleepEachLoop))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "Position_Starting" in setup_dict:
            self.Position_Starting = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("Position_Starting", setup_dict["Position_Starting"], self.Position_Min, self.Position_Max)

        else:
            self.Position_Starting = 0.5*(self.Position_Max - self.Position_Min)

        print("RobotiqGripper2F85_ReubenPython2and3Class: Position_Starting: " + str(self.Position_Starting))
        #########################################################
        #########################################################
        
        #########################################################
        #########################################################
        if "Speed_Starting" in setup_dict:
            self.Speed_Starting = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("Speed_Starting", setup_dict["Speed_Starting"], self.Speed_Min, self.Speed_Max)

        else:
            self.Speed_Starting = 0.5*(self.Speed_Max - self.Speed_Min)

        print("RobotiqGripper2F85_ReubenPython2and3Class: Speed_Starting: " + str(self.Speed_Starting))
        #########################################################
        #########################################################
        
        #########################################################
        #########################################################
        if "Force_Starting" in setup_dict:
            self.Force_Starting = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("Force_Starting", setup_dict["Force_Starting"], self.Force_Min, self.Force_Max)

        else:
            self.Force_Starting = 0.5*(self.Force_Max - self.Force_Min)

        print("RobotiqGripper2F85_ReubenPython2and3Class: Force_Starting: " + str(self.Force_Starting))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "SendPositionSpeedForceCommandToGripper_Queue_MaxSize" in setup_dict:
            self.SendPositionSpeedForceCommandToGripper_Queue_MaxSize = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("SendPositionSpeedForceCommandToGripper_Queue_MaxSize", setup_dict["SendPositionSpeedForceCommandToGripper_Queue_MaxSize"], 1.0, 100000.0))

        else:
            self.SendPositionSpeedForceCommandToGripper_Queue_MaxSize = 1

        print("URarm_ReubenPython2and3Class __init__: SendPositionSpeedForceCommandToGripper_Queue_MaxSize: " + str(self.SendPositionSpeedForceCommandToGripper_Queue_MaxSize))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "SendConfirmationToCommandFlag" in setup_dict:
            self.SendConfirmationToCommandFlag = self.PassThrough0and1values_ExitProgramOtherwise("SendConfirmationToCommandFlag", setup_dict["SendConfirmationToCommandFlag"])
        else:
            self.SendConfirmationToCommandFlag = 0

        print("RobotiqGripper2F85_ReubenPython2and3Class __init__: SendConfirmationToCommandFlag: " + str(self.SendConfirmationToCommandFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.Position_NeedsToBeChangedFlag = 1
        self.Position_ToBeSet = self.Position_Starting
        self.Position_GUIscale_NeedsToBeChangedFlag = 0
        #########################################################
        #########################################################
        
        #########################################################
        #########################################################
        self.Speed_NeedsToBeChangedFlag = 1
        self.Speed_ToBeSet = self.Speed_Starting
        self.Speed_GUIscale_NeedsToBeChangedFlag = 0
        #########################################################
        #########################################################
        
        #########################################################
        #########################################################
        self.Force_NeedsToBeChangedFlag = 1
        self.Force_ToBeSet = self.Force_Starting
        self.Force_GUIscale_NeedsToBeChangedFlag = 0
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.PrintToGui_Label_TextInputHistory_List = [" "]*self.NumberOfPrintLines
        self.PrintToGui_Label_TextInput_Str = ""
        self.GUI_ready_to_be_updated_flag = 0
        #########################################################
        #########################################################

        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:

            ################
            if ftd2xx_IMPORTED_FLAG == 1:
                self.SetAllFTDIdevicesLatencyTimer()
            ################

            ################
            self.FindAssignAndOpenSerialPort()
            ################

        except:
            exceptions = sys.exc_info()[0]
            print("RobotiqGripper2F85_ReubenPython2and3Class __init__: Failed to open serial object, Exceptions: %s" % exceptions)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if self.SerialConnectedFlag == 1:

            #########################################################
            #########################################################
            self.ActivateGripper() #The gripper will move between its motion limits after the first position-command after ActivateGripper is called.
            time.sleep(0.010) #MUST WAIT A LITTLE AFTER ACTIVATING THE GRIPPER BEFORE ISSUING THE FIRST MOTION COMMAND
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            self.MainThread_ThreadingObject = threading.Thread(target=self.MainThread, args=())
            self.MainThread_ThreadingObject.start()
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if self.USE_GUI_FLAG == 1:
                self.StartGUI(self.root)
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            time.sleep(0.25)
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1
            #########################################################
            #########################################################

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
    def getPreciseSecondsTimeStampString(self):
        ts = time.time()

        return ts
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentDataDict(self):

        if self.EXIT_PROGRAM_FLAG == 0:

            self.MostRecentDataDict = dict([("SlaveIDreceivedFromGripper", self.SlaveIDreceivedFromGripper),
                                            ("DataStreamingFrequency_CalculatedFromMainThread", self.DataStreamingFrequency_CalculatedFromMainThread),
                                            ("Time", self.CurrentTime_CalculatedFromMainThread)])

            #deepcopy is NOT required as MostRecentDataDict only contains numbers (no lists, dicts, etc. that go beyond 1-level).
            return self.MostRecentDataDict.copy()

        else:
            return dict() #So that we're not returning variables during the close-down process.
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_MainThread(self):

        try:
            self.DataStreamingDeltaT_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread - self.LastTime_CalculatedFromMainThread

            if self.DataStreamingDeltaT_CalculatedFromMainThread != 0.0:
                self.DataStreamingFrequency_CalculatedFromMainThread = 1.0/self.DataStreamingDeltaT_CalculatedFromMainThread

            self.LastTime_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_MainThread ERROR with Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ###########################################################################################################
    ##########################################################################################################
    def SetAllFTDIdevicesLatencyTimer(self, FTDI_LatencyTimer_ToBeSet = 1):

        FTDI_LatencyTimer_ToBeSet = self.LimitNumber_IntOutputOnly(1, 16, FTDI_LatencyTimer_ToBeSet)

        FTDI_DeviceList = ftd2xx.listDevices()
        print("FTDI_DeviceList: " + str(FTDI_DeviceList))

        if FTDI_DeviceList != None:

            for Index, FTDI_SerialNumber in enumerate(FTDI_DeviceList):

                #################################
                try:
                    if sys.version_info[0] < 3: #Python 2
                        FTDI_SerialNumber = str(FTDI_SerialNumber)
                    else:
                        FTDI_SerialNumber = FTDI_SerialNumber.decode('utf-8')

                    FTDI_Object = ftd2xx.open(Index)
                    FTDI_DeviceInfo = FTDI_Object.getDeviceInfo()

                    '''
                    print("FTDI device with serial number " +
                          str(FTDI_SerialNumber) +
                          ", DeviceInfo: " +
                          str(FTDI_DeviceInfo))
                    '''

                except:
                    exceptions = sys.exc_info()[0]
                    print("FTDI device with serial number " + str(FTDI_SerialNumber) + ", could not open FTDI device, Exceptions: %s" % exceptions)
                #################################

                #################################
                try:
                    FTDI_Object.setLatencyTimer(FTDI_LatencyTimer_ToBeSet)
                    time.sleep(0.005)

                    FTDI_LatencyTimer_ReceivedFromDevice = FTDI_Object.getLatencyTimer()
                    FTDI_Object.close()

                    if FTDI_LatencyTimer_ReceivedFromDevice == FTDI_LatencyTimer_ToBeSet:
                        SuccessString = "succeeded!"
                    else:
                        SuccessString = "failed!"

                    print("FTDI device with serial number " +
                          str(FTDI_SerialNumber) +
                          " commanded setLatencyTimer(" +
                          str(FTDI_LatencyTimer_ToBeSet) +
                          "), and getLatencyTimer() returned: " +
                          str(FTDI_LatencyTimer_ReceivedFromDevice) +
                          ", so command " +
                          SuccessString)

                except:
                    exceptions = sys.exc_info()[0]
                    print("FTDI device with serial number " + str(FTDI_SerialNumber) + ", could not set/get Latency Timer, Exceptions: %s" % exceptions)
                #################################

        else:
            print("SetAllFTDIdevicesLatencyTimer ERROR: FTDI_DeviceList is empty, cannot proceed.")
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def FindAssignAndOpenSerialPort(self):
        self.MyPrint_WithoutLogFile("FindAssignAndOpenSerialPort: Finding all serial ports...")

        ##############
        SerialNumberToCheckAgainst = str(self.DesiredSerialNumber)
        if self.my_platform == "linux" or self.my_platform == "pi":
            SerialNumberToCheckAgainst = SerialNumberToCheckAgainst[:-1] #The serial number gets truncated by one digit in linux
        else:
            SerialNumberToCheckAgainst = SerialNumberToCheckAgainst
        ##############

        ##############
        SerialPortsAvailable_ListPortInfoObjetsList = serial.tools.list_ports.comports()
        ##############

        ###########################################################################
        SerialNumberFoundFlag = 0
        for SerialPort_ListPortInfoObjet in SerialPortsAvailable_ListPortInfoObjetsList:

            SerialPortName = SerialPort_ListPortInfoObjet[0]
            Description = SerialPort_ListPortInfoObjet[1]
            VID_PID_SerialNumber_Info = SerialPort_ListPortInfoObjet[2]
            self.MyPrint_WithoutLogFile(SerialPortName + ", " + Description + ", " + VID_PID_SerialNumber_Info)

            if VID_PID_SerialNumber_Info.find(SerialNumberToCheckAgainst) != -1 and SerialNumberFoundFlag == 0: #Haven't found a match in a prior loop
                self.SerialPortNameCorrespondingToCorrectSerialNumber = SerialPortName
                SerialNumberFoundFlag = 1 #To ensure that we only get one device
                self.MyPrint_WithoutLogFile("FindAssignAndOpenSerialPort: Found serial number " + SerialNumberToCheckAgainst + " on port " + self.SerialPortNameCorrespondingToCorrectSerialNumber)
                #WE DON'T BREAK AT THIS POINT BECAUSE WE WANT TO PRINT ALL SERIAL DEVICE NUMBERS WHEN PLUGGING IN A DEVICE WITH UNKNOWN SERIAL NUMBE RFOR THE FIRST TIME.
        ###########################################################################

        ###########################################################################
        if(self.SerialPortNameCorrespondingToCorrectSerialNumber != "default"): #We found a match

            try: #Will succeed as long as another program hasn't already opened the serial line.

                self.SerialObject = serial.Serial(self.SerialPortNameCorrespondingToCorrectSerialNumber, self.SerialBaudRate, timeout=self.SerialTimeoutSeconds, parity=self.SerialParity, stopbits=self.SerialStopBits, bytesize=self.SerialByteSize)
                self.SerialConnectedFlag = 1
                self.MyPrint_WithoutLogFile("FindAssignAndOpenSerialPort: Serial is connected and open on port: " + self.SerialPortNameCorrespondingToCorrectSerialNumber)

            except:
                self.SerialConnectedFlag = 0
                self.MyPrint_WithoutLogFile("FindAssignAndOpenSerialPort: ERROR: Serial is physically plugged in but IS IN USE BY ANOTHER PROGRAM.")

        else:
            self.SerialConnectedFlag = -1
            self.MyPrint_WithoutLogFile("FindAssignAndOpenSerialPort: ERROR: Could not find the serial device. IS IT PHYSICALLY PLUGGED IN?")
        ###########################################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def LimitNumber_IntOutputOnly(self, min_val, max_val, test_val):
        if test_val > max_val:
            test_val = max_val

        elif test_val < min_val:
            test_val = min_val

        else:
            test_val = test_val

        test_val = int(test_val)

        return test_val
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ActivateGripper(self):

        self.MyPrint_WithoutLogFile("Activating gripper!")

        ActivateGripper_1stMessage_ByteObject = bytes([self.DesiredSlaveID]) + (b"\x10\x03\xE8\x00\x03\x06\x00\x00\x00\x00\x00\x00")
        self.CreateAndTxMessage(ActivateGripper_1stMessage_ByteObject)

        ######################################################################## Tx
        '''
        Example for manual:
        Step 1: Activation Request ( clear and set rACT)
        Request is (clear rAct): 09 10 03 E8 00 03 06 00 00 00 00 00 00 73 30
        
        Bits Description
        09 SlaveID
        10 Function Code 16 (Preset Multiple Registers)
        03E8 Address of the first register
        0003 Number of registers written to
        06 Number of data bytes to follow (3 registers x 2 bytes/register = 6 bytes)
        0000 Value to write to register 0x03E9 (ACTION REQUEST = 0x01 and GRIPPER OPTIONS = 0x00): rACT = 1 for "Activate Gripper"
        0000 Value written to register 0x03EA
        0000 Value written to register 0x03EB
        7330 Cyclic Redundancy Check (CRC)
        '''
        ########################################################################

        ######################################################################## Rx
        if self.SendConfirmationToCommandFlag == 1:
            Data_Raw = self.SerialObject.readline() #Format = b'\t\x10\x03\xe8\x00\x03\x010'
            print("ActivateGripper, Response_1 Data_Raw:" + str(Data_Raw))
            self.ParseRxMessage(Data_Raw)

            '''
            Example for manual:
            Response is: 09 10 03 E8 00 03 01 30
            
            Bits Description
            09 SlaveID
            10 Function Code 16 (Preset Multiple Registers)
            03E8 Address of the first register
            0003 Number of written registers
            0130 Cyclic Redundancy Check (CRC)
            '''
        ########################################################################

        ######################################################################## Tx
        ActivateGripper_2ndMessage_ByteObject = bytes([self.DesiredSlaveID]) + (b"\x03\x07\xD0\x00\x01")
        self.CreateAndTxMessage(ActivateGripper_2ndMessage_ByteObject)

        '''
        Example for manual:
        Step 2: Read Gripper status until the activation is completed
        Request is: 09 03 07 D0 00 01 85 CF
        
        Bits Description
        09 SlaveID
        03 Function Code 03 (Read Holding Registers)
        07D0 Address of the first requested register
        0001 Number of registers requested (1)
        85CF Cyclic Redundancy Check (CRC)
        '''
        ########################################################################

        ######################################################################## Rx
        if self.SendConfirmationToCommandFlag == 1:
            Data_Raw = self.SerialObject.readline()
            print("ActivateGripper, Response_2 Data_Raw:" + str(Data_Raw))
            self.ParseRxMessage(Data_Raw)

            '''
            Example for manual:
            Response (if the activation IS NOT completed): 09 03 02 11 00 55 D5
            
            Bits Description
            09 SlaveID
            03 Function Code 03 (Read Holding Registers)
            02 Number of data bytes to follow (1 register x 2 bytes/register = 2 bytes)
            1100 Content of register 07D0 (GRIPPER STATUS = 0x11, RESERVED = 0x00): gACT = 1 for "Gripper Activation", gSTA = 1 for"Activation in progress"
            55D5 Cyclic Redundancy Check (CRC)
        
            Response (if the activation IS completed): 09 03 02 31 00 4C 15
            
            Bits Description
            09 SlaveID
            03 Function Code 03 (Read Holding Registers)
            02 Number of data bytes to follow (1 register x 2 bytes/register = 2 bytes)
            3100 Content of register 07D0 (GRIPPER STATUS = 0x31, RESERVED = 0x00): gACT = 1 for "Gripper Activation", gSTA = 3 for "Activation is completed"
            4C15 Cyclic Redundancy Check (CRC)
            '''
        ########################################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SendPositionSpeedForceCommandToGripper_ExternalClassFunction(self, Position, Speed, Force, IgnoreNewDataIfQueueIsFullFlag = 1):

        CommandToSendDict = dict([("Position", Position), ("Speed", Speed), ("Force", Force)])

        if self.SendPositionSpeedForceCommandToGripper_Queue.qsize() < self.SendPositionSpeedForceCommandToGripper_Queue_MaxSize:
            self.SendPositionSpeedForceCommandToGripper_Queue.put(CommandToSendDict)
        else:
            if IgnoreNewDataIfQueueIsFullFlag != 1:
                dummy = self.SendPositionSpeedForceCommandToGripper_Queue.get()  # makes room for one more message
                self.SendPositionSpeedForceCommandToGripper_Queue.put(CommandToSendDict)  # backfills that message with new data

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __SendPositionSpeedForceCommandToGripper_InternalClassFunction(self, Position, Speed, Force):

        ########################################################################
        try:
            PositionLimited = self.LimitNumber_IntOutputOnly(self.Position_Min, self.Position_Max, Position)
            SpeedLimited = self.LimitNumber_IntOutputOnly(self.Speed_Min, self.Speed_Max, Speed)
            ForceLimited = self.LimitNumber_IntOutputOnly(self.Force_Min, self.Force_Max, Force)

            __SendPositionSpeedForceCommandToGripper_InternalClassFunction_MessageWithoutChecksum_IntsList = self.ConvertByteAarrayObjectToIntsList(bytes([self.DesiredSlaveID]) + b"\x10\x03\xE8\x00\x03\x06\x09\x00\x00") + [PositionLimited, SpeedLimited, ForceLimited]

            self.CreateAndTxMessage(__SendPositionSpeedForceCommandToGripper_InternalClassFunction_MessageWithoutChecksum_IntsList)

            '''
            Example from manual:
            Step 3: Move the robot to the pick-up location
            Step 4: Close the Gripper at full speed and full force
            Request is: 09 10 03 E8 00 03 06 09 00 00 FF FF FF 42 29
            Bits Description
            09 SlaveID
            10 Function Code 16 (Preset Multiple Registers)
            03E8 Address of the first register
            0003 Number of registers written to
            06 Number of data bytes to follow (3 registers x 2 bytes/register = 6 bytes)
            0900 Value written to register 0x03E8 (ACTION REQUEST = 0x09 and GRIPPER OPTIONS = 0x00): rACT = 1 for "Activate Gripper", rGTO = 1 for "Go to Requested Position"
            00FF Value written to register 0x03E9 (GRIPPER OPTIONS 2 = 0x00 and POSITION REQUEST = 0xFF): rPR = 255/255 for full closing of the Gripper
            FFFF Value written to register 0x03EA (SPEED = 0xFF and FORCE = 0xFF): full speed and full force
            4229 Cyclic Redundancy Check (CRC)
            '''

            ########################################################################
            if self.SendConfirmationToCommandFlag == 1:
                Data_Raw = self.SerialObject.readline()
                print("__SendPositionSpeedForceCommandToGripper_InternalClassFunction, Response:" + str(Data_Raw))
                self.ParseRxMessage(Data_Raw)

                '''
                Example from manual:
                Response is: 09 10 03 E8 00 03 01 30
                Bits Description
                09 SlaveID
                10 Function Code 16 (Preset Multiple Registers)
                03E8 Address of the first register
                0003 Number of written registers
                0130 Cyclic Redundancy Check (CRC)
                '''
                ########################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("__SendPositionSpeedForceCommandToGripper_InternalClassFunction: Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CalculateCRC16modbus(self, InputData):
        #"Steps" copied and pasted from Modbus_over_serial_line_V1_02.pdf

        CRC16modbus = 0xFFFF

        for Byte in InputData:

            CRC16modbus ^= Byte  # For "bytes" object

            for i in range(8):
                if ((CRC16modbus & 1) != 0):
                    CRC16modbus >>= 1
                    CRC16modbus ^= 0xA001

                else:
                    CRC16modbus >>= 1

        CRC16modbus_LoByte = CRC16modbus & 0xFF
        CRC16modbus_HiByte = CRC16modbus >> 8

        return [CRC16modbus_LoByte, CRC16modbus_HiByte]
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ParseRxMessage(self, RxMessage_DataRaw):

        try:
            ###################################
            RxMessage_IntsList = self.ConvertByteAarrayObjectToIntsList(RxMessage_DataRaw)
            ###################################

            ##########################################################################################################
            if len(RxMessage_IntsList) >= 5: #SlaveID, Function Code, Address of the 1st register, .....CRC16modbus is 2 bytes

                ###################################
                CRC16modbus_CalculatedFromMessageBytes_ReturnedAsListOfHiAndLoByte = self.CalculateCRC16modbus(RxMessage_IntsList[:-2])
                CRC16modbus_CalculatedFromMessageBytes_LoByte = CRC16modbus_CalculatedFromMessageBytes_ReturnedAsListOfHiAndLoByte[0]
                CRC16modbus_CalculatedFromMessageBytes_HiByte = CRC16modbus_CalculatedFromMessageBytes_ReturnedAsListOfHiAndLoByte[1]

                CRC16modbus_SwappedLoAndHiBytes_ComboIntoInt = ((CRC16modbus_CalculatedFromMessageBytes_LoByte) << 8) | (CRC16modbus_CalculatedFromMessageBytes_HiByte)
                ###################################

                ###################################
                CRC16modbus_InludedAsLastBytesOfMessage_LoByte = RxMessage_IntsList[-1]
                CRC16modbus_InludedAsLastBytesOfMessage_HiByte = RxMessage_IntsList[-2]
                CRC16modbusBytes_Manual_ComboIntoInt = (CRC16modbus_InludedAsLastBytesOfMessage_HiByte << 8) | (CRC16modbus_InludedAsLastBytesOfMessage_LoByte)
                ###################################

                ###################################
                if CRC16modbus_SwappedLoAndHiBytes_ComboIntoInt != CRC16modbusBytes_Manual_ComboIntoInt:
                    print("ParseRxMessage, Checksum error. CRC16modbus_SwappedLoAndHiBytes_ComboIntoInt = " +
                          str(CRC16modbus_SwappedLoAndHiBytes_ComboIntoInt) +
                          ", CRC16modbusBytes_Manual_ComboIntoInt = " + str(CRC16modbusBytes_Manual_ComboIntoInt))
                    return 0

                else:

                    self.SlaveIDreceivedFromGripper = int(RxMessage_IntsList[0])

                    return 1
                ###################################

            ##########################################################################################################

            ##########################################################################################################
            else:
                return 0
            ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("ParseRxMessage: Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CreateAndTxMessage(self, MessageToSendWithoutCRC16modbus_ByteArrayObject):

        try:
            ###################################
            if type(MessageToSendWithoutCRC16modbus_ByteArrayObject) == bytes:
                MessageToSendWithoutCRC16modbus_IntsList = self.ConvertByteAarrayObjectToIntsList(MessageToSendWithoutCRC16modbus_ByteArrayObject)
            else:
                MessageToSendWithoutCRC16modbus_IntsList = MessageToSendWithoutCRC16modbus_ByteArrayObject
            ###################################

            ###################################
            CRC16modbus_CalculatedFromMessageBytes_ReturnedAsListOfHiAndLoByte = self.CalculateCRC16modbus(MessageToSendWithoutCRC16modbus_IntsList)
            CRC16modbus_CalculatedFromMessageBytes_LoByte = CRC16modbus_CalculatedFromMessageBytes_ReturnedAsListOfHiAndLoByte[0]
            CRC16modbus_CalculatedFromMessageBytes_HiByte = CRC16modbus_CalculatedFromMessageBytes_ReturnedAsListOfHiAndLoByte[1]

            CRC16modbus_SwappedLoAndHiBytes_ComboIntoInt = ((CRC16modbus_CalculatedFromMessageBytes_LoByte) << 8) | (CRC16modbus_CalculatedFromMessageBytes_HiByte)
            ###################################

            ###################################
            CRC16modbus_InludedAsLastBytesOfMessage_LoByte = CRC16modbus_CalculatedFromMessageBytes_HiByte
            CRC16modbus_InludedAsLastBytesOfMessage_HiByte = CRC16modbus_CalculatedFromMessageBytes_LoByte

            MessageToSendIncludingCRC16modbus_IntsList = list(MessageToSendWithoutCRC16modbus_IntsList)
            MessageToSendIncludingCRC16modbus_IntsList.append(CRC16modbus_InludedAsLastBytesOfMessage_HiByte)
            MessageToSendIncludingCRC16modbus_IntsList.append(CRC16modbus_InludedAsLastBytesOfMessage_LoByte)
            ###################################

            ###################################
            self.SerialObject.write(MessageToSendIncludingCRC16modbus_IntsList)
            ###################################
            
        except:
            exceptions = sys.exc_info()[0]
            print("CreateAndTxMessage: Exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ConvertByteAarrayObjectToIntsList(self, Input_ByteArrayObject):

        if type(Input_ByteArrayObject) != bytes:
            print("ConvertByteAarrayObjectToIntsList ERROR, Input_ByteArrayObject must be type = bytes")
            return list()
        else:
            Output_IntsList = list()
            for element in Input_ByteArrayObject:
                Output_IntsList.append(int(element))

            return Output_IntsList
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## unicorn
    ########################################################################################################## 
    def MainThread(self):

        self.MyPrint_WithoutLogFile("Started MainThread for RobotiqGripper2F85_ReubenPython2and3Class object.")
        
        self.MainThread_still_running_flag = 1

        self.StartingTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString()

        self.SendPositionSpeedForceCommandToGripper_ExternalClassFunction(self.Position_ToBeSet, self.Speed_ToBeSet, self.Force_ToBeSet)

        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ###############################################
            ###############################################
            ###############################################
            self.CurrentTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromMainThread
            ###############################################
            ###############################################
            ###############################################

            ###############################################
            ###############################################
            ###############################################
            if self.SendPositionSpeedForceCommandToGripper_Queue.qsize() > 0:
                try:
                    CommandToSendDict = self.SendPositionSpeedForceCommandToGripper_Queue.get()

                    Position = CommandToSendDict["Position"]
                    Speed = CommandToSendDict["Speed"]
                    Force = CommandToSendDict["Force"]

                    ###################
                    if Position != self.Position_ToBeSet:
                        self.Position_ToBeSet = Position
                        self.Position_GUIscale_NeedsToBeChangedFlag = 1
                    ###################

                    ###################
                    if Speed != self.Speed_ToBeSet:
                        self.Speed_ToBeSet = Speed
                        self.Speed_GUIscale_NeedsToBeChangedFlag = 1
                    ###################

                    ###################
                    if Force != self.Force_ToBeSet:
                        self.Force_ToBeSet = Force
                        self.Force_GUIscale_NeedsToBeChangedFlag = 1
                    ###################

                    self.__SendPositionSpeedForceCommandToGripper_InternalClassFunction(self.Position_ToBeSet, self.Speed_ToBeSet, self.Force_ToBeSet)

                except:
                    exceptions = sys.exc_info()[0]
                    print("DedicatedTxThread Exceptions: %s" % exceptions)
            ###############################################
            ###############################################
            ###############################################
            
            ############################################### USE THE TIME.SLEEP() TO SET THE LOOP FREQUENCY
            ###############################################
            ###############################################
            self.UpdateFrequencyCalculation_MainThread()

            if self.MainThread_TimeToSleepEachLoop > 0.0:
                time.sleep(self.MainThread_TimeToSleepEachLoop)
            ###############################################
            ###############################################
            ###############################################

        ##########################################################################################################
        
        self.MyPrint_WithoutLogFile("Finished MainThread for RobotiqGripper2F85_ReubenPython2and3Class object.")
        
        self.MainThread_still_running_flag = 0
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for RobotiqGripper2F85_ReubenPython2and3Class object")

        self.EXIT_PROGRAM_FLAG = 1

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StartGUI(self, GuiParent):

        #self.GUI_Thread_ThreadingObject = threading.Thread(target=self.GUI_Thread, args=(GuiParent,))
        #self.GUI_Thread_ThreadingObject.setDaemon(True) #Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
        #self.GUI_Thread_ThreadingObject.start()

        self.GUI_Thread(GuiParent)
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_Thread(self, parent):

        print("Starting the GUI_Thread for RobotiqGripper2F85_ReubenPython2and3Class object.")

        #################################################
        self.root = parent
        self.parent = parent
        #################################################

        #################################################
        self.myFrame = Frame(self.root)

        if self.UseBorderAroundThisGuiObjectFlag == 1:
            self.myFrame["borderwidth"] = 2
            self.myFrame["relief"] = "ridge"

        self.myFrame.grid(row = self.GUI_ROW,
                          column = self.GUI_COLUMN,
                          padx = self.GUI_PADX,
                          pady = self.GUI_PADY,
                          rowspan = self.GUI_ROWSPAN,
                          columnspan= self.GUI_COLUMNSPAN,
                          sticky = self.GUI_STICKY)
        #################################################

        #################################################
        self.TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150) #RGB
        self.TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150) #RGB
        self.TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
        self.TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
        self.TkinterScaleLabelWidth = 30
        self.TkinterScaleWidth = 10
        self.TkinterScaleLength = 250
        #################################################

        #################################################
        self.DeviceInfo_Label = Label(self.myFrame, text="Device Info", width=50)
        self.DeviceInfo_Label["text"] = self.NameToDisplay_UserSet
        self.DeviceInfo_Label.grid(row=0, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        #################################################

        #################################################
        self.Data_Label = Label(self.myFrame, text="Data_Label", width=100)
        self.Data_Label.grid(row=1, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        #################################################

        ###################################################
        self.ControlsFrame = Frame(self.myFrame)
        self.ControlsFrame.grid(row = 2, column = 0, padx = 1, pady = 1, rowspan = 1, columnspan= 1)
        ###################################################

        ###################################################
        self.Position_GUIscale_LabelObject = Label(self.ControlsFrame, text="Position", width=self.TkinterScaleLabelWidth)
        self.Position_GUIscale_LabelObject.grid(row=0, column=0, padx=1, pady=1, columnspan=1, rowspan=1)

        self.Position_GUIscale_Value = DoubleVar()
        self.Position_GUIscale_ScaleObject = Scale(self.ControlsFrame,
                                        from_=self.Position_Min,
                                        to=self.Position_Max,
                                        #tickinterval=
                                        orient=HORIZONTAL,
                                        borderwidth=2,
                                        showvalue=True,
                                        width=self.TkinterScaleWidth,
                                        length=self.TkinterScaleLength,
                                        resolution=1,
                                        variable=self.Position_GUIscale_Value)
        
        self.Position_GUIscale_ScaleObject.bind('<Button-1>', lambda event: self.Position_GUIscale_EventResponse(event))
        self.Position_GUIscale_ScaleObject.bind('<B1-Motion>', lambda event: self.Position_GUIscale_EventResponse(event))
        self.Position_GUIscale_ScaleObject.bind('<ButtonRelease-1>', lambda event: self.Position_GUIscale_EventResponse(event))
        self.Position_GUIscale_ScaleObject.set(self.Position_ToBeSet)
        self.Position_GUIscale_ScaleObject.grid(row=0, column=1, padx=1, pady=1, columnspan=1, rowspan=1)
        ###################################################

        ###################################################
        self.Speed_GUIscale_LabelObject = Label(self.ControlsFrame, text="Speed", width=self.TkinterScaleLabelWidth)
        self.Speed_GUIscale_LabelObject.grid(row=1, column=0, padx=1, pady=1, columnspan=1, rowspan=1)

        self.Speed_GUIscale_Value = DoubleVar()
        self.Speed_GUIscale_ScaleObject = Scale(self.ControlsFrame,
                                        from_=self.Speed_Min,
                                        to=self.Speed_Max,
                                        #tickinterval=
                                        orient=HORIZONTAL,
                                        borderwidth=2,
                                        showvalue=True,
                                        width=self.TkinterScaleWidth,
                                        length=self.TkinterScaleLength,
                                        resolution=1,
                                        variable=self.Speed_GUIscale_Value)
        
        self.Speed_GUIscale_ScaleObject.bind('<Button-1>', lambda event: self.Speed_GUIscale_EventResponse(event))
        self.Speed_GUIscale_ScaleObject.bind('<B1-Motion>', lambda event: self.Speed_GUIscale_EventResponse(event))
        self.Speed_GUIscale_ScaleObject.bind('<ButtonRelease-1>', lambda event: self.Speed_GUIscale_EventResponse(event))
        self.Speed_GUIscale_ScaleObject.set(self.Speed_ToBeSet)
        self.Speed_GUIscale_ScaleObject.grid(row=1, column=1, padx=1, pady=1, columnspan=1, rowspan=1)
        ###################################################
        
        ###################################################
        self.Force_GUIscale_LabelObject = Label(self.ControlsFrame, text="Force", width=self.TkinterScaleLabelWidth)
        self.Force_GUIscale_LabelObject.grid(row=2, column=0, padx=1, pady=1, columnspan=1, rowspan=1)

        self.Force_GUIscale_Value = DoubleVar()
        self.Force_GUIscale_ScaleObject = Scale(self.ControlsFrame,
                                        from_=self.Force_Min,
                                        to=self.Force_Max,
                                        #tickinterval=
                                        orient=HORIZONTAL,
                                        borderwidth=2,
                                        showvalue=True,
                                        width=self.TkinterScaleWidth,
                                        length=self.TkinterScaleLength,
                                        resolution=1,
                                        variable=self.Force_GUIscale_Value)
        
        self.Force_GUIscale_ScaleObject.bind('<Button-1>', lambda event: self.Force_GUIscale_EventResponse(event))
        self.Force_GUIscale_ScaleObject.bind('<B1-Motion>', lambda event: self.Force_GUIscale_EventResponse(event))
        self.Force_GUIscale_ScaleObject.bind('<ButtonRelease-1>', lambda event: self.Force_GUIscale_EventResponse(event))
        self.Force_GUIscale_ScaleObject.set(self.Force_ToBeSet)
        self.Force_GUIscale_ScaleObject.grid(row=2, column=1, padx=1, pady=1, columnspan=1, rowspan=1)
        ###################################################

        #################################################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=150)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=3, column=0, padx=1, pady=1, columnspan=1, rowspan=10)
        #################################################

        #################################################
        self.GUI_ready_to_be_updated_flag = 1
        #################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Position_GUIscale_EventResponse(self, event):

        self.Position_ToBeSet = self.Position_GUIscale_Value.get()
        # INTENTIONALLY NOT CHECKING THE QSIZE HERE!
        self.SendPositionSpeedForceCommandToGripper_ExternalClassFunction(self.Position_ToBeSet, self.Speed_ToBeSet, self.Force_ToBeSet)

        #self.MyPrint_WithoutLogFile("Position_GUIscale_EventResponse: Position set to " + str(self.Position_ToBeSet))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Speed_GUIscale_EventResponse(self, event):

        self.Speed_ToBeSet = self.Speed_GUIscale_Value.get()
        # INTENTIONALLY NOT CHECKING THE QSIZE HERE!
        self.SendPositionSpeedForceCommandToGripper_ExternalClassFunction(self.Position_ToBeSet, self.Speed_ToBeSet, self.Force_ToBeSet)

        #self.MyPrint_WithoutLogFile("Speed_GUIscale_EventResponse: Speed set to " + str(self.Speed_ToBeSet))
    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    def Force_GUIscale_EventResponse(self, event):

        self.Force_ToBeSet = self.Force_GUIscale_Value.get()
        # INTENTIONALLY NOT CHECKING THE QSIZE HERE!
        self.SendPositionSpeedForceCommandToGripper_ExternalClassFunction(self.Position_ToBeSet, self.Speed_ToBeSet, self.Force_ToBeSet)

        #self.MyPrint_WithoutLogFile("Force_GUIscale_EventResponse: Force set to " + str(self.Force_ToBeSet))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_update_clock(self):

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
                    self.Data_Label["text"] = "SlaveIDreceivedFromGripper: " + str(self.SlaveIDreceivedFromGripper) +\
                                            "\nTime: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.CurrentTime_CalculatedFromMainThread, 0, 3) + \
                                            "\tMain Thread Frequency: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_CalculatedFromMainThread, 0, 3) + \
                                            "\nSendPositionSpeedForceCommandToGripper_Queue.qsize(): " + str(self.SendPositionSpeedForceCommandToGripper_Queue.qsize())
                    #######################################################

                    #######################################################
                    if self.Position_GUIscale_NeedsToBeChangedFlag == 1:
                        self.Position_GUIscale_ScaleObject.set(self.Position_ToBeSet)
                        self.Position_GUIscale_NeedsToBeChangedFlag = 0
                    #######################################################

                    #######################################################
                    if self.Speed_GUIscale_NeedsToBeChangedFlag == 1:
                        self.Speed_GUIscale_ScaleObject.set(self.Speed_ToBeSet)
                        self.Speed_GUIscale_NeedsToBeChangedFlag = 0
                    #######################################################
                    
                    #######################################################
                    if self.Force_GUIscale_NeedsToBeChangedFlag == 1:
                        self.Force_GUIscale_ScaleObject.set(self.Force_ToBeSet)
                        self.Force_GUIscale_NeedsToBeChangedFlag = 0
                    #######################################################
                    
                    #######################################################
                    self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                    #######################################################

                except:
                    exceptions = sys.exc_info()[0]
                    print("RobotiqGripper2F85_ReubenPython2and3Class GUI_update_clock ERROR: Exceptions: %s" % exceptions)
                    traceback.print_exc()
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
    def ConvertBytesObjectToString(self, InputBytesObject):

        if sys.version_info[0] < 3:  # Python 2
            OutputString = str(InputBytesObject)

        else:
            OutputString = InputBytesObject.decode('utf-8')

        return OutputString
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

