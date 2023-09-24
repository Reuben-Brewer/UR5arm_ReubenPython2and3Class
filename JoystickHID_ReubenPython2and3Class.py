# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision H, 09/22/2023

Verified working on: Python 2.7, 3.8 for Windows 8.1, 10 64-bit, Ubuntu 20.04*, and Raspberry Pi Buster (no Mac testing yet).

*Note: This code mostly works in Ubuntu 20.04, but the hat yields strange values for some models of joystick
(such as the VKBsim Gladiator). Running jstest-gtk (sudo apt-get install jstest-gtk) will show you what the
actual values are that are streaming from the joystick without going through JoystickHID_ReubenPython2and3Class.*
'''

__author__ = 'reuben.brewer'

#########################################################
from Joystick2DdotDisplay_ReubenPython2and3Class import *
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
import pygame #Install via "pip install pygame" or "pip install pygame_VersionInfo.whl"
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

class JoystickHID_ReubenPython2and3Class(Frame): #Subclass the Tkinter Frame

    #######################################################################################################################
    #######################################################################################################################
    def __init__(self, setup_dict): #Subclass the Tkinter Frame

        print("#################### JoystickHID_ReubenPython2and3Class __init__ starting. ####################")

        #########################################################
        #########################################################
        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = -1
        self.Joystick_FoundAndOpenedFlag = 0
        self.EnableInternal_MyPrint_Flag = 0
        self.MainThread_still_running_flag = 0

        self.CurrentTime_CalculatedFromMainThread = -11111.0
        self.StartingTime_CalculatedFromMainThread = -11111.0
        self.LastTime_CalculatedFromMainThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromMainThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromMainThread = -11111.0
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

        print("JoystickHID_ReubenPython2and3Class __init__: The OS platform is: " + self.my_platform)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "GUIparametersDict" in setup_dict:
            self.GUIparametersDict = setup_dict["GUIparametersDict"]

            ##########################################
            if "USE_GUI_FLAG" in self.GUIparametersDict:
                self.USE_GUI_FLAG = self.PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG", self.GUIparametersDict["USE_GUI_FLAG"])
            else:
                self.USE_GUI_FLAG = 0

            print("JoystickHID_ReubenPython2and3Class __init__: USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))
            ##########################################

            ##########################################
            if "root" in self.GUIparametersDict:
                self.root = self.GUIparametersDict["root"]
            else:
                print("JoystickHID_ReubenPython2and3Class __init__: Error, must pass in 'root'")
                return
            ##########################################

            ##########################################
            if "EnableInternal_MyPrint_Flag" in self.GUIparametersDict:
                self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", self.GUIparametersDict["EnableInternal_MyPrint_Flag"])
            else:
                self.EnableInternal_MyPrint_Flag = 0

            print("JoystickHID_ReubenPython2and3Class __init__: EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
            ##########################################

            ##########################################
            if "PrintToConsoleFlag" in self.GUIparametersDict:
                self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", self.GUIparametersDict["PrintToConsoleFlag"])
            else:
                self.PrintToConsoleFlag = 1

            print("JoystickHID_ReubenPython2and3Class __init__: PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
            ##########################################

            ##########################################
            if "NumberOfPrintLines" in self.GUIparametersDict:
                self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", self.GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
            else:
                self.NumberOfPrintLines = 10

            print("JoystickHID_ReubenPython2and3Class __init__: NumberOfPrintLines:" + str(self.NumberOfPrintLines))
            ##########################################

            ##########################################
            if "UseBorderAroundThisGuiObjectFlag" in self.GUIparametersDict:
                self.UseBorderAroundThisGuiObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseBorderAroundThisGuiObjectFlag", self.GUIparametersDict["UseBorderAroundThisGuiObjectFlag"])
            else:
                self.UseBorderAroundThisGuiObjectFlag = 0

            print("JoystickHID_ReubenPython2and3Class __init__: UseBorderAroundThisGuiObjectFlag: " + str(self.UseBorderAroundThisGuiObjectFlag))
            ##########################################

            ##########################################
            if "GUI_ROW" in self.GUIparametersDict:
                self.GUI_ROW = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROW", self.GUIparametersDict["GUI_ROW"], 0.0, 1000.0))
            else:
                self.GUI_ROW = 0

            print("JoystickHID_ReubenPython2and3Class __init__: GUI_ROW: " + str(self.GUI_ROW))
            ##########################################

            ##########################################
            if "GUI_COLUMN" in self.GUIparametersDict:
                self.GUI_COLUMN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMN", self.GUIparametersDict["GUI_COLUMN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMN = 0

            print("JoystickHID_ReubenPython2and3Class __init__: GUI_COLUMN: " + str(self.GUI_COLUMN))
            ##########################################

            ##########################################
            if "GUI_PADX" in self.GUIparametersDict:
                self.GUI_PADX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADX", self.GUIparametersDict["GUI_PADX"], 0.0, 1000.0))
            else:
                self.GUI_PADX = 0

            print("JoystickHID_ReubenPython2and3Class __init__: GUI_PADX: " + str(self.GUI_PADX))
            ##########################################

            ##########################################
            if "GUI_PADY" in self.GUIparametersDict:
                self.GUI_PADY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADY", self.GUIparametersDict["GUI_PADY"], 0.0, 1000.0))
            else:
                self.GUI_PADY = 0

            print("JoystickHID_ReubenPython2and3Class __init__: GUI_PADY: " + str(self.GUI_PADY))
            ##########################################

            ##########################################
            if "GUI_ROWSPAN" in self.GUIparametersDict:
                self.GUI_ROWSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROWSPAN", self.GUIparametersDict["GUI_ROWSPAN"], 1.0, 1000.0))
            else:
                self.GUI_ROWSPAN = 1

            print("JoystickHID_ReubenPython2and3Class __init__: GUI_ROWSPAN: " + str(self.GUI_ROWSPAN))
            ##########################################

            ##########################################
            if "GUI_COLUMNSPAN" in self.GUIparametersDict:
                self.GUI_COLUMNSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMNSPAN", self.GUIparametersDict["GUI_COLUMNSPAN"], 1.0, 1000.0))
            else:
                self.GUI_COLUMNSPAN = 1

            print("JoystickHID_ReubenPython2and3Class __init__: GUI_COLUMNSPAN: " + str(self.GUI_COLUMNSPAN))
            ##########################################

            ##########################################
            if "GUI_STICKY" in self.GUIparametersDict:
                self.GUI_STICKY = str(self.GUIparametersDict["GUI_STICKY"])
            else:
                self.GUI_STICKY = "w"

            print("JoystickHID_ReubenPython2and3Class __init__: GUI_STICKY: " + str(self.GUI_STICKY))
            ##########################################

        else:
            self.GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("JoystickHID_ReubenPython2and3Class __init__: No GUIparametersDict present, setting USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))

        #print("JoystickHID_ReubenPython2and3Class __init__: GUIparametersDict: " + str(self.GUIparametersDict))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "Joystick_PrintInfoForAllDetectedJoysticksFlag" in setup_dict:
            self.Joystick_PrintInfoForAllDetectedJoysticksFlag = self.PassThrough0and1values_ExitProgramOtherwise("Joystick_PrintInfoForAllDetectedJoysticksFlag", setup_dict["Joystick_PrintInfoForAllDetectedJoysticksFlag"])
        else:
            self.Joystick_PrintInfoForAllDetectedJoysticksFlag = 0

        print("JoystickHID_ReubenPython2and3Class __init__: Joystick_PrintInfoForAllDetectedJoysticksFlag: " + str(self.Joystick_PrintInfoForAllDetectedJoysticksFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "Joystick_SearchAllJoysticksFlag" in setup_dict:
            self.Joystick_SearchAllJoysticksFlag = self.PassThrough0and1values_ExitProgramOtherwise("Joystick_SearchAllJoysticksFlag", setup_dict["Joystick_SearchAllJoysticksFlag"])
        else:
            self.Joystick_SearchAllJoysticksFlag = 0

        print("JoystickHID_ReubenPython2and3Class __init__: Joystick_SearchAllJoysticksFlag: " + str(self.Joystick_SearchAllJoysticksFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "Joystick_NameDesired" in setup_dict:
            self.Joystick_NameDesired = str(setup_dict["Joystick_NameDesired"])
        else:
            self.Joystick_NameDesired = ""

        print("JoystickHID_ReubenPython2and3Class __init__: Joystick_NameDesired: " + str(self.Joystick_NameDesired))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "Joystick_IntegerIDdesired" in setup_dict:
            self.Joystick_IntegerIDdesired = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("Joystick_IntegerIDdesired", setup_dict["Joystick_IntegerIDdesired"], -1.0, 32.0))
        else:
            self.Joystick_IntegerIDdesired = -1

        print("JoystickHID_ReubenPython2and3Class __init__: Joystick_IntegerIDdesired: " + str(self.Joystick_IntegerIDdesired))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "NameToDisplay_UserSet" in setup_dict:
            self.NameToDisplay_UserSet = str(setup_dict["NameToDisplay_UserSet"])
        else:
            self.NameToDisplay_UserSet = ""

        print("JoystickHID_ReubenPython2and3Class __init__: NameToDisplay_UserSet: " + str(self.NameToDisplay_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "MainThread_TimeToSleepEachLoop" in setup_dict:
            self.MainThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("MainThread_TimeToSleepEachLoop", setup_dict["MainThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.MainThread_TimeToSleepEachLoop = 0.005

        print("JoystickHID_ReubenPython2and3Class __init__: MainThread_TimeToSleepEachLoop: " + str(self.MainThread_TimeToSleepEachLoop))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "Joystick_ShowJustDotMovingFlag" in setup_dict:
            self.Joystick_ShowJustDotMovingFlag = self.PassThrough0and1values_ExitProgramOtherwise("Joystick_ShowJustDotMovingFlag", setup_dict["Joystick_ShowJustDotMovingFlag"])
        else:
            self.Joystick_ShowJustDotMovingFlag = 1

        print("JoystickHID_ReubenPython2and3Class __init__: Joystick_ShowJustDotMovingFlag: " + str(self.Joystick_ShowJustDotMovingFlag))
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
        pygame.init()
        pygame.joystick.init()

        self.Joystick_DetectedParameters_Dict = self.AnalyzeAndInitializeJoystick(self.Joystick_NameDesired, self.Joystick_IntegerIDdesired, self.Joystick_PrintInfoForAllDetectedJoysticksFlag)
        print("self.Joystick_DetectedParameters_Dict: " + str(self.Joystick_DetectedParameters_Dict))
        self.Joystick_FoundAndOpenedFlag = self.Joystick_DetectedParameters_Dict["Joystick_FoundAndOpenedFlag"]
        print("self.Joystick_FoundAndOpenedFlag: " + str(self.Joystick_FoundAndOpenedFlag ))

        if self.Joystick_FoundAndOpenedFlag == 1:

            self.MyPrint_WithoutLogFile("JoystickHID_ReubenPython2and3Class __init__: Found and opened the correct joystick.")

            self.Joystick_NameDetected = self.Joystick_DetectedParameters_Dict["Joystick_NameDetected"]
            self.Joystick_IntegerIDdetected = self.Joystick_DetectedParameters_Dict["Joystick_IntegerIDdetected"]
            self.Joystick_NumberOfAxesDetected = self.Joystick_DetectedParameters_Dict["Joystick_NumberOfAxesDetected"]
            self.Joystick_NumberOfButtonsDetected = self.Joystick_DetectedParameters_Dict["Joystick_NumberOfButtonsDetected"]
            self.Joystick_NumberOfHatsDetected = self.Joystick_DetectedParameters_Dict["Joystick_NumberOfHatsDetected"]
            self.Joystick_NumberOfBallsDetected = self.Joystick_DetectedParameters_Dict["Joystick_NumberOfBallsDetected"]
            self.Joystick_Object = self.Joystick_DetectedParameters_Dict["Joystick_Object"]

            self.Joystick_Axis_Value_List = [-11111.0]*self.Joystick_NumberOfAxesDetected
            self.Joystick_Axis_Value_List_Last = [-11111.0] * self.Joystick_NumberOfAxesDetected
            self.Joystick_Button_Value_List = [-11111]*self.Joystick_NumberOfButtonsDetected
            self.Joystick_Button_Value_List_Last = [-11111] * self.Joystick_NumberOfButtonsDetected
            self.Joystick_Button_LatchingRisingEdgeEvents_List = [0] * self.Joystick_NumberOfButtonsDetected
            self.Joystick_Hat_Value_List = [[-11111, -11111]]*self.Joystick_NumberOfHatsDetected
            self.Joystick_Hat_Value_List_Last = [[-11111, -11111]] * self.Joystick_NumberOfHatsDetected
            self.Joystick_Hat_LatchingRisingEdgeEvents_List = [[0, 0]] * self.Joystick_NumberOfHatsDetected #Two axes per hat
            self.Joystick_Ball_Value_List = [-11111.0]*self.Joystick_NumberOfBallsDetected
            self.Joystick_Ball_Value_List_Last = [-11111.0] * self.Joystick_NumberOfBallsDetected

            self.MostRecentDataDict = dict()

        else:
            self.MyPrint_WithoutLogFile("JoystickHID_ReubenPython2and3Class __init__: Error, could not find and open the correct joystick.")
            return
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "Joystick_Axis_Index_ToDisplayAsHorizontalAxisOn2DdotDisplay" in setup_dict:
            self.Joystick_Axis_Index_ToDisplayAsHorizontalAxisOn2DdotDisplay = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("Joystick_Axis_Index_ToDisplayAsHorizontalAxisOn2DdotDisplay", setup_dict["Joystick_Axis_Index_ToDisplayAsHorizontalAxisOn2DdotDisplay"], 0, self.Joystick_NumberOfAxesDetected))

        else:
            self.Joystick_Axis_Index_ToDisplayAsHorizontalAxisOn2DdotDisplay = 0

        print("Joystick_Axis_Index_ToDisplayAsHorizontalAxisOn2DdotDisplay: " + str(self.Joystick_Axis_Index_ToDisplayAsHorizontalAxisOn2DdotDisplay))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "Joystick_Axis_Index_ToDisplayAsVerticalAxisOn2DdotDisplay" in setup_dict:
            self.Joystick_Axis_Index_ToDisplayAsVerticalAxisOn2DdotDisplay = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("Joystick_Axis_Index_ToDisplayAsVerticalAxisOn2DdotDisplay", setup_dict["Joystick_Axis_Index_ToDisplayAsVerticalAxisOn2DdotDisplay"], 0, self.Joystick_NumberOfAxesDetected))

        else:
            self.Joystick_Axis_Index_ToDisplayAsVerticalAxisOn2DdotDisplay = 1

        print("Joystick_Axis_Index_ToDisplayAsVerticalAxisOn2DdotDisplay: " + str(self.Joystick_Axis_Index_ToDisplayAsVerticalAxisOn2DdotDisplay))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "Joystick_Button_Index_ToDisplayAsDotColorOn2DdotDisplay" in setup_dict:
            self.Joystick_Button_Index_ToDisplayAsDotColorOn2DdotDisplay = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("Joystick_Button_Index_ToDisplayAsDotColorOn2DdotDisplay", setup_dict["Joystick_Button_Index_ToDisplayAsDotColorOn2DdotDisplay"], 0, self.Joystick_NumberOfButtonsDetected))

        else:
            self.Joystick_Button_Index_ToDisplayAsDotColorOn2DdotDisplay = 0

        print("Joystick_Button_Index_ToDisplayAsDotColorOn2DdotDisplay: " + str(self.Joystick_Button_Index_ToDisplayAsDotColorOn2DdotDisplay))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if self.Joystick_FoundAndOpenedFlag == 1:

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

        else:
            return
        #########################################################
        #########################################################

    #######################################################################################################################
    #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    def AnalyzeAndInitializeJoystick(self, NameDesired = "", IntegerIDdesired = -1, PrintInfoForAllDetectedJoysticksFlag = 1):

        JoystickDictToReturn = dict([("Joystick_FoundAndOpenedFlag", 0)])

        #########################################################
        #########################################################
        #########################################################
        try:
            self.Joystick_NumberOfJoysticksDetected = pygame.joystick.get_count()

            #########################################################
            #########################################################
            if self.Joystick_NumberOfJoysticksDetected <= 0:
                self.MyPrint_WithoutLogFile("AnalyzeAndInitializeJoystick, Error: 0 joysticks were detected.")
                return JoystickDictToReturn
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if self.Joystick_NumberOfJoysticksDetected < IntegerIDdesired:
                self.MyPrint_WithoutLogFile("AnalyzeAndInitializeJoystick, Error: IntegerIDdesired (" + str(IntegerIDdesired)+ ") cannot be smaller than the number of joysticks detected (" + str(self.Joystick_NumberOfJoysticksDetected) + ")")
                return JoystickDictToReturn
            #########################################################
            #########################################################

            #########################################################
            #########################################################

            #########################################################
            if self.Joystick_SearchAllJoysticksFlag == 1:
                ListOfJoysticksToSearch = range(0, self.Joystick_NumberOfJoysticksDetected)
            else:
                if IntegerIDdesired != -1:
                    ListOfJoysticksToSearch = [IntegerIDdesired]
                else:
                    ListOfJoysticksToSearch = []
            #########################################################
                
            for IntegerID_TempIndex in ListOfJoysticksToSearch: #In this first loop, discover and print details of each joystick.

                #########################################################
                #IsJoystickInitializedFlag = pygame.joystick.get_init()
                #print("Joystick ID " + str(IntegerID_TempIndex) + " get_init() = " + str(IsJoystickInitializedFlag))

                Joystick_Object = pygame.joystick.Joystick(IntegerID_TempIndex)
                Joystick_Object.init()

                Joystick_NameDetected = Joystick_Object.get_name()
                Joystick_IntegerIDdetected = Joystick_Object.get_id()
                Joystick_NumberOfAxesDetected = Joystick_Object.get_numaxes()
                Joystick_NumberOfButtonsDetected = Joystick_Object.get_numbuttons()
                Joystick_NumberOfHatsDetected = Joystick_Object.get_numhats()
                Joystick_NumberOfBallsDetected = Joystick_Object.get_numballs()

                Joystick_Object.quit()

                ###########################
                if PrintInfoForAllDetectedJoysticksFlag == 1:
                    self.MyPrint_WithoutLogFile("********************************************")
                    self.MyPrint_WithoutLogFile("AnalyzeAndInitializeJoystick, Joystick_NameDetected: " + str(Joystick_NameDetected))
                    self.MyPrint_WithoutLogFile("AnalyzeAndInitializeJoystick, Joystick_IntegerIDdetected: " + str(Joystick_IntegerIDdetected))
                    self.MyPrint_WithoutLogFile("AnalyzeAndInitializeJoystick, Joystick_NumberOfAxesDetected: " + str(Joystick_NumberOfAxesDetected))
                    self.MyPrint_WithoutLogFile("AnalyzeAndInitializeJoystick, Joystick_NumberOfButtonsDetected: " + str(Joystick_NumberOfButtonsDetected))
                    self.MyPrint_WithoutLogFile("AnalyzeAndInitializeJoystick, Joystick_NumberOfHatsDetected: " + str(Joystick_NumberOfHatsDetected))
                    self.MyPrint_WithoutLogFile("AnalyzeAndInitializeJoystick, Joystick_NumberOfBallsDetected: " + str(Joystick_NumberOfBallsDetected))
                    self.MyPrint_WithoutLogFile("********************************************")
                ###########################

                #########################################################

            #########################################################
            #########################################################

            #########################################################
            #########################################################
            for IntegerID_TempIndex in ListOfJoysticksToSearch: #In this second loop, open only the desired joystick.

                #########################################################
                Joystick_Object = pygame.joystick.Joystick(IntegerID_TempIndex)

                Joystick_Object.init()

                Joystick_NameDetected = Joystick_Object.get_name()
                Joystick_IntegerIDdetected = Joystick_Object.get_id()
                Joystick_NumberOfAxesDetected = Joystick_Object.get_numaxes()
                Joystick_NumberOfButtonsDetected = Joystick_Object.get_numbuttons()
                Joystick_NumberOfHatsDetected = Joystick_Object.get_numhats()
                Joystick_NumberOfBallsDetected = Joystick_Object.get_numballs()

                Joystick_Object.quit()

                NameMatchFlag = -1
                IntegerIDmatchFlag = -1

                ###########################
                if NameDesired != "": #Meaning that we really care what the name is
                    if Joystick_NameDetected.strip().find(NameDesired) != -1:
                        NameMatchFlag = 1
                    else:
                        NameMatchFlag = 0
                else:
                    NameMatchFlag = 1
                ###########################

                ###########################
                if IntegerIDdesired != -1: #Meaning that we really care what the IntegerID is
                    if IntegerIDdesired == Joystick_IntegerIDdetected:
                        IntegerIDmatchFlag = 1
                    else:
                        IntegerIDmatchFlag = 0
                else:
                    IntegerIDmatchFlag = 1
                ###########################

                ###########################
                if NameMatchFlag == 1 and IntegerIDmatchFlag == 1:

                    Joystick_Object = pygame.joystick.Joystick(Joystick_IntegerIDdetected)
                    Joystick_Object.init()

                    JoystickDictToReturn = dict([("Joystick_FoundAndOpenedFlag", 1),
                                                ("Joystick_Object", Joystick_Object),
                                                ("Joystick_NameDetected", Joystick_NameDetected),
                                                ("Joystick_IntegerIDdetected", Joystick_IntegerIDdetected),
                                                ("Joystick_NumberOfAxesDetected", Joystick_NumberOfAxesDetected),
                                                ("Joystick_NumberOfButtonsDetected", Joystick_NumberOfButtonsDetected),
                                                ("Joystick_NumberOfHatsDetected", Joystick_NumberOfHatsDetected),
                                                ("Joystick_NumberOfBallsDetected", Joystick_NumberOfBallsDetected)])

                    return JoystickDictToReturn
                ###########################

                #########################################################

            #########################################################
            #########################################################

        except:
            exceptions = sys.exc_info()[0]
            print("AnalyzeAndInitializeJoystick, Exceptions: %s" % exceptions)
            traceback.print_exc()
            return JoystickDictToReturn

        #########################################################
        #########################################################
        #########################################################

        return JoystickDictToReturn

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

    ##########################################################################################################
    ##########################################################################################################
    def Rumble(self, Rumble_LowFrequencyMotor_Strength0to1, Rumble_HighFrequencyMotor_Strength0to1, Rumble_DurationMilliseconds):

        try:

            if self.Joystick_FoundAndOpenedFlag == 1:
                Rumble_LowFrequencyMotor_Strength0to1 = self.LimitNumber_FloatOutputOnly(0.0, 1.0, Rumble_LowFrequencyMotor_Strength0to1)
                Rumble_HighFrequencyMotor_Strength0to1 = self.LimitNumber_FloatOutputOnly(0.0, 1.0, Rumble_HighFrequencyMotor_Strength0to1)
                Rumble_DurationMilliseconds = self.LimitNumber_IntOutputOnly(0.0, 1000000.0, Rumble_DurationMilliseconds)

                self.Joystick_Object.rumble(Rumble_LowFrequencyMotor_Strength0to1, Rumble_HighFrequencyMotor_Strength0to1, Rumble_DurationMilliseconds)

                #print("Rumble event issued!")

        except:
            exceptions = sys.exc_info()[0]
            print("Rumble, Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentDataDict(self):

        if self.EXIT_PROGRAM_FLAG == 0:

            return deepcopy(self.MostRecentDataDict) #deepcopy IS required (beyond .copy()) as MostRecentDataDict contains lists.

        else:
            return dict() #So that we're not returning variables during the close-down process.

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ResetButtonRisingEdgeEventLatch(self, ButtonIndex):

        try:
            ButtonIndex = int(ButtonIndex)

            if ButtonIndex in list(range(0, self.Joystick_NumberOfButtonsDetected)):
                self.Joystick_Button_LatchingRisingEdgeEvents_List[ButtonIndex] = 0
            else:
                print("ResetButtonRisingEdgeEventLatch ERROR: 'ButtonIndex' must be in the range [0, " + str(self.Joystick_NumberOfButtonsDetected) + "]")

        except:
            exceptions = sys.exc_info()[0]
            print("ResetButtonRisingEdgeEventLatch, ERROR with Exceptions: %s" % exceptions)
            #traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ResetHatRisingEdgeEventLatch(self, HatIndex, HatDirectionIndex):

        try:
            HatIndex = int(HatIndex)
            HatDirectionIndex = int(HatDirectionIndex)

            if HatIndex in list(range(0, self.Joystick_NumberOfHatsDetected)):
                if HatDirectionIndex in [0, 1]:
                    self.Joystick_Hat_LatchingRisingEdgeEvents_List[HatIndex][HatDirectionIndex] = 0
                else:
                    print("ResetHatRisingEdgeEventLatch ERROR: 'HatDirectionIndex' must be in the range [0, 1]")
            else:
                print("ResetHatRisingEdgeEventLatch ERROR: 'HatIndex' must be in the range [0," + str(self.Joystick_NumberOfHatsDetected) + "]")

        except:
            exceptions = sys.exc_info()[0]
            print("ResetHatRisingEdgeEventLatch, ERROR with Exceptions: %s" % exceptions)
            #traceback.print_exc()
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
            #traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ########################################################################################################## unicorn
    def MainThread(self):

        self.MyPrint_WithoutLogFile("Started MainThread for JoystickHID_ReubenPython2and3Class object.")
        
        self.MainThread_still_running_flag = 1

        self.StartingTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString()

        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            if self.Joystick_FoundAndOpenedFlag == 1:
                try:

                    ##########################################################################################################
                    self.CurrentTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromMainThread
                    ##########################################################################################################

                    ##########################################################################################################
                    pygame_event_list = pygame.event.get()
                    ##########################################################################################################
                    
                    ##########################################################################################################
                    for AxisIndex in range(self.Joystick_NumberOfAxesDetected):
                        self.Joystick_Axis_Value_List[AxisIndex] = self.Joystick_Object.get_axis(AxisIndex)
                    ##########################################################################################################

                    ##########################################################################################################
                    for ButtonIndex in range(self.Joystick_NumberOfButtonsDetected):
                        self.Joystick_Button_Value_List[ButtonIndex] = self.Joystick_Object.get_button(ButtonIndex)

                        if self.Joystick_Button_Value_List[ButtonIndex] != 0 and self.Joystick_Button_Value_List_Last[ButtonIndex] == 0:
                            self.Joystick_Button_LatchingRisingEdgeEvents_List[ButtonIndex] = self.Joystick_Button_Value_List[ButtonIndex]
                    ##########################################################################################################

                    ##########################################################################################################
                    for HatIndex in range(self.Joystick_NumberOfHatsDetected):
                        self.Joystick_Hat_Value_List[HatIndex] = self.Joystick_Object.get_hat(HatIndex)

                        for HatDirectionIndex in range(0, len(self.Joystick_Hat_Value_List[HatIndex])):
                            if self.Joystick_Hat_Value_List[HatIndex][HatDirectionIndex] != 0 and self.Joystick_Hat_Value_List_Last[HatIndex][HatDirectionIndex] == 0:
                                self.Joystick_Hat_LatchingRisingEdgeEvents_List[HatIndex][HatDirectionIndex] = self.Joystick_Hat_Value_List[HatIndex][HatDirectionIndex]
                    ##########################################################################################################

                    ##########################################################################################################
                    for BallIndex in range(self.Joystick_NumberOfBallsDetected):
                        self.Joystick_Ball_Value_List[BallIndex] = self.Joystick_Object.get_ball(BallIndex)
                    ##########################################################################################################

                    ##########################################################################################################
                    self.MostRecentDataDict = dict([("Joystick_Axis_Value_List", self.Joystick_Axis_Value_List),
                                                    ("Joystick_Button_Value_List", self.Joystick_Button_Value_List),
                                                    ("Joystick_Button_LatchingRisingEdgeEvents_List", self.Joystick_Button_LatchingRisingEdgeEvents_List),
                                                    ("Joystick_Hat_Value_List", self.Joystick_Hat_Value_List),
                                                    ("Joystick_Hat_LatchingRisingEdgeEvents_List", self.Joystick_Hat_LatchingRisingEdgeEvents_List),
                                                    ("Joystick_Ball_Value_List", self.Joystick_Ball_Value_List),
                                                    ("DataStreamingFrequency", self.DataStreamingFrequency_CalculatedFromMainThread),
                                                    ("Time", self.CurrentTime_CalculatedFromMainThread)])
                    ##########################################################################################################

                    ##########################################################################################################
                    self.Joystick_Axis_Value_List_Last = list(self.Joystick_Axis_Value_List)
                    self.Joystick_Button_Value_List_Last = list(self.Joystick_Button_Value_List)
                    self.Joystick_Hat_Value_List_Last = list(self.Joystick_Hat_Value_List)
                    self.Joystick_Ball_Value_List_Last = list(self.Joystick_Ball_Value_List)
                    ##########################################################################################################

                    ##########################################################################################################USE THE TIME.SLEEP() TO SET THE LOOP FREQUENCY
                    self.UpdateFrequencyCalculation_MainThread()

                    if self.MainThread_TimeToSleepEachLoop > 0.0:
                        time.sleep(self.MainThread_TimeToSleepEachLoop)
                    ##########################################################################################################

                except:
                    exceptions = sys.exc_info()[0]
                    print("JoystickHID_ReubenPython2and3Class MainThread " + self.Joystick_NameDetected + ", ID: " + str(self.Joystick_IntegerIDdetected) + ", Exceptions: %s" % exceptions, 0)
                    traceback.print_exc()

        ##########################################################################################################
        ##########################################################################################################

        self.MyPrint_WithoutLogFile("Finished MainThread for JoystickHID_ReubenPython2and3Class object.")
        
        self.MainThread_still_running_flag = 0
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for JoystickHID_ReubenPython2and3Class object")

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

        print("Starting the GUI_Thread for JoystickHID_ReubenPython2and3Class object.")

        ###################################################
        self.root = parent
        self.parent = parent
        ###################################################

        ###################################################
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
        ###################################################

        ###################################################
        self.TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150) #RGB
        self.TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150) #RGB
        self.TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
        self.TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
        ###################################################

        #################################################
        #################################################
        self.DeviceInfo_Label = Label(self.myFrame, text="Device Info", width=50)

        if self.Joystick_ShowJustDotMovingFlag == 0:
            self.DeviceInfo_Label.grid(row=0, column=0, padx=10, pady=10, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.Joystick2DdotDisplay_ReubenPython2and3ClassObject_GUIparametersDict = dict([("root", self.myFrame), ("GUI_ROW", 0), ("GUI_COLUMN", 1), ("GUI_PADX", 1), ("GUI_PADY", 1), ("GUI_ROWSPAN", 1), ("GUI_COLUMNSPAN", 1)])
        self.Joystick2DdotDisplay_ReubenPython2and3ClassObject_setup_dict = dict([("GUIparametersDict", self.Joystick2DdotDisplay_ReubenPython2and3ClassObject_GUIparametersDict)])
        self.Joystick2DdotDisplay_ReubenPython2and3ClassObject = Joystick2DdotDisplay_ReubenPython2and3Class(self.Joystick2DdotDisplay_ReubenPython2and3ClassObject_setup_dict)
        #################################################
        #################################################

        #################################################
        #################################################
        self.DataDisplay_Label = Label(self.myFrame, text="Debug Info", width=125)

        if self.Joystick_ShowJustDotMovingFlag == 0:
            self.DataDisplay_Label.grid(row=1, column=0, padx=10, pady=10, columnspan=2, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=125)

        if self.EnableInternal_MyPrint_Flag == 1 and self.Joystick_ShowJustDotMovingFlag == 0:
            self.PrintToGui_Label.grid(row=2, column=0, padx=10, pady=10, columnspan=2, rowspan=1)
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
                    self.DeviceInfo_Label["text"] = str(self.NameToDisplay_UserSet) +\
                                                     "\nJoystick Name: " + self.Joystick_NameDetected +\
                                                    "\nJoystick ID: " + str(self.Joystick_IntegerIDdetected) + \
                                                    "\nNumber of Axes: " + str(self.Joystick_NumberOfAxesDetected) + \
                                                    "\nNumber of Buttons: " + str(self.Joystick_NumberOfButtonsDetected) + \
                                                    "\nNumber of Hats: " + str(self.Joystick_NumberOfHatsDetected) + \
                                                    "\nNumber of Balls: " + str(self.Joystick_NumberOfBallsDetected)
                    #######################################################

                    #######################################################
                    DataDisplay_Label_TEMP = "Axes: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.Joystick_Axis_Value_List, 0, 3) +\
                                            "\nButtons: ["

                    #######
                    WrapLineButtonCounter = 0
                    for ButtonValue in self.Joystick_Button_Value_List:
                        DataDisplay_Label_TEMP = DataDisplay_Label_TEMP + str(ButtonValue) + ", "
                        WrapLineButtonCounter = WrapLineButtonCounter + 1
                        if WrapLineButtonCounter >= 50:
                            DataDisplay_Label_TEMP = DataDisplay_Label_TEMP + "\n"
                            WrapLineButtonCounter = 0

                    DataDisplay_Label_TEMP = DataDisplay_Label_TEMP[:-2] + "]"
                    #######

                    DataDisplay_Label_TEMP = DataDisplay_Label_TEMP + "\nButtons Latching: ["

                    #######
                    WrapLineButtonLatchingCounter = 0
                    for ButtonLatchingValue in self.Joystick_Button_LatchingRisingEdgeEvents_List:
                        DataDisplay_Label_TEMP = DataDisplay_Label_TEMP + str(ButtonLatchingValue) + ", "
                        WrapLineButtonLatchingCounter = WrapLineButtonLatchingCounter + 1
                        if WrapLineButtonLatchingCounter >= 50:
                            DataDisplay_Label_TEMP = DataDisplay_Label_TEMP + "\n"
                            WrapLineButtonLatchingCounter = 0

                    DataDisplay_Label_TEMP = DataDisplay_Label_TEMP[:-2] + "]"
                    #######

                    DataDisplay_Label_TEMP = DataDisplay_Label_TEMP + "\nHats: " + str(self.Joystick_Hat_Value_List) + \
                                                    "\nHats Latching: " + str(self.Joystick_Hat_LatchingRisingEdgeEvents_List) + \
                                                    "\nBalls: " + str(self.Joystick_Ball_Value_List) + \
                                                    "\nFrequency: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_CalculatedFromMainThread, 0, 3) + \
                                                    "\nTime: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.CurrentTime_CalculatedFromMainThread, 0, 3)

                    self.DataDisplay_Label["text"] = DataDisplay_Label_TEMP
                    #######################################################

                    #######################################################
                    self.Joystick2DdotDisplay_ReubenPython2and3ClassObject.UpdateDotCoordinatesAndDotColor(self.Joystick_Axis_Value_List[self.Joystick_Axis_Index_ToDisplayAsHorizontalAxisOn2DdotDisplay], self.Joystick_Axis_Value_List[self.Joystick_Axis_Index_ToDisplayAsVerticalAxisOn2DdotDisplay], self.Joystick_Button_Value_List[self.Joystick_Button_Index_ToDisplayAsDotColorOn2DdotDisplay])
                    self.Joystick2DdotDisplay_ReubenPython2and3ClassObject.GUI_update_clock()
                    #######################################################

                    #######################################################
                    self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                    #######################################################

                except:
                    exceptions = sys.exc_info()[0]
                    print("JoystickHID_ReubenPython2and3Class GUI_update_clock ERROR: Exceptions: %s" % exceptions)
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

