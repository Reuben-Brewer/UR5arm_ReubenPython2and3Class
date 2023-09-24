# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision F, 09/24/2023

Verified working on: Python 3.8 for Windows 10 64-bit, Ubuntu 20.04, and Raspberry Pi Buster (no Mac testing yet).
'''

__author__ = 'reuben.brewer'

#########################################################
#https://github.com/Reuben-Brewer/CameraStreamerClass_ReubenPython2and3Class
from CameraStreamerClass_ReubenPython2and3Class import *

#https://github.com/Reuben-Brewer/LowPassFilter_ReubenPython2and3Class
from LowPassFilter_ReubenPython2and3Class import *

#https://github.com/Reuben-Brewer/LowPassFilterForDictsOfLists_ReubenPython2and3Class
from LowPassFilterForDictsOfLists_ReubenPython2and3Class import *
#########################################################

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
from scipy.spatial.transform import Rotation
from copy import * #for deepcopy(dict)
#########################################################

#########################################################
import cv2 #pip install opencv-contrib-python==4.5.5.64
import numpy
print("OpenCV version: " + str(cv2.__version__))
#########################################################

#########################################################
from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
#########################################################

#########################################################
import queue as Queue
#########################################################

#########################################################
from future.builtins import input as input
######################################################### "sudo pip3 install future" (Python 3) AND "sudo pip install future" (Python 2)

#########################################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
#########################################################

class ArucoTagDetectionFromCameraFeed_ReubenPython3Class(Frame): #Subclass the Tkinter Frame

    #######################################################################################################################
    #######################################################################################################################
    def __init__(self, setup_dict): #Subclass the Tkinter Frame

        print("#################### ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__ starting. ####################")

        #########################################################
        #########################################################
        self.setup_dict = setup_dict

        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
        self.MainThread_StillRunningFlag = 0
        self.OpenCVdisplayThread_StillRunningFlag = 0
        self.ImageSavingThread_StillRunningFlag = 0
        self.CAMERA_OPEN_FLAG = 0

        self.CurrentTime_CalculatedFromMainThread = -11111.0
        self.LastTime_CalculatedFromMainThread = -11111.0
        self.StartingTime_CalculatedFromMainThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromMainThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromMainThread = -11111.0

        self.CurrentTime_CalculatedFromOpenCVdisplayThread = -11111.0
        self.LastTime_CalculatedFromOpenCVdisplayThread = -11111.0
        self.StartingTime_CalculatedFromOpenCVdisplayThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromOpenCVdisplayThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromOpenCVdisplayThread = -11111.0

        self.CAMERA_MostRecentDict_Time = -11111.0
        self.CAMERA_MostRecentDict_Time_LAST = -11111.0

        self.AcceptNewImagesForSavingFlag = 0
        self.SaveImageFlag = 0
        self.SaveImageFlag_NeedsToBeChangedFlag = 0
        self.SaveSingleSnapshotOrContinuousStreamOfImages_state = 0
        self.SavedImageFrameCounter = 0

        #https://docs.opencv.org/3.4/d9/d6a/group__aruco.html

        self.ArucoTag_DictType_AcceptableEnglishStringValuesDictOfDicts = dict([("DICT_4X4_50", dict([("cv2intValue", cv2.aruco.DICT_4X4_50), ("MaxIDvalue", 50 - 1), ("MinHammingDistanceBetweenCodes", 4)])),
                                                                         ("DICT_4X4_100", dict([("cv2intValue", cv2.aruco.DICT_4X4_100), ("MaxIDvalue", 100 - 1), ("MinHammingDistanceBetweenCodes", 3)])),
                                                                         ("DICT_4X4_250", dict([("cv2intValue", cv2.aruco.DICT_4X4_250), ("MaxIDvalue", 250 - 1), ("MinHammingDistanceBetweenCodes", 4)])),
                                                                         ("DICT_4X4_1000", dict([("cv2intValue", cv2.aruco.DICT_4X4_1000), ("MaxIDvalue", 1000 - 1), ("MinHammingDistanceBetweenCodes", 5)])),
                                                                         ("DICT_5X5_50", dict([("cv2intValue", cv2.aruco.DICT_5X5_50), ("MaxIDvalue", 50 - 1), ("MinHammingDistanceBetweenCodes", 8)])),
                                                                         ("DICT_5X5_100", dict([("cv2intValue", cv2.aruco.DICT_5X5_100), ("MaxIDvalue", 100 - 1), ("MinHammingDistanceBetweenCodes", 7)])),
                                                                         ("DICT_5X5_250", dict([("cv2intValue", cv2.aruco.DICT_5X5_250), ("MaxIDvalue", 250 - 1), ("MinHammingDistanceBetweenCodes", 6)])),
                                                                         ("DICT_5X5_1000", dict([("cv2intValue", cv2.aruco.DICT_5X5_1000), ("MaxIDvalue", 1000 - 1), ("MinHammingDistanceBetweenCodes", 5)])),
                                                                         ("DICT_6X6_50", dict([("cv2intValue", cv2.aruco.DICT_6X6_50), ("MaxIDvalue", 50 - 1), ("MinHammingDistanceBetweenCodes", 13)])),
                                                                         ("DICT_6X6_100", dict([("cv2intValue", cv2.aruco.DICT_6X6_100), ("MaxIDvalue", 100 - 1), ("MinHammingDistanceBetweenCodes", 12)])),
                                                                         ("DICT_6X6_250", dict([("cv2intValue", cv2.aruco.DICT_6X6_250), ("MaxIDvalue", 250 - 1), ("MinHammingDistanceBetweenCodes", 11)])),
                                                                         ("DICT_6X6_1000", dict([("cv2intValue", cv2.aruco.DICT_6X6_1000), ("MaxIDvalue", 1000 - 1), ("MinHammingDistanceBetweenCodes", 9)])),
                                                                         ("DICT_7X7_50", dict([("cv2intValue", cv2.aruco.DICT_7X7_50), ("MaxIDvalue", 50 - 1), ("MinHammingDistanceBetweenCodes", 19)])),
                                                                         ("DICT_7X7_100", dict([("cv2intValue", cv2.aruco.DICT_7X7_100), ("MaxIDvalue", 100 - 1), ("MinHammingDistanceBetweenCodes", 18)])),
                                                                         ("DICT_7X7_250", dict([("cv2intValue", cv2.aruco.DICT_7X7_250), ("MaxIDvalue", 250 - 1), ("MinHammingDistanceBetweenCodes", 17)])),
                                                                         ("DICT_7X7_1000", dict([("cv2intValue", cv2.aruco.DICT_7X7_1000), ("MaxIDvalue", 1000 - 1), ("MinHammingDistanceBetweenCodes", 14)])),
                                                                         ("DICT_ARUCO_ORIGINAL", dict([("cv2intValue", cv2.aruco.DICT_ARUCO_ORIGINAL), ("MaxIDvalue", 1024 - 1), ("MinHammingDistanceBetweenCodes", 3)])),
                                                                         ("DICT_APRILTAG_16h5", dict([("cv2intValue", cv2.aruco.DICT_APRILTAG_16h5), ("MaxIDvalue", 30 - 1), ("MinHammingDistanceBetweenCodes", 5)])),
                                                                         ("DICT_APRILTAG_16H5", dict([("cv2intValue", cv2.aruco.DICT_APRILTAG_16H5), ("MaxIDvalue", 30 - 1), ("MinHammingDistanceBetweenCodes", 5)])),
                                                                         ("DICT_APRILTAG_25h9", dict([("cv2intValue", cv2.aruco.DICT_APRILTAG_25h9), ("MaxIDvalue", 35 - 1), ("MinHammingDistanceBetweenCodes", 9)])),
                                                                         ("DICT_APRILTAG_25H9", dict([("cv2intValue", cv2.aruco.DICT_APRILTAG_25H9), ("MaxIDvalue", 35 - 1), ("MinHammingDistanceBetweenCodes", 9)])),
                                                                         ("DICT_APRILTAG_36h10", dict([("cv2intValue", cv2.aruco.DICT_APRILTAG_36h10), ("MaxIDvalue", 2320 - 1), ("MinHammingDistanceBetweenCodes", 10)])),
                                                                         ("DICT_APRILTAG_36H10", dict([("cv2intValue", cv2.aruco.DICT_APRILTAG_36H10), ("MaxIDvalue", 2320 - 1), ("MinHammingDistanceBetweenCodes", 10)])),
                                                                         ("DICT_APRILTAG_36h11", dict([("cv2intValue", cv2.aruco.DICT_APRILTAG_36h11), ("MaxIDvalue", 587 - 1), ("MinHammingDistanceBetweenCodes", 11)])),
                                                                         ("DICT_APRILTAG_36H11", dict([("cv2intValue", cv2.aruco.DICT_APRILTAG_36H11), ("MaxIDvalue", 587 - 1), ("MinHammingDistanceBetweenCodes", 11)]))])

        self.ArucoTag_TranslationVectorOfMarkerCenter_PythonList = list()
        self.ArucoTag_RotationVectorOfMarkerCenter_PythonList = list()

        self.MostRecentDataDict = dict()
        self.MostRecentDataDict_LAST = dict()
        self.MostRecentDataDict_BlockFromBeingReadFlag = 0

        self.DetectedArucoTag_InfoDict = dict()
        self.DetectedArucoTag_LowPassFiltersOnlyDict = dict()

        self.ImagesToBeSaveQueue = Queue.Queue()
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

        print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: The OS platform is: " + self.my_platform)
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

            print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "root" in self.GUIparametersDict:
                self.root = self.GUIparametersDict["root"]
            else:
                print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: ERROR, must pass in 'root'")
                return
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "EnableInternal_MyPrint_Flag" in self.GUIparametersDict:
                self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", self.GUIparametersDict["EnableInternal_MyPrint_Flag"])
            else:
                self.EnableInternal_MyPrint_Flag = 0

            print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "PrintToConsoleFlag" in self.GUIparametersDict:
                self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", self.GUIparametersDict["PrintToConsoleFlag"])
            else:
                self.PrintToConsoleFlag = 1

            print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "NumberOfPrintLines" in self.GUIparametersDict:
                self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", self.GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
            else:
                self.NumberOfPrintLines = 10

            print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: NumberOfPrintLines: " + str(self.NumberOfPrintLines))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "UseBorderAroundThisGuiObjectFlag" in self.GUIparametersDict:
                self.UseBorderAroundThisGuiObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseBorderAroundThisGuiObjectFlag", self.GUIparametersDict["UseBorderAroundThisGuiObjectFlag"])
            else:
                self.UseBorderAroundThisGuiObjectFlag = 0

            print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: UseBorderAroundThisGuiObjectFlag: " + str(self.UseBorderAroundThisGuiObjectFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_ROW" in self.GUIparametersDict:
                self.GUI_ROW = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROW", self.GUIparametersDict["GUI_ROW"], 0.0, 1000.0))
            else:
                self.GUI_ROW = 0

            print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: GUI_ROW: " + str(self.GUI_ROW))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMN" in self.GUIparametersDict:
                self.GUI_COLUMN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMN", self.GUIparametersDict["GUI_COLUMN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMN = 0

            print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: GUI_COLUMN: " + str(self.GUI_COLUMN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADX" in self.GUIparametersDict:
                self.GUI_PADX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADX", self.GUIparametersDict["GUI_PADX"], 0.0, 1000.0))
            else:
                self.GUI_PADX = 0

            print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: GUI_PADX: " + str(self.GUI_PADX))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADY" in self.GUIparametersDict:
                self.GUI_PADY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADY", self.GUIparametersDict["GUI_PADY"], 0.0, 1000.0))
            else:
                self.GUI_PADY = 0

            print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: GUI_PADY: " + str(self.GUI_PADY))
            #########################################################
            #########################################################

            ##########################################
            if "GUI_ROWSPAN" in self.GUIparametersDict:
                self.GUI_ROWSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROWSPAN", self.GUIparametersDict["GUI_ROWSPAN"], 1.0, 1000.0))
            else:
                self.GUI_ROWSPAN = 1

            print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: GUI_ROWSPAN: " + str(self.GUI_ROWSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMNSPAN" in self.GUIparametersDict:
                self.GUI_COLUMNSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMNSPAN", self.GUIparametersDict["GUI_COLUMNSPAN"], 1.0, 1000.0))
            else:
                self.GUI_COLUMNSPAN = 1

            print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: GUI_COLUMNSPAN: " + str(self.GUI_COLUMNSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_STICKY" in self.GUIparametersDict:
                self.GUI_STICKY = str(self.GUIparametersDict["GUI_STICKY"])
            else:
                self.GUI_STICKY = "w"

            print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: GUI_STICKY: " + str(self.GUI_STICKY))
            #########################################################
            #########################################################

        else:
            self.GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: No GUIparametersDict present, setting USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))

        #print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: GUIparametersDict: " + str(self.GUIparametersDict))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "NameToDisplay_UserSet" in self.setup_dict:
            self.NameToDisplay_UserSet = str(self.setup_dict["NameToDisplay_UserSet"])
        else:
            self.NameToDisplay_UserSet = str(self.getPreciseSecondsTimeStampString())

        print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: NameToDisplay_UserSet: " + str(self.NameToDisplay_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "MainThread_TimeToSleepEachLoop" in self.setup_dict:
            self.MainThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("MainThread_TimeToSleepEachLoop", self.setup_dict["MainThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.MainThread_TimeToSleepEachLoop = 0.005

        print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: MainThread_TimeToSleepEachLoop: " + str(self.MainThread_TimeToSleepEachLoop))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "ArucoTag_DictType_EnglishString" in self.setup_dict:
            ArucoTag_DictType_EnglishString_TEMP = self.setup_dict["ArucoTag_DictType_EnglishString"]
            
            if ArucoTag_DictType_EnglishString_TEMP in self.ArucoTag_DictType_AcceptableEnglishStringValuesDictOfDicts:

                self.ArucoTag_DictType_EnglishString = ArucoTag_DictType_EnglishString_TEMP
                self.ArucoTag_DictType_cv2Int = self.ArucoTag_DictType_AcceptableEnglishStringValuesDictOfDicts[self.ArucoTag_DictType_EnglishString]["cv2intValue"]

        else:
            self.ArucoTag_DictType_EnglishString = "DICT_4X4_50"
            self.ArucoTag_DictType_cv2Int = cv2.aruco.DICT_4X4_50

        print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: ArucoTag_DictType_EnglishString: " + str(self.ArucoTag_DictType_EnglishString))
        print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: ArucoTag_DictType_cv2Int: " + str(self.ArucoTag_DictType_cv2Int))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "ArucoTag_MarkerLengthInMillimeters" in self.setup_dict:
            self.ArucoTag_MarkerLengthInMillimeters = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("ArucoTag_MarkerLengthInMillimeters", self.setup_dict["ArucoTag_MarkerLengthInMillimeters"], 0.001, 100000.0)

        else:
            self.ArucoTag_MarkerLengthInMillimeters = 25.0

        print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: ArucoTag_MarkerLengthInMillimeters: " + str(self.ArucoTag_MarkerLengthInMillimeters))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "ArucoTag_AxesToDrawLengthInMillimeters" in self.setup_dict:
            self.ArucoTag_AxesToDrawLengthInMillimeters = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("ArucoTag_AxesToDrawLengthInMillimeters", self.setup_dict["ArucoTag_AxesToDrawLengthInMillimeters"], 0.001, 100000.0)

        else:
            self.ArucoTag_AxesToDrawLengthInMillimeters = 5.0

        print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: ArucoTag_AxesToDrawLengthInMillimeters: " + str(self.ArucoTag_AxesToDrawLengthInMillimeters))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "ArucoTag_TranslationVectorOfMarkerCenter_ExponentialSmoothingFilterLambda" in self.setup_dict:
            self.ArucoTag_TranslationVectorOfMarkerCenter_ExponentialSmoothingFilterLambda = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("ArucoTag_TranslationVectorOfMarkerCenter_ExponentialSmoothingFilterLambda", self.setup_dict["ArucoTag_TranslationVectorOfMarkerCenter_ExponentialSmoothingFilterLambda"], 0.0, 1.0)

        else:
            self.ArucoTag_TranslationVectorOfMarkerCenter_ExponentialSmoothingFilterLambda = 0.1 #new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value

        print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: ArucoTag_TranslationVectorOfMarkerCenter_ExponentialSmoothingFilterLambda: " + str(self.ArucoTag_TranslationVectorOfMarkerCenter_ExponentialSmoothingFilterLambda))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "ArucoTag_RotationVectorOfMarkerCenter_ExponentialSmoothingFilterLambda" in self.setup_dict:
            self.ArucoTag_RotationVectorOfMarkerCenter_ExponentialSmoothingFilterLambda = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("ArucoTag_RotationVectorOfMarkerCenter_ExponentialSmoothingFilterLambda", self.setup_dict["ArucoTag_RotationVectorOfMarkerCenter_ExponentialSmoothingFilterLambda"], 0.0, 1.0)

        else:
            self.ArucoTag_RotationVectorOfMarkerCenter_ExponentialSmoothingFilterLambda = 0.1 #new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value

        print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: ArucoTag_RotationVectorOfMarkerCenter_ExponentialSmoothingFilterLambda: " + str(self.ArucoTag_RotationVectorOfMarkerCenter_ExponentialSmoothingFilterLambda))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "ArucoTag_DetectInvertedMarkersAsWellAsNormalOnesFlag" in self.setup_dict:
            self.ArucoTag_DetectInvertedMarkersAsWellAsNormalOnesFlag = self.PassThrough0and1values_ExitProgramOtherwise("ArucoTag_DetectInvertedMarkersAsWellAsNormalOnesFlag", self.setup_dict["ArucoTag_DetectInvertedMarkersAsWellAsNormalOnesFlag"])
        else:
            self.ArucoTag_DetectInvertedMarkersAsWellAsNormalOnesFlag = 1

        print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: ArucoTag_DetectInvertedMarkersAsWellAsNormalOnesFlag: " + str(self.ArucoTag_DetectInvertedMarkersAsWellAsNormalOnesFlag))
        #########################################################
        #########################################################


        #########################################################
        #########################################################
        if "OpenCVwindow_UpdateEveryNmilliseconds" in self.setup_dict:
            self.OpenCVwindow_UpdateEveryNmilliseconds = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("OpenCVwindow_UpdateEveryNmilliseconds", self.setup_dict["OpenCVwindow_UpdateEveryNmilliseconds"], 30, 1000))

        else:
            self.OpenCVwindow_UpdateEveryNmilliseconds = 30

        print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: OpenCVwindow_UpdateEveryNmilliseconds: " + str(self.OpenCVwindow_UpdateEveryNmilliseconds))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "ShowOpenCVwindowsFlag" in self.setup_dict:
            self.ShowOpenCVwindowsFlag = self.PassThrough0and1values_ExitProgramOtherwise("ShowOpenCVwindowsFlag", self.setup_dict["ShowOpenCVwindowsFlag"])

        else:
            self.ShowOpenCVwindowsFlag = 0

        print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: ShowOpenCVwindowsFlag: " + str(self.ShowOpenCVwindowsFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "OpenCVwindowPosX" in self.setup_dict:
            self.OpenCVwindowPosX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("OpenCVwindowPosX", self.setup_dict["OpenCVwindowPosX"], 0.0, 1920.0))
        else:
            self.OpenCVwindowPosX = 0

        print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: OpenCVwindowPosX: " + str(self.OpenCVwindowPosX))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "OpenCVwindowPosY" in self.setup_dict:
            self.OpenCVwindowPosY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("OpenCVwindowPosY", self.setup_dict["OpenCVwindowPosY"], 0.0, 1080.0))
        else:
            self.OpenCVwindowPosY = 0

        print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: OpenCVwindowPosY: " + str(self.OpenCVwindowPosY))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "TkinterPreviewImageScalingFactor" in self.setup_dict:
            self.TkinterPreviewImageScalingFactor = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("TkinterPreviewImageScalingFactor", self.setup_dict["TkinterPreviewImageScalingFactor"], 0.1, 10.0)
        else:
            self.TkinterPreviewImageScalingFactor = 1.0

        print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: TkinterPreviewImageScalingFactor: " + str(self.TkinterPreviewImageScalingFactor))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "ArucoTag_SavedImages_LocalDirectoryNameNoSlashes" in self.setup_dict:
            self.ArucoTag_SavedImages_LocalDirectoryNameNoSlashes = self.setup_dict["ArucoTag_SavedImages_LocalDirectoryNameNoSlashes"]
        else:
            self.ArucoTag_SavedImages_LocalDirectoryNameNoSlashes = "ArucoTag_SavedImages"

        print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: ArucoTag_SavedImages_LocalDirectoryNameNoSlashes: " + str(self.ArucoTag_SavedImages_LocalDirectoryNameNoSlashes))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "ArucoTag_SavedImages_FilenamePrefix" in self.setup_dict:
            self.ArucoTag_SavedImages_FilenamePrefix = self.setup_dict["ArucoTag_SavedImages_FilenamePrefix"]
        else:
            self.ArucoTag_SavedImages_FilenamePrefix = "ArucoTag_"

        print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: ArucoTag_SavedImages_FilenamePrefix: " + str(self.ArucoTag_SavedImages_FilenamePrefix))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.image_width = self.setup_dict["CameraStreamerClass_ReubenPython2and3ClassObject_setup_dict"]["image_width"]
        self.image_height = self.setup_dict["CameraStreamerClass_ReubenPython2and3ClassObject_setup_dict"]["image_height"]

        self.camera_selection_number = self.setup_dict["CameraStreamerClass_ReubenPython2and3ClassObject_setup_dict"]["camera_selection_number"]
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.PrintToGui_Label_TextInputHistory_List = [" "] * self.NumberOfPrintLines
        self.PrintToGui_Label_TextInput_Str = ""
        self.GUI_ready_to_be_updated_flag = 0
        #########################################################
        #########################################################

        ######################################################### START THE GUI HERE SO THAT WE CAN CREATE self.CameraFrame to feed to the camera object!
        #########################################################
        if self.USE_GUI_FLAG == 1:
            self.StartGUI(self.root)
            time.sleep(0.25)
        else:
            self.CameraFrame = None
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:
            self.DataStreamingFrequency_CalculatedFromMainThread_LowPassFilter_ReubenPython2and3ClassObject = LowPassFilter_ReubenPython2and3Class(dict([("UseMedianFilterFlag", 1),
                                                                                                            ("UseExponentialSmoothingFilterFlag", 1),
                                                                                                            ("ExponentialSmoothingFilterLambda", 0.05)])) ##new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value

        except:
            exceptions = sys.exc_info()[0]
            print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: DataStreamingFrequency_CalculatedFromMainThread_LowPassFilter_ReubenPython2and3ClassObject, Exceptions: %s" % exceptions)
            traceback.print_exc()
            return
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:
            self.CameraStreamerClass_ReubenPython2and3ClassObject_GUIparametersDict = dict([("USE_GUI_FLAG", self.USE_GUI_FLAG),
                                                     ("root", self.CameraFrame),
                                                     ("EnableInternal_MyPrint_Flag", 1),
                                                     ("NumberOfPrintLines", 10),
                                                     ("UseBorderAroundThisGuiObjectFlag", 0),
                                                     ("GUI_ROW", 0),
                                                     ("GUI_COLUMN", 0),
                                                     ("GUI_PADX", 10),
                                                     ("GUI_PADY", 10),
                                                     ("GUI_ROWSPAN", 1),
                                                     ("GUI_COLUMNSPAN", 1)])

            self.setup_dict["CameraStreamerClass_ReubenPython2and3ClassObject_setup_dict"]["GUIparametersDict"] = self.CameraStreamerClass_ReubenPython2and3ClassObject_GUIparametersDict

            self.CameraStreamerClass_ReubenPython2and3ClassObject = CameraStreamerClass_ReubenPython2and3Class(self.setup_dict["CameraStreamerClass_ReubenPython2and3ClassObject_setup_dict"])
            self.CAMERA_OPEN_FLAG = self.CameraStreamerClass_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("CameraStreamerClass_ReubenPython2and3ClassObject __init__: Exceptions: %s" % exceptions, 0)
            traceback.print_exc()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if self.CAMERA_OPEN_FLAG == 1:

            ##########################################
            self.CameraImage_Color_Adjusted = numpy.zeros((self.image_height, self.image_width, 3), numpy.uint8)

            self.CameraImage_ConvertedToGray = numpy.zeros((self.image_height, self.image_width, 1), numpy.uint8)

            self.CameraImage_Color_ArucoDetected = numpy.zeros((self.image_height, self.image_width, 3), numpy.uint8)
            self.CameraImage_Gray_ArucoDetected = numpy.zeros((self.image_height, self.image_width, 1), numpy.uint8)

            self.CameraImage_ToBeDisplayedInPreviewScreens = numpy.zeros((self.image_height, self.image_width, 1), numpy.uint8) #May end up being either gray or color
            ##########################################

            ##########################################
            self.StartingTime_AllThreads = self.getPreciseSecondsTimeStampString()
            ##########################################
            
            ##########################################
            self.MainThread_ThreadingObject = threading.Thread(target=self.MainThread, args=())
            self.MainThread_ThreadingObject.start()
            ##########################################

            ##########################################
            self.ImageSavingThread_ThreadingObject = threading.Thread(target=self.ImageSavingThread, args=())
            self.ImageSavingThread_ThreadingObject.start()
            ##########################################

            ##########################################
            if self.ShowOpenCVwindowsFlag == 1:
                self.OpenCVdisplayThread_ThreadingObject = threading.Thread(target=self.OpenCVdisplayThread, args=())
                self.OpenCVdisplayThread_ThreadingObject.start()
            ##########################################

            ##########################################
            time.sleep(0.25)
            ##########################################

            ##########################################
            self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1
            ##########################################

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
            if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1.0:
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
    def CreateNewDirectoryIfItDoesntExist(self, directory):
        try:
            #print("CreateNewDirectoryIfItDoesntExist, directory: " + directory)
            if os.path.isdir(directory) == 0: #No directory with this name exists
                os.makedirs(directory)
        except:
            exceptions = sys.exc_info()[0]
            print("CreateNewDirectoryIfItDoesntExist, Exceptions: %s" % exceptions)
            traceback.print_exc()
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
    def getPreciseSecondsTimeStampString_MillisecondsInteger(self):
        ts_milliseconds = int(decimal.Decimal(1000.0 * time.time()))

        return ts_milliseconds

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentDataDict(self):

        if self.EXIT_PROGRAM_FLAG == 0:

            if self.MostRecentDataDict_BlockFromBeingReadFlag == 0:
                return deepcopy(self.MostRecentDataDict) #deepcopy IS required as MostRecentDataDict contains lists.
            else:
                return deepcopy(self.MostRecentDataDict_LAST) #deepcopy IS required as MostRecentDataDict contains lists.

        else:
            return dict()  # So that we're not returning variables during the close-down process.
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_MainThread_Filtered(self):

        try:
            self.DataStreamingDeltaT_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread - self.LastTime_CalculatedFromMainThread

            if self.DataStreamingDeltaT_CalculatedFromMainThread != 0.0:
                DataStreamingFrequency_CalculatedFromMainThread_TEMP = 1.0/self.DataStreamingDeltaT_CalculatedFromMainThread
                self.DataStreamingFrequency_CalculatedFromMainThread = self.DataStreamingFrequency_CalculatedFromMainThread_LowPassFilter_ReubenPython2and3ClassObject.AddDataPointFromExternalProgram(DataStreamingFrequency_CalculatedFromMainThread_TEMP)["SignalOutSmoothed"]

            self.LastTime_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_MainThread_Filtered, Exceptions: %s" % exceptions)
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
    def CreateAndSaveImageOfArucoTagMarker(self, ID_integer, ArucoTag_DictType_EnglishString = "", EdgeLengthInPixels_integer = 100, WhiteBorderPixelWidth_integer = -1, BlackOutermostBorderPixelWidth_integer = -1):

        try:

            ##########################################################################################################
            ArucoTag_DictType_EnglishString = str(ArucoTag_DictType_EnglishString)
            ID_integer = int(ID_integer)
            EdgeLengthInPixels_integer = int(EdgeLengthInPixels_integer)
            WhiteBorderPixelWidth_integer = int(WhiteBorderPixelWidth_integer)
            BlackOutermostBorderPixelWidth_integer = int(BlackOutermostBorderPixelWidth_integer)

            if WhiteBorderPixelWidth_integer == -1:
                WhiteBorderPixelWidth_integer = round(EdgeLengthInPixels_integer/6.0)

            if BlackOutermostBorderPixelWidth_integer < 0:
                BlackOutermostBorderPixelWidth_integer = 0
            ##########################################################################################################

            ##########################################################################################################
            if ArucoTag_DictType_EnglishString == "":
                ArucoTag_DictType_EnglishString = self.ArucoTag_DictType_EnglishString
            ##########################################################################################################

            ##########################################################################################################
            if ArucoTag_DictType_EnglishString not in self.ArucoTag_DictType_AcceptableEnglishStringValuesDictOfDicts:
                print("CreateAndSaveImageOfArucoTagMarker: Error, ArucoTag_DictType_EnglishString = '" + str(ArucoTag_DictType_EnglishString) + "' must be within dict " + str(self.ArucoTag_DictType_AcceptableEnglishStringValuesDictOfDicts))
                return
            ##########################################################################################################

            ##########################################################################################################
            MaxIDvalue = self.ArucoTag_DictType_AcceptableEnglishStringValuesDictOfDicts[ArucoTag_DictType_EnglishString]["MaxIDvalue"]
            if ID_integer < 0 or ID_integer > MaxIDvalue:
                print("CreateAndSaveImageOfArucoTagMarker: Error, ID_integer must be in range [0, " + str(MaxIDvalue) + "].")
                return
            ##########################################################################################################

            ##########################################################################################################
            TagImageToBeSaved_NoBorder = numpy.zeros((EdgeLengthInPixels_integer, EdgeLengthInPixels_integer, 1), dtype="uint8")

            Width_TagImageToBeSaved_WithBorder = EdgeLengthInPixels_integer + 2*WhiteBorderPixelWidth_integer + 2*BlackOutermostBorderPixelWidth_integer
            Height_TagImageToBeSaved_WithBorder = EdgeLengthInPixels_integer + 2*WhiteBorderPixelWidth_integer + 2*BlackOutermostBorderPixelWidth_integer
            TagImageToBeSaved_WithBorder = 255*numpy.ones((Height_TagImageToBeSaved_WithBorder, Width_TagImageToBeSaved_WithBorder, 1), dtype="uint8")

            cv2.aruco.drawMarker(cv2.aruco.Dictionary_get(self.ArucoTag_DictType_AcceptableEnglishStringValuesDictOfDicts[ArucoTag_DictType_EnglishString]["cv2intValue"]),
                                 id=ID_integer,
                                 sidePixels=EdgeLengthInPixels_integer,
                                 img=TagImageToBeSaved_NoBorder,
                                 borderBits=1) #When boderBits isn't 1, it saves an all-black image

            TagImageToBeSaved_WithBorder[WhiteBorderPixelWidth_integer+BlackOutermostBorderPixelWidth_integer:EdgeLengthInPixels_integer+WhiteBorderPixelWidth_integer+BlackOutermostBorderPixelWidth_integer, WhiteBorderPixelWidth_integer+BlackOutermostBorderPixelWidth_integer:EdgeLengthInPixels_integer+WhiteBorderPixelWidth_integer+BlackOutermostBorderPixelWidth_integer] = TagImageToBeSaved_NoBorder

            if BlackOutermostBorderPixelWidth_integer != 0:
                TagImageToBeSaved_WithBorder[0:Height_TagImageToBeSaved_WithBorder, 0] = 0
                TagImageToBeSaved_WithBorder[0:Height_TagImageToBeSaved_WithBorder, Width_TagImageToBeSaved_WithBorder - 1] = 0
                TagImageToBeSaved_WithBorder[0, 0:Width_TagImageToBeSaved_WithBorder] = 0
                TagImageToBeSaved_WithBorder[Height_TagImageToBeSaved_WithBorder - 1, 0:Width_TagImageToBeSaved_WithBorder] = 0

            cv2.imwrite("ArucoTag_Type_" + self.ArucoTag_DictType_EnglishString + "_ID_" + str(ID_integer) + ".png", TagImageToBeSaved_WithBorder)
            ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("CreateAndSaveImageOfArucoTagMarker, Exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## unicorn
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def MainThread(self):

        self.MyPrint_WithoutLogFile("Started MainThread for ArucoTagDetectionFromCameraFeed_ReubenPython3Class object.")
        self.MainThread_StillRunningFlag = 1

        #########################################################
        self.cv2ArucoDetectionParameters = cv2.aruco.DetectorParameters_create()
        self.cv2ArucoDetectionParameters.aprilTagDeglitch = 1
        self.cv2ArucoDetectionParameters.detectInvertedMarker = int(self.ArucoTag_DetectInvertedMarkersAsWellAsNormalOnesFlag)

        #enable the new and faster Aruco detection strategy.
        #Proposed in the paper: Romero-Ramirez et al: Speeded up detection of squared fiducial markers (2018) https://www.researchgate.net/publication/325787310_Speeded_Up_Detection_of_Squared_Fiducial_Markers
        #self.cv2ArucoDetectionParameters.useAruco3Detection = 1

        self.cv2ArucoDetectionParameters.adaptiveThreshConstant = 7 #default of 7

        self.cv2ArucoDetectionParameters.aprilTagMinWhiteBlackDiff = 5 #default of 5

        self.cv2ArucoDetectionParameters.aprilTagQuadSigma = 0.0 #default is 0
        #print("blur: " + str(self.cv2ArucoDetectionParameters.aprilTagQuadSigma))# = #what Gaussian blur should be applied to the segmented image (used for quad detection?)
        #########################################################

        self.StartingTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            self.CurrentTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_AllThreads
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
            ##########################################################################################################
            ##########################################################################################################
            if self.CAMERA_OPEN_FLAG == 1:

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                try:

                    ##########################################################################################################
                    ##########################################################################################################
                    ##########################################################################################################
                    ##########################################################################################################
                    self.CAMERA_MostRecentDict = self.CameraStreamerClass_ReubenPython2and3ClassObject.GetMostRecentDataDict()
                    ##########################################################################################################
                    ##########################################################################################################
                    ##########################################################################################################
                    ##########################################################################################################

                    ##########################################################################################################
                    ##########################################################################################################
                    ##########################################################################################################
                    ##########################################################################################################
                    if "Time" in self.CAMERA_MostRecentDict:

                        ##########################################################################################################
                        ##########################################################################################################
                        ##########################################################################################################
                        self.CAMERA_MostRecentDict_OriginalImage = self.CAMERA_MostRecentDict["OriginalImage"]
                        #print("self.CAMERA_MostRecentDict_OriginalImage shape = " + str(numpy.shape(self.CAMERA_MostRecentDict_OriginalImage)))

                        self.CAMERA_MostRecentDict_Time = self.CAMERA_MostRecentDict["Time"]
                        self.CAMERA_MostRecentDict_CameraCalibration_Kmatrix_CameraIntrinsicsMatrix = self.CAMERA_MostRecentDict["CameraCalibration_Kmatrix_CameraIntrinsicsMatrix"]
                        self.CAMERA_MostRecentDict_CameraCalibration_Darray_DistortionCoefficients = self.CAMERA_MostRecentDict["CameraCalibration_Darray_DistortionCoefficients"]
                        ##########################################################################################################
                        ##########################################################################################################
                        ##########################################################################################################

                        ##########################################################################################################
                        ##########################################################################################################
                        ##########################################################################################################
                        if self.CAMERA_MostRecentDict_Time != self.CAMERA_MostRecentDict_Time_LAST: #New data

                            ##########################################################################################################
                            ##########################################################################################################
                            self.CAMERA_MostRecentDict_Time_LAST = self.CAMERA_MostRecentDict_Time
                            ##########################################################################################################
                            ##########################################################################################################

                            ##########################################################################################################
                            ##########################################################################################################
                            #self.CameraImage_ConvertedToGray = cv2.cvtColor(self.CAMERA_MostRecentDict_OriginalImage.copy(), cv2.COLOR_BGR2GRAY)
                            ##########################################################################################################
                            ##########################################################################################################

                            ##########################################################################################################
                            ##########################################################################################################
                            '''
                            #To perform Histogram Equalization on a color image, do it on each color channel independently and then add the results.
                            B, G, R = cv2.split(self.CAMERA_MostRecentDict_OriginalImage.copy())
                            B = cv2.equalizeHist(B)
                            G = cv2.equalizeHist(G)
                            R = cv2.equalizeHist(R)
                            out = cv2.merge((B,G,R))
                            '''

                            #cv2.equalizeHist(self.CameraImage_ConvertedToGray, self.CameraImage_ConvertedToGray)
                            ##########################################################################################################
                            ##########################################################################################################

                            ##########################################################################################################
                            ##########################################################################################################
                            #https://stackoverflow.com/questions/39308030/how-do-i-increase-the-contrast-of-an-image-in-python-opencv
                            #https://docs.opencv.org/4.x/d3/dc1/tutorial_basic_linear_transform.html
                            alpha = 1.0  # Contrast control (1.0-3.0)
                            beta = 0  # Brightness control (0-100)

                            #self.CameraImage_ConvertedToGray = cv2.convertScaleAbs(self.CameraImage_ConvertedToGray, alpha=alpha, beta=beta)
                            self.CameraImage_Color_Adjusted = cv2.convertScaleAbs(self.CAMERA_MostRecentDict_OriginalImage, alpha=alpha, beta=beta)
                            ##########################################################################################################
                            ##########################################################################################################

                            ##########################################################################################################
                            ##########################################################################################################
                            #The actual DETECTION takes place here. Can run on either gray or color images, but the detector will automatically convert color to gray.
                            self.DetectedArucoTags_CornersList_ImageCoordinates, self.DetectedArucoTags_IDsList, self.DetectedArucoTags_RejectedImagePoints = cv2.aruco.detectMarkers(self.CameraImage_Color_Adjusted,
                                                                                        cv2.aruco.Dictionary_get(self.ArucoTag_DictType_cv2Int),
                                                                                        parameters=self.cv2ArucoDetectionParameters,
                                                                                        cameraMatrix=self.CAMERA_MostRecentDict_CameraCalibration_Kmatrix_CameraIntrinsicsMatrix,
                                                                                        distCoeff=self.CAMERA_MostRecentDict_CameraCalibration_Darray_DistortionCoefficients)

                            ##########################################################################################################
                            ##########################################################################################################

                            ##########################################################################################################
                            ##########################################################################################################
                            if len(self.DetectedArucoTags_CornersList_ImageCoordinates) > 0:

                                self.DetectedArucoTags_CenterOfMarker_ImageCoordinates = [-11111.0]*len(self.DetectedArucoTags_CornersList_ImageCoordinates)

                                ##########################################################################################################
                                CameraImage_Color_ArucoDetected_TEMP = self.CameraImage_Color_Adjusted.copy()
                                CameraImage_Gray_ArucoDetected_TEMP = self.CameraImage_ConvertedToGray.copy()
                                ##########################################################################################################

                                ##########################################################################################################
                                for Index in range(0, len(self.DetectedArucoTags_IDsList)):

                                    '''
                                    This function receives the detected markers and returns their pose estimation respect to
                                    the camera individually. So for each marker, one rotation and translation vector is returned.
                                    The returned transformation is the one that transforms points from each marker coordinate system
                                    to the camera coordinate system.
                                    The marker corrdinate system is centered on the middle of the marker, with the Z axis
                                    perpendicular to the marker plane.
                                    The coordinates of the four corners of the marker in its own coordinate system are:
                                    (-markerLength/2, markerLength/2, 0), (markerLength/2, markerLength/2, 0),
                                    (markerLength/2, -markerLength/2, 0), (-markerLength/2, -markerLength/2, 0)
                                    '''

                                    #########################################################
                                    self.DetectedArucoTags_CenterOfMarker_ImageCoordinates[Index] = numpy.mean(self.DetectedArucoTags_CornersList_ImageCoordinates[Index][0], 0)

                                    ArucoTag_RotationVectorOfMarkerCenter_RodriguesAxisAngle_NumpyArray, ArucoTag_TranslationVectorOfMarkerCenter_NumpyArray, MarkerPoints = cv2.aruco.estimatePoseSingleMarkers(self.DetectedArucoTags_CornersList_ImageCoordinates[Index],
                                                                                                   self.ArucoTag_MarkerLengthInMillimeters,
                                                                                                   self.CAMERA_MostRecentDict_CameraCalibration_Kmatrix_CameraIntrinsicsMatrix,
                                                                                                   self.CAMERA_MostRecentDict_CameraCalibration_Darray_DistortionCoefficients)

                                    #Not sure why we have to include the [0] after [0]
                                    ArucoTag_TranslationVectorOfMarkerCenter_PythonList = ArucoTag_TranslationVectorOfMarkerCenter_NumpyArray[0][0].tolist()
                                    ArucoTag_RotationVectorOfMarkerCenter_RodriguesAxisAngle_PythonList = ArucoTag_RotationVectorOfMarkerCenter_RodriguesAxisAngle_NumpyArray[0][0].tolist()
                                    #########################################################

                                    #########################################################
                                    RotationObjectScipy = Rotation.from_rotvec(ArucoTag_RotationVectorOfMarkerCenter_RodriguesAxisAngle_PythonList)
                                    ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInDegrees_PythonList = RotationObjectScipy.as_euler('xyz', degrees=True).tolist()
                                    ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInRadians_PythonList = numpy.deg2rad(numpy.array(ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInDegrees_PythonList)).tolist()
                                    #########################################################

                                    #########################################################
                                    #Not sure why we have to include the [0] after [Index]
                                    ArucoMarker_ID_Str = str(self.DetectedArucoTags_IDsList[Index][0])
                                    #print("ArucoMarker_ID_Str: " + str(ArucoMarker_ID_Str))

                                    if ArucoMarker_ID_Str not in self.DetectedArucoTag_InfoDict: #Marker ID hasn't been detected previously

                                        LowPassFilter_DictOfVariableFilterSettings = dict([("ArucoTag_TranslationVectorOfMarkerCenter_PythonList", dict([("UseMedianFilterFlag", 1), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", self.ArucoTag_TranslationVectorOfMarkerCenter_ExponentialSmoothingFilterLambda)])),
                                                                                            ("ArucoTag_RotationVectorOfMarkerCenter_RodriguesAxisAngle_PythonList", dict([("UseMedianFilterFlag", 1), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", self.ArucoTag_RotationVectorOfMarkerCenter_ExponentialSmoothingFilterLambda)])),
                                                                                            ("ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInDegrees_PythonList", dict([("UseMedianFilterFlag", 1), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", self.ArucoTag_RotationVectorOfMarkerCenter_ExponentialSmoothingFilterLambda)])) ])

                                        SetupDict = dict([("DictOfVariableFilterSettings", LowPassFilter_DictOfVariableFilterSettings)])

                                        self.DetectedArucoTag_InfoDict[ArucoMarker_ID_Str] = dict([("ArucoTag_TranslationVectorOfMarkerCenter_PythonList", ArucoTag_TranslationVectorOfMarkerCenter_PythonList),
                                                                        ("ArucoTag_RotationVectorOfMarkerCenter_RodriguesAxisAngle_PythonList", ArucoTag_RotationVectorOfMarkerCenter_RodriguesAxisAngle_PythonList),
                                                                        ("ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInDegrees_PythonList", ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInDegrees_PythonList),
                                                                        ("ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInRadians_PythonList", ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInRadians_PythonList),
                                                                        ("ArucoTag_DetectionTimeInMilliseconds", int(1000.0*self.CAMERA_MostRecentDict_Time)),
                                                                        ("ArucoTag_DetectedArucoTags_CornersList_ImageCoordinates", self.DetectedArucoTags_CornersList_ImageCoordinates[Index]),
                                                                        ("ArucoTag_DetectedArucoTags_CenterOfMarker_ImageCoordinates", self.DetectedArucoTags_CenterOfMarker_ImageCoordinates[Index]),
                                                                        ("LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject", LowPassFilterForDictsOfLists_ReubenPython2and3Class(SetupDict))])

                                        #print("self.DetectedArucoTag_InfoDict[ArucoMarker_ID_Str]: " + str(self.DetectedArucoTag_InfoDict[ArucoMarker_ID_Str]))

                                    else: #we HAVE seen this marker ID before

                                        Results = self.DetectedArucoTag_InfoDict[ArucoMarker_ID_Str]["LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject"].AddDataDictFromExternalProgram(dict([("ArucoTag_TranslationVectorOfMarkerCenter_PythonList", ArucoTag_TranslationVectorOfMarkerCenter_PythonList),
                                                                                                                                                                                        ("ArucoTag_RotationVectorOfMarkerCenter_RodriguesAxisAngle_PythonList", ArucoTag_RotationVectorOfMarkerCenter_RodriguesAxisAngle_PythonList),
                                                                                                                                                                                        ("ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInDegrees_PythonList", ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInDegrees_PythonList)]))

                                        #print(self.DetectedArucoTag_InfoDict[ArucoMarker_ID_Str]["ArucoTag_TranslationVectorOfMarkerCenter_PythonList"])
                                        self.DetectedArucoTag_InfoDict[ArucoMarker_ID_Str]["ArucoTag_DetectionTimeInMilliseconds"] = int(1000.0*self.CAMERA_MostRecentDict_Time)
                                        self.DetectedArucoTag_InfoDict[ArucoMarker_ID_Str]["ArucoTag_TranslationVectorOfMarkerCenter_PythonList"] = Results["ArucoTag_TranslationVectorOfMarkerCenter_PythonList"]["Filtered_MostRecentValuesList"]
                                        self.DetectedArucoTag_InfoDict[ArucoMarker_ID_Str]["ArucoTag_RotationVectorOfMarkerCenter_RodriguesAxisAngle_PythonList"] = Results["ArucoTag_RotationVectorOfMarkerCenter_RodriguesAxisAngle_PythonList"]["Filtered_MostRecentValuesList"]
                                        self.DetectedArucoTag_InfoDict[ArucoMarker_ID_Str]["ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInDegrees_PythonList"] = Results["ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInDegrees_PythonList"]["Filtered_MostRecentValuesList"]
                                        self.DetectedArucoTag_InfoDict[ArucoMarker_ID_Str]["ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInRadians_PythonList"] = numpy.deg2rad(numpy.array(Results["ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInDegrees_PythonList"]["Filtered_MostRecentValuesList"])).tolist()
                                        self.DetectedArucoTag_InfoDict[ArucoMarker_ID_Str]["ArucoTag_DetectedArucoTags_CornersList_ImageCoordinates"] = self.DetectedArucoTags_CornersList_ImageCoordinates[Index]
                                        self.DetectedArucoTag_InfoDict[ArucoMarker_ID_Str]["ArucoTag_DetectedArucoTags_CenterOfMarker_ImageCoordinates"] = self.DetectedArucoTags_CenterOfMarker_ImageCoordinates[Index]
                                        #print("yahtze, index " + str(str(self.DetectedArucoTags_IDsList[Index])[0]))
                                    #########################################################

                                    #########################################################
                                    cv2.aruco.drawDetectedMarkers(CameraImage_Color_ArucoDetected_TEMP, self.DetectedArucoTags_CornersList_ImageCoordinates) #Render perimeter of tag
                                    cv2.aruco.drawDetectedMarkers(CameraImage_Gray_ArucoDetected_TEMP, self.DetectedArucoTags_CornersList_ImageCoordinates) #Render perimeter of tag

                                    cv2.aruco.drawAxis(image=CameraImage_Color_ArucoDetected_TEMP,
                                                       cameraMatrix=self.CAMERA_MostRecentDict_CameraCalibration_Kmatrix_CameraIntrinsicsMatrix,
                                                       distCoeffs=self.CAMERA_MostRecentDict_CameraCalibration_Darray_DistortionCoefficients,
                                                       rvec=ArucoTag_RotationVectorOfMarkerCenter_RodriguesAxisAngle_NumpyArray,
                                                       tvec=ArucoTag_TranslationVectorOfMarkerCenter_NumpyArray,
                                                       length=self.ArucoTag_AxesToDrawLengthInMillimeters)

                                    cv2.aruco.drawAxis(image=CameraImage_Gray_ArucoDetected_TEMP,
                                                       cameraMatrix=self.CAMERA_MostRecentDict_CameraCalibration_Kmatrix_CameraIntrinsicsMatrix,
                                                       distCoeffs=self.CAMERA_MostRecentDict_CameraCalibration_Darray_DistortionCoefficients,
                                                       rvec=ArucoTag_RotationVectorOfMarkerCenter_RodriguesAxisAngle_NumpyArray,
                                                       tvec=ArucoTag_TranslationVectorOfMarkerCenter_NumpyArray,
                                                       length=self.ArucoTag_AxesToDrawLengthInMillimeters)
                                    #########################################################

                                    ######################################################### UPDATE THE IMAGE TO BE DISPLAYED IN PREVIEW WINDOW
                                    self.CameraImage_Color_ArucoDetected = CameraImage_Color_ArucoDetected_TEMP.copy()
                                    self.CameraImage_Gray_ArucoDetected = CameraImage_Gray_ArucoDetected_TEMP.copy()
                                    #########################################################

                                ##########################################################################################################

                                ########################################################################################################## unicorn
                                self.MostRecentDataDict_BlockFromBeingReadFlag = 1

                                self.MostRecentDataDict = dict([("Time", int(1000.0*self.CAMERA_MostRecentDict_Time)),#self.CurrentTime_CalculatedFromMainThread),
                                                                ("Frequency", self.DataStreamingFrequency_CalculatedFromMainThread),
                                                                ("DetectedArucoTag_InfoDict", self.DetectedArucoTag_InfoDict),
                                                                ("SaveImageFlag", self.SaveImageFlag),
                                                                ("AcceptNewImagesForSavingFlag", self.AcceptNewImagesForSavingFlag),
                                                                ("ImagesToBeSaveQueue_qsize", self.ImagesToBeSaveQueue.qsize()),
                                                                ("SavedImageFrameCounter", self.SavedImageFrameCounter),
                                                                ("OriginalImage", self.CAMERA_MostRecentDict_OriginalImage),
                                                                ("CameraImage_Color_ArucoDetected", self.CameraImage_Color_ArucoDetected),
                                                                ("CameraCalibration_Kmatrix_CameraIntrinsicsMatrix", self.CAMERA_MostRecentDict_CameraCalibration_Kmatrix_CameraIntrinsicsMatrix),
                                                                ("CameraCalibration_Darray_DistortionCoefficients", self.CAMERA_MostRecentDict_CameraCalibration_Darray_DistortionCoefficients)])

                                self.MostRecentDataDict_LAST = self.MostRecentDataDict

                                self.MostRecentDataDict_BlockFromBeingReadFlag = 0
                                ##########################################################################################################

                            ##########################################################################################################
                            ##########################################################################################################

                            ##########################################################################################################
                            ##########################################################################################################
                            else:
                                self.CameraImage_Color_ArucoDetected = self.CAMERA_MostRecentDict_OriginalImage.copy()
                                self.CameraImage_Gray_ArucoDetected = self.CameraImage_ConvertedToGray.copy()
                                #print("No Aruco tags detected!")
                            ##########################################################################################################
                            ##########################################################################################################

                            ##########################################################################################################
                            ##########################################################################################################
                            if self.AcceptNewImagesForSavingFlag == 1:
                                self.ImagesToBeSaveQueue.put(dict([("TIMEms", int(1000.0*self.CAMERA_MostRecentDict_Time)),
                                                                   ("ImageToWrite", self.CameraImage_Color_ArucoDetected)]))

                                if self.SaveSingleSnapshotOrContinuousStreamOfImages_state == 0:
                                    self.AcceptNewImagesForSavingFlag = 0
                                    self.SaveImageFlag_NeedsToBeChangedFlag = 1

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
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                except:
                    exceptions = sys.exc_info()[0]
                    print("MainThread, Exceptions: %s" % exceptions)
                    traceback.print_exc()
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
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            self.UpdateFrequencyCalculation_MainThread_Filtered()

            if self.MainThread_TimeToSleepEachLoop > 0.0:
                if self.MainThread_TimeToSleepEachLoop > 0.001:
                    time.sleep(self.MainThread_TimeToSleepEachLoop - 0.001) #The "- 0.001" corrects for slight deviation from intended frequency due to other functions being called.
                else:
                    time.sleep(self.MainThread_TimeToSleepEachLoop)
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
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        self.CameraStreamerClass_ReubenPython2and3ClassObject.ExitProgram_Callback()
        time.sleep(5.0)

        self.MyPrint_WithoutLogFile("Finished MainThread for ArucoTagDetectionFromCameraFeed_ReubenPython3Class object.")
        self.MainThread_StillRunningFlag = 0
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
    def StartWritingImages(self):
    
        self.CreateNewDirectoryIfItDoesntExist(os.getcwd() + "\\" + self.ArucoTag_SavedImages_LocalDirectoryNameNoSlashes)
    
        self.AcceptNewImagesForSavingFlag = 1
        self.SaveImageFlag = 1
        
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StopWritingImagesImmediately(self):

        self.AcceptNewImagesForSavingFlag = 0
        self.SaveImageFlag = 0

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ########################################################################################################## unicorn
    def ImageSavingThread(self):

        self.MyPrint_WithoutLogFile("Started ImageSavingThread for ArucoTagDetectionFromCameraFeed_ReubenPython3Class object.")
        
        self.ImageSavingThread_StillRunningFlag = 1

        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            try:

                ##########################################################################################################
                ##########################################################################################################
                if self.SaveImageFlag_NeedsToBeChangedFlag == 1:

                    if self.SaveImageFlag == 1:
                        self.AcceptNewImagesForSavingFlag = 0

                    if self.ImagesToBeSaveQueue.qsize() == 0:
                        if self.SaveImageFlag == 1:  # Currently saving, need to stop.
                            self.StopWritingImagesImmediately()

                        else:  #Currently NOT saving, need to start.
                            self.StartWritingImages()

                        self.SaveImageFlag_NeedsToBeChangedFlag = 0

                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.ImagesToBeSaveQueue.qsize() > 0:
                    ImageToWriteDict = self.ImagesToBeSaveQueue.get()

                    cv2.imwrite(os.getcwd() +
                                "\\" + self.ArucoTag_SavedImages_LocalDirectoryNameNoSlashes +
                                "\\" + self.ArucoTag_SavedImages_FilenamePrefix +
                                "_CAM" + str(self.camera_selection_number) +
                                "_TIMEms" + str(ImageToWriteDict["TIMEms"]) +
                                "_Frame" + str(self.SavedImageFrameCounter) +
                                ".jpg", ImageToWriteDict["ImageToWrite"])

                    self.SavedImageFrameCounter = self.SavedImageFrameCounter + 1

                time.sleep(0.002)
                ##########################################################################################################
                ##########################################################################################################

            except:
                exceptions = sys.exc_info()[0]
                print("CameraDisplayThread_1, Exceptions: %s" % exceptions)
                traceback.print_exc()

        ##########################################################################################################
        ##########################################################################################################

        self.MyPrint_WithoutLogFile("Finished ImageSavingThread for ArucoTagDetectionFromCameraFeed_ReubenPython3Class object.")
        self.ImageSavingThread_StillRunningFlag = 0

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ########################################################################################################## unicorn
    def OpenCVdisplayThread(self):

        self.MyPrint_WithoutLogFile("Started OpenCVdisplayThread for ArucoTagDetectionFromCameraFeed_ReubenPython3Class object.")
        
        self.OpenCVdisplayThread_StillRunningFlag = 1

        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            try:

                ##########################################################################################################
                self.CurrentTime_CalculatedFromCameraDisplayThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_AllThreads
                ##########################################################################################################

                ##########################################################################################################
                if self.CAMERA_OPEN_FLAG == 1:

                    ImageToShow = self.CameraImage_ToBeDisplayedInPreviewScreens


                    #cv2.imshow("ArucoDetected, " + self.NameToDisplay_UserSet, self.CameraImage_Color_ArucoDetected)
                    #cv2.moveWindow("ArucoDetected, " + self.NameToDisplay_UserSet, self.OpenCVwindowPosX, self.OpenCVwindowPosY)

                    cv2WindowName = "ArucoDetected, " + self.NameToDisplay_UserSet
                    cv2.imshow(cv2WindowName, ImageToShow)
                    cv2.moveWindow(cv2WindowName, self.OpenCVwindowPosX, self.OpenCVwindowPosY)
                    #cv2.resizeWindow(cv2WindowName, int(self.TkinterPreviewImageScalingFactor*self.image_width), int(self.TkinterPreviewImageScalingFactor*self.image_height))
                    cv2.waitKey(self.OpenCVwindow_UpdateEveryNmilliseconds)

                else:
                    time.sleep(self.OpenCVwindow_UpdateEveryNmilliseconds / 1000.0)
                ##########################################################################################################

            except:
                exceptions = sys.exc_info()[0]
                print("OpenCVdisplayThread, Exceptions: %s" % exceptions)
                traceback.print_exc()

        ##########################################################################################################
        ##########################################################################################################

        #cv2.destroyAllWindows() #DON'T CALL THIS AS IT WAS CAUSING THE CODE TO HANG (Possible explanation: https://stackoverflow.com/questions/13734276/python-freezes-after-cv2-destroywindow)!!!

        self.MyPrint_WithoutLogFile("Finished OpenCVdisplayThread for ArucoTagDetectionFromCameraFeed_ReubenPython3Class object.")
        self.OpenCVdisplayThread_StillRunningFlag = 0

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def IsSaving(self):

        return self.SaveImageFlag
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for ArucoTagDetectionFromCameraFeed_ReubenPython3Class object")

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

        print("Starting the GUI_Thread for object.")

        ################################################
        ################################################
        self.root = parent
        self.parent = parent
        ################################################
        ################################################

        ################################################
        ################################################
        self.TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150)  # RGB
        self.TKinter_LightBlueColor = '#%02x%02x%02x' % (150, 150, 255)  # RGB
        self.TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150)  # RGB
        self.TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
        self.TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
        self.Tkinter_SliderLength = 250
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
        self.TabControlObject = ttk.Notebook(self.myFrame)

        #Tab_MainControls = ttk.Frame(TabControlObject)
        #TabControlObject.add(Tab_MainControls, text='   Main Controls   ')

        self.Tab_ArucoTagDetection = ttk.Frame(self.TabControlObject)
        self.TabControlObject.add(self.Tab_ArucoTagDetection, text='   ArucoTagDetection  ')

        self.Tab_Camera = ttk.Frame(self.TabControlObject)
        self.TabControlObject.add(self.Tab_Camera, text='   Camera   ')

        #Tab_MyPrint = ttk.Frame(TabControlObject)
        #TabControlObject.add(Tab_MyPrint, text='   MyPrint Terminal   ')

        self.TabControlObject.pack(expand=1, fill="both")  # CANNOT MIX PACK AND GRID IN THE SAME FRAME/TAB, SO ALL .GRID'S MUST BE CONTAINED WITHIN THEIR OWN FRAME/TAB.

        ############# #Set the tab header font
        self.TabStyle = ttk.Style()
        self.TabStyle.configure('TNotebook.Tab', font=('Helvetica', '12', 'bold'))
        #############

        ################################################
        ################################################

        ################################################
        ################################################
        self.CameraFrame = Frame(self.Tab_Camera)
        self.CameraFrame.grid(row=0,column=0,padx=1,pady=1,rowspan=1,columnspan=1,sticky="w")
        ################################################
        ################################################

        ################################################
        ################################################
        self.ArucoTagDetectionControlsFrame = Frame(self.Tab_ArucoTagDetection)
        self.ArucoTagDetectionControlsFrame.grid(row=0,column=0,padx=1,pady=1,rowspan=1,columnspan=1,sticky="w")
        ################################################
        ################################################

        ################################################
        ################################################
        self.ClassObjectInfo_Label = Label(self.ArucoTagDetectionControlsFrame, text="Device Info", width=150)
        self.ClassObjectInfo_Label["text"] = self.NameToDisplay_UserSet
        self.ClassObjectInfo_Label.grid(row=0, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        ################################################
        ################################################

        ################################################
        ################################################
        self.image_label = Label(self.ArucoTagDetectionControlsFrame, text="image_label")
        self.image_label.grid(row=1, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        ################################################
        ################################################

        ################################################
        ################################################
        self.SaveImageButton = Button(self.ArucoTagDetectionControlsFrame,
                                                    text="Save Image",
                                                    state="normal",
                                                    width=30,
                                                    command=lambda i=1: self.SaveImageButtonResponse())
        self.SaveImageButton.grid(row=2, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        ################################################
        ################################################

        ################################################
        ################################################
        self.SaveSingleSnapshotOrContinuousStreamOfImages_Checkbutton_Value = DoubleVar()

        if self.SaveSingleSnapshotOrContinuousStreamOfImages_state == 1:
            self.SaveSingleSnapshotOrContinuousStreamOfImages_Checkbutton_Value.set(1)
        else:
            self.SaveSingleSnapshotOrContinuousStreamOfImages_Checkbutton_Value.set(0)

        self.SaveSingleSnapshotOrContinuousStreamOfImages_Checkbutton = Checkbutton(self.ArucoTagDetectionControlsFrame,
                                                         width=60,
                                                         text='SnapshotOrContinuousSaving',
                                                         state="normal",
                                                         variable=self.SaveSingleSnapshotOrContinuousStreamOfImages_Checkbutton_Value)
        self.SaveSingleSnapshotOrContinuousStreamOfImages_Checkbutton.bind('<ButtonRelease-1>', lambda event, name="SaveSingleSnapshotOrContinuousStreamOfImages_Checkbutton": self.SaveSingleSnapshotOrContinuousStreamOfImages_CheckbuttonResponse(event, name))
        self.SaveSingleSnapshotOrContinuousStreamOfImages_Checkbutton.grid(row=3, column=0, padx=1, pady=1, columnspan=1,rowspan=1)
        ################################################
        ################################################

        ################################################
        ################################################
        self.Data_Label = Label(self.ArucoTagDetectionControlsFrame, text="Data_Label", width=150)
        self.Data_Label.grid(row=4, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        ################################################
        ################################################

        ################################################
        ################################################
        self.PrintToGui_Label = Label(self.ArucoTagDetectionControlsFrame, text="PrintToGui_Label", width=150)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=5, column=0, padx=1, pady=1, columnspan=10, rowspan=10)
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
    def AcceptNewImagesForSavingFlag_ToggleState(self):

        if self.AcceptNewImagesForSavingFlag == 1:
            self.AcceptNewImagesForSavingFlag = 0
        else:
            self.AcceptNewImagesForSavingFlag = 1

        #self.MyPrint_WithoutLogFile("AcceptNewImagesForSavingFlag_ToggleState: AcceptNewImagesForSavingFlag = " + str(self.AcceptNewImagesForSavingFlag))
    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    def SaveImageFlag_ToggleState(self):

        if self.SaveImageFlag == 1:
            self.SaveImageFlag = 0
        else:
            self.SaveImageFlag = 1

        #self.MyPrint_WithoutLogFile("SaveImageFlag_ToggleState: SaveImageFlag = " + str(self.SaveImageFlag))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SaveImageButtonResponse(self):

        #self.AcceptNewImagesForSavingFlag = 0
        self.SaveImageFlag_NeedsToBeChangedFlag = 1

        #print("SaveImageButtonResponse event fired!")
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SaveSingleSnapshotOrContinuousStreamOfImages_CheckbuttonResponse(self, event, name):

        temp_value = self.SaveSingleSnapshotOrContinuousStreamOfImages_Checkbutton_Value.get()

        if temp_value == 0:
            self.SaveSingleSnapshotOrContinuousStreamOfImages_state = 1  ########## This reversal is needed for the variable state to match the checked state, but we don't know why
        elif temp_value == 1:
            self.SaveSingleSnapshotOrContinuousStreamOfImages_state = 0

        #self.MyPrint_WithoutLogFile("SaveSingleSnapshotOrContinuousStreamOfImages_CheckbuttonResponse, self.SaveSingleSnapshotOrContinuousStreamOfImages_state: " + str(self.SaveSingleSnapshotOrContinuousStreamOfImages_state))
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
                    self.Data_Label["text"] = "Time: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.CurrentTime_CalculatedFromMainThread, 0, 3) + \
                                                "\nFrequency: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_CalculatedFromMainThread, 0, 3) + \
                                                "\nArucoTag_DictType: " + self.ArucoTag_DictType_EnglishString + \
                                                "\nArucoTag_MarkerLengthInMillimeters: " + str(self.ArucoTag_MarkerLengthInMillimeters) + \
                                                "\n\n" +\
                                                self.ConvertDictToProperlyFormattedStringForPrinting(self.MostRecentDataDict, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3)

                    #######################################################

                    #######################################################
                    if self.SaveImageFlag == 1:
                        self.SaveImageButton["bg"] = self.TKinter_LightRedColor
                        self.SaveImageButton["text"] = "Saving images"
                    else:
                        self.SaveImageButton["bg"] = self.TKinter_LightGreenColor
                        self.SaveImageButton["text"] = "Not saving images"
                    #######################################################

                    #######################################################
                    #self.CameraImage_ToBeDisplayedInPreviewScreens = self.ResizeImage(self.CameraImage_Gray_ArucoDetected, self.TkinterPreviewImageScalingFactor)
                    self.CameraImage_ToBeDisplayedInPreviewScreens = self.ResizeImage(self.CameraImage_Color_ArucoDetected, self.TkinterPreviewImageScalingFactor)

                    self.GUI_label_PhotoImage = self.ConvertNumpyArrayToTkinterPhotoImage(self.CameraImage_ToBeDisplayedInPreviewScreens)

                    self.image_label.configure(image=self.GUI_label_PhotoImage)
                    #######################################################

                    #######################################################
                    self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                    #######################################################

                    #########################################################
                    if self.CAMERA_OPEN_FLAG == 1:
                        self.CameraStreamerClass_ReubenPython2and3ClassObject.GUI_update_clock()
                    #########################################################

                except:
                    exceptions = sys.exc_info()[0]
                    print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class, GUI_update_clock: Exceptions: %s" % exceptions)
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
    def LimitTextEntryInput(self, min_val, max_val, test_val, TextEntryObject):

        try:
            test_val = float(test_val)  # MUST HAVE THIS LINE TO CATCH STRINGS PASSED INTO THE FUNCTION

            if test_val > max_val:
                test_val = max_val
            elif test_val < min_val:
                test_val = min_val
            else:
                test_val = test_val

        except:
            pass

        try:
            if TextEntryObject != "":
                if isinstance(TextEntryObject, list) == 1:  # Check if the input 'TextEntryObject' is a list or not
                    TextEntryObject[0].set(str(test_val))  # Reset the text, overwriting the bad value that was entered.
                else:
                    TextEntryObject.set(str(test_val))  # Reset the text, overwriting the bad value that was entered.
        except:
            pass

        return test_val
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
                                                     str(Key) + ":\n" + \
                                                     self.ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key], NumberOfDecimalsPlaceToUse, NumberOfEntriesPerLine, NumberOfTabsBetweenItems)

            else:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     str(Key) + ": " + \
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


