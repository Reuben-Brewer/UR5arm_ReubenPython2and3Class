# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision G, 05/10/2023

Verified working on: Python 3.8 for Windows10 64-bit (no testing on Raspberry Pi or Mac testing yet).
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
from copy import * #for deepcopy(dict)
import inspect #To enable 'TellWhichFileWereIn'
import threading
import decimal
import traceback
#########################################################

#########################################################
import cv2 #"pip install opencv-contrib-python==4.5.5.64"
import numpy
print("OpenCV version: " + str(cv2.__version__))
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

class CameraStreamerClass_ReubenPython2and3Class(Frame): #Subclass the Tkinter Frame

    ##########################################################################################################
    ##########################################################################################################
    def __init__(self, setup_dict): #Subclass the Tkinter Frame

        print("#################### CameraStreamerClass_ReubenPython2and3Class __init__ starting. ####################")

        #########################################################
        #########################################################
        self.setup_dict = setup_dict

        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = -1
        self.EnableInternal_MyPrint_Flag = 0

        self.CameraCaptureThread_still_running_flag = 0
        self.CurrentTime_CalculatedFromCameraCaptureThread = -11111.0
        self.StartingTime_CalculatedFromCameraCaptureThread = -11111.0
        self.LastTime_CalculatedFromCameraCaptureThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromCameraCaptureThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromCameraCaptureThread = -11111.0
        self.LoopCounter_CalculatedFromCameraCaptureThread = 0

        self.CameraEncodeThread_still_running_flag = 0
        self.CurrentTime_CalculatedFromCameraEncodeThread = -11111.0
        self.StartingTime_CalculatedFromCameraEncodeThread = -11111.0
        self.LastTime_CalculatedFromCameraEncodeThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromCameraEncodeThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromCameraEncodeThread = -11111.0
        self.LoopCounter_CalculatedFromCameraEncodeThread = 0
        self.EncodingProcessStartTime_CalculatedFromCameraEncodeThread = -1
        self.EncodingProcessEndTime_CalculatedFromCameraEncodeThread = -1
        self.EncodingProcessTotalTime_CalculatedFromCameraEncodeThread = -1

        self.ImageSavingThread_still_running_flag = 0
        self.CurrentTime_CalculatedFromImageSavingThread = -11111.0
        self.StartingTime_CalculatedFromImageSavingThread = -11111.0
        self.LastTime_CalculatedFromImageSavingThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromImageSavingThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromImageSavingThread = -11111.0
        self.LoopCounter_CalculatedFromImageSavingThread = 0
        self.ImageSavingProcessStartTime_CalculatedFromImageSavingThread = -1
        self.ImageSavingProcessEndTime_CalculatedFromImageSavingThread = -1
        self.ImageSavingProcessTotalTime_CalculatedFromImageSavingThread = -1
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.image_jpg_encoding_quality_min = 0
        self.image_jpg_encoding_quality_max = 100
        self.image_jpg_encoding_quality_NeedsToBeChangedFlag = 1

        self.CameraSetting_exposure_min = -12
        self.CameraSetting_exposure_max = -2
        self.CameraSetting_exposure_NeedsToBeChangedFlag = 1

        self.CameraSetting_gain_min = 0
        self.CameraSetting_gain_max = 255
        self.CameraSetting_gain_NeedsToBeChangedFlag = 1

        self.CameraSetting_brightness_min = 0
        self.CameraSetting_brightness_max = 255
        self.CameraSetting_brightness_NeedsToBeChangedFlag = 1

        self.CameraSetting_ManualFocus_min = 0
        self.CameraSetting_ManualFocus_max = 255
        self.CameraSetting_ManualFocus_NeedsToBeChangedFlag = 1

        self.CameraSetting_contrast_min = 0
        self.CameraSetting_contrast_max = 255
        self.CameraSetting_contrast_NeedsToBeChangedFlag = 1

        self.CameraSetting_saturation_min = 0
        self.CameraSetting_saturation_max = 255
        self.CameraSetting_saturation_NeedsToBeChangedFlag = 1

        self.CameraSetting_hue_min = 0
        self.CameraSetting_hue_max = 255
        self.CameraSetting_hue_NeedsToBeChangedFlag = 1

        self.CameraSetting_Autofocus_NeedsToBeChangedFlag = 1

        self.CameraSetting_Autoexposure_NeedsToBeChangedFlag = 1

        self.DisplaySnapshotInGUI_state = 0

        self.SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_state = 0

        self.image_height_ActualFromReceivedImage = -1
        self.image_width_ActualFromReceivedImage = -1
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.OpenCVsupportedBackendsDictWithEnglishNamesAsKeys = self.OpenCVgetSupportedBackends()
        print("CameraStreamerClass_ReubenPython2and3Class __init__: self.OpenCVsupportedBackendsDictWithEnglishNamesAsKeys: " + str(self.OpenCVsupportedBackendsDictWithEnglishNamesAsKeys))
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

        print("CameraStreamerClass_ReubenPython2and3Class __init__: The OS platform is: " + self.my_platform)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "GUIparametersDict" in self.setup_dict:
            self.GUIparametersDict = self.setup_dict["GUIparametersDict"]

            #########################################################
            #########################################################
            if "USE_GUI_FLAG" in self.GUIparametersDict:
                self.USE_GUI_FLAG = self.PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG", self.GUIparametersDict["USE_GUI_FLAG"])
            else:
                self.USE_GUI_FLAG = 0

            print("CameraStreamerClass_ReubenPython2and3Class __init__: USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "root" in self.GUIparametersDict:
                self.root = self.GUIparametersDict["root"]
            else:
                print("CameraStreamerClass_ReubenPython2and3Class __init__: ERROR, must pass in 'root'")
                return
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "EnableInternal_MyPrint_Flag" in self.GUIparametersDict:
                self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", self.GUIparametersDict["EnableInternal_MyPrint_Flag"])
            else:
                self.EnableInternal_MyPrint_Flag = 0

            print("CameraStreamerClass_ReubenPython2and3Class __init__: EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "PrintToConsoleFlag" in self.GUIparametersDict:
                self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", self.GUIparametersDict["PrintToConsoleFlag"])
            else:
                self.PrintToConsoleFlag = 1

            print("CameraStreamerClass_ReubenPython2and3Class __init__: PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "NumberOfPrintLines" in self.GUIparametersDict:
                self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", self.GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
            else:
                self.NumberOfPrintLines = 10

            print("CameraStreamerClass_ReubenPython2and3Class __init__: NumberOfPrintLines: " + str(self.NumberOfPrintLines))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "UseBorderAroundThisGuiObjectFlag" in self.GUIparametersDict:
                self.UseBorderAroundThisGuiObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseBorderAroundThisGuiObjectFlag", self.GUIparametersDict["UseBorderAroundThisGuiObjectFlag"])
            else:
                self.UseBorderAroundThisGuiObjectFlag = 0

            print("CameraStreamerClass_ReubenPython2and3Class __init__: UseBorderAroundThisGuiObjectFlag: " + str(self.UseBorderAroundThisGuiObjectFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_ROW" in self.GUIparametersDict:
                self.GUI_ROW = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROW", self.GUIparametersDict["GUI_ROW"], 0.0, 1000.0))
            else:
                self.GUI_ROW = 0

            print("CameraStreamerClass_ReubenPython2and3Class __init__: GUI_ROW: " + str(self.GUI_ROW))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMN" in self.GUIparametersDict:
                self.GUI_COLUMN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMN", self.GUIparametersDict["GUI_COLUMN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMN = 0

            print("CameraStreamerClass_ReubenPython2and3Class __init__: GUI_COLUMN: " + str(self.GUI_COLUMN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADX" in self.GUIparametersDict:
                self.GUI_PADX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADX", self.GUIparametersDict["GUI_PADX"], 0.0, 1000.0))
            else:
                self.GUI_PADX = 0

            print("CameraStreamerClass_ReubenPython2and3Class __init__: GUI_PADX: " + str(self.GUI_PADX))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADY" in self.GUIparametersDict:
                self.GUI_PADY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADY", self.GUIparametersDict["GUI_PADY"], 0.0, 1000.0))
            else:
                self.GUI_PADY = 0

            print("CameraStreamerClass_ReubenPython2and3Class __init__: GUI_PADY: " + str(self.GUI_PADY))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_ROWSPAN" in self.GUIparametersDict:
                self.GUI_ROWSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROWSPAN", self.GUIparametersDict["GUI_ROWSPAN"], 1.0, 1000.0))
            else:
                self.GUI_ROWSPAN = 1

            print("CameraStreamerClass_ReubenPython2and3Class __init__: GUI_ROWSPAN: " + str(self.GUI_ROWSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMNSPAN" in self.GUIparametersDict:
                self.GUI_COLUMNSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMNSPAN", self.GUIparametersDict["GUI_COLUMNSPAN"], 1.0, 1000.0))
            else:
                self.GUI_COLUMNSPAN = 1

            print("CameraStreamerClass_ReubenPython2and3Class __init__: GUI_COLUMNSPAN: " + str(self.GUI_COLUMNSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_STICKY" in self.GUIparametersDict:
                self.GUI_STICKY = str(self.GUIparametersDict["GUI_STICKY"])
            else:
                self.GUI_STICKY = "w"

            print("CameraStreamerClass_ReubenPython2and3Class __init__: GUI_STICKY: " + str(self.GUI_STICKY))
            #########################################################
            #########################################################

        else:
            self.GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("CameraStreamerClass_ReubenPython2and3Class __init__: No GUIparametersDict present, setting USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))

        #print("CameraStreamerClass_ReubenPython2and3Class __init__: GUIparametersDict = " + str(self.GUIparametersDict))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "camera_selection_number" in self.setup_dict:
            self.camera_selection_number = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("camera_selection_number", self.setup_dict["camera_selection_number"], 0.0, 10000.0))

        else:
            print("CameraStreamerClass_ReubenPython2and3Class __init__: ERROR, must pass 'camera_selection_number' into setup_dict.")
            return

        print("CameraStreamerClass_ReubenPython2and3Class __init__: camera_selection_number: " + str(self.camera_selection_number))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "camera_frame_rate" in self.setup_dict:
            self.camera_frame_rate = round(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("camera_frame_rate", self.setup_dict["camera_frame_rate"], 0.0, 10000.0))

        else:
            print("CameraStreamerClass_ReubenPython2and3Class __init__: ERROR, must pass 'camera_frame_rate' into setup_dict.")
            return

        print("CameraStreamerClass_ReubenPython2and3Class __init__: camera_frame_rate: " + str(self.camera_frame_rate))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "image_width" in self.setup_dict:
            self.image_width = round(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("image_width", self.setup_dict["image_width"], 0.0, 10000.0))

        else:
            print("CameraStreamerClass_ReubenPython2and3Class __init__: ERROR, must pass 'image_width' into setup_dict.")
            return

        print("CameraStreamerClass_ReubenPython2and3Class __init__: image_width: " + str(self.image_width))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "image_height" in self.setup_dict:
            self.image_height = round(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("image_height", self.setup_dict["image_height"], 0.0, 10000.0))

        else:
            print("CameraStreamerClass_ReubenPython2and3Class __init__: ERROR, must pass 'image_height' into setup_dict.")
            return

        print("CameraStreamerClass_ReubenPython2and3Class __init__: image_height: " + str(self.image_height))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "NameToDisplay_UserSet" in self.setup_dict:
            self.NameToDisplay_UserSet = str(self.setup_dict["NameToDisplay_UserSet"])
        else:
            self.NameToDisplay_UserSet = ""

        print("CameraStreamerClass_ReubenPython2and3Class __init__: NameToDisplay_UserSet: " + str(self.NameToDisplay_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DrawCircleAtImageCenterFlag" in self.setup_dict:
            self.DrawCircleAtImageCenterFlag = self.PassThrough0and1values_ExitProgramOtherwise("DrawCircleAtImageCenterFlag", self.setup_dict["DrawCircleAtImageCenterFlag"])
        else:
            self.DrawCircleAtImageCenterFlag = 0

        print("CameraStreamerClass_ReubenPython2and3Class __init__: DrawCircleAtImageCenterFlag: " + str(self.DrawCircleAtImageCenterFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "image_jpg_encoding_quality" in self.setup_dict:
            self.image_jpg_encoding_quality = round(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("image_jpg_encoding_quality", self.setup_dict["image_jpg_encoding_quality"], self.image_jpg_encoding_quality_min, self.image_jpg_encoding_quality_max))

        else:
            self.image_jpg_encoding_quality = round((self.image_jpg_encoding_quality_min + self.image_jpg_encoding_quality_max)/2.0)

        print("CameraStreamerClass_ReubenPython2and3Class __init__: image_jpg_encoding_quality: " + str(self.image_jpg_encoding_quality))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "CameraSetting_exposure" in self.setup_dict:
            self.CameraSetting_exposure = round(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("CameraSetting_exposure", self.setup_dict["CameraSetting_exposure"], self.CameraSetting_exposure_min, self.CameraSetting_exposure_max))

        else:
            self.CameraSetting_exposure = round((self.CameraSetting_exposure_min + self.CameraSetting_exposure_max)/2.0)

        print("CameraStreamerClass_ReubenPython2and3Class __init__: CameraSetting_exposure: " + str(self.CameraSetting_exposure))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "CameraSetting_gain" in self.setup_dict:
            self.CameraSetting_gain = round(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("CameraSetting_gain", self.setup_dict["CameraSetting_gain"], self.CameraSetting_gain_min, self.CameraSetting_gain_max))

        else:
            self.CameraSetting_gain = round((self.CameraSetting_gain_min + self.CameraSetting_gain_max)/2.0)

        print("CameraStreamerClass_ReubenPython2and3Class __init__: CameraSetting_gain: " + str(self.CameraSetting_gain))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "CameraSetting_brightness" in self.setup_dict:
            self.CameraSetting_brightness = round(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("CameraSetting_brightness", self.setup_dict["CameraSetting_brightness"], self.CameraSetting_brightness_min, self.CameraSetting_brightness_max))

        else:
            self.CameraSetting_brightness = round((self.CameraSetting_brightness_min + self.CameraSetting_brightness_max)/2.0)

        print("CameraStreamerClass_ReubenPython2and3Class __init__: CameraSetting_brightness: " + str(self.CameraSetting_brightness))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "CameraSetting_contrast" in self.setup_dict:
            self.CameraSetting_contrast = round(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("CameraSetting_contrast", self.setup_dict["CameraSetting_contrast"], self.CameraSetting_contrast_min, self.CameraSetting_contrast_max))

        else:
            self.CameraSetting_contrast = round((self.CameraSetting_contrast_min + self.CameraSetting_contrast_max)/2.0)

        print("CameraStreamerClass_ReubenPython2and3Class __init__: CameraSetting_contrast: " + str(self.CameraSetting_contrast))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "CameraSetting_saturation" in self.setup_dict:
            self.CameraSetting_saturation = round(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("CameraSetting_saturation", self.setup_dict["CameraSetting_saturation"], self.CameraSetting_saturation_min, self.CameraSetting_saturation_max))

        else:
            self.CameraSetting_saturation = round((self.CameraSetting_saturation_min + self.CameraSetting_saturation_max)/2.0)

        print("CameraStreamerClass_ReubenPython2and3Class __init__: CameraSetting_saturation: " + str(self.CameraSetting_saturation))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "CameraSetting_hue" in self.setup_dict:
            self.CameraSetting_hue = round(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("CameraSetting_hue", self.setup_dict["CameraSetting_hue"], self.CameraSetting_hue_min, self.CameraSetting_hue_max))

        else:
            self.CameraSetting_hue = round((self.CameraSetting_hue_min + self.CameraSetting_hue_max)/2.0)

        print("CameraStreamerClass_ReubenPython2and3Class __init__: CameraSetting_hue: " + str(self.CameraSetting_hue))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "CameraSetting_ManualFocus" in self.setup_dict:
            self.CameraSetting_ManualFocus = round(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("CameraSetting_ManualFocus", self.setup_dict["CameraSetting_ManualFocus"], self.CameraSetting_ManualFocus_min, self.CameraSetting_ManualFocus_max))

        else:
            self.CameraSetting_ManualFocus = round((self.CameraSetting_ManualFocus_min + self.CameraSetting_ManualFocus_max)/2.0)

        print("CameraStreamerClass_ReubenPython2and3Class __init__: CameraSetting_ManualFocus: " + str(self.CameraSetting_ManualFocus))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "CameraSetting_Autofocus" in self.setup_dict:
            self.CameraSetting_Autofocus = self.PassThrough0and1values_ExitProgramOtherwise("CameraSetting_Autofocus", self.setup_dict["CameraSetting_Autofocus"])
        else:
            self.CameraSetting_Autofocus = 1

        print("CameraStreamerClass_ReubenPython2and3Class __init__: CameraSetting_Autofocus: " + str(self.CameraSetting_Autofocus))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "CameraSetting_Autoexposure" in self.setup_dict:
            self.CameraSetting_Autoexposure = self.PassThrough0and1values_ExitProgramOtherwise("CameraSetting_Autoexposure", self.setup_dict["CameraSetting_Autoexposure"])
        else:
            self.CameraSetting_Autoexposure = 1

        print("CameraStreamerClass_ReubenPython2and3Class __init__: CameraSetting_Autoexposure: " + str(self.CameraSetting_Autoexposure))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "LaunchCameraSettingsDialog" in self.setup_dict:
            self.LaunchCameraSettingsDialog = self.PassThrough0and1values_ExitProgramOtherwise("LaunchCameraSettingsDialog", self.setup_dict["LaunchCameraSettingsDialog"])
        else:
            self.LaunchCameraSettingsDialog = 0

        print("CameraStreamerClass_ReubenPython2and3Class __init__: LaunchCameraSettingsDialog: " + str(self.LaunchCameraSettingsDialog))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "TkinterPreviewImageScalingFactor" in self.setup_dict:
            self.TkinterPreviewImageScalingFactor = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("TkinterPreviewImageScalingFactor", self.setup_dict["TkinterPreviewImageScalingFactor"], 0.1, 10.0)

        else:
            self.TkinterPreviewImageScalingFactor = 1.0

        print("CameraStreamerClass_ReubenPython2and3Class __init__: TkinterPreviewImageScalingFactor: " + str(self.TkinterPreviewImageScalingFactor))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "CameraCaptureThread_TimeToSleepEachLoop" in self.setup_dict:
            self.CameraCaptureThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("CameraCaptureThread_TimeToSleepEachLoop", self.setup_dict["CameraCaptureThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.CameraCaptureThread_TimeToSleepEachLoop = 0.001

        print("CameraStreamerClass_ReubenPython2and3Class __init__: CameraCaptureThread_TimeToSleepEachLoop: " + str(self.CameraCaptureThread_TimeToSleepEachLoop))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "CameraEncodeThread_TimeToSleepEachLoop" in self.setup_dict:
            self.CameraEncodeThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("CameraEncodeThread_TimeToSleepEachLoop", self.setup_dict["CameraEncodeThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.CameraEncodeThread_TimeToSleepEachLoop = 0.001

        print("CameraStreamerClass_ReubenPython2and3Class __init__: CameraEncodeThread_TimeToSleepEachLoop: " + str(self.CameraEncodeThread_TimeToSleepEachLoop))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "ImageSavingThread_TimeToSleepEachLoop" in self.setup_dict:
            self.ImageSavingThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("ImageSavingThread_TimeToSleepEachLoop", self.setup_dict["ImageSavingThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.ImageSavingThread_TimeToSleepEachLoop = 0.001

        print("CameraStreamerClass_ReubenPython2and3Class __init__: ImageSavingThread_TimeToSleepEachLoop: " + str(self.ImageSavingThread_TimeToSleepEachLoop))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "EnableCameraEncodeThreadFlag" in self.setup_dict:
            self.EnableCameraEncodeThreadFlag = self.PassThrough0and1values_ExitProgramOtherwise("EnableCameraEncodeThreadFlag", self.setup_dict["EnableCameraEncodeThreadFlag"])
        else:
            self.EnableCameraEncodeThreadFlag = 0

        print("CameraStreamerClass_ReubenPython2and3Class __init__: EnableCameraEncodeThreadFlag: " + str(self.EnableCameraEncodeThreadFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "EnableImageSavingThreadFlag" in self.setup_dict:
            self.EnableImageSavingThreadFlag = self.PassThrough0and1values_ExitProgramOtherwise("EnableImageSavingThreadFlag", self.setup_dict["EnableImageSavingThreadFlag"])
        else:
            self.EnableImageSavingThreadFlag = 0

        print("CameraStreamerClass_ReubenPython2and3Class __init__: EnableImageSavingThreadFlag:" + str(self.EnableImageSavingThreadFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "RemoveFisheyeDistortionFromImage_Flag" in self.setup_dict:
            self.RemoveFisheyeDistortionFromImage_Flag = self.PassThrough0and1values_ExitProgramOtherwise("RemoveFisheyeDistortionFromImage_Flag", self.setup_dict["RemoveFisheyeDistortionFromImage_Flag"])
        else:
            self.RemoveFisheyeDistortionFromImage_Flag = 0

        print("CameraStreamerClass_ReubenPython2and3Class __init__: RemoveFisheyeDistortionFromImage_Flag: " + str(self.RemoveFisheyeDistortionFromImage_Flag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.RemoveFisheyeDistortionFromImage_Flag_NeedsToBeChangedFlag = self.RemoveFisheyeDistortionFromImage_Flag
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "Camera_SavedImages_LocalDirectoryNameNoSlashes" in self.setup_dict:
            self.Camera_SavedImages_LocalDirectoryNameNoSlashes = self.setup_dict["Camera_SavedImages_LocalDirectoryNameNoSlashes"]
        else:
            self.Camera_SavedImages_LocalDirectoryNameNoSlashes = "Camera_SavedImages"

        print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: Camera_SavedImages_LocalDirectoryNameNoSlashes: " + str(self.Camera_SavedImages_LocalDirectoryNameNoSlashes))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "Camera_SavedImages_FilenamePrefix" in self.setup_dict:
            self.Camera_SavedImages_FilenamePrefix = self.setup_dict["Camera_SavedImages_FilenamePrefix"]
        else:
            self.Camera_SavedImages_FilenamePrefix = "Camera_"

        print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: Camera_SavedImages_FilenamePrefix: " + str(self.Camera_SavedImages_FilenamePrefix))
        #########################################################
        #########################################################

        ######################################################### unicorn
        #########################################################
        if "CameraCalibrationParametersDict" in self.setup_dict:

            #########################################################
            CameraCalibrationParametersDict_TEMP = self.setup_dict["CameraCalibrationParametersDict"]
            self.CameraCalibrationParametersDict = dict()

            KeysToVerifyExist = ["fx", "fy", "cx", "cy", "k1", "k2", "p1", "p2"]

            for Key in KeysToVerifyExist:
                if Key not in CameraCalibrationParametersDict_TEMP:
                    print("CameraStreamerClass_ReubenPython2and3Class __init__: CameraCalibrationParametersDict is missing key '" + str(self.Key) + "'.")
                    return
                else:
                    self.CameraCalibrationParametersDict[Key] = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("CameraCalibrationParametersDict, " + Key,
                                                                                                                        float(CameraCalibrationParametersDict_TEMP[Key]),
                                                                                                                        -1000000000.0,
                                                                                                                        1000000000.0)
            #########################################################

        else:
            self.CameraCalibrationParametersDict = dict([("fx", 1.0),("fy", 1.0),("cx", 0.0),("cy", 0.0),("k1", 0.0),("k2", 0.0),("p1", 0.0),("p2", 0.0)])

        print("CameraStreamerClass_ReubenPython2and3Class __init__: CameraCalibrationParametersDict: " + str(self.CameraCalibrationParametersDict))

        if "fx" not in self.CameraCalibrationParametersDict and self.RemoveFisheyeDistortionFromImage_Flag == 1:
            print("CameraStreamerClass_ReubenPython2and3Class __init__: CameraCalibrationParametersDict must be passed into class for RemoveFisheyeDistortionFromImage_Flag = 1!")
            return
        #########################################################
        #########################################################

        #########################################################

        #########################################################
        self.CameraCalibration_Kmatrix_CameraIntrinsicsMatrix, self.CameraCalibration_Darray_DistortionCoefficients = self.CreateCameraCalibrationAndDistortionMatricesFromCalibrationParameters(self.CameraCalibrationParametersDict)
        print("self.CameraCalibration_Kmatrix_CameraIntrinsicsMatrix: " + str(self.CameraCalibration_Kmatrix_CameraIntrinsicsMatrix))
        print("self.CameraCalibration_Darray_DistortionCoefficients: " + str(self.CameraCalibration_Darray_DistortionCoefficients))

        self.FisheyeWarpage_Map1, self.FisheyeWarpage_Map2 = self.RemoveFisheyeDistortionFromImage_CreateMapsOnly(image_width = self.image_width,
                                                                                                                image_height = self.image_height,
                                                                                                                CameraCalibationParamametersDict = self.CameraCalibrationParametersDict)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "OpenCVbackendToUseEnglishName" in self.setup_dict:
            OpenCVbackendToUseEnglishName_TEMP = self.setup_dict["OpenCVbackendToUseEnglishName"]

            if OpenCVbackendToUseEnglishName_TEMP in self.OpenCVsupportedBackendsDictWithEnglishNamesAsKeys:
                self.OpenCVbackendToUseEnglishName = OpenCVbackendToUseEnglishName_TEMP
            else:
                print("CameraStreamerClass_ReubenPython2and3Class __init__: ERROR, 'OpenCVbackendToUseEnglishName' must be contained in " + str(self.OpenCVsupportedBackendsDictWithEnglishNamesAsKeys))
                return

        else:
            self.OpenCVbackendToUseEnglishName = "CAP_ANY"

        print("CameraStreamerClass_ReubenPython2and3Class __init__: OpenCVbackendToUseEnglishName: " + str(self.OpenCVbackendToUseEnglishName))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "FOURCC_ToUse" in self.setup_dict:
            self.FOURCC_ToUse = self.setup_dict["FOURCC_ToUse"]

        else:
            self.FOURCC_ToUse = cv2.VideoWriter_fourcc(*'MJPG') #cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
            #self.FOURCC_ToUse = cv2.VideoWriter_fourcc(*'YUYV')

        print("CameraStreamerClass_ReubenPython2and3Class __init__: self.FOURCC_ToUse: " + str(self.FOURCC_ToUse))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.image_jpg_encoding_quality_TO_BE_SET = self.image_jpg_encoding_quality
        self.CameraSetting_exposure_TO_BE_SET = self.CameraSetting_exposure
        self.CameraSetting_gain_TO_BE_SET = self.CameraSetting_gain
        self.CameraSetting_brightness_TO_BE_SET = self.CameraSetting_brightness
        self.CameraSetting_ManualFocus_TO_BE_SET = self.CameraSetting_ManualFocus
        self.CameraSetting_contrast_TO_BE_SET = self.CameraSetting_contrast
        self.CameraSetting_saturation_TO_BE_SET = self.CameraSetting_saturation
        self.CameraSetting_hue_TO_BE_SET = self.CameraSetting_hue
        self.CameraSetting_Autofocus_TO_BE_SET = self.CameraSetting_Autofocus
        self.CameraSetting_Autoexposure_TO_BE_SET = self.CameraSetting_Autoexposure
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.SaveEachEncodedJPGImageFlag = 0 #Start the program not recording
        self.SaveEachEncodedJPGImageFlag_STATE_TO_BE_SET = 0 #Start the program not recording
        self.SaveEachEncodedJPGImageFlag_NEEDS_TO_BE_CHANGED_FLAG = 0 #Start the program not recording
        self.SaveEachEncodedJPGImageFlag_NEEDS_TO_BE_CHANGED_FLAG_GUI = 0 #Start the program not recording
        self.SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_NEEDS_TO_BE_CHANGED_FLAG_GUI = 0 #Start the program saving only snapshots
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
        self.camera_auto_exposure = 0

        self.original_captured_image = numpy.zeros((self.image_height, self.image_width, 3), numpy.uint8)
        self.encoded_image = numpy.zeros((self.image_height, self.image_width, 3), numpy.uint8)
        self.encoded_image_str_current = "default"

        self.original_captured_image_queue_FOR_ENCODING_IMAGES = Queue.Queue()
        self.original_captured_image_queue_FOR_ENCODING_IMAGES_MaxLength = 1000

        self.original_captured_image_queue_FOR_SAVING_IMAGES = Queue.Queue()
        self.original_captured_image_queue_FOR_SAVING_IMAGES_MaxLength = 1000

        self.encoded_image_str_queue = Queue.Queue()
        self.encoded_image_str_queue_MaxLength = self.original_captured_image_queue_FOR_ENCODING_IMAGES_MaxLength

        # http://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html, 0 to 100 (the higher is the better)
        self.encoding_parameters = [int(cv2.IMWRITE_JPEG_QUALITY), int(self.image_jpg_encoding_quality)]

        self.MostRecentDataDict = dict([("OriginalImage", self.original_captured_image),
                                        ("Time", self.CurrentTime_CalculatedFromCameraCaptureThread)])
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:
            ############################################### We're opening, closing, and re-opening to reset camera in case it didn't close properly in last program run
            self.CVcapture = cv2.VideoCapture(self.camera_selection_number, self.OpenCVsupportedBackendsDictWithEnglishNamesAsKeys[self.OpenCVbackendToUseEnglishName])
            time.sleep(0.050)
            self.CVcapture.release()

            time.sleep(0.050)

            self.CVcapture = cv2.VideoCapture(self.camera_selection_number, self.OpenCVsupportedBackendsDictWithEnglishNamesAsKeys[self.OpenCVbackendToUseEnglishName])

            '''
            #Test from image on-disk
            ImageSequenceDirectory = os.getcwd()
            ImageName = "WIN_20220524_16_38_58_Pro.jpg"
            self.CVcapture  = cv2.VideoCapture(ImageSequenceDirectory + "\\" + ImageName)
            '''

            self.IsCameraOpenFlag = self.CVcapture.isOpened()
            ###############################################

        except:
            exceptions = sys.exc_info()[0]
            print("CameraStreamerClass_ReubenPython2and3Class __init__: Failed to open camera, exceptions: %s" % exceptions)
            self.IsCameraOpenFlag = 0
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if self.IsCameraOpenFlag == 1:

            try:
                ###############################################
                ###############################################
                ###############################################
                #https: // docs.opencv.org / 3.4 / d4 / d15 / group__videoio__flags__base.html
                #LISTS ALL OF THE NUMERICAL CODES INSTEAD OF cv2.prop
                ###############################################
                ###############################################
                ###############################################

                #self.CVcapture.set(cv2.CV_CAP_PROP_CONVERT_RGB, 0) #DOESN'T WORK
                #self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')#ALL CODES AVAILABLE AT http://www.fourcc.org/codecs.php#letter_m
                #self.MyPrint_WithoutLogFile(self.CVcapture.get(cv2.CV_CAP_PROP_MODE)) #DOESN'T WORK
                #self.MyPrint_WithoutLogFile(self.CVcapture.get(cv2.CV_CAP_PROP_FORMAT)) #DOESN'T WORK
                #self.MyPrint_WithoutLogFile(self.CVcapture.get(cv2.CV_CAP_PROP_SETTINGS)) #DOESN'T WORK

                ###############################################
                ###############################################
                ###############################################
                self.CVcapture.set(cv2.CAP_PROP_FOURCC, self.FOURCC_ToUse) #Depending on which version of OpenCV, 6 MIGHT WORK INSTEAD OF cv2.CAP_PROP_FOURCC SOMEWHOW WORKS WHEREAS cv2.CV_CAP_PROP_FOURCC DOESN'T IN CV3.2.0 http://answers.opencv.org/question/135832/need-to-read-video-in-mjpeg-format-using-videocapture/

                [self.FOURCC_int_ReceivedFromVideoCaptureObject, self.FOURCC_string_ReceivedFromVideoCaptureObject] = self.OpenCVgetFOURCCfromVideoCapture(self.CVcapture)
                print("self.FOURCC_int_ReceivedFromVideoCaptureObject: " + str(self.FOURCC_int_ReceivedFromVideoCaptureObject) +
                      ", self.FOURCC_string_ReceivedFromVideoCaptureObject: " + str(self.FOURCC_string_ReceivedFromVideoCaptureObject))
                ###############################################
                ###############################################
                ###############################################

                self.CVcapture.set(cv2.CAP_PROP_FPS, self.camera_frame_rate)
                self.CVcapture.set(cv2.CAP_PROP_FRAME_WIDTH, self.image_width)
                self.CVcapture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.image_height)

                ###############################################
                ###############################################
                ###############################################
                # https://www.makehardware.com/2016/06/21/manual-exposure-vs-auto-exposure-for-elp-2-mp-usb-camera/
                if self.LaunchCameraSettingsDialog == 1:
                    self.CVcapture.set(cv2.CAP_PROP_SETTINGS, 0) #LAUNCHES THE CAMERA PARAMETERS DIALOG
                    print("Launching CameraSettingsDialog!")
                    time.sleep(2.0)
                ###############################################
                ###############################################
                ###############################################

                print("CAP_PROP_AUTOFOCUS read from camera is currently: " +\
                              str(self.CVcapture.get(cv2.CAP_PROP_AUTOFOCUS)))

                print("CAP_PROP_AUTO_EXPOSURE read from camera is currently: " +\
                              str(self.CVcapture.get(cv2.CAP_PROP_AUTO_EXPOSURE)))

                print("CAP_PROP_EXPOSURE read from camera is currently: " +\
                              str(self.CVcapture.get(cv2.CAP_PROP_EXPOSURE)))

                print("CAP_PROP_GAIN read from camera is currently: " +\
                              str(self.CVcapture.get(cv2.CAP_PROP_GAIN)))

                print("CAP_PROP_BRIGHTNESS read from camera is currently: " +\
                    str(self.CVcapture.get(cv2.CAP_PROP_BRIGHTNESS)))

                print("CAP_PROP_CONTRAST read from camera is currently: " +\
                              str(self.CVcapture.get(cv2.CAP_PROP_CONTRAST)))

                print("CAP_PROP_SATURATION read from camera is currently: " +\
                              str(self.CVcapture.get(cv2.CAP_PROP_SATURATION)))

                print("CAP_PROP_HUE read from camera is currently: " +\
                              str(self.CVcapture.get(cv2.CAP_PROP_HUE)))

                ##########################################################################################################
                self.CreateNewDirectory(os.getcwd() + "\\" + self.Camera_SavedImages_LocalDirectoryNameNoSlashes)
                ##########################################################################################################
            except:
                exceptions = sys.exc_info()[0]
                print("CameraStreamerClass __init__, exceptions: %s" % exceptions)

            #########################################################
            #########################################################
            self.CameraCaptureThread_ThreadingObject = threading.Thread(target=self.CameraCaptureThread, args=())
            self.CameraCaptureThread_ThreadingObject.start()
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if self.EnableCameraEncodeThreadFlag == 1:
                self.CameraEncodeThread_ThreadingObject = threading.Thread(target=self.CameraEncodeThread, args=())
                self.CameraEncodeThread_ThreadingObject.start()
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if self.EnableImageSavingThreadFlag == 1:
                self.ImageSavingThread_ThreadingObject = threading.Thread(target=self.ImageSavingThread, args=())
                self.ImageSavingThread_ThreadingObject.start()
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
        try:
            print("Camera " + str(self.camera_selection_number) + " released by __del__!")
            #self.CVcapture.release()

        except:
            pass
    ##########################################################################################################
    ##########################################################################################################

    ###########################################################################################################
    ##########################################################################################################
    def OpenCVgetFOURCCfromVideoCapture(self, VideoCaptureObject):

        FOURCC_int = -1
        FOURCC_string = ""

        try:
            FOURCC_int = int(VideoCaptureObject.get(cv2.CAP_PROP_FOURCC))

            ################################################### BOTH OF THESE LINES WORK
            # FOURCC_string = "%s" % struct.pack("<I", FOURCC_int)
            FOURCC_string = "".join([chr((int(FOURCC_int) >> 8 * i) & 0xFF) for i in range(4)])
            ###################################################

        except:
            exceptions = sys.exc_info()[0]
            print("OpenCVgetFOURCCfromVideoCapture: Exceptions, %s" % exceptions)
            #traceback.print_exc()

        return [FOURCC_int, FOURCC_string]
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def OpenCVgetSupportedBackends(self):

        try:
            OpenCVsupportedBackendsDictWithEnglishNamesAsKeys = dict()
            OpenCVsupportedBackendsListOfIntegerCodes = cv2.videoio_registry.getBackends()

            for BackendIntegerCode in OpenCVsupportedBackendsListOfIntegerCodes:
                EnglishNameString = cv2.videoio_registry.getBackendName(BackendIntegerCode)
                OpenCVsupportedBackendsDictWithEnglishNamesAsKeys["CAP_" + EnglishNameString] = BackendIntegerCode

            OpenCVsupportedBackendsDictWithEnglishNamesAsKeys["CAP_ANY"] = cv2.CAP_ANY
            return OpenCVsupportedBackendsDictWithEnglishNamesAsKeys

        except:
            exceptions = sys.exc_info()[0]
            print("OpenCVgetSupportedBackends, Exceptions: %s" % exceptions)
            return dict()
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CreateCameraCalibrationAndDistortionMatricesFromCalibrationParameters(self, CalibationParamametersDict):

        #CALIBATION PARAMETERS FOUND VIA https://github.com/darkpgmr/DarkCamCalibrator
        #CODE FROM https://medium.com/@kennethjiang/calibrate-fisheye-lens-using-opencv-333b05afa0b0
        #OPENCV: https://docs.opencv.org/3.4/db/d58/group__calib3d__fisheye.html
        #COULD TRY THIS CODE NEXT: https://github.com/smidm/opencv-python-fisheye-example/blob/master/fisheye_example.py

        try:

            ####
            fx = CalibationParamametersDict["fx"]
            fy = CalibationParamametersDict["fy"]
            cx = CalibationParamametersDict["cx"]
            cy = CalibationParamametersDict["cy"]
            k1 = CalibationParamametersDict["k1"]
            k2 = CalibationParamametersDict["k2"]
            p1 = CalibationParamametersDict["p1"]
            p2 = CalibationParamametersDict["p2"]
            ####

            ####
            CameraCalibration_Kmatrix_CameraIntrinsicsMatrix = numpy.zeros((3,3), numpy.float)
            CameraCalibration_Kmatrix_CameraIntrinsicsMatrix[0, 0] = float(fx)
            CameraCalibration_Kmatrix_CameraIntrinsicsMatrix[1, 1] = float(fy)
            CameraCalibration_Kmatrix_CameraIntrinsicsMatrix[2, 2] = 1.0
            CameraCalibration_Kmatrix_CameraIntrinsicsMatrix[0, 2] = float(cx)
            CameraCalibration_Kmatrix_CameraIntrinsicsMatrix[1, 2] = float(cy)
            ####

            ####
            CameraCalibration_Darray_DistortionCoefficients = numpy.zeros((1,4), numpy.float)
            CameraCalibration_Darray_DistortionCoefficients[0, 0] = float(k1)
            CameraCalibration_Darray_DistortionCoefficients[0, 1] = float(k2)
            CameraCalibration_Darray_DistortionCoefficients[0, 2] = float(p1)
            CameraCalibration_Darray_DistortionCoefficients[0, 3] = float(p2)
            ####

        except:
            exceptions = sys.exc_info()[0]
            print("CreateCameraCalibrationAndDistortionMatricesFromCalibrationParameters: Exceptions: %s" % exceptions)
            traceback.print_exc()

        return CameraCalibration_Kmatrix_CameraIntrinsicsMatrix, CameraCalibration_Darray_DistortionCoefficients
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def RemoveFisheyeDistortionFromImage_CreateMapsOnly(self, image_width, image_height, CameraCalibationParamametersDict):

        #CALIBATION PARAMETERS FOUND VIA https://github.com/darkpgmr/DarkCamCalibrator
        #CODE FROM https://medium.com/@kennethjiang/calibrate-fisheye-lens-using-opencv-333b05afa0b0
        #OPENCV: https://docs.opencv.org/3.4/db/d58/group__calib3d__fisheye.html
        #COULD TRY THIS CODE NEXT: https://github.com/smidm/opencv-python-fisheye-example/blob/master/fisheye_example.py

        FisheyeWarpage_Map1 = numpy.zeros((image_height, image_width, 3), numpy.float)
        FisheyeWarpage_Map2 = numpy.zeros((image_height, image_width, 3), numpy.float)

        try:

            ####
            CameraCalibration_Kmatrix_CameraIntrinsicsMatrix, CameraCalibration_Darray_DistortionCoefficients = self.CreateCameraCalibrationAndDistortionMatricesFromCalibrationParameters(CameraCalibationParamametersDict)
            ####

            ####
            #https://stackoverflow.com/questions/34316306/opencv-fisheye-calibration-cuts-too-much-of-the-resulting-image
            #How to lose less of the image
            CameraCalibration_Kmatrix_CameraIntrinsicsMatrix_ScaleFactor = 1.0
            CameraCalibration_Kmatrix_CameraIntrinsicsMatrix_Scaled = self.CameraCalibration_Kmatrix_CameraIntrinsicsMatrix.copy()
            CameraCalibration_Kmatrix_CameraIntrinsicsMatrix_Scaled[0, 0] = CameraCalibration_Kmatrix_CameraIntrinsicsMatrix[0, 0] / CameraCalibration_Kmatrix_CameraIntrinsicsMatrix_ScaleFactor
            CameraCalibration_Kmatrix_CameraIntrinsicsMatrix_Scaled[1, 1] = CameraCalibration_Kmatrix_CameraIntrinsicsMatrix[1, 1] / CameraCalibration_Kmatrix_CameraIntrinsicsMatrix_ScaleFactor
            ####

            ####
            RotationMatrix = numpy.eye(3)
            ####

            ####
            #cv.initUndistortRectifyMap(cameraMatrix, distCoeffs, R, newCameraMatrix, size, m1type[, map1[, map2]]	) -> map1, map2
            FisheyeWarpage_Map1, FisheyeWarpage_Map2 = cv2.fisheye.initUndistortRectifyMap(CameraCalibration_Kmatrix_CameraIntrinsicsMatrix,
                                                                                           CameraCalibration_Darray_DistortionCoefficients,
                                                                                           RotationMatrix,
                                                                                           CameraCalibration_Kmatrix_CameraIntrinsicsMatrix_Scaled,
                                                                                           (image_width, image_height),
                                                                                           cv2.CV_16SC2)
            ####

        except:
            exceptions = sys.exc_info()[0]
            print("RemoveFisheyeDistortionFromImage_CreateMapsOnly: Exceptions: %s" % exceptions)
            traceback.print_exc()

        return FisheyeWarpage_Map1, FisheyeWarpage_Map2
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def RemoveFisheyeDistortionFromImage(self, FisheyeWarpage_Map1, FisheyeWarpage_Map2, InputImage):

        UndistortedImage = cv2.remap(InputImage, FisheyeWarpage_Map1, FisheyeWarpage_Map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)#cv2.BORDER_CONSTANT)

        #cv2.Remap(InputImage, OutputImage, mapx, mapy, cv.CV_INTER_LINEAR + cv.CV_WARP_FILL_OUTLIERS,  cv.ScalarAll(0))
        #cv2.Undistort2(InputImage, OutputImage, intrinsics, dist_coeffs)

        return UndistortedImage
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CreateNewDirectory(self, directory):
        try:
            # print("CreateNewDirectory, directory: " + directory)
            if os.path.isdir(directory) == 0:  # No directory with this name exists
                os.makedirs(directory)
        except:
            exceptions = sys.exc_info()[0]
            print("CreateNewDirectory, Exceptions: %s" % exceptions)
            traceback.print_exc()

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
    def getPreciseSecondsTimeStampString_Milliseconds(self):
        ts_milliseconds = decimal.Decimal(1000.0 * time.time())

        return ts_milliseconds
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
    def StartSavingVideoStream(self, Camera_SavedImages_LocalDirectoryNameNoSlashes_Input = "", Camera_SavedImages_FilenamePrefix_Input = ""):

        if Camera_SavedImages_LocalDirectoryNameNoSlashes_Input != "":
            self.Camera_SavedImages_LocalDirectoryNameNoSlashes = Camera_SavedImages_LocalDirectoryNameNoSlashes_Input
            self.CreateNewDirectory(self.Camera_SavedImages_LocalDirectoryNameNoSlashes)

        if Camera_SavedImages_FilenamePrefix_Input != "":
            self.Camera_SavedImages_FilenamePrefix = Camera_SavedImages_FilenamePrefix_Input

        self.SaveEachEncodedJPGImageFlag = 1
        self.SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_state = 1

        self.SaveEachEncodedJPGImageFlag_NEEDS_TO_BE_CHANGED_FLAG_GUI = 1
        self.SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_NEEDS_TO_BE_CHANGED_FLAG_GUI = 1

        print("StartSavingVideoStream event fired!")
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StopSavingVideoStream(self):

        self.SaveEachEncodedJPGImageFlag = 0
        self.SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_state = 0

        self.SaveEachEncodedJPGImageFlag_NEEDS_TO_BE_CHANGED_FLAG_GUI = 1
        self.SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_NEEDS_TO_BE_CHANGED_FLAG_GUI = 1

        print("StopSavingVideoStream event fired!")
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def IsSaving(self):

        if self.original_captured_image_queue_FOR_SAVING_IMAGES.qsize() > 0:
            return 1
        else:
            return 0
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentDataDict(self):

        if self.EXIT_PROGRAM_FLAG == 0:
            self.MostRecentDataDict = dict([("OriginalImage", self.original_captured_image.copy()), #MUST COPY OR ELSE THE RECEIVING PROGRAM CAN CHANGE IT ALL THE WAY BACK TO THIS CLASS.
                                            ("CameraCalibration_Kmatrix_CameraIntrinsicsMatrix", self.CameraCalibration_Kmatrix_CameraIntrinsicsMatrix),
                                            ("CameraCalibration_Darray_DistortionCoefficients", self.CameraCalibration_Darray_DistortionCoefficients),
                                            ("Time", self.CurrentTime_CalculatedFromCameraCaptureThread)])

            #Deepcopy isn't needed here. Normally a numpy array wouldn't be safe to return within self.MostRecentDataDict WITHOUT deepcopy.
            #However, because we're first performing .copy on self.original_captured_image, that information is safe even without a deepcopy.
            return self.MostRecentDataDict.copy()

        else:
            return dict()  # So that we're not returning variables during the close-down process.
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_CameraCaptureThread(self):

        try:
            self.DataStreamingDeltaT_CalculatedFromCameraCaptureThread = self.CurrentTime_CalculatedFromCameraCaptureThread - self.LastTime_CalculatedFromCameraCaptureThread

            if self.DataStreamingDeltaT_CalculatedFromCameraCaptureThread != 0.0:
                self.DataStreamingFrequency_CalculatedFromCameraCaptureThread = 1.0/self.DataStreamingDeltaT_CalculatedFromCameraCaptureThread

            self.LastTime_CalculatedFromCameraCaptureThread = self.CurrentTime_CalculatedFromCameraCaptureThread

            self.LoopCounter_CalculatedFromCameraCaptureThread = self.LoopCounter_CalculatedFromCameraCaptureThread + 1
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_CameraCaptureThread ERROR with Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_CameraEncodeThread(self):

        try:
            self.DataStreamingDeltaT_CalculatedFromCameraEncodeThread = self.CurrentTime_CalculatedFromCameraEncodeThread - self.LastTime_CalculatedFromCameraEncodeThread

            if self.DataStreamingDeltaT_CalculatedFromCameraEncodeThread != 0.0:
                self.DataStreamingFrequency_CalculatedFromCameraEncodeThread = 1.0/self.DataStreamingDeltaT_CalculatedFromCameraEncodeThread

            self.LastTime_CalculatedFromCameraEncodeThread = self.CurrentTime_CalculatedFromCameraEncodeThread

            self.LoopCounter_CalculatedFromCameraEncodeThread = self.LoopCounter_CalculatedFromCameraEncodeThread + 1
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_CameraEncodeThread ERROR with Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_ImageSavingThread(self):

        try:
            self.DataStreamingDeltaT_CalculatedFromImageSavingThread = self.CurrentTime_CalculatedFromImageSavingThread - self.LastTime_CalculatedFromImageSavingThread

            if self.DataStreamingDeltaT_CalculatedFromImageSavingThread != 0.0:
                self.DataStreamingFrequency_CalculatedFromImageSavingThread = 1.0/self.DataStreamingDeltaT_CalculatedFromImageSavingThread

            self.LastTime_CalculatedFromImageSavingThread = self.CurrentTime_CalculatedFromImageSavingThread

            self.LoopCounter_CalculatedFromImageSavingThread = self.LoopCounter_CalculatedFromImageSavingThread + 1
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_ImageSavingThread ERROR with Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetImageSizeAsHeightWidthNumberOfChannelsList(self, InputImageAsNumpyArray):

        try:

            ################################################
            if len(InputImageAsNumpyArray.shape) == 2:
                Height, Width = InputImageAsNumpyArray.shape
                NumberOfChannels = 1
            elif len(InputImageAsNumpyArray.shape) == 3:
                Height, Width, NumberOfChannels = InputImageAsNumpyArray.shape
            else:
                print("GetImageSizeAsHeightWidthNumberOfChannelsList, error: len(InputImageAsNumpyArray.shape) should be 2 or 3.")
                return [-1, -1, -1]

            return [Height, Width, NumberOfChannels]
            ################################################

        except:
            exceptions = sys.exc_info()[0]
            print("GetImageSizeAsHeightWidthNumberOfChannelsList, Exceptions: %s" % exceptions)
            #traceback.print_exc()
            return [-1, -1, -1]

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ResizeImage(self, InputImageAsNumpyArray, ScalingFactor = 1.0):

        try:
            ################################################
            ################################################
            [Height, Width, NumberOfChannels] = self.GetImageSizeAsHeightWidthNumberOfChannelsList(InputImageAsNumpyArray)

            '''
            To shrink an image, it will generally look best with INTER_AREA interpolation, whereas to enlarge an image,
            it will generally look best with INTER_CUBIC (slow) or INTER_LINEAR (faster but still looks OK).
            '''

            ################################################
            if ScalingFactor <= 1.0:
                InterpolationMethod = cv2.INTER_AREA
            else:
                InterpolationMethod = cv2.INTER_LINEAR
            ################################################

            Height_Resized = int(ScalingFactor * Height)
            Width_Resized = int(ScalingFactor * Width)
            InputImageAsNumpyArray_Resized = cv2.resize(InputImageAsNumpyArray, (Width_Resized, Height_Resized), interpolation=InterpolationMethod)

            return InputImageAsNumpyArray_Resized
            ################################################
            ################################################

        except:
            exceptions = sys.exc_info()[0]
            print("ConvertNumpyArrayToTkinterPhotoImage, Exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ConvertNumpyArrayToTkinterPhotoImage(self, InputImageAsNumpyArray):

        try:

            ################################################
            ################################################
            [Height, Width, NumberOfChannels] = self.GetImageSizeAsHeightWidthNumberOfChannelsList(InputImageAsNumpyArray)

            PPM_ImageHeader = f'P6 {Width} {Height} 255 '.encode()

            if NumberOfChannels == 1:
                ImageData = PPM_ImageHeader + cv2.cvtColor(InputImageAsNumpyArray, cv2.COLOR_GRAY2RGB).tobytes()
            else:
                ImageData = PPM_ImageHeader + cv2.cvtColor(InputImageAsNumpyArray, cv2.COLOR_BGR2RGB).tobytes()

            ImageToReturnAsTkinterPhotoImagePPM = PhotoImage(width=Width, height=Height, data=ImageData, format='PPM') #PPM is color-only


            return ImageToReturnAsTkinterPhotoImagePPM
            ################################################
            ################################################

        except:
            exceptions = sys.exc_info()[0]
            print("ConvertNumpyArrayToTkinterPhotoImage, Exceptions: %s" % exceptions)
            traceback.print_exc()
            return -1

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ########################################################################################################## unicorn
    def CameraCaptureThread(self):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        self.MyPrint_WithoutLogFile("Started CameraCaptureThread for CameraStreamerClass_ReubenPython2and3Class object.")
        self.CameraCaptureThread_still_running_flag = 1
        self.StartingTime_CalculatedFromCameraCaptureThread = self.getPreciseSecondsTimeStampString()

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            try:

                ##########################################################################################################
                ##########################################################################################################
                self.CurrentTime_CalculatedFromCameraCaptureThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromCameraCaptureThread
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.RemoveFisheyeDistortionFromImage_Flag_NeedsToBeChangedFlag == 1:

                    self.RemoveFisheyeDistortionFromImage_Flag = self.RemoveFisheyeDistortionFromImage_Flag #PLACEHOLDER FOR DOING SOMETHING ELSE

                    self.RemoveFisheyeDistortionFromImage_Flag_NeedsToBeChangedFlag = 0
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.CameraSetting_Autofocus_NeedsToBeChangedFlag == 1:

                    self.CVcapture.set(cv2.CAP_PROP_AUTOFOCUS, int(self.CameraSetting_Autofocus_TO_BE_SET))
                    self.MyPrint_WithoutLogFile("Changed cv2.CAP_PROP_AUTO_focus to " + str(self.CameraSetting_Autofocus_TO_BE_SET))
                    self.CameraSetting_Autofocus = self.CameraSetting_Autofocus_TO_BE_SET
                    self.CameraSetting_Autofocus_NeedsToBeChangedFlag = 0
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.CameraSetting_Autoexposure_NeedsToBeChangedFlag == 1:

                    if self.CameraSetting_Autoexposure_TO_BE_SET == 1:
                        self.CVcapture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75) #https://github.com/opencv/opencv/issues/9738
                    else:
                        self.CVcapture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25) #https://github.com/opencv/opencv/issues/9738

                    self.MyPrint_WithoutLogFile("Changed cv2.CAP_PROP_AUTO_exposure to " + str(self.CameraSetting_Autoexposure_TO_BE_SET))
                    self.CameraSetting_Autoexposure = self.CameraSetting_Autoexposure_TO_BE_SET
                    self.CameraSetting_Autoexposure_NeedsToBeChangedFlag = 0
                ##########################################################################################################
                ##########################################################################################################

                #'''
                ########################################################################################################## Why is this code here in addition to the above code?
                ##########################################################################################################
                if self.CameraSetting_Autoexposure == 0:

                    if self.CameraSetting_exposure_NeedsToBeChangedFlag == 1:

                        self.CVcapture.set(cv2.CAP_PROP_EXPOSURE, int(self.CameraSetting_exposure_TO_BE_SET))
                        self.MyPrint_WithoutLogFile("Changed CAP_PROP_EXPOSURE to " + str(self.CameraSetting_exposure_TO_BE_SET))
                        self.CameraSetting_exposure = self.CameraSetting_exposure_TO_BE_SET
                        self.CameraSetting_exposure_NeedsToBeChangedFlag = 0
                ##########################################################################################################
                ##########################################################################################################
                #'''

                ##########################################################################################################
                ##########################################################################################################
                if self.CameraSetting_gain_NeedsToBeChangedFlag == 1:

                    self.CVcapture.set(cv2.CAP_PROP_GAIN, int(self.CameraSetting_gain_TO_BE_SET))
                    self.MyPrint_WithoutLogFile("Changed CAP_PROP_GAIN to " + str(self.CameraSetting_gain_TO_BE_SET))
                    self.CameraSetting_gain = self.CameraSetting_gain_TO_BE_SET
                    self.CameraSetting_gain_NeedsToBeChangedFlag = 0
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.CameraSetting_brightness_NeedsToBeChangedFlag == 1:

                    self.CVcapture.set(cv2.CAP_PROP_BRIGHTNESS, int(self.CameraSetting_brightness_TO_BE_SET))
                    self.MyPrint_WithoutLogFile("Changed CAP_PROP_BRIGHTNESS to " + str(self.CameraSetting_brightness_TO_BE_SET))
                    self.CameraSetting_brightness = self.CameraSetting_brightness_TO_BE_SET
                    self.CameraSetting_brightness_NeedsToBeChangedFlag = 0
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.CameraSetting_Autofocus == 0:

                    if self.CameraSetting_ManualFocus_NeedsToBeChangedFlag == 1:

                        self.CVcapture.set(28, int(self.CameraSetting_ManualFocus_TO_BE_SET))
                        self.MyPrint_WithoutLogFile("Changed CAP_PROP_ManualFocus to " + str(self.CameraSetting_ManualFocus_TO_BE_SET))
                        self.CameraSetting_ManualFocus = self.CameraSetting_ManualFocus_TO_BE_SET
                        self.CameraSetting_ManualFocus_NeedsToBeChangedFlag = 0
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.CameraSetting_contrast_NeedsToBeChangedFlag:

                    self.CVcapture.set(cv2.CAP_PROP_CONTRAST, int(self.CameraSetting_contrast_TO_BE_SET))
                    self.MyPrint_WithoutLogFile("Changed CAP_PROP_CONTRAST to " + str(self.CameraSetting_contrast_TO_BE_SET))
                    self.CameraSetting_contrast = self.CameraSetting_contrast_TO_BE_SET
                    self.CameraSetting_contrast_NeedsToBeChangedFlag = 0
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.CameraSetting_saturation_NeedsToBeChangedFlag:

                    self.CVcapture.set(cv2.CAP_PROP_SATURATION, int(self.CameraSetting_saturation_TO_BE_SET))
                    self.MyPrint_WithoutLogFile("Changed CAP_PROP_SATURATION to " + str(self.CameraSetting_saturation_TO_BE_SET))
                    self.CameraSetting_saturation = self.CameraSetting_saturation_TO_BE_SET
                    self.CameraSetting_saturation_NeedsToBeChangedFlag = 0
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.CameraSetting_hue_NeedsToBeChangedFlag == 1:

                    self.CVcapture.set(cv2.CAP_PROP_HUE, int(self.CameraSetting_hue_TO_BE_SET))
                    self.MyPrint_WithoutLogFile("Changed CAP_PROP_HUE to " + str(self.CameraSetting_hue_TO_BE_SET))
                    self.CameraSetting_hue = self.CameraSetting_hue_TO_BE_SET
                    self.CameraSetting_hue_NeedsToBeChangedFlag = 0
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                image_capture_success_flag, original_captured_image_TEMP = self.CVcapture.read()
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if image_capture_success_flag == 1:
                    image_capture_time_milliseconds = self.getPreciseSecondsTimeStampString_Milliseconds()

                    ##########################################################################################################
                    if self.RemoveFisheyeDistortionFromImage_Flag == 1 and "fx" in self.CameraCalibrationParametersDict:
                        self.original_captured_image = self.RemoveFisheyeDistortionFromImage(FisheyeWarpage_Map1 = self.FisheyeWarpage_Map1,
                                                                                             FisheyeWarpage_Map2 = self.FisheyeWarpage_Map2,
                                                                                             InputImage = original_captured_image_TEMP)
                    else:
                        self.original_captured_image = original_captured_image_TEMP
                    ##########################################################################################################

                    ##########################################################################################################
                    if self.original_captured_image_queue_FOR_ENCODING_IMAGES.qsize() < self.original_captured_image_queue_FOR_ENCODING_IMAGES_MaxLength:
                        self.original_captured_image_queue_FOR_ENCODING_IMAGES.put([image_capture_time_milliseconds, self.original_captured_image])
                    else:
                        #self.MyPrint_WithoutLogFile("ERROR: original_captured_image_queue_FOR_ENCODING_IMAGES has reached length limit, cannot add to queue.")
                        pass
                    ##########################################################################################################

                    ##########################################################################################################
                    if self.SaveEachEncodedJPGImageFlag == 1:
                        if self.original_captured_image_queue_FOR_SAVING_IMAGES.qsize() < self.original_captured_image_queue_FOR_SAVING_IMAGES_MaxLength:
                            self.original_captured_image_queue_FOR_SAVING_IMAGES.put([image_capture_time_milliseconds, self.original_captured_image])

                            if self.SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_state == 0: #single snapshot only, no continuous saving
                                self.SaveEachEncodedJPGImage_ToggleState()
                        else:
                            #self.MyPrint_WithoutLogFile("ERROR: original_captured_image_queue_FOR_SAVING_IMAGES has reached length limit, cannot add to queue.")
                            pass
                    ##########################################################################################################

                    ##########################################################################################################
                    self.image_height_ActualFromReceivedImage, self.image_width_ActualFromReceivedImage = self.original_captured_image.shape[:2]
                    ##########################################################################################################

                    ########################################################################################################## USE THE TIME.SLEEP() TO SET THE LOOP FREQUENCY
                    self.UpdateFrequencyCalculation_CameraCaptureThread()

                    if self.CameraCaptureThread_TimeToSleepEachLoop > 0.0:
                        time.sleep(self.CameraCaptureThread_TimeToSleepEachLoop)
                    ##########################################################################################################

                else:
                    time.sleep(0.001)
                ##########################################################################################################
                ##########################################################################################################

            except:
                exceptions = sys.exc_info()[0]
                self.MyPrint_WithoutLogFile("Failed to read new camera frame. Exceptions: %s" % exceptions)
                traceback.print_exc()
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        self.CVcapture.release()

        self.MyPrint_WithoutLogFile("Finished CameraCaptureThread for CameraStreamerClass_ReubenPython2and3Class object.")
        self.CameraCaptureThread_still_running_flag = 0
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ########################################################################################################## unicorn
    def CameraEncodeThread(self):

        self.MyPrint_WithoutLogFile("Started CameraEncodeThread for CameraStreamerClass_ReubenPython2and3Class object.")
        self.CameraEncodeThread_still_running_flag = 1
        self.StartingTime_CalculatedFromCameraEncodeThread = self.getPreciseSecondsTimeStampString()

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            try:

                ##########################################################################################################
                ##########################################################################################################
                if self.original_captured_image_queue_FOR_ENCODING_IMAGES.qsize() > 0:

                    self.CurrentTime_CalculatedFromCameraEncodeThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromCameraEncodeThread
                    [next_img_to_encode_original_acquisition_time_milliseconds, next_img_to_encode] = self.original_captured_image_queue_FOR_ENCODING_IMAGES.get()

                    ##########################################################################################################
                    if self.DrawCircleAtImageCenterFlag == 1:
                        dummy = 0
                        #radius = 5
                        #cv2.circle(next_img_to_encode, (int(self.image_width/2.0), int(self.image_height/2.0)), int(radius), (0, 0, 255), -1) #BGR

                        thickness = 1
                        if self.image_height_ActualFromReceivedImage != -1 and self.image_width_ActualFromReceivedImage != -1:
                            cv2.line(next_img_to_encode, (0, int(self.image_height_ActualFromReceivedImage/2.0)), (self.image_width_ActualFromReceivedImage, int(self.image_height_ActualFromReceivedImage/2.0)), (0, 0, 255), thickness) #BGR
                            cv2.line(next_img_to_encode, (int(self.image_width_ActualFromReceivedImage/2.0), 0), (int(self.image_width_ActualFromReceivedImage/2.0), self.image_height_ActualFromReceivedImage), (0, 0, 255), thickness)  # BGR
                    ##########################################################################################################

                    ########################################################################################################## UPDATE ENCODING PARAMETERS BASED ON IMAGE QUALITY SLIDER
                    if self.image_jpg_encoding_quality_NeedsToBeChangedFlag == 1:
                        self.encoding_parameters = [int(cv2.IMWRITE_JPEG_QUALITY), int(self.image_jpg_encoding_quality_TO_BE_SET)]
                        self.image_jpg_encoding_quality = self.image_jpg_encoding_quality_TO_BE_SET
                        self.image_jpg_encoding_quality_NeedsToBeChangedFlag = 0
                    ##########################################################################################################

                    ##########################################################################################################
                    self.EncodingProcessStartTime_CalculatedFromCameraEncodeThread = self.getPreciseSecondsTimeStampString()

                    encoding_success_flag, self.encoded_image = cv2.imencode('.jpg', next_img_to_encode, self.encoding_parameters)
                    self.encoded_image_str_current = bytearray(self.encoded_image)

                    self.EncodingProcessEndTime_CalculatedFromCameraEncodeThread = self.getPreciseSecondsTimeStampString()

                    if self.encoded_image_str_queue.qsize() < self.encoded_image_str_queue_MaxLength:
                        self.encoded_image_str_queue.put([next_img_to_encode_original_acquisition_time_milliseconds, self.encoded_image_str_current])
                    else:
                        #self.MyPrint_WithoutLogFile("ERROR: encoded_image_str_queue has reached length limit, cannot add to queue.")
                        pass

                    self.EncodingProcessTotalTime_CalculatedFromCameraEncodeThread = self.EncodingProcessEndTime_CalculatedFromCameraEncodeThread - self.EncodingProcessStartTime_CalculatedFromCameraEncodeThread
                    ##########################################################################################################

                    ########################################################################################################## USE THE TIME.SLEEP() TO SET THE LOOP FREQUENCY
                    self.UpdateFrequencyCalculation_CameraEncodeThread()
    
                    if self.CameraEncodeThread_TimeToSleepEachLoop > 0.0:
                        time.sleep(self.CameraEncodeThread_TimeToSleepEachLoop)
                    ##########################################################################################################

                else:
                    time.sleep(0.001)
                ##########################################################################################################
                ##########################################################################################################

            except:
                exceptions = sys.exc_info()[0]
                self.MyPrint_WithoutLogFile("Failed to encode frame. Exceptions: %s" % exceptions)
                traceback.print_exc()
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        self.MyPrint_WithoutLogFile("Finished CameraEncodeThread for CameraStreamerClass_ReubenPython2and3Class object.")
        self.CameraEncodeThread_still_running_flag = 0
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ########################################################################################################## unicorn
    def ImageSavingThread(self):

        self.MyPrint_WithoutLogFile("Started ImageSavingThread for CameraStreamerClass_ReubenPython2and3Class object.")
        self.ImageSavingThread_still_running_flag = 1
        self.StartingTime_CalculatedFromImageSavingThread = self.getPreciseSecondsTimeStampString()

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ##########################################################################################################
            ##########################################################################################################
            try:

                ##########################################################################################################
                if self.SaveEachEncodedJPGImageFlag_NEEDS_TO_BE_CHANGED_FLAG == 1: #Tripped by the ButtonResponse function
                    self.SaveEachEncodedJPGImageFlag = self.SaveEachEncodedJPGImageFlag_STATE_TO_BE_SET
                    self.SaveEachEncodedJPGImageFlag_NEEDS_TO_BE_CHANGED_FLAG_GUI = 1 #Set this so that the GUI thread knows to update
                    self.SaveEachEncodedJPGImageFlag_NEEDS_TO_BE_CHANGED_FLAG = 0
                ##########################################################################################################

                ########################################################################################################## unicorn
                if self.original_captured_image_queue_FOR_SAVING_IMAGES.qsize() > 0:

                    self.ImageSavingProcessStartTime_CalculatedFromImageSavingThread = self.getPreciseSecondsTimeStampString()

                    self.CurrentTime_CalculatedFromImageSavingThread = self.getPreciseSecondsTimeStampString()
                    [next_img_to_encode_and_save_original_acquisition_time_milliseconds, next_img_to_encode_and_save] = self.original_captured_image_queue_FOR_SAVING_IMAGES.get()

                    FileNameToSaveWith = os.getcwd() + "\\" +\
                                        self.Camera_SavedImages_LocalDirectoryNameNoSlashes + "\\" +\
                                        self.Camera_SavedImages_FilenamePrefix +\
                                        "CAM" + str(self.camera_selection_number) +\
                                        "_IMGQUAL" + str(self.image_jpg_encoding_quality) +\
                                        "_TIMEms" + str(int(next_img_to_encode_and_save_original_acquisition_time_milliseconds)) +\
                                        "_Frame" + str(self.LoopCounter_CalculatedFromImageSavingThread) +\
                                        ".jpg"

                    #self.MyPrint_WithoutLogFile(FileNameToSaveWith)
                    cv2.imwrite(FileNameToSaveWith, next_img_to_encode_and_save, [int(cv2.IMWRITE_JPEG_QUALITY), self.image_jpg_encoding_quality])

                    self.ImageSavingProcessEndTime_CalculatedFromImageSavingThread = self.getPreciseSecondsTimeStampString()

                    self.ImageSavingProcessTotalTime_CalculatedFromImageSavingThread = self.ImageSavingProcessEndTime_CalculatedFromImageSavingThread - self.ImageSavingProcessStartTime_CalculatedFromImageSavingThread

                    ############################################### USE THE TIME.SLEEP() TO SET THE LOOP FREQUENCY
                    self.UpdateFrequencyCalculation_ImageSavingThread()

                    if self.ImageSavingThread_TimeToSleepEachLoop > 0.0:
                        time.sleep(self.ImageSavingThread_TimeToSleepEachLoop)
                    ###############################################

                else:
                    time.sleep(0.001)
                ##########################################################################################################

            except:
                exceptions = sys.exc_info()[0]
                self.MyPrint_WithoutLogFile("Failed to save image. Exceptions: %s" % exceptions)
                traceback.print_exc()

            ##########################################################################################################
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        self.MyPrint_WithoutLogFile("Finished ImageSavingThread for CameraStreamerClass_ReubenPython2and3Class object.")
        self.ImageSavingThread_still_running_flag = 0
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for CameraStreamerClass_ReubenPython2and3Class object")

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

        print("Starting the GUI_Thread for CameraStreamerClass_ReubenPython2and3Class object.")

        ################################################
        ################################################
        self.root = parent
        self.parent = parent
        ################################################
        ################################################

        ################################################
        ################################################
        self.TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150) #RGB
        self.TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150) #RGB
        self.TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
        self.TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
        self.TkinterScaleLength = 200
        self.TkinterCheckbuttonWidth = 20
        ################################################
        ################################################

        ################################################
        ################################################
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
        ################################################
        ################################################

        ################################################
        ################################################
        self.MainProgramAndControlsInfoFrame = Frame(self.myFrame)
        self.MainProgramAndControlsInfoFrame.grid(row=0, column=1, padx=1, pady=1, columnspan=1, rowspan=1, sticky="w")
        ################################################
        ################################################

        ################################################
        ################################################
        self.image_label = Label(self.myFrame, text="image_label")
        self.image_label.grid(row=0, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        self.image_label.bind('<ButtonRelease-1>', lambda event, name="DisplaySnapshotInGUI_Checkbutton": self.image_label_ClickResponse(event, name))
        ################################################
        ################################################

        ################################################
        ################################################
        self.CameraSettings_Sliders_Frame = Frame(self.myFrame)
        self.CameraSettings_Sliders_Frame.grid(row=1, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        ################################################
        ################################################

        ################################################
        ################################################
        self.CameraSettings_Checkbuttons_Frame = Frame(self.myFrame)
        self.CameraSettings_Checkbuttons_Frame.grid(row=2, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        ################################################
        ################################################

        ################################################
        ################################################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=50)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=1, column=1, padx=1, pady=1, columnspan=1, rowspan=1, sticky="w")
        ################################################
        ################################################

        ################################################
        ################################################
        self.DeviceInfo_label = Label(self.MainProgramAndControlsInfoFrame, text="Device Info", width=50)
        self.DeviceInfo_label["text"] = self.NameToDisplay_UserSet
        self.DeviceInfo_label.grid(row=0, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        ################################################
        ################################################

        ################################################
        ################################################
        self.CameraCapture_loop_info_label = Label(self.MainProgramAndControlsInfoFrame, text="CameraCapture_loop_info_label", width=50)
        self.CameraCapture_loop_info_label.grid(row=1, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        ################################################
        ################################################

        ################################################
        ################################################
        self.CameraEncode_loop_info_label = Label(self.MainProgramAndControlsInfoFrame, text="CameraEncode_loop_info_label", width=50)
        self.CameraEncode_loop_info_label.grid(row=2, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        ################################################
        ################################################

        ################################################
        ################################################
        self.ImageSaving_loop_info_label = Label(self.MainProgramAndControlsInfoFrame, text="ImageSaving_loop_info_label", width=50)
        self.ImageSaving_loop_info_label.grid(row=3, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        ################################################
        ################################################

        ################################################
        ################################################
        self.SaveEachEncodedJPGImageButton = Button(self.MainProgramAndControlsInfoFrame,
                                                    text="SaveEachEncodedJPGImage\nNot Saving",
                                                    state="normal",
                                                    bg = self.TKinter_LightRedColor,
                                                    width=30,
                                                    command=lambda i=1: self.SaveEachEncodedJPGImageButtonResponse())
        self.SaveEachEncodedJPGImageButton.grid(row=4, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        ################################################
        ################################################

        ################################################
        ################################################
        self.SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_Checkbutton_Value = DoubleVar()

        if self.SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_state == 1:
            self.SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_Checkbutton_Value.set(1)
        else:
            self.SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_Checkbutton_Value.set(0)

        self.SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_Checkbutton = Checkbutton(self.MainProgramAndControlsInfoFrame,
                                                         width=int(2.0*self.TkinterCheckbuttonWidth),
                                                         text='SnapshotOrContinuousSaving',
                                                         state="normal",
                                                         variable=self.SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_Checkbutton_Value)
        self.SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_Checkbutton.bind('<ButtonRelease-1>', lambda event, name="SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_Checkbutton": self.SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_CheckbuttonResponse(event, name))
        self.SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_Checkbutton.grid(row=5, column=0, padx=1, pady=1, columnspan=1,rowspan=1)
        ################################################
        ################################################

        ################################################
        ################################################
        try:
            ################################################
            self.image_jpg_encoding_quality_Slider_DoubleVar = DoubleVar()

            self.image_jpg_encoding_quality_Slider = Scale(self.CameraSettings_Sliders_Frame,
                                                           label = "Image Jpg Enc Qual",
                                                           state="normal",
                                                           from_ = self.image_jpg_encoding_quality_min,
                                                           to = self.image_jpg_encoding_quality_max,
                                                           tickinterval = 50,
                                                           orient=HORIZONTAL,
                                                           showvalue=1,
                                                           width = 10,
                                                           length = self.TkinterScaleLength,
                                                           resolution = 1,
                                                           variable = self.image_jpg_encoding_quality_Slider_DoubleVar)
            self.image_jpg_encoding_quality_Slider.bind('<Button-1>', lambda event, name="image_jpg_encoding_quality_Slider": self.image_jpg_encoding_quality_Slider_Response(event, name))
            self.image_jpg_encoding_quality_Slider.bind('<B1-Motion>', lambda event, name="image_jpg_encoding_quality_Slider": self.image_jpg_encoding_quality_Slider_Response(event, name))
            self.image_jpg_encoding_quality_Slider.bind('<ButtonRelease-1>', lambda event, name="image_jpg_encoding_quality_Slider": self.image_jpg_encoding_quality_Slider_Response(event, name))
            self.image_jpg_encoding_quality_Slider.set(int(self.image_jpg_encoding_quality))
            self.image_jpg_encoding_quality_Slider.grid(row=5, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
            ################################################

            ################################################
            self.CameraSetting_exposure_slider_DoubleVar = DoubleVar()

            self.CameraSetting_exposure_slider = Scale(self.CameraSettings_Sliders_Frame,
                                                       label = "Exposure",
                                                       state="normal",
                                                       from_ = self.CameraSetting_exposure_min,
                                                       to = self.CameraSetting_exposure_max,
                                                       tickinterval = int((self.CameraSetting_exposure_max - self.CameraSetting_exposure_min)/2.0),
                                                       orient=HORIZONTAL,
                                                       showvalue=1,
                                                       width = 10,
                                                       length = self.TkinterScaleLength,
                                                       resolution = 1,
                                                       variable = self.CameraSetting_exposure_slider_DoubleVar)
            self.CameraSetting_exposure_slider.bind('<Button-1>', lambda event, name="CameraSetting_exposure_slider": self.CameraSetting_exposure_slider_Response(event, name))
            self.CameraSetting_exposure_slider.bind('<B1-Motion>', lambda event, name="CameraSetting_exposure_slider": self.CameraSetting_exposure_slider_Response(event, name))
            self.CameraSetting_exposure_slider.bind('<ButtonRelease-1>', lambda event, name="CameraSetting_exposure_slider": self.CameraSetting_exposure_slider_Response(event, name))
            self.CameraSetting_exposure_slider.set(int(self.CameraSetting_exposure))
            self.CameraSetting_exposure_slider.grid(row=6, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
            ################################################

            ################################################
            self.CameraSetting_gain_slider_DoubleVar = DoubleVar()

            self.CameraSetting_gain_slider = Scale(self.CameraSettings_Sliders_Frame,
                                                   label = "Gain",
                                                   state="normal",
                                                   from_ = self.CameraSetting_gain_min,
                                                   to = self.CameraSetting_gain_max,
                                                   tickinterval = int((self.CameraSetting_gain_max - self.CameraSetting_gain_min)/2.0),
                                                   orient=HORIZONTAL,
                                                   showvalue=1,
                                                   width = 10,
                                                   length = self.TkinterScaleLength,
                                                   resolution = 1,
                                                   variable = self.CameraSetting_gain_slider_DoubleVar)
            self.CameraSetting_gain_slider.bind('<Button-1>', lambda event, name="CameraSetting_gain_slider": self.CameraSetting_gain_slider_Response(event, name))
            self.CameraSetting_gain_slider.bind('<B1-Motion>', lambda event, name="CameraSetting_gain_slider": self.CameraSetting_gain_slider_Response(event, name))
            self.CameraSetting_gain_slider.bind('<ButtonRelease-1>', lambda event, name="CameraSetting_gain_slider": self.CameraSetting_gain_slider_Response(event, name))
            self.CameraSetting_gain_slider.set(int(self.CameraSetting_gain))
            self.CameraSetting_gain_slider.grid(row=7, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
            ################################################

            ################################################
            self.CameraSetting_brightness_slider_DoubleVar = DoubleVar()

            self.CameraSetting_brightness_slider = Scale(self.CameraSettings_Sliders_Frame,
                                                         label = "Brightness",
                                                         state="normal",
                                                         from_ = self.CameraSetting_brightness_min,
                                                         to = self.CameraSetting_brightness_max,
                                                         tickinterval = int((self.CameraSetting_brightness_max - self.CameraSetting_brightness_min)/2.0),
                                                         orient=HORIZONTAL,
                                                         showvalue=1,
                                                         width = 10,
                                                         length = self.TkinterScaleLength,
                                                         resolution = 1,
                                                         variable = self.CameraSetting_brightness_slider_DoubleVar)
            self.CameraSetting_brightness_slider.bind('<Button-1>', lambda event, name="CameraSetting_brightness_slider": self.CameraSetting_brightness_slider_Response(event, name))
            self.CameraSetting_brightness_slider.bind('<B1-Motion>', lambda event, name="CameraSetting_brightness_slider": self.CameraSetting_brightness_slider_Response(event, name))
            self.CameraSetting_brightness_slider.bind('<ButtonRelease-1>', lambda event, name="CameraSetting_brightness_slider": self.CameraSetting_brightness_slider_Response(event, name))
            self.CameraSetting_brightness_slider.set(int(self.CameraSetting_brightness))
            self.CameraSetting_brightness_slider.grid(row=8, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
            ################################################

            ################################################
            self.CameraSetting_ManualFocus_slider_DoubleVar = DoubleVar()

            self.CameraSetting_ManualFocus_slider = Scale(self.CameraSettings_Sliders_Frame,
                                                          label = "ManualFocus",
                                                          state="normal",
                                                          from_ = self.CameraSetting_ManualFocus_min,
                                                          to = self.CameraSetting_ManualFocus_max,
                                                          tickinterval = int((self.CameraSetting_ManualFocus_max - self.CameraSetting_ManualFocus_min)/2.0),
                                                          orient=HORIZONTAL,
                                                          showvalue=1,
                                                          width = 10,
                                                          length = self.TkinterScaleLength,
                                                          resolution = 5,
                                                          variable = self.CameraSetting_ManualFocus_slider_DoubleVar)
            self.CameraSetting_ManualFocus_slider.bind('<Button-1>', lambda event, name="CameraSetting_ManualFocus_slider": self.CameraSetting_ManualFocus_slider_Response(event, name))
            self.CameraSetting_ManualFocus_slider.bind('<B1-Motion>', lambda event, name="CameraSetting_ManualFocus_slider": self.CameraSetting_ManualFocus_slider_Response(event, name))
            self.CameraSetting_ManualFocus_slider.bind('<ButtonRelease-1>', lambda event, name="CameraSetting_ManualFocus_slider": self.CameraSetting_ManualFocus_slider_Response(event, name))
            self.CameraSetting_ManualFocus_slider.set(int(self.CameraSetting_ManualFocus))
            self.CameraSetting_ManualFocus_slider.grid(row=5, column=1, padx=1, pady=1, columnspan=1, rowspan=1)
            ################################################

            ################################################
            self.CameraSetting_contrast_slider_DoubleVar = DoubleVar()

            self.CameraSetting_contrast_slider = Scale(self.CameraSettings_Sliders_Frame,
                                                       label = "Contrast",
                                                       state="normal",
                                                       from_ = self.CameraSetting_contrast_min,
                                                       to = self.CameraSetting_contrast_max,
                                                       tickinterval = int((self.CameraSetting_contrast_max - self.CameraSetting_contrast_min)/2.0),
                                                       orient=HORIZONTAL,
                                                       showvalue=1,
                                                       width = 10,
                                                       length = self.TkinterScaleLength,
                                                       resolution = 1,
                                                       variable = self.CameraSetting_contrast_slider_DoubleVar)
            self.CameraSetting_contrast_slider.bind('<Button-1>', lambda event, name="CameraSetting_contrast_slider": self.CameraSetting_contrast_slider_Response(event, name))
            self.CameraSetting_contrast_slider.bind('<B1-Motion>', lambda event, name="CameraSetting_contrast_slider": self.CameraSetting_contrast_slider_Response(event, name))
            self.CameraSetting_contrast_slider.bind('<ButtonRelease-1>', lambda event, name="CameraSetting_contrast_slider": self.CameraSetting_contrast_slider_Response(event, name))
            self.CameraSetting_contrast_slider.set(int(self.CameraSetting_contrast))
            self.CameraSetting_contrast_slider.grid(row=6, column=1, padx=1, pady=1, columnspan=1, rowspan=1)
            ################################################

            ################################################
            self.CameraSetting_saturation_slider_DoubleVar = DoubleVar()

            self.CameraSetting_saturation_slider = Scale(self.CameraSettings_Sliders_Frame,
                                                         label = "Saturation",
                                                         state="normal",
                                                         from_ = self.CameraSetting_saturation_min,
                                                         to = self.CameraSetting_saturation_max,
                                                         tickinterval = int((self.CameraSetting_saturation_max - self.CameraSetting_saturation_min)/2.0),
                                                         orient=HORIZONTAL,
                                                         showvalue=1,
                                                         width = 10,
                                                         length = self.TkinterScaleLength,
                                                         resolution = 1,
                                                         variable = self.CameraSetting_saturation_slider_DoubleVar)
            self.CameraSetting_saturation_slider.bind('<Button-1>', lambda event, name="CameraSetting_saturation_slider": self.CameraSetting_saturation_slider_Response(event, name))
            self.CameraSetting_saturation_slider.bind('<B1-Motion>', lambda event, name="CameraSetting_saturation_slider": self.CameraSetting_saturation_slider_Response(event, name))
            self.CameraSetting_saturation_slider.bind('<ButtonRelease-1>', lambda event, name="CameraSetting_saturation_slider": self.CameraSetting_saturation_slider_Response(event, name))
            self.CameraSetting_saturation_slider.set(int(self.CameraSetting_saturation))
            self.CameraSetting_saturation_slider.grid(row=7, column=1, padx=1, pady=1, columnspan=1, rowspan=1)
            ################################################

            ################################################
            self.CameraSetting_hue_slider_DoubleVar = DoubleVar()

            self.CameraSetting_hue_slider = Scale(self.CameraSettings_Sliders_Frame,
                                                  label = "Hue",
                                                  state="normal",
                                                  from_ = self.CameraSetting_hue_min,
                                                  to = self.CameraSetting_hue_max,
                                                  tickinterval = int((self.CameraSetting_hue_max - self.CameraSetting_hue_min)/2.0),
                                                  orient=HORIZONTAL,
                                                  showvalue=1,
                                                  width = 10,
                                                  length = self.TkinterScaleLength,
                                                  resolution = 1,
                                                  variable = self.CameraSetting_hue_slider_DoubleVar)
            self.CameraSetting_hue_slider.bind('<Button-1>', lambda event, name="CameraSetting_hue_slider": self.CameraSetting_hue_slider_Response(event, name))
            self.CameraSetting_hue_slider.bind('<B1-Motion>', lambda event, name="CameraSetting_hue_slider": self.CameraSetting_hue_slider_Response(event, name))
            self.CameraSetting_hue_slider.bind('<ButtonRelease-1>', lambda event, name="CameraSetting_hue_slider": self.CameraSetting_hue_slider_Response(event, name))
            self.CameraSetting_hue_slider.set(int(self.CameraSetting_hue))
            self.CameraSetting_hue_slider.grid(row=8, column=1, padx=1, pady=1, columnspan=1, rowspan=1)
            ################################################

            ###########################################################
            self.CameraSetting_Autofocus_Checkbutton_Value = DoubleVar()

            if self.CameraSetting_Autofocus == 1:
                self.CameraSetting_Autofocus_Checkbutton_Value.set(1)
            else:
                self.CameraSetting_Autofocus_Checkbutton_Value.set(0)

            self.CameraSetting_Autofocus_Checkbutton = Checkbutton(self.CameraSettings_Checkbuttons_Frame,
                                                             width=self.TkinterCheckbuttonWidth,
                                                             text='Autofocus',
                                                             state="normal",
                                                             variable=self.CameraSetting_Autofocus_Checkbutton_Value)
            self.CameraSetting_Autofocus_Checkbutton.bind('<ButtonRelease-1>', lambda event, name="CameraSetting_Autofocus_Checkbutton": self.CameraSetting_Autofocus_CheckbuttonResponse(event, name))
            self.CameraSetting_Autofocus_Checkbutton.grid(row=0, column=0, padx=1, pady=1, columnspan=1,rowspan=1)
            ###########################################################

            ###########################################################
            self.CameraSetting_Autoexposure_Checkbutton_Value = DoubleVar()

            if self.CameraSetting_Autoexposure == 1:
                self.CameraSetting_Autoexposure_Checkbutton_Value.set(1)
            else:
                self.CameraSetting_Autoexposure_Checkbutton_Value.set(0)

            self.CameraSetting_Autoexposure_Checkbutton = Checkbutton(self.CameraSettings_Checkbuttons_Frame,
                                                             width=self.TkinterCheckbuttonWidth,
                                                             text='Autoexposure',
                                                             state="normal",
                                                             variable=self.CameraSetting_Autoexposure_Checkbutton_Value)
            self.CameraSetting_Autoexposure_Checkbutton.bind('<ButtonRelease-1>', lambda event, name="CameraSetting_Autoexposure_Checkbutton": self.CameraSetting_Autoexposure_CheckbuttonResponse(event, name))
            self.CameraSetting_Autoexposure_Checkbutton.grid(row=0, column=1, padx=1, pady=1, columnspan=1,rowspan=1)
            ###########################################################
            
            ###########################################################
            self.DisplaySnapshotInGUI_Checkbutton_Value = DoubleVar()

            if self.DisplaySnapshotInGUI_state == 1:
                self.DisplaySnapshotInGUI_Checkbutton_Value.set(1)
            else:
                self.DisplaySnapshotInGUI_Checkbutton_Value.set(0)

            self.DisplaySnapshotInGUI_Checkbutton = Checkbutton(self.CameraSettings_Checkbuttons_Frame,
                                                             width=self.TkinterCheckbuttonWidth,
                                                             text='PreviewSnapshot',
                                                             state="normal",
                                                             variable=self.DisplaySnapshotInGUI_Checkbutton_Value)
            self.DisplaySnapshotInGUI_Checkbutton.bind('<ButtonRelease-1>', lambda event, name="DisplaySnapshotInGUI_Checkbutton": self.DisplaySnapshotInGUI_CheckbuttonResponse(event, name))
            self.DisplaySnapshotInGUI_Checkbutton.grid(row=0, column=2, padx=1, pady=1, columnspan=1,rowspan=1)
            ###########################################################
            
            ###########################################################
            self.RemoveFisheyeDistortionFromImage_Checkbutton_Value = DoubleVar()

            if self.RemoveFisheyeDistortionFromImage_Flag == 1:
                self.RemoveFisheyeDistortionFromImage_Checkbutton_Value.set(1)
            else:
                self.RemoveFisheyeDistortionFromImage_Checkbutton_Value.set(0)

            self.RemoveFisheyeDistortionFromImage_Checkbutton = Checkbutton(self.CameraSettings_Checkbuttons_Frame,
                                                             width=self.TkinterCheckbuttonWidth,
                                                             text='Remove Fisheye',
                                                             state="normal",
                                                             variable=self.RemoveFisheyeDistortionFromImage_Checkbutton_Value)
            self.RemoveFisheyeDistortionFromImage_Checkbutton.bind('<ButtonRelease-1>', lambda event, name="RemoveFisheyeDistortionFromImage_Checkbutton": self.RemoveFisheyeDistortionFromImage_CheckbuttonResponse(event, name))
            self.RemoveFisheyeDistortionFromImage_Checkbutton.grid(row=0, column=3, padx=1, pady=1, columnspan=1,rowspan=1)
            ###########################################################
            
        except:
            exceptions = sys.exc_info()[0]
            print("GUI_Thread ERROR, Exceptions: %s" % exceptions)
            traceback.print_exc()
        ################################################
        ################################################

        ################################################
        ################################################
        self.GUI_ready_to_be_updated_flag = 1
        ################################################
        ################################################

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

                    #######################################################
                    self.CameraCapture_loop_info_label["text"] = "camera_selection_number: " + str(self.camera_selection_number) +\
                                                                 "\nCapture counter: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.LoopCounter_CalculatedFromCameraCaptureThread) +\
                                                                 "\nCapture Freq: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_CalculatedFromCameraCaptureThread) +\
                                                                 "\nCapturing is : " + str(self.LoopCounter_CalculatedFromCameraCaptureThread - self.LoopCounter_CalculatedFromCameraEncodeThread) + " frames ahead of encoding." +\
                                                                 "\nCaptured image is : " + str(self.image_width_ActualFromReceivedImage) + " x " + str(self.image_height_ActualFromReceivedImage) + " pixels."
                    #######################################################

                    #######################################################
                    self.CameraEncode_loop_info_label["text"] = "Encode counter: " +\
                                                                       self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.LoopCounter_CalculatedFromCameraEncodeThread) +\
                                                                       "\nEncode Freq: " +\
                                                                       self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_CalculatedFromCameraEncodeThread) +\
                                                                       "\nEncodingProcessTotalTime_CalculatedFromCameraEncodeThread: " +\
                                                                       self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.EncodingProcessTotalTime_CalculatedFromCameraEncodeThread)
                    #######################################################

                    #######################################################
                    self.ImageSaving_loop_info_label["text"] = "ImageSaving counter: " +\
                                                                       self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.LoopCounter_CalculatedFromImageSavingThread) +\
                                                                       "\nImageSaving Freq: " +\
                                                                       self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_CalculatedFromImageSavingThread) +\
                                                                       "\nSaving qsize(): " +\
                                                                       self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.original_captured_image_queue_FOR_SAVING_IMAGES.qsize())
                    #######################################################

                    #######################################################
                    try:
                        if self.DisplaySnapshotInGUI_state == 0:

                            self.CameraImage_ToBeDisplayedInPreviewScreens = self.ResizeImage(self.original_captured_image, self.TkinterPreviewImageScalingFactor)
                            self.GUI_label_PhotoImage = self.ConvertNumpyArrayToTkinterPhotoImage(self.CameraImage_ToBeDisplayedInPreviewScreens)

                            self.image_label.configure(image=self.GUI_label_PhotoImage)
                            
                    except:
                        exceptions = sys.exc_info()[0]
                        print("GUI_update_clock, DisplaySnapshotInGUI_state Exceptions: %s" % exceptions)
                        #traceback.print_exc()

                    #######################################################

                    #########################################################
                    try:
                        if self.SaveEachEncodedJPGImageFlag_NEEDS_TO_BE_CHANGED_FLAG_GUI == 1:

                            if self.SaveEachEncodedJPGImageFlag == 1:
                                self.SaveEachEncodedJPGImageButton["bg"] = self.TKinter_LightGreenColor
                                self.SaveEachEncodedJPGImageButton["text"] = "SaveEachEncodedJPGImage\nSaving"
                            else:
                                self.SaveEachEncodedJPGImageButton["bg"] = self.TKinter_LightRedColor
                                self.SaveEachEncodedJPGImageButton["text"] = "SaveEachEncodedJPGImage\nNot Saving"

                            self.SaveEachEncodedJPGImageFlag_NEEDS_TO_BE_CHANGED_FLAG_GUI = 0
                    except:
                        exceptions = sys.exc_info()[0]
                        print("ERROR changing the SaveEachEncodedJPGImageButton, Exceptions: %s" % exceptions)
                        #traceback.print_exc()

                    #########################################################

                    #########################################################
                    try:
                        if self.SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_NEEDS_TO_BE_CHANGED_FLAG_GUI == 1:

                            if self.SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_state == 1:
                                self.SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_Checkbutton_Value.set(1)
                            else:
                                self.SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_Checkbutton_Value.set(0)

                            self.SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_NEEDS_TO_BE_CHANGED_FLAG_GUI = 0
                    except:
                        exceptions = sys.exc_info()[0]
                        print("ERROR changing the SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_Checkbutton, Exceptions: %s" % exceptions)
                        #traceback.print_exc()

                    #########################################################

                    #######################################################

                    #######################################################
                    self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                    #######################################################

                except:
                    exceptions = sys.exc_info()[0]
                    print("CameraStreamerClass_ReubenPython2and3Class GUI_update_clock ERROR: Exceptions: %s" % exceptions)
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
    def SaveEachEncodedJPGImageButtonResponse(self):

        self.SaveEachEncodedJPGImage_ToggleState()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SaveEachEncodedJPGImage_ToggleState(self):

        self.SaveEachEncodedJPGImageFlag_NEEDS_TO_BE_CHANGED_FLAG = 1

        if self.SaveEachEncodedJPGImageFlag == 0:
            self.SaveEachEncodedJPGImageFlag_STATE_TO_BE_SET = 1
        else:
            self.SaveEachEncodedJPGImageFlag_STATE_TO_BE_SET = 0

        #self.MyPrint_WithoutLogFile("SaveEachEncodedJPGImageButtonResponse: SaveEachEncodedJPGImageFlag changed to " + str(self.SaveEachEncodedJPGImageFlag))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def image_jpg_encoding_quality_Slider_Response(self, event, name):
        self.image_jpg_encoding_quality_TO_BE_SET = self.image_jpg_encoding_quality_Slider_DoubleVar.get()

        self.image_jpg_encoding_quality_NeedsToBeChangedFlag = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CameraSetting_exposure_slider_Response(self, event, name):
        self.CameraSetting_exposure_TO_BE_SET = self.CameraSetting_exposure_slider_DoubleVar.get()

        self.CameraSetting_exposure_NeedsToBeChangedFlag = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CameraSetting_gain_slider_Response(self, event, name):
        self.CameraSetting_gain_TO_BE_SET = self.CameraSetting_gain_slider_DoubleVar.get()

        self.CameraSetting_gain_NeedsToBeChangedFlag = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CameraSetting_brightness_slider_Response(self, event, name):
        self.CameraSetting_brightness_TO_BE_SET = self.CameraSetting_brightness_slider_DoubleVar.get()

        self.CameraSetting_brightness_NeedsToBeChangedFlag = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CameraSetting_ManualFocus_slider_Response(self, event, name):
        self.CameraSetting_ManualFocus_TO_BE_SET = self.CameraSetting_ManualFocus_slider_DoubleVar.get()

        self.CameraSetting_ManualFocus_NeedsToBeChangedFlag = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CameraSetting_contrast_slider_Response(self, event, name):
        self.CameraSetting_contrast_TO_BE_SET = self.CameraSetting_contrast_slider_DoubleVar.get()

        self.CameraSetting_contrast_NeedsToBeChangedFlag = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CameraSetting_saturation_slider_Response(self, event, name):
        self.CameraSetting_saturation_TO_BE_SET = self.CameraSetting_saturation_slider_DoubleVar.get()

        self.CameraSetting_saturation_NeedsToBeChangedFlag = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CameraSetting_hue_slider_Response(self, event, name):
        self.CameraSetting_hue = self.CameraSetting_hue_slider_DoubleVar.get()

        self.CameraSetting_hue_NeedsToBeChangedFlag = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CameraSetting_Autofocus_CheckbuttonResponse(self, event, name):

        temp_value = self.CameraSetting_Autofocus_Checkbutton_Value.get()

        if temp_value == 0:
            self.CameraSetting_Autofocus_TO_BE_SET = 1  ########## This reversal is needed for the variable state to match the checked state, but we don't know why
        elif temp_value == 1:
            self.CameraSetting_Autofocus_TO_BE_SET = 0

        #self.MyPrint_WithoutLogFile("CameraSetting_Autofocus_TO_BE_SET changed to " + str(self.CameraSetting_Autofocus_TO_BE_SET))

        self.CameraSetting_Autofocus_NeedsToBeChangedFlag = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CameraSetting_Autoexposure_CheckbuttonResponse(self, event, name):

        temp_value = self.CameraSetting_Autoexposure_Checkbutton_Value.get()

        if temp_value == 0:
            self.CameraSetting_Autoexposure_TO_BE_SET = 1  ########## This reversal is needed for the variable state to match the checked state, but we don't know why
        elif temp_value == 1:
            self.CameraSetting_Autoexposure_TO_BE_SET = 0

        #self.MyPrint_WithoutLogFile("CameraSetting_Autoexposure_TO_BE_SET changed to " + str(self.CameraSetting_Autoexposure_TO_BE_SET))

        self.CameraSetting_Autoexposure_NeedsToBeChangedFlag = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DisplaySnapshotInGUI_CheckbuttonResponse(self, event, name):

        temp_value = self.DisplaySnapshotInGUI_Checkbutton_Value.get()

        if temp_value == 0:
            self.DisplaySnapshotInGUI_state = 1  ########## This reversal is needed for the variable state to match the checked state, but we don't know why
        elif temp_value == 1:
            self.DisplaySnapshotInGUI_state = 0

        #self.MyPrint_WithoutLogFile("DisplaySnapshotInGUI_CheckbuttonResponse, self.DisplaySnapshotInGUI_state: " + str(self.DisplaySnapshotInGUI_state))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def RemoveFisheyeDistortionFromImage_CheckbuttonResponse(self, event, name):

        temp_value = self.RemoveFisheyeDistortionFromImage_Checkbutton_Value.get()

        if temp_value == 0:
            self.RemoveFisheyeDistortionFromImage_Flag = 1  ########## This reversal is needed for the variable state to match the checked state, but we don't know why
        elif temp_value == 1:
            self.RemoveFisheyeDistortionFromImage_Flag = 0

        self.RemoveFisheyeDistortionFromImage_Flag_NeedsToBeChangedFlag = 1

        #self.MyPrint_WithoutLogFile("RemoveFisheyeDistortionFromImage_CheckbuttonResponse, self.RemoveFisheyeDistortionFromImage_Flag: " + str(self.RemoveFisheyeDistortionFromImage_Flag))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def image_label_ClickResponse(self, event, name):

        if self.DisplaySnapshotInGUI_state == 0:
            self.DisplaySnapshotInGUI_state = 1
            self.DisplaySnapshotInGUI_Checkbutton_Value.set(1)
        else:
            self.DisplaySnapshotInGUI_state = 0
            self.DisplaySnapshotInGUI_Checkbutton_Value.set(0)

        self.MyPrint_WithoutLogFile("image_label_ClickResponse, self.DisplaySnapshotInGUI_state: " + str(self.DisplaySnapshotInGUI_state))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_CheckbuttonResponse(self, event, name):

        temp_value = self.SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_Checkbutton_Value.get()

        if temp_value == 0:
            self.SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_state = 1  ########## This reversal is needed for the variable state to match the checked state, but we don't know why
        elif temp_value == 1:
            self.SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_state = 0

        self.MyPrint_WithoutLogFile("SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_CheckbuttonResponse, self.SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_state: " + str(self.SaveSingleSnapshotOrContinuousStreamEncodedJPGImage_state))
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

