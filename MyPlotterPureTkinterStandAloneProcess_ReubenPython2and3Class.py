# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com,
www.reubotics.com

Apache 2 License
Software Revision J, 09/21/2022

Verified working on: Python 3.8 for Windows 8.1, 10 64-bit, Ubuntu 20.04, and Raspberry Pi Buster (no Mac testing yet).
THE SEPARATE-PROCESS-SPAWNING COMPONENT OF THIS CLASS IS NOT AVAILABLE IN PYTHON 2 DUE TO LIMITATION OF
"multiprocessing.set_start_method('spawn', force=True)" ONLY BEING AVAILABLE IN PYTHON 3. PLOTTING WITHIN A SINGLE PROCESS STILL WORKS.
'''

__author__ = 'reuben.brewer'

#########################################################
import os
import sys
import time
import datetime
import numpy
import multiprocessing
import collections
from copy import * #for deepcopy(dict)
import inspect #To enable 'TellWhichFileWereIn'
import traceback
import math
from decimal import Decimal
import threading
import psutil
import pexpect
import subprocess
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

#Tkinter releases: https://www.tcl.tk/software/tcltk/choose.html
#Shows new features in 8.6: https://www.tcl.tk/software/tcltk/8.6.html
#Complicated: https://tkdocs.com/tutorial/install.html
#WE'RE RUNNING TKINTER=8.6 ON RASPBERRY PI 4B

#print("Tkinter version: " + str(TkVersion))
#print("Tkinter.TclVersion = " + str(TclVersion))
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
    from future.builtins import input as input #"sudo pip3 install future" (Python 3) AND "sudo pip install future" (Python 2)
#########################################################

#########################################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
#########################################################

class MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class(Frame): #Subclass the Tkinter Frame

    ##########################################################################################################
    ##########################################################################################################
    def __init__(self, setup_dict):

        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0

        #########################################################
        #########################################################
        #########################################################
        if sys.version_info[0] >= 3:

            try: #MUST PUT IN TRY TO PREVENT ERROR, "raise RuntimeError('context has already been set')"
                multiprocessing_StartMethod = multiprocessing.get_start_method()
                print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: multiprocessing.get_start_method(): " + str(multiprocessing_StartMethod))
                if multiprocessing_StartMethod != "spawn":
                    print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: Issuing multiprocessing.set_start_method('spawn', force=True).")
                    multiprocessing.set_start_method('spawn', force=True) #'spawn' is required for all Linux flavors, with 'force=True' required specicially by Ubuntu (not Raspberry Pi).
            except:
                exceptions = sys.exc_info()[0]
                print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: multiprocessing.set_start_method('spawn', force=True) Exceptions: %s" % exceptions)

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
        self.job_for_another_core = multiprocessing.Process(target=self.StandAlonePlottingProcess,args=(self.MultiprocessingQueue_Rx, self.MultiprocessingQueue_Tx, setup_dict)) #args=(self.MultiprocessingQueue_Rx,)
        self.job_for_another_core.start()
        #########################################################
        #########################################################
        #########################################################

        #########################################################
        time.sleep(0.25)
        #########################################################

        #########################################################
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1
        #########################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ProcessSetupDictAndInitializeVariables(self, setup_dict):

        self.EXIT_PROGRAM_FLAG = 0

        ##########################################
        ##########################################
        if "GUIparametersDict" in setup_dict:
            self.GUIparametersDict = setup_dict["GUIparametersDict"]

            ##########################################
            if "GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents" in self.GUIparametersDict:
                self.GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents", self.GUIparametersDict["GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents"], 0.0, 1000.0))
            else:
                self.GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents = 15 #Will get us around 30Hz actual when plottting 2 curves with 100 data points each and 35 tick marks on each axis

            print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents: " + str(self.GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents))
            ##########################################

            ##########################################
            if "EnableInternal_MyPrint_Flag" in self.GUIparametersDict:
                self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", self.GUIparametersDict["EnableInternal_MyPrint_Flag"])
            else:
                self.EnableInternal_MyPrint_Flag = 0

            print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
            ##########################################

            ##########################################
            if "PrintToConsoleFlag" in self.GUIparametersDict:
                self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", self.GUIparametersDict["PrintToConsoleFlag"])
            else:
                self.PrintToConsoleFlag = 1

            print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
            ##########################################

            ##########################################
            if "NumberOfPrintLines" in self.GUIparametersDict:
                self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", self.GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
            else:
                self.NumberOfPrintLines = 10

            print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: NumberOfPrintLines: " + str(self.NumberOfPrintLines))
            ##########################################

            ##########################################
            if "GraphCanvasWidth" in self.GUIparametersDict:
                self.GraphCanvasWidth = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GraphCanvasWidth", self.GUIparametersDict["GraphCanvasWidth"], 0.0, 1920.0)
            else:
                self.GraphCanvasWidth = 640.0
    
            print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: GraphCanvasWidth: " + str(self.GraphCanvasWidth))
            ##########################################
    
            ##########################################
            if "GraphCanvasHeight" in self.GUIparametersDict:
                self.GraphCanvasHeight = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GraphCanvasHeight", self.GUIparametersDict["GraphCanvasHeight"], 0.0, 1080.0)
            else:
                self.GraphCanvasHeight = 480.0
    
            print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: GraphCanvasHeight: " + str(self.GraphCanvasHeight))
            ##########################################
    
            ##########################################
            if "GraphCanvasWindowStartingX" in self.GUIparametersDict:
                self.GraphCanvasWindowStartingX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GraphCanvasWindowStartingX", self.GUIparametersDict["GraphCanvasWindowStartingX"], 0.0, 1920.0))
            else:
                self.GraphCanvasWindowStartingX = 0.0
    
            print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: GraphCanvasWindowStartingX: " + str(self.GraphCanvasWindowStartingX))
            ##########################################
    
            ##########################################
            if "GraphCanvasWindowStartingY" in self.GUIparametersDict:
                self.GraphCanvasWindowStartingY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GraphCanvasWindowStartingY", self.GUIparametersDict["GraphCanvasWindowStartingY"], 0.0, 1080.0))
            else:
                self.GraphCanvasWindowStartingY = 0.0
    
            print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: GraphCanvasWindowStartingY: " + str(self.GraphCanvasWindowStartingY))
            ##########################################

            ##########################################
            if "GraphCanvasWindowTitle" in self.GUIparametersDict:
                self.GraphCanvasWindowTitle = str(self.GUIparametersDict["GraphCanvasWindowTitle"])
            else:
                self.GraphCanvasWindowTitle = "MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class"

            print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: GraphCanvasWindowTitle: " + self.GraphCanvasWindowTitle)
            ##########################################

        else:
            self.GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: No GUIparametersDict present, setting USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))

        #print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: GUIparametersDict: " + str(self.GUIparametersDict))
        ##########################################
        ##########################################

        ##########################################
        if "ParentPID" in setup_dict:
            self.ParentPID = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("ParentPID", setup_dict["ParentPID"], 0.0, 100000000.0))
        else:
            self.ParentPID = -11111

        print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: ParentPID: " + str(self.ParentPID))
        ##########################################

        ##########################################
        if "WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess" in setup_dict:
            self.WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess", setup_dict["WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess"], 0.0, 1000.0)
        else:
            self.WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess = 0.0

        print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess: " + str(self.WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess))
        ##########################################

        ##########################################
        if "CurvesToPlotNamesAndColorsDictOfLists" in setup_dict:
            self.CurvesToPlotNamesAndColorsDictOfLists = setup_dict["CurvesToPlotNamesAndColorsDictOfLists"]
        else:
            self.CurvesToPlotNamesAndColorsDictOfLists = dict([(list(), "NameList"),(list(), "ColorList")])

        print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: CurvesToPlotNamesAndColorsDictOfLists: " + str(self.CurvesToPlotNamesAndColorsDictOfLists))
        ##########################################

        ##########################################
        if "NumberOfDataPointToPlot" in setup_dict:
            self.NumberOfDataPointToPlot = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfDataPointToPlot", setup_dict["NumberOfDataPointToPlot"], 0.0, 1000000))
        else:
            self.NumberOfDataPointToPlot = 10

        print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: NumberOfDataPointToPlot: " + str(self.NumberOfDataPointToPlot))
        ##########################################

        ##########################################
        if "XaxisNumberOfTickMarks" in setup_dict:
            self.XaxisNumberOfTickMarks = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("XaxisNumberOfTickMarks", setup_dict["XaxisNumberOfTickMarks"], 0.0, 1000))
        else:
            self.XaxisNumberOfTickMarks = 30

        print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: XaxisNumberOfTickMarks: " + str(self.XaxisNumberOfTickMarks))
        ##########################################

        ##########################################
        if "YaxisNumberOfTickMarks" in setup_dict:
            self.YaxisNumberOfTickMarks = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("YaxisNumberOfTickMarks", setup_dict["YaxisNumberOfTickMarks"], 0.0, 1000))
        else:
            self.YaxisNumberOfTickMarks = 30

        print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: YaxisNumberOfTickMarks: " + str(self.YaxisNumberOfTickMarks))
        ##########################################

        ##########################################
        if "XaxisNumberOfDecimalPlacesForLabels" in setup_dict:
            self.XaxisNumberOfDecimalPlacesForLabels = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("XaxisNumberOfDecimalPlacesForLabels", setup_dict["XaxisNumberOfDecimalPlacesForLabels"], 0.0, 3.0))
        else:
            self.XaxisNumberOfDecimalPlacesForLabels = 1

        print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: XaxisNumberOfDecimalPlacesForLabels: " + str(self.XaxisNumberOfDecimalPlacesForLabels))
        ##########################################

        ##########################################
        if "YaxisNumberOfDecimalPlacesForLabels" in setup_dict:
            self.YaxisNumberOfDecimalPlacesForLabels = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("YaxisNumberOfDecimalPlacesForLabels", setup_dict["YaxisNumberOfDecimalPlacesForLabels"], 0.0, 3.0))
        else:
            self.YaxisNumberOfDecimalPlacesForLabels = 1

        print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: YaxisNumberOfDecimalPlacesForLabels: " + str(self.YaxisNumberOfDecimalPlacesForLabels))
        ##########################################

        ##########################################
        if "MarkerSize" in setup_dict:
            self.MarkerSize = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("MarkerSize", setup_dict["MarkerSize"], 0.0, 1080.0)
        else:
            self.MarkerSize = 2.0

        print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: MarkerSize: " + str(self.MarkerSize))
        ##########################################

        ##########################################
        if "X_min" in setup_dict:
            self.X_min = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("X_min", setup_dict["X_min"], -1000000000000.0, 1000000000000.0)
        else:
            self.X_min = 0.0

        print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: X_min: " + str(self.X_min))
        ##########################################

        ##########################################
        if "X_max" in setup_dict:
            self.X_max = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("X_max", setup_dict["X_max"], -1000000000000.0, 1000000000000.0)
        else:
            self.X_max = 10.0

        print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: X_max: " + str(self.X_max))
        ##########################################

        ##########################################
        if "Y_min" in setup_dict:
            self.Y_min = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("Y_min", setup_dict["Y_min"], -1000000000000.0, 1000000000000.0)
        else:
            self.Y_min = -10.0

        print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: Y_min: " + str(self.Y_min))
        ##########################################

        ##########################################
        if "Y_max" in setup_dict:
            self.Y_max = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("Y_max", setup_dict["Y_max"], -1000000000000.0, 1000000000000.0)
        else:
            self.Y_max = 10.0

        print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: Y_max: " + str(self.Y_max))
        ##########################################

        ##########################################
        if "XaxisAutoscaleFlag" in setup_dict:
            self.XaxisAutoscaleFlag = self.PassThrough0and1values_ExitProgramOtherwise("XaxisAutoscaleFlag", setup_dict["XaxisAutoscaleFlag"])
        else:
            self.XaxisAutoscaleFlag = 1

        print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: XaxisAutoscaleFlag: " + str(self.XaxisAutoscaleFlag))

        if self.XaxisAutoscaleFlag == 1:
            self.X_min = 0  # Have to override any other X_min, X_max values that may have been passed-in in the setup_dict
            self.X_max = 0.1  # Have to override any other X_min, X_max values that may have been passed-in in the setup_dict
        ##########################################

        ##########################################
        if "YaxisAutoscaleFlag" in setup_dict:
            self.YaxisAutoscaleFlag = self.PassThrough0and1values_ExitProgramOtherwise("YaxisAutoscaleFlag", setup_dict["YaxisAutoscaleFlag"])
        else:
            self.YaxisAutoscaleFlag = 1

        print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: YaxisAutoscaleFlag: " + str(self.YaxisAutoscaleFlag))

        if self.YaxisAutoscaleFlag == 1:
            self.Y_min = 0  # Have to override any other X_min, X_max values that may have been passed-in in the setup_dict
            self.Y_max = 0.1  # Have to override any other X_min, X_max values that may have been passed-in in the setup_dict
        ##########################################

        ##########################################
        if "XaxisDrawnAtBottomOfGraph" in setup_dict:
            self.XaxisDrawnAtBottomOfGraph = self.PassThrough0and1values_ExitProgramOtherwise("XaxisDrawnAtBottomOfGraph", setup_dict["XaxisDrawnAtBottomOfGraph"])
        else:
            self.XaxisDrawnAtBottomOfGraph = 1

        print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: XaxisDrawnAtBottomOfGraph: " + str(self.XaxisDrawnAtBottomOfGraph))
        ##########################################

        ##########################################
        if "ShowLegendFlag" in setup_dict:
            self.ShowLegendFlag = self.PassThrough0and1values_ExitProgramOtherwise("ShowLegendFlag", setup_dict["ShowLegendFlag"])
        else:
            self.ShowLegendFlag = 0

        print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: ShowLegendFlag: " + str(self.ShowLegendFlag))
        ##########################################

        ##########################################
        if "XaxisLabelString" in setup_dict:
            self.XaxisLabelString = str(setup_dict["XaxisLabelString"])
        else:
            self.XaxisLabelString = ""

        print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: XaxisLabelString: " + str(self.XaxisLabelString))
        ##########################################

        ##########################################
        if "YaxisLabelString" in setup_dict:
            self.YaxisLabelString = str(setup_dict["YaxisLabelString"])
        else:
            self.YaxisLabelString = ""

        print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: YaxisLabelString: " + str(self.YaxisLabelString))
        ##########################################

        ##########################################
        self.PrintToGui_Label_TextInputHistory_List = [" "]*self.NumberOfPrintLines
        self.PrintToGui_Label_TextInput_Str = ""
        self.GUI_ready_to_be_updated_flag = 0
        ##########################################

        ##########################################
        self.TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150) #RGB
        self.TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150) #RGB
        self.TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
        self.TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
        ##########################################

        self.GraphBoxOutline_X0 = 50 #Offset from the Canvas object so that there's room for the axis-labels UNICORN
        self.GraphBoxOutline_Y0 = 50 #Offset from the Canvas object so that there's room for the axis-labels UNICORN

        self.CurvesToPlotDictOfDicts = dict()

        ########## IT APPEARS THAT IF THE VARIABLE IS CREATED BY THE PARENT BEFORE THE CHILD, THEN THE CHILD KNOWS ABOUT IT.
        ########## HOWEVER, YOU CAN'T MODIFY IT, OUTSIDE OF THAT PROCESS.
        ##########################################
        if "NameList" in self.CurvesToPlotNamesAndColorsDictOfLists:
            NameList = self.CurvesToPlotNamesAndColorsDictOfLists["NameList"]
            if "ColorList" in self.CurvesToPlotNamesAndColorsDictOfLists:
                ColorList = self.CurvesToPlotNamesAndColorsDictOfLists["ColorList"]

                if len(NameList) == len(ColorList):
                    for counter, element in enumerate(NameList):
                        self.AddCurveToPlot(NameList[counter], ColorList[counter])
                else:
                    print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: Error, 'CurveList' and 'NameList' must be the same length in self.CurvesToPlotNamesAndColorsDictOfLists.")
                    return
            else:
                print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: Error, 'CurveList' key must be in self.CurvesToPlotNamesAndColorsDictOfLists.")
                return
        else:
            print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: Error, 'NameList' key must be in self.CurvesToPlotNamesAndColorsDictOfLists.")
            return
        ##########################################

        self.CurrentTime_CalculatedFromGUIthread = -11111.0
        self.LastTime_CalculatedFromGUIthread = -11111.0
        self.LoopFrequency_CalculatedFromGUIthread = -11111.0
        self.LoopDeltaT_CalculatedFromGUIthread = -11111.0

        self.CurrentTime_CalculatedFromStandAlonePlottingProcess = -11111.0
        self.LastTime_CalculatedFromStandAlonePlottingProcess = -11111.0
        self.LoopFrequency_CalculatedFromStandAlonePlottingProcess = -11111.0
        self.LoopDeltaT_CalculatedFromStandAlonePlottingProcess = -11111.0

        self.StandAlonePlottingProcess_ReadyForWritingFlag = 0

        self.MostRecentDataDict = dict()
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
    def WatchdogTimerCheck(self):

        #############################################
        if self.WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess > 0.0:
            if self.getPreciseSecondsTimeStampString() - self.LastTime_CalculatedFromStandAlonePlottingProcess >= self.WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess:
                print("***** MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, Watchdog fired! *****")
                self.EXIT_PROGRAM_FLAG = 1
        #############################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StandAlonePlottingProcess(self, MultiprocessingQueue_Rx_Local, MultiprocessingQueue_Tx_Local, setup_dict): #UNICORN

        print("Entering MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class StandAlonePlottingProcess.")

        self.ProcessSetupDictAndInitializeVariables(setup_dict)

        self.StartGUI()

        self.LastTime_CalculatedFromStandAlonePlottingProcess = self.getPreciseSecondsTimeStampString()

        self.StandAlonePlottingProcess_ReadyForWritingFlag = 1

        while self.EXIT_PROGRAM_FLAG == 0:

            #############################################
            try:

                #############################################
                self.WatchdogTimerCheck()
                #############################################

                #############################################
                while not MultiprocessingQueue_Rx_Local.empty():
                    try:

                        ###############
                        self.WatchdogTimerCheck()
                        ###############

                        ###############
                        self.CurrentTime_CalculatedFromStandAlonePlottingProcess = self.getPreciseSecondsTimeStampString()
                        #print("self.CurrentTime_CalculatedFromStandAlonePlottingProcess: " + str(self.CurrentTime_CalculatedFromStandAlonePlottingProcess))
                        self.UpdateFrequencyCalculation_CalculatedFromStandAlonePlottingProcess()
                        ###############

                        ###############
                        inputDict = MultiprocessingQueue_Rx_Local.get(FALSE)  #for queue, non-blocking with "FALSE" argument, could also use MultiprocessingQueue_Rx_Local.get_nowait() for non-blocking

                        ###############
                        if "EndStandAloneProcessFlag" in inputDict:
                            self.EXIT_PROGRAM_FLAG = 1

                        else:
                            CurveName = inputDict["CurveName"]
                            x = inputDict["x"]
                            y = inputDict["y"]

                            #print(str([x,y]))

                            self.AddPointOrListOfPointsToPlot(CurveName, x, y)
                        ###############

                    except:
                        exceptions = sys.exc_info()[0]
                        print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class StandAlonePlottingProcess, exceptions: %s" % exceptions)  # unicorn
                        traceback.print_exc()
                #############################################

                self.MostRecentDataDict = dict([("CurvesToPlotDictOfDicts", self.CurvesToPlotDictOfDicts),
                                                ("StandAlonePlottingProcess_ReadyForWritingFlag", self.StandAlonePlottingProcess_ReadyForWritingFlag)])

                #deepcopy is required (beyond .copy() ) because self.MostRecentDataDict contains a dict.
                MultiprocessingQueue_Tx_Local.put(deepcopy(self.MostRecentDataDict)) #unicorn

                time.sleep(0.005) #THIS IS THE MAGIC LINE THAT ALLOWS WORKING ON RASPBERRY-PI

            except:
                exceptions = sys.exc_info()[0]
                print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, exceptions: %s" % exceptions)  # unicorn
                traceback.print_exc()
            #############################################

        #############################################
        #############################################

        try:  # Need the try/except for if the StandAloneProcess window is closed before that of its parent which is still communicating with it.
            ############ Drain all remaining items in Queues OR ELSE THIS THREAD WON'T DRAIN.
            while not self.MultiprocessingQueue_Rx.empty():
                #print("DummyToDrainRemainingItemsInRxQueue")
                DummyToDrainRemainingItemsInRxQueue = self.MultiprocessingQueue_Rx.get(FALSE)
                time.sleep(0.001) #WITHOUT THIS SLEEP, THE PROGRAM WON'T TERMINATE CORRECTLY!

            while not self.MultiprocessingQueue_Tx.empty():
                #print("DummyToDrainRemainingItemsInTxQueue")
                DummyToDrainRemainingItemsInTxQueue = self.MultiprocessingQueue_Tx.get(FALSE)
                time.sleep(0.001) #WITHOUT THIS SLEEP, THE PROGRAM WON'T TERMINATE CORRECTLY!
            ############
        except:
            pass

        #############################################
        #############################################

        ############################################# EXPERIMENTAL Close GUI
        #self.end_program_GUI_callback() #DON'T USE THIS IN A MULTIPROCESSING CONTEXT. INSTEAD, MAKE GUI_THREAD A DAEMON THAT CLOSES AUTOMATICALLY WHEN THE PARENT THREAD CLOSES.
        #self.GUI_Thread_ThreadingObject.join()
        #############################################

        ############################################# EXPERIMENTAL Close job DON'T ISSUE THESE COMMANDS FROM THIS THREAD OR ELSE THERE WILL BE ERRORS
        #self.job_for_another_core.close()
        #self.job_for_another_core.join_thread()
        #self.job_for_another_core.terminate()
        #############################################

        print("Exited MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class.")
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def IsNumber0or1(self, InputNumber):

        if float(InputNumber) == 0.0 or float(InputNumber) == 1:
            return 1
        else:
            return 0

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
                InputTextToDisplay = "PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '"# + \
                          #InputNameString + \
                          #"' must be in the range [" + \
                          #str(RangeMinValue) + \
                          #", " + \
                          #str(RangeMaxValue) + \
                          #"] (value was " + \
                          #str(InputNumber_ConvertedToFloat) + "). Press any key (and enter) to exit."
                input(InputTextToDisplay)

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
    @staticmethod
    def RangeOfFloatNumberOfIncrements_PurePythonNoNumpy(StartValue, StopValue, NumberOfIndices):
        #Reuben modified from https://stackoverflow.com/questions/6683690/making-a-list-of-evenly-spaced-numbers-in-a-certain-range-in-python

        StartValue = float(StartValue) #Otherwise we'll get incorrect results sometimes.
        StopValue = float(StopValue)  # Otherwise we'll get incorrect results sometimes.
        NumberOfIndices = int(NumberOfIndices) #Range function only accepts ints

        #ListToReturn = [StopValue + x*(StartValue-StopValue)/(NumberOfIndices-1) for x in range(NumberOfIndices)] #Returns a list in the opposite order from what we want
        ListToReturn = [StopValue + x * (StartValue - StopValue) / (NumberOfIndices - 1) for x in range(NumberOfIndices-1, -1, -1)] #Have to change the range inputs to get the correct order in the list

        return ListToReturn
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    @staticmethod
    def RangeForFloats(start, stop, step, digits_to_round=3):
        u"""
        Works like range for doubles

        :param start: starting value
        :param stop: ending value
        :param step: the increment_value
        :param digits_to_round: the digits to which to round \
        (makes floating-point numbers much easier to work with)
        :return: generator
        """
        while start < stop:
            yield round(start, digits_to_round)
            start += step
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

        if self.MultiprocessingQueue_Tx.empty() != 1:
            return self.MultiprocessingQueue_Tx.get(FALSE)
        else:
            return dict()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_CalculatedFromGUIthread(self):

        try:
            self.LoopDeltaT_CalculatedFromGUIthread = self.CurrentTime_CalculatedFromGUIthread - self.LastTime_CalculatedFromGUIthread

            ##########################
            if self.LoopDeltaT_CalculatedFromGUIthread != 0.0:
                self.LoopFrequency_CalculatedFromGUIthread = 1.0/self.LoopDeltaT_CalculatedFromGUIthread
            ##########################

            self.LastTime_CalculatedFromGUIthread = self.CurrentTime_CalculatedFromGUIthread

        except:
            exceptions = sys.exc_info()[0]
            self.MyPrint_WithoutLogFile("UpdateFrequencyCalculation_CalculatedFromGUIthread ERROR, exceptions: %s" % exceptions)
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_CalculatedFromStandAlonePlottingProcess(self):

        try:
            self.LoopDeltaT_CalculatedFromStandAlonePlottingProcess = self.CurrentTime_CalculatedFromStandAlonePlottingProcess - self.LastTime_CalculatedFromStandAlonePlottingProcess

            ##########################
            if self.LoopDeltaT_CalculatedFromStandAlonePlottingProcess != 0.0:
                self.LoopFrequency_CalculatedFromStandAlonePlottingProcess = 1.0/self.LoopDeltaT_CalculatedFromStandAlonePlottingProcess
            ##########################

            self.LastTime_CalculatedFromStandAlonePlottingProcess = self.CurrentTime_CalculatedFromStandAlonePlottingProcess

        except:
            exceptions = sys.exc_info()[0]
            self.MyPrint_WithoutLogFile("UpdateFrequencyCalculation_CalculatedFromStandAlonePlottingProcess ERROR, exceptions: %s" % exceptions)
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def AddCurveToPlot(self, CurveName, Color):
        if CurveName not in self.CurvesToPlotDictOfDicts:
            self.CurvesToPlotDictOfDicts[CurveName] = (dict([("CurveName", CurveName), ("Color", Color), ("PointToDrawList", []), ("AddPointOrListOfPointsToPlot_TimeLastCalled", -11111.0)]))
            return 1
        else:
            self.MyPrint_WithoutLogFile("AddCurveToPlot ERROR: '" + CurveName + "' already in the CurvesToPlotDictOfDicts.")
            return 0
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SendEndCommandToStandAloneProcess(self):

        try:
            self.MultiprocessingQueue_Rx.put(dict([("EndStandAloneProcessFlag", 1)]))
        except:
            pass

    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## unicorn
    ##########################################################################################################
    def ExternalAddPointOrListOfPointsToPlot(self, CurveName, x, y):

        if self.IsInputList(CurveName) == 1:
            #####
            if len(CurveName) != len(x) or len(CurveName) != len(y):
                print("ExternalAddPointOrListOfPointsToPlot: ERROR, length of CurveName (" +
                      str(len(CurveName)) + "), x ("
                      + str(len(x)) + "), and y (" +
                      str(len(y)) + ") inputs must all match!")
            #####

            #####
            for index, CurveNameElement in enumerate(CurveName):
                self.MultiprocessingQueue_Rx.put(dict([("CurveName", CurveNameElement), ("x", x[index]), ("y", y[index])]))
            #####

        else:
            self.MultiprocessingQueue_Rx.put(dict([("CurveName", CurveName), ("x", x), ("y", y)]))

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def AddPointOrListOfPointsToPlot(self, CurveName, x, y):

        if self.IsInputList(x) == 0:
            x = list([x])
        if self.IsInputList(y) == 0:
            y = list([y])

        temp_AddPointOrListOfPointsToPlot_CurrentTime = self.getPreciseSecondsTimeStampString()

        if temp_AddPointOrListOfPointsToPlot_CurrentTime - self.CurvesToPlotDictOfDicts[CurveName]["AddPointOrListOfPointsToPlot_TimeLastCalled"] >= self.GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents/1000.0: #0.030

            if CurveName in self.CurvesToPlotDictOfDicts:
                ############################################
                for i in range(0, len(x)): #Cycle through points in list
                    #print("i: " + str(i) + ", x: " + str(x[i]) + ", y: " + str(y[i])) #unicorn
                    if len(self.CurvesToPlotDictOfDicts[CurveName]["PointToDrawList"]) < self.NumberOfDataPointToPlot:
                        self.CurvesToPlotDictOfDicts[CurveName]["PointToDrawList"].append([x[i],y[i]])
                    else:
                        self.CurvesToPlotDictOfDicts[CurveName]["PointToDrawList"].append(self.CurvesToPlotDictOfDicts[CurveName]["PointToDrawList"].pop(0))
                        self.CurvesToPlotDictOfDicts[CurveName]["PointToDrawList"][-1] = [x[i], y[i]]

                self.CurvesToPlotDictOfDicts[CurveName]["AddPointOrListOfPointsToPlot_TimeLastCalled"] = temp_AddPointOrListOfPointsToPlot_CurrentTime

                return 1
                ############################################
            else:
                self.MyPrint_WithoutLogFile("AddPointOrListOfPointsToPlot ERROR: '" + CurveName + "' not in CurvesToPlotDictOfDicts.")
                return 0
        else:
            self.MyPrint_WithoutLogFile("AddPointOrListOfPointsToPlot: ERROR, calling function too quickly (must be less frequently than GUI_RootAfterCallbackInterval_Milliseconds of " + str(self.GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents) + " ms).")

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class object")

        self.EXIT_PROGRAM_FLAG = 1

        self.SendEndCommandToStandAloneProcess()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StartGUI(self):

        self.GUI_Thread_ThreadingObject = threading.Thread(target=self.GUI_Thread)
        self.GUI_Thread_ThreadingObject.setDaemon(True) #Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
        self.GUI_Thread_ThreadingObject.start()

        time.sleep(0.15)
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_Thread(self):

        ###################################################
        self.root = Tk()
        ###################################################

        ###################################################
        self.myFrame = Frame(self.root)
        self.myFrame.grid()
        ###################################################

        ###################################################
        ###################################################
        self.root.title(self.GraphCanvasWindowTitle)
        self.root.protocol("WM_DELETE_WINDOW", self.ExitProgram_Callback)
        self.root.after(self.GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents, self.__GUI_update_clock)
        self.root.geometry('%dx%d+%d+%d' % (self.GraphCanvasWidth, self.GraphCanvasHeight+20, self.GraphCanvasWindowStartingX, self.GraphCanvasWindowStartingY)) #+20 for debug_label
        ###################################################
        ###################################################

        ################################################### SET THE DEFAULT FONT FOR ALL WIDGETS CREATED AFTTER/BELOW THIS CALL
        ###################################################
        default_font = tkFont.nametofont("TkDefaultFont") #TkTextFont, TkFixedFont
        default_font.configure(size=8)
        self.root.option_add("*Font", default_font)
        ###################################################
        ###################################################

        #################################################
        self.CanvasForDrawingGraph = Canvas(self.myFrame, width=self.GraphCanvasWidth, height=self.GraphCanvasHeight, bg="white")
        self.CanvasForDrawingGraph["highlightthickness"] = 0  # Remove light grey border around the Canvas
        self.CanvasForDrawingGraph["bd"] = 0 #Setting "bd", along with "highlightthickness" to 0 makes the Canvas be in the (0,0) pixel location instead of offset by those thicknesses
        '''
        From https://stackoverflow.com/questions/4310489/how-do-i-remove-the-light-grey-border-around-my-canvas-widget
        The short answer is, the Canvas has two components which affect the edges: the border (borderwidth attribute) and highlight ring (highlightthickness attribute).
        If you have a border width of zero and a highlight thickness of zero, the canvas coordinates will begin at 0,0. Otherwise, these two components of the canvas infringe upon the coordinate space.
        What I most often do is set these attributes to zero. Then, if I actually want a border I'll put that canvas inside a frame and give the frame a border.
        '''

        self.CanvasForDrawingGraph.grid(row=0, column=0)
        #################################################

        #################################################
        self.debug_label = Label(self.myFrame, text="debug_label", width=100)
        self.debug_label.grid(row=1, column=0, padx=0, pady=0, columnspan=1, rowspan=10)
        #################################################

        #################################################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=100)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=0, column=3, padx=0, pady=0, columnspan=1, rowspan=10)
        #################################################

        #################################################
        self.myFrame["bg"] = "white"
        self.debug_label["bg"] = "white"
        self.PrintToGui_Label["bg"] = "white"
        #################################################

        #################################################
        #################################################
        #################################################

        self.GUI_ready_to_be_updated_flag = 1

        self.root.mainloop() #THIS MUST BE THE LAST LINE IN THE GUI THREAD SETUP BECAUSE IT'S BLOCKING!!!!

        #self.root.quit()  # Stop the GUI thread. This is the normal call we'd make for a multithreaded application, but it doesn't work when we're doing a stand-along process!
        #self.root.destroy()  # Close down the GUI thread, MUST BE CALLED FROM GUI_Thread. This is the normal call we'd make for a multithreaded application, but it doesn't work when we're doing a stand-along process!

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ConvertMathPointToCanvasCoordinates(self, PointListXY):

        x = PointListXY[0]
        y = PointListXY[1]

        W = self.GraphCanvasWidth*0.8 # #If we use the whole width, then we'll clip labels, tick marks, etc. UNICORN
        H = self.GraphCanvasHeight*0.9 # #If we use the whole width, then we'll clip labels, tick marks, etc. UNICORN

        m_Xaxis = ((W - self.GraphBoxOutline_X0)/(self.X_max - self.X_min))
        b_Xaxis = W - m_Xaxis*self.X_max

        X_out = m_Xaxis*x + b_Xaxis


        m_Yaxis = ((H - self.GraphBoxOutline_Y0) / (self.Y_max - self.Y_min))
        b_Yaxis = H - m_Yaxis * self.Y_max

        Y_out = m_Yaxis * y + b_Yaxis


        X_out = X_out
        Y_out = self.GraphCanvasHeight - Y_out #Flip y-axis

        return [X_out, Y_out]
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DrawLineBetween2pointListsInMathCoordinates(self, PointListXY0_MathCoord, PointListXY1_MathCoord):

        PointListXY0_CanvasCoord = self.ConvertMathPointToCanvasCoordinates(PointListXY0_MathCoord)
        PointListXY1_CanvasCoord = self.ConvertMathPointToCanvasCoordinates(PointListXY1_MathCoord)

        #print("PointListXY0_MathCoord: " + str(PointListXY0_MathCoord) + ", Transformed to PointListXY0_CanvasCoord: " + str(PointListXY0_CanvasCoord))
        #print("PointListXY1_MathCoord: " + str(PointListXY1_MathCoord) + ", Transformed to PointListXY1_CanvasCoord: " + str(PointListXY1_CanvasCoord))

        self.CanvasForDrawingGraph.create_line(PointListXY0_CanvasCoord[0],
                                               PointListXY0_CanvasCoord[1],
                                               PointListXY1_CanvasCoord[0],
                                               PointListXY1_CanvasCoord[1],
                                               fill=u"black")
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DrawAxes(self, temp_CurvesToPlotDictOfDicts, temp_X_min, temp_X_max, temp_Y_min, temp_Y_max):

        #################################################### Compute axis tick-mark locations
        XaxisTickMarksList = self.RangeOfFloatNumberOfIncrements_PurePythonNoNumpy(temp_X_min, temp_X_max, self.XaxisNumberOfTickMarks)
        YaxisTickMarksList = self.RangeOfFloatNumberOfIncrements_PurePythonNoNumpy(temp_Y_min, temp_Y_max, self.YaxisNumberOfTickMarks)
        ####################################################

        #################################################### Compute where to place the X axis
        if self.XaxisDrawnAtBottomOfGraph == 1:
            XaxisVerticalCoord_MathCoord = temp_Y_min #Draw x-axis at the bottom of the graph
        else:
            XaxisVerticalCoord_MathCoord = 0.0 #Draw x-axis at the zero-crossing of the y-axis
        ####################################################

        #################################################### Draw the axes
        self.DrawLineBetween2pointListsInMathCoordinates([temp_X_min, XaxisVerticalCoord_MathCoord], [temp_X_max, XaxisVerticalCoord_MathCoord]) #Draw X-axis
        self.DrawLineBetween2pointListsInMathCoordinates([temp_X_min, temp_Y_min], [temp_X_min, temp_Y_max]) #Draw Y-axis at the left of the graph
        ####################################################

        #################################################### Draw axis labels (NOT tick mark labels)
        XaxisLabelStartX_MathCoord = temp_X_min + 1.1*abs(temp_X_max - temp_X_min)
        XaxisLabelStartY_MathCoord = temp_Y_min
        [XaxisLabelStartX_CanvasCoord, XaxisLabelStartY_CanvasCoord] = self.ConvertMathPointToCanvasCoordinates([XaxisLabelStartX_MathCoord, XaxisLabelStartY_MathCoord])
        self.CanvasForDrawingGraph.create_text(XaxisLabelStartX_CanvasCoord, XaxisLabelStartY_CanvasCoord, text=self.XaxisLabelString, font="Helvetica 12 bold")

        YaxisLabelStartX_MathCoord = temp_X_min + 0.05*abs(temp_X_max - temp_X_min)
        YaxisLabelStartY_MathCoord = temp_Y_min + 1.05*abs(temp_Y_max - temp_Y_min)
        [YaxisLabelStartX_CanvasCoord, YaxisLabelStartY_CanvasCoord] = self.ConvertMathPointToCanvasCoordinates([YaxisLabelStartX_MathCoord, YaxisLabelStartY_MathCoord])
        self.CanvasForDrawingGraph.create_text(YaxisLabelStartX_CanvasCoord, YaxisLabelStartY_CanvasCoord, text=self.YaxisLabelString, font="Helvetica 12 bold")
        ####################################################

        #################################################### Compute info for tick-mark line and label placement
        #Must compute tick-mark length of X and Y axes separately as they scale differently
        XaxisTickMarkLength_MathCoord = 0.01 * abs(temp_Y_max - temp_Y_min)
        YaxisTickMarkLength_MathCoord = 0.01 * abs(temp_X_max - temp_X_min)

        YaxisTickMarkLabelXcoord_MathCoord = temp_X_min-0.03*abs(temp_X_max - temp_X_min)
        XaxisTickMarkLabelYcoord_MathCoord = XaxisVerticalCoord_MathCoord-0.03*abs(temp_Y_max - temp_Y_min)
        ####################################################

        #################################################### Draw X-axis tick marks AND labels
        for x in XaxisTickMarksList:
            self.DrawLineBetween2pointListsInMathCoordinates([x, XaxisVerticalCoord_MathCoord - XaxisTickMarkLength_MathCoord], [x, XaxisVerticalCoord_MathCoord + XaxisTickMarkLength_MathCoord])#For drawing the x-axis at the bottom of the graph

            LabelPoint = self.ConvertMathPointToCanvasCoordinates([x, XaxisTickMarkLabelYcoord_MathCoord])
            self.CanvasForDrawingGraph.create_text(LabelPoint[0], LabelPoint[1], fill=u"black", text=round(Decimal(x), self.XaxisNumberOfDecimalPlacesForLabels), font="Helvetica 7") #font="Times 20 italic bold", angle=90, #, width=1 WILL FORCE WRAPPING
        ####################################################

        #################################################### Draw Y-axis tick marks AND labels
        for y in YaxisTickMarksList:
            self.DrawLineBetween2pointListsInMathCoordinates([temp_X_min - YaxisTickMarkLength_MathCoord, y], [temp_X_min + YaxisTickMarkLength_MathCoord, y])
            LabelPoint = self.ConvertMathPointToCanvasCoordinates([YaxisTickMarkLabelXcoord_MathCoord, y])
            self.CanvasForDrawingGraph.create_text(LabelPoint[0], LabelPoint[1], fill=u"black", text=round(Decimal(y), self.YaxisNumberOfDecimalPlacesForLabels), font="Helvetica 7") #font="Times 20 italic bold", angle=90
        ####################################################

        #################################################### Draw legend
        if self.ShowLegendFlag == 1:
            CurveNameLabelsStartX_MathCoord = temp_X_min + 1.1*abs(temp_X_max - temp_X_min)
            CurveNameLabelsStartY_MathCoord = temp_Y_min + 0.5*abs(temp_Y_max - temp_Y_min)

            [CurveNameLabelsStartX_CanvasCoord, CurveNameLabelsStartY_CanvasCoord] = self.ConvertMathPointToCanvasCoordinates([CurveNameLabelsStartX_MathCoord, CurveNameLabelsStartY_MathCoord])

            LabelCounter = 0
            for CurveName in temp_CurvesToPlotDictOfDicts:
                self.CanvasForDrawingGraph.create_text(CurveNameLabelsStartX_CanvasCoord, CurveNameLabelsStartY_CanvasCoord + LabelCounter*20, fill=temp_CurvesToPlotDictOfDicts[CurveName]["Color"], text=temp_CurvesToPlotDictOfDicts[CurveName]["CurveName"], font="Helvetica 12 bold") #font="Times 20 italic bold", angle=90
                LabelCounter = LabelCounter + 1
        ####################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateNewXandYlimits(self, temp_CurvesToPlotDictOfDicts, temp_X_min, temp_X_max, temp_Y_min, temp_Y_max):

        X_min_NEW = temp_X_min
        X_max_NEW = temp_X_max
        Y_min_NEW = temp_Y_min
        Y_max_NEW = temp_Y_max

        temp_AllPointsXlist = list()
        temp_AllPointsYlist = list()
        for CurveName in temp_CurvesToPlotDictOfDicts:
            TempListOfPointToDrawForThisCurve = temp_CurvesToPlotDictOfDicts[CurveName]["PointToDrawList"]

            for temp_Point in TempListOfPointToDrawForThisCurve:
                temp_AllPointsXlist.append(temp_Point[0])
                temp_AllPointsYlist.append(temp_Point[1])


        if len(temp_AllPointsXlist) > 0:
            #print temp_AllPointsXlist

            X_min_temp = min(temp_AllPointsXlist)
            X_max_temp = max(temp_AllPointsXlist)
            Y_min_temp = min(temp_AllPointsYlist)
            Y_max_temp = max(temp_AllPointsYlist)

            if X_min_temp != X_max_temp and self.XaxisAutoscaleFlag == 1:
                X_min_NEW = X_min_temp
                X_max_NEW = X_max_temp

            if Y_min_temp != Y_max_temp and self.YaxisAutoscaleFlag == 1:
                Y_min_NEW = Y_min_temp
                Y_max_NEW = Y_max_temp

        # print("X_min_NEW: " + str(X_min_NEW) + ", X_max_NEW: " + str(X_max_NEW) + ", Len: " + str(len(TempListOfPointToDraw)))
        # print("Y_min_NEW: " + str(Y_min_NEW) + ", Y_max_NEW: " + str(Y_max_NEW) + ", Len: " + str(len(TempListOfPointToDraw)))

        return [X_min_NEW, X_max_NEW, Y_min_NEW, Y_max_NEW]
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DrawOnePoint_MathCoord(self, PointToDraw_MathCoord, Color="Black"):

        PointToDraw_CanvasCoord = self.ConvertMathPointToCanvasCoordinates(PointToDraw_MathCoord)

        self.CanvasForDrawingGraph.create_oval(PointToDraw_CanvasCoord[0] - self.MarkerSize,
                                               PointToDraw_CanvasCoord[1] - self.MarkerSize,
                                               PointToDraw_CanvasCoord[0] + self.MarkerSize,
                                               PointToDraw_CanvasCoord[1] + self.MarkerSize,
                                               fill=Color,
                                               outline=Color)
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DrawAllPoints_MathCoord(self, temp_CurvesToPlotDictOfDicts):

        for CurveName in temp_CurvesToPlotDictOfDicts:

            TempListOfPointToDraw = temp_CurvesToPlotDictOfDicts[CurveName]["PointToDrawList"]
            TempColor = temp_CurvesToPlotDictOfDicts[CurveName]["Color"]

            if len(TempListOfPointToDraw) > 0:
                ########################
                for PointToDraw_MathCoord in TempListOfPointToDraw:
                    self.DrawOnePoint_MathCoord(PointToDraw_MathCoord, TempColor)
                ########################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ########################################################################################################## UNICORN def GUI
    def __GUI_update_clock(self): #THIS FUNCTION NEEDS TO BE CALLED INTERNALLY BY THE CLASS, NOT EXTERNALLY LIKE WE NORMALLY DO BECAUSE WE'RE FIRING THESE ROOT.AFTER CALLBACKS FASTER THAN THE PARENT ROOT GUI

        if self.EXIT_PROGRAM_FLAG == 0:

            if self.GUI_ready_to_be_updated_flag == 1:

                #######################################################
                self.CurrentTime_CalculatedFromGUIthread = self.getPreciseSecondsTimeStampString()
                #print("self.CurrentTime_CalculatedFromGUIthread: " + str(self.CurrentTime_CalculatedFromGUIthread ))
                #######################################################

                #######################################################
                self.CanvasForDrawingGraph.delete(u'all')

                #################  #Make local copy so that adding new points from external program won't change anything mid-plotting.
                temp_CurvesToPlotDictOfDicts = dict(self.CurvesToPlotDictOfDicts)
                temp_X_min = float(self.X_min)
                temp_X_max = float(self.X_max)
                temp_Y_min = float(self.Y_min)
                temp_Y_max = float(self.Y_max)
                #################

                [self.X_min, self.X_max, self.Y_min, self.Y_max] = self.UpdateNewXandYlimits(temp_CurvesToPlotDictOfDicts, temp_X_min, temp_X_max, temp_Y_min, temp_Y_max) #temp_X_min, temp_X_max, temp_Y_min, temp_Y_max

                temp_X_min = float(self.X_min)
                temp_X_max = float(self.X_max)
                temp_Y_min = float(self.Y_min)
                temp_Y_max = float(self.Y_max)

                self.DrawAxes(temp_CurvesToPlotDictOfDicts, temp_X_min, temp_X_max, temp_Y_min, temp_Y_max) #self.X_min, self.X_max, self.Y_min, self.Y_max

                self.DrawAllPoints_MathCoord(temp_CurvesToPlotDictOfDicts)
                #######################################################

                ####################################################### TEST AREA FOR PLOTTING KNOWN POINTS
                '''
                self.DrawOnePoint_MathCoord([self.X_min, self.Y_min], "Green")
                self.DrawOnePoint_MathCoord([self.X_min, self.Y_max], "Green")
                self.DrawOnePoint_MathCoord([self.X_max, self.Y_min], "Green")
                self.DrawOnePoint_MathCoord([self.X_max, self.Y_max], "Green")
                '''
                #######################################################

                #######################################################
                self.debug_label["text"] = "ParentPID = " + str(self.ParentPID) + \
                                           ", PlottingPID = " + str(os.getpid()) + \
                                           ", GUI Time: " + str(self.CurrentTime_CalculatedFromGUIthread) +\
                                            ", GUI Frequency: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.LoopFrequency_CalculatedFromGUIthread, 0, 3)
                #######################################################

                #######################################################
                self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                #######################################################

                #######################################################
                self.UpdateFrequencyCalculation_CalculatedFromGUIthread()
                #######################################################

                #time.sleep(0.001)

            #######################################################
            self.root.after(self.GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents, self.__GUI_update_clock)
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