# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision D, 08/29/2022

Verified working on: Python 3.8 for Windows 10 64-bit.
'''

__author__ = 'reuben.brewer'

#########################################################
from LowPassFilter_ReubenPython2and3Class import *
#########################################################

#########################################################
import os
import sys
import platform
import time
import datetime
import math
import collections
from copy import * #for deepcopy
import inspect #To enable 'TellWhichFileWereIn'
import threading
import traceback

import numpy
from scipy.spatial.transform import Rotation #For ConvertQuaterionsToEulerAngles_RollPitchYawAbtXYZ_ScipyCalculation and ConvertRotationMatrixToEulerAngles_RollPitchYawAbtXYZ

import pyzed.sl as StereoLabs #Stereolabs ZED, https://github.com/stereolabs/zed-python-api, https://www.stereolabs.com/docs/api/python/
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

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
class ZEDasHandController_ReubenPython2and3Class(Frame): #Subclass the Tkinter Frame

    #######################################################################################################################
    #######################################################################################################################
    def __init__(self, setup_dict): #Subclass the Tkinter Frame

        print("#################### ZEDasHandController_ReubenPython2and3Class __init__ starting. ####################")

        #########################################################
        #########################################################
        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
        self.EnableInternal_MyPrint_Flag = 0
        self.MainThread_still_running_flag = 0

        self.CurrentTime_CalculatedFromMainThread = -11111.0
        self.StartingTime_CalculatedFromMainThread = -11111.0
        self.LastTime_CalculatedFromMainThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromMainThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromMainThread = -11111.0

        self.Position_NeedsToBeZeroedFlag = 0
        self.Position_DataForZeroing_EnableCollectionFlag = 0
        
        self.PosList_Raw_DataForZeroingQueue = Queue.Queue()
        self.PosList_Filtered_DataForZeroingQueue = Queue.Queue()
        self.PosList_Raw_ZeroOffsetValue = [0.0] * 3
        self.PosList_Filtered_ZeroOffsetValue = [0.0] * 3
        
        self.Rotation_NeedsToBeZeroedFlag = 0
        self.Rotation_DataForZeroing_EnableCollectionFlag = 0
        
        self.RollPitchYaw_AbtXYZ_List_Radians_Raw_DataForZeroingQueue = Queue.Queue()
        self.RollPitchYaw_AbtXYZ_List_Radians_Filtered_DataForZeroingQueue = Queue.Queue()
        self.RollPitchYaw_AbtXYZ_List_Radians_Raw_ZeroOffsetValue = [0.0] * 3
        self.RollPitchYaw_AbtXYZ_List_Degrees_Raw_ZeroOffsetValue = [0.0] * 3
        self.RollPitchYaw_AbtXYZ_List_Radians_Filtered_ZeroOffsetValue = [0.0] * 3
        self.RollPitchYaw_AbtXYZ_List_Degrees_Filtered_ZeroOffsetValue = [0.0] * 3

        self.ZEDcoordinateSystemOptions = ["RIGHT_HANDED_Y_DOWN",   #default
                                    "LEFT_HANDED_Y_UP",             #Unity
                                    "RIGHT_HANDED_Y_UP",            #OpenGL
                                    "LEFT_HANDED_Z_UP",             #Unreal Engine
                                    "RIGHT_HANDED_Z_UP"]            #ROS


        self.ZEDresolutionOptions = ["HD2K",    #2208*1242 (x2), available framerates: 15 fps.
                                    "HD1080",   #1920*1080 (x2), available framerates: 15, 30 fps.
                                    "HD720",    #1280*720 (x2), available framerates: 15, 30, 60 fps.
                                    "VGA"]  #672*376 (x2), available framerates: 15, 30, 60, 100 fps.

        self.NumberOfFramesGrabbed = 0
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

        print("ZEDasHandController_ReubenPython2and3Class __init__: The OS platform is: " + self.my_platform)
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

            print("ZEDasHandController_ReubenPython2and3Class __init__: USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "root" in self.GUIparametersDict:
                self.root = self.GUIparametersDict["root"]
            else:
                print("ZEDasHandController_ReubenPython2and3Class __init__: Error, must pass in 'root'")
                return
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "EnableInternal_MyPrint_Flag" in self.GUIparametersDict:
                self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", self.GUIparametersDict["EnableInternal_MyPrint_Flag"])
            else:
                self.EnableInternal_MyPrint_Flag = 0

            print("ZEDasHandController_ReubenPython2and3Class __init__: EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "PrintToConsoleFlag" in self.GUIparametersDict:
                self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", self.GUIparametersDict["PrintToConsoleFlag"])
            else:
                self.PrintToConsoleFlag = 1

            print("ZEDasHandController_ReubenPython2and3Class __init__: PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "NumberOfPrintLines" in self.GUIparametersDict:
                self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", self.GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
            else:
                self.NumberOfPrintLines = 10

            print("ZEDasHandController_ReubenPython2and3Class __init__: NumberOfPrintLines: " + str(self.NumberOfPrintLines))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "UseBorderAroundThisGuiObjectFlag" in self.GUIparametersDict:
                self.UseBorderAroundThisGuiObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseBorderAroundThisGuiObjectFlag", self.GUIparametersDict["UseBorderAroundThisGuiObjectFlag"])
            else:
                self.UseBorderAroundThisGuiObjectFlag = 0

            print("ZEDasHandController_ReubenPython2and3Class __init__: UseBorderAroundThisGuiObjectFlag: " + str(self.UseBorderAroundThisGuiObjectFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_ROW" in self.GUIparametersDict:
                self.GUI_ROW = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROW", self.GUIparametersDict["GUI_ROW"], 0.0, 1000.0))
            else:
                self.GUI_ROW = 0

            print("ZEDasHandController_ReubenPython2and3Class __init__: GUI_ROW: " + str(self.GUI_ROW))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMN" in self.GUIparametersDict:
                self.GUI_COLUMN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMN", self.GUIparametersDict["GUI_COLUMN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMN = 0

            print("ZEDasHandController_ReubenPython2and3Class __init__: GUI_COLUMN: " + str(self.GUI_COLUMN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADX" in self.GUIparametersDict:
                self.GUI_PADX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADX", self.GUIparametersDict["GUI_PADX"], 0.0, 1000.0))
            else:
                self.GUI_PADX = 0

            print("ZEDasHandController_ReubenPython2and3Class __init__: GUI_PADX: " + str(self.GUI_PADX))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADY" in self.GUIparametersDict:
                self.GUI_PADY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADY", self.GUIparametersDict["GUI_PADY"], 0.0, 1000.0))
            else:
                self.GUI_PADY = 0

            print("ZEDasHandController_ReubenPython2and3Class __init__: GUI_PADY: " + str(self.GUI_PADY))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_ROWSPAN" in self.GUIparametersDict:
                self.GUI_ROWSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROWSPAN", self.GUIparametersDict["GUI_ROWSPAN"], 1.0, 1000.0))
            else:
                self.GUI_ROWSPAN = 1

            print("ZEDasHandController_ReubenPython2and3Class __init__: GUI_ROWSPAN: " + str(self.GUI_ROWSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMNSPAN" in self.GUIparametersDict:
                self.GUI_COLUMNSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMNSPAN", self.GUIparametersDict["GUI_COLUMNSPAN"], 1.0, 1000.0))
            else:
                self.GUI_COLUMNSPAN = 1

            print("ZEDasHandController_ReubenPython2and3Class __init__: GUI_COLUMNSPAN: " + str(self.GUI_COLUMNSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_STICKY" in self.GUIparametersDict:
                self.GUI_STICKY = str(self.GUIparametersDict["GUI_STICKY"])
            else:
                self.GUI_STICKY = "w"

            print("ZEDasHandController_ReubenPython2and3Class __init__: GUI_STICKY: " + str(self.GUI_STICKY))
            #########################################################
            #########################################################

        else:
            self.GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("ZEDasHandController_ReubenPython2and3Class __init__: No GUIparametersDict present, setting USE_GUI_FLAG = " + str(self.USE_GUI_FLAG))

        #print("ZEDasHandController_ReubenPython2and3Class __init__: GUIparametersDict: " + str(self.GUIparametersDict))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "NameToDisplay_UserSet" in setup_dict:
            self.NameToDisplay_UserSet = str(setup_dict["NameToDisplay_UserSet"])
        else:
            self.NameToDisplay_UserSet = ""

        print("ZEDasHandController_ReubenPython2and3Class __init__: NameToDisplay_UserSet: " + self.NameToDisplay_UserSet )
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "MainThread_TimeToSleepEachLoop" in setup_dict:
            self.MainThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("MainThread_TimeToSleepEachLoop", setup_dict["MainThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.MainThread_TimeToSleepEachLoop = 0.005

        print("ZEDasHandController_ReubenPython2and3Class __init__: MainThread_TimeToSleepEachLoop: " + str(self.MainThread_TimeToSleepEachLoop))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "Position_ExponentialFilterLambda" in setup_dict:
            self.Position_ExponentialFilterLambda = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("Position_ExponentialFilterLambda", setup_dict["Position_ExponentialFilterLambda"], -sys.float_info.max, sys.float_info.max)

        else:
            self.Position_ExponentialFilterLambda = 1.0 #Default to no filtering, new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value

        print("ZEDasHandController_ReubenPython2and3Class __init__: Position_ExponentialFilterLambda: " + str(self.Position_ExponentialFilterLambda))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "Rotation_ExponentialFilterLambda" in setup_dict:
            self.Rotation_ExponentialFilterLambda = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("Rotation_ExponentialFilterLambda", setup_dict["Rotation_ExponentialFilterLambda"], -sys.float_info.max, sys.float_info.max)

        else:
            self.Rotation_ExponentialFilterLambda = 1.0 #Default to no filtering, new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value

        print("ZEDasHandController_ReubenPython2and3Class __init__: Rotation_ExponentialFilterLambda: " + str(self.Rotation_ExponentialFilterLambda))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DataCollectionDurationInSecondsForZeroing" in setup_dict:
            self.DataCollectionDurationInSecondsForZeroing = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("DataCollectionDurationInSecondsForZeroing", setup_dict["DataCollectionDurationInSecondsForZeroing"], 0.0, 60.0)

        else:
            self.DataCollectionDurationInSecondsForZeroing = 1.0

        print("ZEDasHandController_ReubenPython2and3Class __init__: DataCollectionDurationInSecondsForZeroing: " + str(self.DataCollectionDurationInSecondsForZeroing))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "ZEDcoordinateSystem" in setup_dict:
            ZEDcoordinateSystem_TEMP = str(setup_dict["ZEDcoordinateSystem"])

            if ZEDcoordinateSystem_TEMP in self.ZEDcoordinateSystemOptions:
                self.ZEDcoordinateSystem = ZEDcoordinateSystem_TEMP
            else:
                print("ZEDasHandController_ReubenPython2and3Class __init__: ERROR, ZEDcoordinateSystem must be in " + str(self.ZEDcoordinateSystemOptions))
                return

        else:
            self.ZEDcoordinateSystem = "RIGHT_HANDED_Y_DOWN" #default value for ZED

        print("ZEDasHandController_ReubenPython2and3Class __init__: ZEDcoordinateSystem: " + str(self.ZEDcoordinateSystem))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "ZEDresolution" in setup_dict:
            ZEDresolution_TEMP = str(setup_dict["ZEDresolution"])

            if ZEDresolution_TEMP in self.ZEDresolutionOptions:
                self.ZEDresolution = ZEDresolution_TEMP
            else:
                print("ZEDasHandController_ReubenPython2and3Class __init__: ERROR, ZEDresolution must be in " + str(self.ZEDresolutionOptions))
                return

        else:
            self.ZEDresolution = "HD720"
            # NOTE: Positional tracking uses image and depth information to estimate the position of the camera in 3D space.
            # To improve tracking results, use high FPS video modes such as HD720 and WVGA.

        print("ZEDasHandController_ReubenPython2and3Class __init__: ZEDresolution: " + str(self.ZEDresolution))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "ZEDfps" in setup_dict:
            ZEDfps_TEMP = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("ZEDfps", setup_dict["ZEDfps"], 0.0, 100.0))

            if self.ZEDresolution == "HD2K":
                self.ZEDfpsOptions = [15]

            elif self.ZEDresolution == "HD1080":
                self.ZEDfpsOptions = [15, 30]

            elif self.ZEDresolution == "HD720":
                self.ZEDfpsOptions = [15, 30, 60]

            elif self.ZEDresolution == "VGA":
                self.ZEDfpsOptions = [15, 30, 60, 100]
                
            else:
                self.ZEDfpsOptions = [15]

            if ZEDfps_TEMP in self.ZEDfpsOptions:
                self.ZEDfps = ZEDfps_TEMP
                
            else:
                print("ZEDasHandController_ReubenPython2and3Class __init__: ERROR, ZEDfps must be in " + str(self.ZEDfpsOptions))
                return

        else:
            self.ZEDfps = 60.0
            # NOTE: Positional tracking uses image and depth information to estimate the position of the camera in 3D space.
            # To improve tracking results, use high FPS video modes such as HD720 and WVGA.

        print("ZEDasHandController_ReubenPython2and3Class __init__: ZEDfps: " + str(self.ZEDfps))
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
        self.Position_LowPassFilter_ReubenPython2and3ClassObject = list()
        for Index in range(0, 3):
            self.Position_LowPassFilter_ReubenPython2and3ClassObject.append(LowPassFilter_ReubenPython2and3Class(dict([("UseMedianFilterFlag", 1),
                                                                                                                ("UseExponentialSmoothingFilterFlag", 1),
                                                                                                                ("ExponentialSmoothingFilterLambda", self.Position_ExponentialFilterLambda)])))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.Rotation_LowPassFilter_ReubenPython2and3ClassObject = list()
        for Index in range(0, 3):
            self.Rotation_LowPassFilter_ReubenPython2and3ClassObject.append(LowPassFilter_ReubenPython2and3Class(dict([("UseMedianFilterFlag", 1),
                                                                                                                ("UseExponentialSmoothingFilterFlag", 1),
                                                                                                                ("ExponentialSmoothingFilterLambda", self.Rotation_ExponentialFilterLambda)])))
        #########################################################
        #########################################################


        #########################################################
        #########################################################
        #https://www.stereolabs.com/docs/api/python/group__PositionalTracking__group.html

        #########################################################
        if self.ZEDcoordinateSystem != "RIGHT_HANDED_Y_DOWN": #Apparently there's no entry for this one, so you leave it blank to get default value.
            self.ZEDcameraInitParameters = StereoLabs.InitParameters(camera_resolution=getattr(StereoLabs.RESOLUTION, self.ZEDresolution),
                                                                     camera_fps=self.ZEDfps,
                                                                     coordinate_units=StereoLabs.UNIT.METER,
                                                                     coordinate_system=getattr(StereoLabs.COORDINATE_SYSTEM, self.ZEDcoordinateSystem))
        else:
            self.ZEDcameraInitParameters = StereoLabs.InitParameters(camera_resolution=getattr(StereoLabs.RESOLUTION, self.ZEDresolution),
                                                                     camera_fps=self.ZEDfps,
                                                                     coordinate_units=StereoLabs.UNIT.METER,)


        #NOTE: Positional tracking uses image and depth information to estimate the position of the camera in 3D space.
        #To improve tracking results, use high FPS video modes such as HD720 and WVGA.
        #########################################################

        #########################################################
        self.ZEDcameraObject = StereoLabs.Camera()
        
        self.ZEDcameraOpenFlag = self.ZEDcameraObject.open(self.ZEDcameraInitParameters)
        if self.ZEDcameraOpenFlag != StereoLabs.ERROR_CODE.SUCCESS:
            print("ZEDasHandController_ReubenPython2and3Class __init__: Failed to open ZED camera, " + str(repr(self.ZEDcameraOpenFlag)))
            return
        #########################################################

        #########################################################
        #https://www.stereolabs.com/docs/api/structsl_1_1PositionalTrackingParameters.html
        self.ZEDcameraTrackingParameters = StereoLabs.PositionalTrackingParameters()
        self.ZEDcameraObject.enable_positional_tracking(self.ZEDcameraTrackingParameters)
        #########################################################

        #########################################################
        self.ZEDcameraRuntimeParameters = StereoLabs.RuntimeParameters()
        self.ZEDcameraPose = StereoLabs.Pose()
        #########################################################

        #########################################################
        self.ZEDcameraInfoStructureFieldNameStrings = ["sensors_configuration", #Device Sensors configuration as defined in SensorsConfiguration.
                                                        "camera_configuration", #Camera configuration as defined in CameraConfiguration.
                                                        "input_type", #Input type used in SDK.
                                                        "camera_resolution", #Resolution of the camera
                                                        "camera_fps", #FPS of the camera.
                                                        "camera_model", #The model of the camera (ZED, ZED2 or ZED-M).
                                                        "calibration_parameters", #Intrinsic and Extrinsic stereo CalibrationParameters for rectified/undistorded images (default).
                                                        "calibration_parameters_raw", #Intrinsic and Extrinsic stereo CalibrationParameters for original images (unrectified/distorded).
                                                        "camera_imu_transform", #IMU to Left camera transform matrix, that contains rotation and translation between IMU frame and camera frame. More...
                                                        "serial_number", #The serial number of the camera.
                                                        "camera_firmware_version", #The internal firmware version of the camera.
                                                        "sensors_firmware_version",] #The internal firmware version of the sensors of ZEDM or ZED2.

        self.ZEDcameraInfo = self.ZEDcameraObject.get_camera_information()

        self.ZEDcameraInfoDict = dict()
        for NameString in self.ZEDcameraInfoStructureFieldNameStrings:
            self.ZEDcameraInfoDict[NameString] = getattr(self.ZEDcameraInfo, NameString)
        #########################################################

        #########################################################
        self.ZEDcameraPyTranslation = StereoLabs.Translation()

        self.ZEDcameraTranslationList = [-11111.0]*3
        self.ZEDcameraRotationVector = [-11111.0]*3
        self.ZEDcameraRotationEulerAnglesList = [-11111.0]*3
        self.ZEDcameraRotationEulerAnglesList_Radians = [-11111.0]*3
        self.ZEDcameraRotationEulerAnglesList_Degrees = [-11111.0] * 3
        #########################################################

        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.MostRecentDataDict = dict()
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

    #######################################################################################################################
    #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    def __del__(self):
        pass
    #######################################################################################################################
    #######################################################################################################################

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

            return deepcopy(self.MostRecentDataDict) #deepcopy IS required as MostRecentDataDict contains lists.

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
            print("UpdateFrequencyCalculation_MainThread Error with Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## unicorn
    ##########################################################################################################
    ##########################################################################################################
    def FilterPositionAndRotation(self):

        try:
            FilteredPositionAndRotationDict = dict()
            
            ##########################################################################################################
            ##########################################################################################################
            PosList_Raw_WITHOUT_ZeroOffset_TEMP = self.ZEDcameraTranslationList

            PosList_Filtered_WITHOUT_ZeroOffset_TEMP = [-11111.0]*3
            FilteredPositionAndRotationDict["PosList_Raw"] = [-11111.0] * 3
            FilteredPositionAndRotationDict["PosList_Filtered"] = [-11111.0]*3

            ##########################################################################################################
            for Index in range(0, 3):
                FilteredPositionAndRotationDict["PosList_Raw"][Index] = PosList_Raw_WITHOUT_ZeroOffset_TEMP[Index] - self.PosList_Raw_ZeroOffsetValue[Index]
                PosList_Filtered_WITHOUT_ZeroOffset_TEMP[Index] = self.Position_LowPassFilter_ReubenPython2and3ClassObject[Index].AddDataPointFromExternalProgram(PosList_Raw_WITHOUT_ZeroOffset_TEMP[Index])["SignalOutSmoothed"]
                FilteredPositionAndRotationDict["PosList_Filtered"][Index] = PosList_Filtered_WITHOUT_ZeroOffset_TEMP[Index] - self.PosList_Filtered_ZeroOffsetValue[Index]
            ##########################################################################################################
            
            ##########################################################################################################
            if self.Position_DataForZeroing_EnableCollectionFlag == 1:
                self.PosList_Raw_DataForZeroingQueue.put(PosList_Raw_WITHOUT_ZeroOffset_TEMP)
                self.PosList_Filtered_DataForZeroingQueue.put(PosList_Filtered_WITHOUT_ZeroOffset_TEMP)
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            RollPitchYaw_AbtXYZ_List_Radians_Raw_WITHOUT_ZeroOffset_TEMP = self.ZEDcameraRotationEulerAnglesList_Radians

            RollPitchYaw_AbtXYZ_List_Radians_Filtered_WITHOUT_ZeroOffset_TEMP = [-11111.0]*3
            FilteredPositionAndRotationDict["RollPitchYaw_AbtXYZ_List_Radians_Raw"] = [-11111.0]*3
            FilteredPositionAndRotationDict["RollPitchYaw_AbtXYZ_List_Radians_Filtered"] = [-11111.0]*3
            FilteredPositionAndRotationDict["RollPitchYaw_AbtXYZ_List_Degrees_Raw"] = [-11111.0]*3
            FilteredPositionAndRotationDict["RollPitchYaw_AbtXYZ_List_Degrees_Filtered"] = [-11111.0]*3
            ##########################################################################################################

            ##########################################################################################################
            for Index in range(0, 3):
                FilteredPositionAndRotationDict["RollPitchYaw_AbtXYZ_List_Radians_Raw"][Index] = RollPitchYaw_AbtXYZ_List_Radians_Raw_WITHOUT_ZeroOffset_TEMP[Index] - self.RollPitchYaw_AbtXYZ_List_Radians_Raw_ZeroOffsetValue[Index]
                RollPitchYaw_AbtXYZ_List_Radians_Filtered_WITHOUT_ZeroOffset_TEMP[Index] = self.Rotation_LowPassFilter_ReubenPython2and3ClassObject[Index].AddDataPointFromExternalProgram(RollPitchYaw_AbtXYZ_List_Radians_Raw_WITHOUT_ZeroOffset_TEMP[Index])["SignalOutSmoothed"]
                FilteredPositionAndRotationDict["RollPitchYaw_AbtXYZ_List_Radians_Filtered"][Index] = RollPitchYaw_AbtXYZ_List_Radians_Filtered_WITHOUT_ZeroOffset_TEMP[Index] - self.RollPitchYaw_AbtXYZ_List_Radians_Filtered_ZeroOffsetValue[Index]
                FilteredPositionAndRotationDict["RollPitchYaw_AbtXYZ_List_Degrees_Raw"][Index] = (180.0/math.pi)*FilteredPositionAndRotationDict["RollPitchYaw_AbtXYZ_List_Radians_Raw"][Index]
                FilteredPositionAndRotationDict["RollPitchYaw_AbtXYZ_List_Degrees_Filtered"][Index] = (180.0/math.pi)*FilteredPositionAndRotationDict["RollPitchYaw_AbtXYZ_List_Radians_Filtered"][Index]
            ##########################################################################################################
            
            ##########################################################################################################
            if self.Rotation_DataForZeroing_EnableCollectionFlag == 1:
                self.RollPitchYaw_AbtXYZ_List_Radians_Raw_DataForZeroingQueue.put(RollPitchYaw_AbtXYZ_List_Radians_Raw_WITHOUT_ZeroOffset_TEMP)
                self.RollPitchYaw_AbtXYZ_List_Radians_Filtered_DataForZeroingQueue.put(RollPitchYaw_AbtXYZ_List_Radians_Filtered_WITHOUT_ZeroOffset_TEMP)
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            
            return FilteredPositionAndRotationDict

        except:
            exceptions = sys.exc_info()[0]
            print("Convert_HandDict_DictOnlySingleNumbersNoListsOrMatrices_To_DictListsAndMatrices, Exceptions: %s" % exceptions)
            traceback.print_exc()
            return dict()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StopCollectingDataForZeroingPosition(self):

        self.Position_DataForZeroing_EnableCollectionFlag = 2
        self.MyPrint_WithoutLogFile("StopCollectingDataForZeroingPosition event fired!")
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StopCollectingDataForZeroingRotation(self):

        self.Rotation_DataForZeroing_EnableCollectionFlag = 2
        self.MyPrint_WithoutLogFile("StopCollectingDataForZeroingRotation event fired!")
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GrabNewPositionAndRotation(self, RefFrameInput = "WORLD"):

        ZEDcameraTranslationList_LOCAL = [-11111.0]*3
        ZEDcameraRotationVector_LOCAL = [-11111.0]*3
        ZEDcameraRotationEulerAnglesList_Radians_LOCAL = [-11111.0]*3
        ZEDcameraRotationEulerAnglesList_Degrees_LOCAL = [-11111.0]*3

        try:

            ##########################################################################################################
            if RefFrameInput.upper() == "WORLD":
                ReferenceFrameToUse = StereoLabs.REFERENCE_FRAME.WORLD
            elif RefFrameInput.upper() == "CAMERA":
                ReferenceFrameToUse = StereoLabs.REFERENCE_FRAME.CAMERA
            else:
                print("GrabNewPositionAndRotation ERROR, RefFrameInput must be either 'WORLD' or 'CAMERA'.")
                return [ZEDcameraTranslationList_LOCAL, ZEDcameraRotationVector_LOCAL, ZEDcameraRotationEulerAnglesList_Radians_LOCAL, ZEDcameraRotationEulerAnglesList_Degrees_LOCAL]
            ##########################################################################################################

            #NOTE ON GRAB(): Since ZED SDK 3.0, this function is blocking. It means that grab() will wait until a new frame is detected and available.
            #If no new frames is available until timeout is reached, grab() will return ERROR_CODE::CAMERA_NOT_DETECTED.
            if self.ZEDcameraObject.grab(self.ZEDcameraRuntimeParameters) == StereoLabs.ERROR_CODE.SUCCESS:

                ##########################################################################################################
                self.ZEDcameraTrackingState = self.ZEDcameraObject.get_position(self.ZEDcameraPose, ReferenceFrameToUse)

                if self.ZEDcameraTrackingState == StereoLabs.POSITIONAL_TRACKING_STATE.OK:

                    #.tolist() converts Numpy array to std list
                    ZEDcameraRotationVector_LOCAL = self.ZEDcameraPose.get_rotation_vector().tolist() #Returns the 3x1 rotation vector obtained from 3x3 rotation matrix using Rodrigues formula
                    ZEDcameraRotationEulerAnglesList_Radians_LOCAL = self.ZEDcameraPose.get_euler_angles(radian = True).tolist() #The Euler angles, as a numpy array representing the rotations arround the X, Y and Z axes.
                    ZEDcameraRotationEulerAnglesList_Degrees_LOCAL = self.ConvertListOfValuesRadToDeg(ZEDcameraRotationEulerAnglesList_Radians_LOCAL)

                    ZEDcameraTranslationList_LOCAL = self.ZEDcameraPose.get_translation(self.ZEDcameraPyTranslation).get().tolist()

                    self.NumberOfFramesGrabbed = self.NumberOfFramesGrabbed + 1
                ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("GrabNewPositionAndRotation, Exceptions: %s" % exceptions)
            traceback.print_exc()
            return [ZEDcameraTranslationList_LOCAL, ZEDcameraRotationVector_LOCAL, ZEDcameraRotationEulerAnglesList_Radians_LOCAL, ZEDcameraRotationEulerAnglesList_Degrees_LOCAL]

        return [ZEDcameraTranslationList_LOCAL, ZEDcameraRotationVector_LOCAL, ZEDcameraRotationEulerAnglesList_Radians_LOCAL, ZEDcameraRotationEulerAnglesList_Degrees_LOCAL]
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ########################################################################################################## unicorn
    def MainThread(self):

        self.MyPrint_WithoutLogFile("Started MainThread for ZEDasHandController_ReubenPython2and3Class object.")
        
        self.MainThread_still_running_flag = 1

        self.StartingTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString()

        FilteredPositionAndRotationDict_LOCAL = dict([("PosList_Raw", [-11111.0]*3),
                                                ("PosList_Filtered", [-11111.0]*3),
                                                ("RollPitchYaw_AbtXYZ_List_Radians_Raw", [-11111.0]*3),
                                                ("RollPitchYaw_AbtXYZ_List_Radians_Filtered", [-11111.0]*3),
                                                ("RollPitchYaw_AbtXYZ_List_Degrees_Raw", [-11111.0]*3),
                                                ("RollPitchYaw_AbtXYZ_List_Degrees_Filtered", [-11111.0]*3)])

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            try:

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                self.CurrentTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromMainThread
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                #THIS LINE IS BLOCKING!
                [ZEDcameraTranslationList_LOCAL, ZEDcameraRotationVector_LOCAL, ZEDcameraRotationEulerAnglesList_Radians_LOCAL, ZEDcameraRotationEulerAnglesList_Degrees_LOCAL] = self.GrabNewPositionAndRotation("WORLD")
                #THIS LINE IS BLOCKING!

                if ZEDcameraTranslationList_LOCAL[0] != -11111.0: #If we have a valid new frame
                    ##########################################################################################################
                    ##########################################################################################################
                    self.ZEDcameraTranslationList = ZEDcameraTranslationList_LOCAL
                    self.ZEDcameraRotationVector = ZEDcameraRotationVector_LOCAL
                    self.ZEDcameraRotationEulerAnglesList = ZEDcameraRotationVector_LOCAL
                    self.ZEDcameraRotationEulerAnglesList_Radians = ZEDcameraRotationEulerAnglesList_Radians_LOCAL
                    self.ZEDcameraRotationEulerAnglesList_Degrees = ZEDcameraRotationEulerAnglesList_Degrees_LOCAL

                    FilteredPositionAndRotationDict_LOCAL = self.FilterPositionAndRotation()
                    ##########################################################################################################
                    ##########################################################################################################

                    ##########################################################################################################
                    ##########################################################################################################
                    if self.NumberOfFramesGrabbed == 1:
                        self.ZEDcameraRotationVector_INITIAL = self.ZEDcameraRotationVector
                        print("self.ZEDcameraRotationVector: " + str(self.ZEDcameraRotationVector))

                        initial_position = StereoLabs.Transform()
                        initial_position.set_rotation_vector(*self.ZEDcameraRotationVector_INITIAL)

                        self.ZEDcameraTrackingParameters.set_initial_world_transform(initial_position)
                    ##########################################################################################################
                    ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                MainLoopInfoDict = dict([("TrackingState", self.ZEDcameraTrackingState),
                                        ("ZEDcameraRotationVector", self.ZEDcameraRotationVector),
                                        ("NumberOfFramesGrabbed", self.NumberOfFramesGrabbed),
                                        ("DataStreamingFrequency", self.DataStreamingFrequency_CalculatedFromMainThread),
                                        ("Time", self.CurrentTime_CalculatedFromMainThread)])

                self.MostRecentDataDict = {**MainLoopInfoDict, **FilteredPositionAndRotationDict_LOCAL}
                ##########################################################################################################
                ##########################################################################################################

                ########################################################################################################## USE THE TIME.SLEEP() TO SET THE LOOP FREQUENCY
                ##########################################################################################################
                self.UpdateFrequencyCalculation_MainThread()

                if self.MainThread_TimeToSleepEachLoop > 0.0:
                    time.sleep(self.MainThread_TimeToSleepEachLoop)
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ########################################################################################################## START position zeroing
                ##########################################################################################################
                ##########################################################################################################
                if self.Position_NeedsToBeZeroedFlag == 1:

                    ##########################################################################################################
                    ##########################################################################################################
                    if self.Position_DataForZeroing_EnableCollectionFlag == 0:
                        print("Starting to collect data to zero PosList.")
                        self.Position_DataForZeroing_EnableCollectionFlag = 1
                        self.TimerCallbackFunctionWithFunctionAsArgument_SingleShot_NoParenthesesAfterFunctionName(self.DataCollectionDurationInSecondsForZeroing, self.StopCollectingDataForZeroingPosition, [])
                    ##########################################################################################################
                    ##########################################################################################################

                    ##########################################################################################################
                    ##########################################################################################################
                    elif self.Position_DataForZeroing_EnableCollectionFlag == 1:
                        pass
                    ##########################################################################################################
                    ##########################################################################################################

                    ##########################################################################################################
                    ##########################################################################################################
                    else: #Like 2

                        print("Computing average for position.")
                        self.Position_DataForZeroing_EnableCollectionFlag = 0

                        ##########################################################################################################
                        self.PosList_Raw_ZeroOffsetValue = self.AverageDataInQueueOfLists(self.PosList_Raw_DataForZeroingQueue)
                        self.PosList_Filtered_ZeroOffsetValue = self.AverageDataInQueueOfLists(self.PosList_Filtered_DataForZeroingQueue)
                        ##########################################################################################################

                        self.MyPrint_WithoutLogFile("self.PosList_Raw_ZeroOffsetValue: " + str(self.PosList_Raw_ZeroOffsetValue) +
                                                    ", self.PosList_Filtered_ZeroOffsetValue: " + str(self.PosList_Filtered_ZeroOffsetValue))

                        self.Position_NeedsToBeZeroedFlag = 0

                    ##########################################################################################################
                    ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ########################################################################################################## END position zeroing

                ########################################################################################################## START rotation zeroing
                ##########################################################################################################
                ##########################################################################################################
                if self.Rotation_NeedsToBeZeroedFlag == 1:

                    ##########################################################################################################
                    ##########################################################################################################
                    if self.Rotation_DataForZeroing_EnableCollectionFlag == 0:
                        print("Starting to collect data to zero rotation.")
                        self.Rotation_DataForZeroing_EnableCollectionFlag = 1
                        self.TimerCallbackFunctionWithFunctionAsArgument_SingleShot_NoParenthesesAfterFunctionName(self.DataCollectionDurationInSecondsForZeroing, self.StopCollectingDataForZeroingRotation, [])
                    ##########################################################################################################
                    ##########################################################################################################

                    ##########################################################################################################
                    ##########################################################################################################
                    elif self.Rotation_DataForZeroing_EnableCollectionFlag == 1:
                        pass
                    ##########################################################################################################
                    ##########################################################################################################

                    ##########################################################################################################
                    ##########################################################################################################
                    else: #Like 2

                        print("Computing average for rotation.")
                        self.Rotation_DataForZeroing_EnableCollectionFlag = 0

                        ##########################################################################################################
                        self.RollPitchYaw_AbtXYZ_List_Radians_Raw_ZeroOffsetValue = self.AverageDataInQueueOfLists(self.RollPitchYaw_AbtXYZ_List_Radians_Raw_DataForZeroingQueue)
                        self.RollPitchYaw_AbtXYZ_List_Radians_Filtered_ZeroOffsetValue = self.AverageDataInQueueOfLists(self.RollPitchYaw_AbtXYZ_List_Radians_Filtered_DataForZeroingQueue)
                        ##########################################################################################################

                        ##########################################################################################################
                        for Index in range(0, 3):
                            self.RollPitchYaw_AbtXYZ_List_Degrees_Raw_ZeroOffsetValue[Index] = (180.0/math.pi)*self.RollPitchYaw_AbtXYZ_List_Radians_Raw_ZeroOffsetValue[Index]
                            self.RollPitchYaw_AbtXYZ_List_Degrees_Filtered_ZeroOffsetValue[Index] = (180.0/math.pi)*self.RollPitchYaw_AbtXYZ_List_Radians_Filtered_ZeroOffsetValue[Index]
                        ##########################################################################################################

                        self.MyPrint_WithoutLogFile("self.RollPitchYaw_AbtXYZ_List_Radians_Raw_ZeroOffsetValue: " + str(self.RollPitchYaw_AbtXYZ_List_Radians_Raw_ZeroOffsetValue) +
                                                    ", self.RollPitchYaw_AbtXYZ_List_Degrees_Raw_ZeroOffsetValue: " + str(self.RollPitchYaw_AbtXYZ_List_Degrees_Raw_ZeroOffsetValue))

                        self.MyPrint_WithoutLogFile("self.RollPitchYaw_AbtXYZ_List_Radians_Filtered_ZeroOffsetValue: " + str(self.RollPitchYaw_AbtXYZ_List_Radians_Filtered_ZeroOffsetValue) +
                                                    ", self.RollPitchYaw_AbtXYZ_List_Degrees_Filtered_ZeroOffsetValue: " + str(self.RollPitchYaw_AbtXYZ_List_Degrees_Filtered_ZeroOffsetValue))

                        self.Rotation_NeedsToBeZeroedFlag = 0

                    ##########################################################################################################
                    ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ########################################################################################################## END rotation zeroing

            except:
                exceptions = sys.exc_info()[0]
                print("ZEDasHandController_ReubenPython2and3Class MainThread, Exceptions: %s" % exceptions)
                traceback.print_exc()

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        self.ZEDcameraObject.close()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        self.MyPrint_WithoutLogFile("Finished MainThread for ZEDasHandController_ReubenPython2and3Class object.")
        self.MainThread_still_running_flag = 0
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def AverageDataInQueueOfLists(self, InputQueue):
        try:

            if isinstance(InputQueue, Queue.Queue) == 1:

                InputQueueSize = InputQueue.qsize()

                if InputQueueSize > 0:
                    DataElement = InputQueue.get()

                    IsListFlag = 1
                    ####
                    if isinstance(DataElement, list) == 0:  # If not a list, make it one.
                        DataElement = [DataElement]
                        IsListFlag = 0
                    ####

                    DataElementListLength = len(DataElement)

                    SumOfIndex_List = list()
                    for Value in DataElement:
                        SumOfIndex_List.append(Value)  # Just to initialize SumOfIndex_List with the first element that we removed.

                    ##########################################################################################################
                    while InputQueue.qsize() > 0:
                        DataElementValue = InputQueue.get()

                        if IsListFlag == 0:
                            DataElementValue = [DataElementValue]

                        for Index in range(0, DataElementListLength):
                            SumOfIndex_List[Index] = SumOfIndex_List[Index] + DataElementValue[Index]

                    ##########################################################################################################

                    ##########################################################################################################
                    AverageOfIndex_List = [0.0] * DataElementListLength
                    for Index in range(0, DataElementListLength):
                        AverageOfIndex_List[Index] = SumOfIndex_List[Index] / InputQueueSize
                    ##########################################################################################################

                    #print("AverageOfIndex_List: " + str(AverageOfIndex_List))
                    return AverageOfIndex_List

                else:
                    print("AverageDataInQueueOfLists, Error: Queue is empty!")
                    return [-11111.0]

            else:
                print("AverageDataInQueueOfLists, Error: Input must be a Queue.Queue!")
                return [-11111.0]

        except:
            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print("AverageDataInQueueOfLists, Exceptions: %s" % exceptions)
            traceback.print_exc()

            #########################################################
            if InputQueue.qsize() > 0:
                DataElement = InputQueue.get()
                if isinstance(DataElement, list) == 1:
                    return [-11111.0] * len(DataElement)
                else:
                    return [-11111.0]
            else:
                return [-11111.0]
            #########################################################

            ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for ZEDasHandController_ReubenPython2and3Class object")

        self.EXIT_PROGRAM_FLAG = 1

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StartGUI(self, GuiParent):

        self.GUI_Thread_ThreadingObject = threading.Thread(target=self.GUI_Thread, args=(GuiParent,))
        self.GUI_Thread_ThreadingObject.setDaemon(True) #Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
        self.GUI_Thread_ThreadingObject.start()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_Thread(self, parent):

        print("Starting the GUI_Thread for ZEDasHandController_ReubenPython2and3Class object.")

        #################################################
        #################################################
        self.root = parent
        self.parent = parent
        #################################################
        #################################################

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

        #################################################
        #################################################
        self.TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150) #RGB
        self.TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150) #RGB
        self.TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
        self.TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
        #################################################
        #################################################

        #################################################
        #################################################
        self.DeviceInfo_Label = Label(self.myFrame, text="Device Info", width=125)

        #######################################################
        self.DeviceInfo_Label["text"] = str(self.NameToDisplay_UserSet) + \
                                        "\n" + \
                                        "\nCamera Model: " + str(self.ZEDcameraInfoDict["camera_model"]) + \
                                        "\nSerial Number: " + str(self.ZEDcameraInfoDict["serial_number"]) + \
                                        "\nCamera FW version: " + str(self.ZEDcameraInfoDict["camera_firmware_version"]) + \
                                        "\nSensors FW version: " + str(self.ZEDcameraInfoDict["sensors_firmware_version"])  + \
                                        "\nFPS: " + str(self.ZEDcameraInfoDict["camera_fps"])
        #######################################################

        self.DeviceInfo_Label.grid(row=0, column=0, padx=10, pady=10, columnspan=1, rowspan=1)
        #################################################
        #################################################

         #################################################
        #################################################
        self.ZeroingButtonsFrame = Frame(self.myFrame)

        self.ZeroingButtonsFrame.grid(row = 1,
                          column = 0,
                          padx = 10,
                          pady = 10,
                          rowspan = 1,
                          columnspan= 1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.ZeroPosition_Button = Button(self.ZeroingButtonsFrame, text="Zero Position", state="normal", width=15, command=lambda: self.ZeroPosition())
        self.ZeroPosition_Button.grid(row=0, column=0, padx=10, pady=1, rowspan=1, columnspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.ZeroRotation_Button = Button(self.ZeroingButtonsFrame, text="Zero Rotation", state="normal", width=15, command=lambda: self.ZeroRotation())
        self.ZeroRotation_Button.grid(row=0, column=1, padx=10, pady=1, rowspan=1, columnspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.DataDisplay_Label = Label(self.myFrame, text="DataDisplay_Label", width=125)
        self.DataDisplay_Label.grid(row=2, column=0, padx=10, pady=10, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.MostRecentDataDict_Label = Label(self.myFrame, text="MostRecentDataDict_Label", width=125, font=('Helvetica', 12))
        self.MostRecentDataDict_Label.grid(row=3, column=0, padx=10, pady=10, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=125)

        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=4, column=0, padx=10, pady=10, columnspan=10, rowspan=10)
        #################################################
        #################################################

        #################################################
        #################################################
        self.GUI_ready_to_be_updated_flag = 1
        #################################################
        #################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ZeroPosition(self):

        self.Position_NeedsToBeZeroedFlag = 1
        self.MyPrint_WithoutLogFile("ZeroPosition: Event fired !")

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ZeroRotation(self):

        self.Rotation_NeedsToBeZeroedFlag = 1
        self.MyPrint_WithoutLogFile("ZeroRotation: Event fired !")

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
                    self.DataDisplay_Label["text"] = "self.ZEDcameraTrackingState: " + str(self.ZEDcameraTrackingState) + \
                        "\nself.NumberOfFramesGrabbed: " + str(self.NumberOfFramesGrabbed) + \
                        "\nPosList_Raw_ZeroOffsetValue: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.PosList_Filtered_ZeroOffsetValue, 0, 3) + \
                        "\nPosList_Filtered_ZeroOffsetValue: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.PosList_Raw_ZeroOffsetValue, 0, 3) + \
                        "\n" +\
                        "\nRollPitchYaw_AbtXYZ_List_Radians_Raw_ZeroOffsetValue: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.RollPitchYaw_AbtXYZ_List_Radians_Raw_ZeroOffsetValue, 0, 3) + \
                        "\nRollPitchYaw_AbtXYZ_List_Degrees_Raw_ZeroOffsetValue: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.RollPitchYaw_AbtXYZ_List_Degrees_Raw_ZeroOffsetValue, 0, 3) + \
                        "\nRollPitchYaw_AbtXYZ_List_Radians_Filtered_ZeroOffsetValue: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.RollPitchYaw_AbtXYZ_List_Radians_Filtered_ZeroOffsetValue, 0, 3) + \
                        "\nRollPitchYaw_AbtXYZ_List_Degrees_Filtered_ZeroOffsetValue: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.RollPitchYaw_AbtXYZ_List_Degrees_Filtered_ZeroOffsetValue, 0, 3) + \
                        "\n" +\
                        "DataForZeroingQueue.qsize(): " + str(self.RollPitchYaw_AbtXYZ_List_Radians_Raw_DataForZeroingQueue.qsize())
                    #######################################################

                    #######################################################
                    self.MostRecentDataDict_Label["text"] = self.ConvertDictToProperlyFormattedStringForPrinting(self.MostRecentDataDict, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3)
                    #######################################################

                    #######################################################
                    self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                    #######################################################

                except:
                    exceptions = sys.exc_info()[0]
                    print("ZEDasHandController_ReubenPython2and3Class GUI_update_clock Error: Exceptions: %s" % exceptions)
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
    def TimerCallbackFunctionWithFunctionAsArgument_SingleShot_NoParenthesesAfterFunctionName(self, CallbackAfterDeltaTseconds, FunctionToCall_NoParenthesesAfterFunctionName, ArgumentListToFunction):

        self.TimerObject = threading.Timer(CallbackAfterDeltaTseconds, FunctionToCall_NoParenthesesAfterFunctionName, ArgumentListToFunction) #Must pass arguments to callback-function via list as the third argument to Timer call
        self.TimerObject.daemon = True #Without the daemon=True, this recursive function won't terminate when the main program does.
        self.TimerObject.start()

        print("TimerCallbackFunctionWithFunctionAsArgument_SingleShot_NoParenthesesAfterFunctionName event fired to call function: '" + str(FunctionToCall_NoParenthesesAfterFunctionName.__name__) + "' at time " + str(self.getPreciseSecondsTimeStampString()))
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

    ###########################################################################################################
    ##########################################################################################################
    def ConvertListOfValuesRadToDeg(self, ListOfValuesRadToDegToBeConverted):

        ListOfValuesDegToBeReturned = list()

        try:
            if isinstance(ListOfValuesRadToDegToBeConverted, list) == 0:
                ListOfValuesDegToRadToBeConverted = list([ListOfValuesRadToDegToBeConverted])

            for index, value in enumerate(ListOfValuesRadToDegToBeConverted):
                ListOfValuesDegToBeReturned.append(value*180.0/math.pi)

            return ListOfValuesDegToBeReturned

        except:
            exceptions = sys.exc_info()[0]
            print("ConvertListOfValuesRadToDeg Exceptions: %s" % exceptions)
            traceback.print_exc()
            return ListOfValuesDegToBeReturned

    ##########################################################################################################
    ##########################################################################################################

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################