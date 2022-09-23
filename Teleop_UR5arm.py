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

#########################################################
#https://github.com/Reuben-Brewer/UR5arm_ReubenPython2and3Class
import SharedGlobals_Teleop_UR5arm

#https://github.com/Reuben-Brewer/MyPrint_ReubenPython2and3Class
from MyPrint_ReubenPython2and3Class import *

#https://github.com/Reuben-Brewer/UR5arm_ReubenPython2and3Class
from UR5arm_ReubenPython2and3Class import *

#https://github.com/Reuben-Brewer/JoystickHID_ReubenPython2and3Class
from JoystickHID_ReubenPython2and3Class import *

#https://github.com/Reuben-Brewer/LowPassFilter_ReubenPython2and3Class
from LowPassFilter_ReubenPython2and3Class import *

#https://github.com/Reuben-Brewer/MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class
from MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class import *

try:
    #https://stackoverflow.com/questions/5286210/is-there-a-way-to-access-parent-modules-in-python/45895490
    #Get the name of the file that's importing this one.
    ParentModuleName = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__'].__file__
    if ParentModuleName.find("Teleop_UR5arm.py") != -1:

        ############################
        try:
            #https://github.com/Reuben-Brewer/ZEDasHandController_ReubenPython2and3Class
            from ZEDasHandController_ReubenPython2and3Class import *
            print("@@@@@@@@@@ ParentModuleName: " + str(ParentModuleName) + " successfully imported ZEDasHandController_ReubenPython2and3Class @@@@@@@@@@")

        except:
            exceptions = sys.exc_info()[0]
            print("@@@@@@@@@@ ParentModuleName: " + str(ParentModuleName) + " FAILED to import ZEDasHandController_ReubenPython2and3Class @@@@@@@@@@, Exceptions: %s" % exceptions)
        ############################

        ############################
        try:
            #https://github.com/Reuben-Brewer/RobotiqGripper2F85_ReubenPython2and3Class
            from RobotiqGripper2F85_ReubenPython2and3Class import *
            print("@@@@@@@@@@ ParentModuleName: " + str(ParentModuleName) + " successfully imported RobotiqGripper2F85_ReubenPython2and3Class @@@@@@@@@@")

        except:
            exceptions = sys.exc_info()[0]
            print("@@@@@@@@@@ ParentModuleName: " + str(ParentModuleName) + " FAILED to import RobotiqGripper2F85_ReubenPython2and3Class @@@@@@@@@@, Exceptions: %s" % exceptions)
        ############################

except:
    exceptions = sys.exc_info()[0]
    print("@@@@@@@@@@ ParentModuleName imports failed, Exceptions: %s" % exceptions)

#########################################################

#########################################################
import os
import sys
import platform
import time
import datetime
import threading
import collections
from copy import * #for deep_copy of dicts
import json
import keyboard #"sudo pip install keyboard" https://pypi.org/project/keyboard/, https://github.com/boppreh/keyboard
import subprocess #for beep command line call
import numpy
import re
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
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
#########################################################

#######################################################################################################################
#######################################################################################################################
global ParametersToBeLoaded_Directory_Windows
ParametersToBeLoaded_Directory_Windows = os.getcwd().replace("\\", "//") + "//ParametersToBeLoaded"

global LogFile_Directory_Windows
LogFile_Directory_Windows = os.getcwd().replace("\\", "//") + "//Logs"

global ParametersToBeLoaded_Directory_LinuxNonRaspberryPi
ParametersToBeLoaded_Directory_LinuxNonRaspberryPi = os.getcwd().replace("\\", "//") + "//ParametersToBeLoaded"

global LogFile_Directory_LinuxNonRaspberryPi
LogFile_Directory_LinuxNonRaspberryPi = os.getcwd().replace("\\", "//") + "//Logs"

global ParametersToBeLoaded_Directory_Mac
ParametersToBeLoaded_Directory_Mac = os.getcwd().replace("\\", "//") + "//ParametersToBeLoaded"

global LogFile_Directory_Mac
LogFile_Directory_Mac = os.getcwd().replace("\\", "//") + "//Logs"
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def LoadAndParseJSONfile_UseClassesFlags():
    global ParametersToBeLoaded_UseClassesFlags_Dict

    #################################
    JSONfilepathFull_UseClassesFlags = ParametersToBeLoaded_Directory_TO_BE_USED + "//ParametersToBeLoaded_UseClassesFlags.json"

    #def LoadAndParseJSONfile_AddDictKeysToGlobalsDict(GlobalsDict, JSONfilepathFull, USE_PassThrough0and1values_ExitProgramOtherwise_FOR_FLAGS = 0, PrintResultsFlag = 0):
    ParametersToBeLoaded_UseClassesFlags_Dict = LoadAndParseJSONfile_AddDictKeysToGlobalsDict(globals(), JSONfilepathFull_UseClassesFlags, 1, 1)
    #################################

    #################################
    if USE_GUI_FLAG_ARGV_OVERRIDE != -1:
        USE_GUI_FLAG = USE_GUI_FLAG_ARGV_OVERRIDE
    else:
        USE_GUI_FLAG = PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG", ParametersToBeLoaded_UseClassesFlags_Dict["USE_GUI_FLAG"])
    #################################

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def LoadAndParseJSONfile_GUIsettings():
    global ParametersToBeLoaded_GUIsettings_Dict

    #################################
    JSONfilepathFull_GUIsettings = ParametersToBeLoaded_Directory_TO_BE_USED + "//ParametersToBeLoaded_GUIsettings.json"

    #def LoadAndParseJSONfile_AddDictKeysToGlobalsDict(GlobalsDict, JSONfilepathFull, USE_PassThrough0and1values_ExitProgramOtherwise_FOR_FLAGS = 0, PrintResultsFlag = 0):
    ParametersToBeLoaded_GUIsettings_Dict = LoadAndParseJSONfile_AddDictKeysToGlobalsDict(globals(), JSONfilepathFull_GUIsettings, 1, 1)
    #################################

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def LoadAndParseJSONfile_Plotter():
    global ParametersToBeLoaded_Plotter_Dict

    #################################
    JSONfilepathFull_Plotter = ParametersToBeLoaded_Directory_TO_BE_USED + "//ParametersToBeLoaded_Plotter.json"

    #def LoadAndParseJSONfile_AddDictKeysToGlobalsDict(GlobalsDict, JSONfilepathFull, USE_PassThrough0and1values_ExitProgramOtherwise_FOR_FLAGS = 0, PrintResultsFlag = 0):
    ParametersToBeLoaded_Plotter_Dict = LoadAndParseJSONfile_AddDictKeysToGlobalsDict(globals(), JSONfilepathFull_Plotter, 1, 1)
    #################################

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def LoadAndParseJSONfile_UR5():
    global ParametersToBeLoaded_UR5_Dict

    #################################
    JSONfilepathFull_UR5arm = ParametersToBeLoaded_Directory_TO_BE_USED + "//ParametersToBeLoaded_UR5arm.json"

    #def LoadAndParseJSONfile_AddDictKeysToGlobalsDict(GlobalsDict, JSONfilepathFull, USE_PassThrough0and1values_ExitProgramOtherwise_FOR_FLAGS = 0, PrintResultsFlag = 0):
    ParametersToBeLoaded_UR5_Dict = LoadAndParseJSONfile_AddDictKeysToGlobalsDict(globals(), JSONfilepathFull_UR5arm, 1, 1)
    #################################

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def LoadAndParseJSONfile_ZEDasHandController():
    global ParametersToBeLoaded_ZEDasHandController_Dict

    #################################
    JSONfilepathFull_ZEDasHandController = ParametersToBeLoaded_Directory_TO_BE_USED + "//ParametersToBeLoaded_ZEDasHandController.json"

    #def LoadAndParseJSONfile_AddDictKeysToGlobalsDict(GlobalsDict, JSONfilepathFull, USE_PassThrough0and1values_ExitProgramOtherwise_FOR_FLAGS = 0, PrintResultsFlag = 0):
    ParametersToBeLoaded_ZEDasHandController_Dict = LoadAndParseJSONfile_AddDictKeysToGlobalsDict(globals(), JSONfilepathFull_ZEDasHandController, 1, 1)
    #################################

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def LoadAndParseJSONfile_RobotiqGripper2F85():
    global ParametersToBeLoaded_RobotiqGripper2F85_Dict

    #################################
    JSONfilepathFull_RobotiqGripper2F85 = ParametersToBeLoaded_Directory_TO_BE_USED + "//ParametersToBeLoaded_RobotiqGripper2F85.json"

    #def LoadAndParseJSONfile_AddDictKeysToGlobalsDict(GlobalsDict, JSONfilepathFull, USE_PassThrough0and1values_ExitProgramOtherwise_FOR_FLAGS = 0, PrintResultsFlag = 0):
    ParametersToBeLoaded_RobotiqGripper2F85_Dict = LoadAndParseJSONfile_AddDictKeysToGlobalsDict(globals(), JSONfilepathFull_RobotiqGripper2F85, 1, 1)
    #################################

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def LoadAndParseJSONfile_Keyboard():
    global ParametersToBeLoaded_Keyboard_Dict
    global Keyboard_KeysToTeleopControlsMapping_DictOfDicts_FormattedAsNicelyPrintedString
    global Keyboard_KeysToTeleopControlsMapping_DictOfDicts

    #################################
    JSONfilepathFull_Keyboard = ParametersToBeLoaded_Directory_TO_BE_USED + "//ParametersToBeLoaded_Keyboard.json"

    #def LoadAndParseJSONfile_AddDictKeysToGlobalsDict(GlobalsDict, JSONfilepathFull, USE_PassThrough0and1values_ExitProgramOtherwise_FOR_FLAGS = 0, PrintResultsFlag = 0):
    ParametersToBeLoaded_Keyboard_Dict = LoadAndParseJSONfile_AddDictKeysToGlobalsDict(globals(), JSONfilepathFull_Keyboard, 1, 1)
    #################################

    Keyboard_KeysToTeleopControlsMapping_DictOfDicts_FormattedAsNicelyPrintedString = ConvertDictToProperlyFormattedStringForPrinting(Keyboard_KeysToTeleopControlsMapping_DictOfDicts, NumberOfDecimalsPlaceToUse = 2, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 1)

    SharedGlobals_Teleop_UR5arm.Keyboard_KeysToTeleopControlsMapping_DictOfDicts = Keyboard_KeysToTeleopControlsMapping_DictOfDicts

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def LoadAndParseJSONfile_Joystick():
    global ParametersToBeLoaded_Joystick_Dict
    global Joystick_AxisHatButtonOrBallTo6DOFposeMapping_ListOfDicts_FormattedAsNicelyPrintedString

    #################################
    JSONfilepathFull_Joystick = ParametersToBeLoaded_Directory_TO_BE_USED + "//ParametersToBeLoaded_Joystick.json"

    #def LoadAndParseJSONfile_AddDictKeysToGlobalsDict(GlobalsDict, JSONfilepathFull, USE_PassThrough0and1values_ExitProgramOtherwise_FOR_FLAGS = 0, PrintResultsFlag = 0):
    ParametersToBeLoaded_Joystick_Dict = LoadAndParseJSONfile_AddDictKeysToGlobalsDict(globals(), JSONfilepathFull_Joystick, 1, 1)
    #################################

    Joystick_AxisHatButtonOrBallTo6DOFposeMapping_ListOfDicts_FormattedAsNicelyPrintedString = ""
    for Index, Value in enumerate(Joystick_AxisHatButtonOrBallTo6DOFposeMapping_ListOfDicts):
        Joystick_AxisHatButtonOrBallTo6DOFposeMapping_ListOfDicts_FormattedAsNicelyPrintedString = Joystick_AxisHatButtonOrBallTo6DOFposeMapping_ListOfDicts_FormattedAsNicelyPrintedString + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(Value, 0, 2) + "\n"

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def LoadAndParseJSONfile_ControlLawParameters():
    global ParametersToBeLoaded_ControlLawParameters_Dict

    #################################
    JSONfilepathFull_ControlLawParameters = ParametersToBeLoaded_Directory_TO_BE_USED + "//ParametersToBeLoaded_ControlLawParameters.json"

    #def LoadAndParseJSONfile_AddDictKeysToGlobalsDict(GlobalsDict, JSONfilepathFull, USE_PassThrough0and1values_ExitProgramOtherwise_FOR_FLAGS = 0, PrintResultsFlag = 0):
    ParametersToBeLoaded_ControlLawParameters_Dict = LoadAndParseJSONfile_AddDictKeysToGlobalsDict(globals(), JSONfilepathFull_ControlLawParameters, 1, 1)
    #################################

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def LoadAndParseJSONfile_AddDictKeysToGlobalsDict(GlobalsDict, JSONfilepathFull, USE_PassThrough0and1values_ExitProgramOtherwise_FOR_FLAGS = 0, PrintResultsFlag = 0):

    try:
        #################################

        ##############
        with open(JSONfilepathFull) as ParametersToBeLoaded_JSONfileObject:
            ParametersToBeLoaded_JSONfileParsedIntoDict = json.load(ParametersToBeLoaded_JSONfileObject)

        ParametersToBeLoaded_JSONfileObject.close()
        ##############

        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        ##############
        for key, value in ParametersToBeLoaded_JSONfileParsedIntoDict.items():
            if USE_PassThrough0and1values_ExitProgramOtherwise_FOR_FLAGS == 1:
                if key.upper().find("_FLAG") != -1:
                    GlobalsDict[key] = PassThrough0and1values_ExitProgramOtherwise(key, value)
                else:
                    GlobalsDict[key] = value
            else:
                GlobalsDict[key] = value

            if PrintResultsFlag == 1:
                print(key + ": " + str(value))

        ##############
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

        return ParametersToBeLoaded_JSONfileParsedIntoDict
        #################################
    except:
        #################################
        exceptions = sys.exc_info()[0]
        print("LoadAndParseJSONfile_Advanced Error, Exceptions: %s" % exceptions)
        return dict()
        #################################

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def ParseColonCommaSeparatedVariableString(line, print_line_flag = 0, numeric_values_only = 0):

    if print_line_flag == 1:
        print("ParseColonCommaSeparatedVariableString input: " + line)

    line_as_dict = dict()

    if len(line) > 0:
        try:
            line = line.replace("\n", "").replace("\r", "")
            line_as_list = filter(None, re.split("[,:]+", line))
            #print(line_as_list)

            toggle_counter = 0
            key = ""
            for element in line_as_list:
                if toggle_counter == 0:  # Every other element is a key, every other element is the value
                    key = element.strip()
                    toggle_counter = 1
                else:
                    if numeric_values_only == 1:
                        try:
                            line_as_dict[key] = float(element)
                            #print(key + " , " + element)
                        except:
                            line_as_dict[key] = "ERROR"
                    else:
                        line_as_dict[key] = element
                    toggle_counter = 0

            return line_as_dict
        except:
            exceptions = sys.exc_info()[0]
            print("ParseColonCommaSeparatedVariableString ERROR: Exceptions: %s" % exceptions)
            traceback.print_exc()
            return line_as_dict
    else:
        print("ParseColonCommaSeparatedVariableString WARNING: input string was zero-length")
        return line_as_dict
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def CreateNewDirectoryIfItDoesntExist(directory):
    try:
        #print("CreateNewDirectoryIfItDoesntExist, directory: " + directory)
        if os.path.isdir(directory) == 0: #No directory with this name exists
            os.makedirs(directory)
    except:
        exceptions = sys.exc_info()[0]
        print("CreateNewDirectoryIfItDoesntExist, Exceptions: %s" % exceptions)
        traceback.print_exc()
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def CreateCSVfileForTrajectoryDataAndStartWritingData():
    global CSVfileForTrajectoryData_FileObject
    global CSVfileForTrajectoryData_SaveFlag
    global CSVfileForTrajectoryData_DirectoryPath
    global CSVfileForTrajectoryData_FilepathFull
    global UR5arm_MostRecentDict_ToolVectorActual_SnapshotAtTimeOfCreatingCSVfileForTrajectoryData
    global UR5arm_Zero_UR5arm_MostRecentDict_ToolVectorActual_WhenCreatingCSVfileForTrajectoryData_Flag

    try:
        if UR5arm_Zero_UR5arm_MostRecentDict_ToolVectorActual_WhenCreatingCSVfileForTrajectoryData_Flag == 1:
            UR5arm_MostRecentDict_ToolVectorActual_SnapshotAtTimeOfCreatingCSVfileForTrajectoryData = SharedGlobals_Teleop_UR5arm.UR5arm_MostRecentDict_ToolVectorActual
        else:
            UR5arm_MostRecentDict_ToolVectorActual_SnapshotAtTimeOfCreatingCSVfileForTrajectoryData = [0.0]*6

        CSVfileForTrajectoryData_FilepathFull = CSVfileForTrajectoryData_DirectoryPath + "//ZEDlog_" + getTimeStampString() + ".csv"

        CSVfileForTrajectoryData_FileObject = open(CSVfileForTrajectoryData_FilepathFull, "a") #Will append to file if it exists, create new file with this as first entry if file doesn't exist.
        CSVfileForTrajectoryData_FileObject.write("Time, ZED_X, ZED_Y, ZED_Z, UR5arm_X, UR5arm_Y, UR5arm_Z, UR5arm_Rx, UR5arm_Ry, UR5arm_Rz" + "\n")

        CSVfileForTrajectoryData_SaveFlag = 1

        print("CreateCSVfileForTrajectoryDataAndStartWritingData: Opened file " + CSVfileForTrajectoryData_FilepathFull + " and started writing data!")

    except:
        exceptions = sys.exc_info()[0]
        print("CreateCSVfileForTrajectoryDataAndStartWritingData, Exceptions: %s" % exceptions)
        traceback.print_exc()

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def CloseCSVfileForTrajectoryDataAndStopWritingData():
    global CSVfileForTrajectoryData_FileObject
    global CSVfileForTrajectoryData_SaveFlag
    global CSVfileForTrajectoryData_DirectoryPath
    global CSVfileForTrajectoryData_FilepathFull

    try:
        CSVfileForTrajectoryData_SaveFlag = 0

        CSVfileForTrajectoryData_FileObject.close()

        print("CloseCSVfileForTrajectoryDataAndStopWritingData: Closed file " + CSVfileForTrajectoryData_FilepathFull + " and stopped writing data!")

    except:
        exceptions = sys.exc_info()[0]
        print("CloseCSVfileForTrajectoryDataAndStopWritingData, Exceptions: %s" % exceptions)
        traceback.print_exc()

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

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
                ListOfStringsToJoin.append(ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

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
                ListOfStringsToJoin.append("TUPLE" + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

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
                ListOfStringsToJoin.append(str(Key) + ": " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

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

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def ConvertDictToProperlyFormattedStringForPrinting(DictToPrint, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3):

    ProperlyFormattedStringForPrinting = ""
    ItemsPerLineCounter = 0

    for Key in DictToPrint:

        if isinstance(DictToPrint[Key], dict): #RECURSION
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                 Key + ":\n" + \
                                                 ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key], NumberOfDecimalsPlaceToUse, NumberOfEntriesPerLine, NumberOfTabsBetweenItems)

        else:
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                 Key + ": " + \
                                                 ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key], 0, NumberOfDecimalsPlaceToUse)

        if ItemsPerLineCounter < NumberOfEntriesPerLine - 1:
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\t"*NumberOfTabsBetweenItems
            ItemsPerLineCounter = ItemsPerLineCounter + 1
        else:
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\n"
            ItemsPerLineCounter = 0

    return ProperlyFormattedStringForPrinting
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def getPreciseSecondsTimeStampString():
    ts = time.time()

    return ts
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def getTimeStampString():

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%m_%d_%Y---%H_%M_%S')

    return st
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def ExitProgram_Callback():

    print("ExitProgram_Callback event fired!")

    SharedGlobals_Teleop_UR5arm.EXIT_PROGRAM_FLAG = 1
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def PassThrough0and1values_ExitProgramOtherwise(InputNameString, InputNumber):

    try:
        InputNumber_ConvertedToFloat = float(InputNumber)
    except:
        exceptions = sys.exc_info()[0]
        print("PassThrough0and1values_ExitProgramOtherwise Error. InputNumber for variable_name '" + InputNameString + "' must be a float value, Exceptions: %s" % exceptions)
        input("Press any key to continue")
        sys.exit()

    try:
        if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1:
            return InputNumber_ConvertedToFloat
        else:
            input("PassThrough0and1values_ExitProgramOtherwise Error. '" + InputNameString + "' must be 0 or 1 (value was " + str(InputNumber_ConvertedToFloat) + "). Press any key (and enter) to exit.")
            sys.exit()
    except:
        exceptions = sys.exc_info()[0]
        print("PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
        input("Press any key to continue")
        sys.exit()
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def PassThroughFloatValuesInRange_ExitProgramOtherwise(InputNameString, InputNumber, RangeMinValue, RangeMaxValue):
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
            input("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" + InputNameString + "' must be in the range [" + str(RangeMinValue) + ", " + str(RangeMaxValue) + "] (value was " + str(InputNumber_ConvertedToFloat) + "). Press any key (and enter) to exit.")
            sys.exit()
    except:
        exceptions = sys.exc_info()[0]
        print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
        input("Press any key to continue")
        sys.exit()
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def TimerCallbackFunctionWithFunctionAsArgument_SingleShot_NoParenthesesAfterFunctionName(CallbackAfterDeltaTseconds, FunctionToCall_NoParenthesesAfterFunctionName, ArgumentListToFunction):

    TimerObject = threading.Timer(CallbackAfterDeltaTseconds, FunctionToCall_NoParenthesesAfterFunctionName, ArgumentListToFunction) #Must pass arguments to callback-function via list as the third argument to Timer call
    TimerObject.daemon = True #Without the daemon=True, this recursive function won't terminate when the main program does.
    TimerObject.start()

    print("TimerCallbackFunctionWithFunctionAsArgument_SingleShot_NoParenthesesAfterFunctionName event fired to call function: '" + str(FunctionToCall_NoParenthesesAfterFunctionName.__name__) + "' at time " + str(getPreciseSecondsTimeStampString()))

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def UpdateFrequencyCalculation(LoopCounter, CurrentTime, LastTime, DataStreamingFrequency, DataStreamingDeltaT):

    try:

        DataStreamingDeltaT = CurrentTime - LastTime

        ##########################
        if DataStreamingDeltaT != 0.0:
            DataStreamingFrequency = 1.0/DataStreamingDeltaT
        ##########################

        LastTime = CurrentTime

        LoopCounter = LoopCounter + 1

        return [LoopCounter, LastTime, DataStreamingFrequency, DataStreamingDeltaT]

    except:
        exceptions = sys.exc_info()[0]
        print("UpdateFrequencyCalculation, exceptions: %s" % exceptions)
        return [-11111.0]*4
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def LimitNumber_FloatOutputOnly(min_val, max_val, test_val):
    if test_val > max_val:
        test_val = max_val

    elif test_val < min_val:
        test_val = min_val

    else:
        test_val = test_val

    test_val = float(test_val)

    return test_val
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def LimitNumber_IntOutputOnly(min_val, max_val, test_val):
    if test_val > max_val:
        test_val = max_val

    elif test_val < min_val:
        test_val = min_val

    else:
        test_val = test_val

    test_val = int(test_val)

    return test_val
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def LimitTextEntryInput(min_val, max_val, test_val, TextEntryObject):

    test_val = float(test_val)  # MUST HAVE THIS LINE TO CATCH STRINGS PASSED INTO THE FUNCTION

    if test_val > max_val:
        test_val = max_val
    elif test_val < min_val:
        test_val = min_val
    else:
        test_val = test_val

    if TextEntryObject != "":
        if isinstance(TextEntryObject, list) == 1:  # Check if the input 'TextEntryObject' is a list or not
            TextEntryObject[0].set(str(test_val))  # Reset the text, overwriting the bad value that was entered.
        else:
            TextEntryObject.set(str(test_val))  # Reset the text, overwriting the bad value that was entered.

    return test_val
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def GetMyPlatform():
    my_platform = "other"

    if platform.system() == "Linux":

        if "raspberrypi" in platform.uname():  # os.uname() doesn't work in windows
            my_platform = "pi"
        else:
            my_platform = "linux"

    elif platform.system() == "Windows":
        my_platform = "windows"

    elif platform.system() == "Darwin":
        my_platform = "mac"

    else:
        my_platform = "other"

    print("The OS platform is: " + my_platform)

    return my_platform
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def ParseARGV_USE_GUI_and_SOFTWARE_LAUNCH_METHOD():

    try:
        USE_GUI_FLAG_ARGV_OVERRIDE = -1
        SOFTWARE_LAUNCH_METHOD = -1

        if len(sys.argv) >= 2:
            ARGV_1 = sys.argv[1].strip().lower()

            print("ARGV_1: " + str(ARGV_1))
            ARGV_1_ParsedDict = ParseColonCommaSeparatedVariableString(ARGV_1)

            if "use_gui_flag" in ARGV_1_ParsedDict:
                USE_GUI_FLAG_ARGV_OVERRIDE = PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG_ARGV_OVERRIDE", int(ARGV_1_ParsedDict["use_gui_flag"]))

            if "software_launch_method" in ARGV_1_ParsedDict:
                SOFTWARE_LAUNCH_METHOD = ARGV_1_ParsedDict["software_launch_method"]

    except:
        exceptions = sys.exc_info()[0]
        print("Parsing ARGV_1, exceptions: %s" % exceptions)
        traceback.print_exc()
        time.sleep(0.25)

    #print("ARGV_1, USE_GUI_FLAG_ARGV_OVERRIDE: " + str(USE_GUI_FLAG_ARGV_OVERRIDE))
    #print("ARGV_1, SOFTWARE_LAUNCH_METHOD: " + str(SOFTWARE_LAUNCH_METHOD))

    return [USE_GUI_FLAG_ARGV_OVERRIDE, SOFTWARE_LAUNCH_METHOD]

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def IsTheTimeCurrentlyAM():
    ts = time.time()
    hour = int(datetime.datetime.fromtimestamp(ts).strftime('%H'))
    if hour < 12:
        return 1
    else:
        return 0
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def KeyboardMapKeysToCallbackFunctions():

    keyboard.unhook_all() #Remove all current mappings

    ###############################################
    for AxisNameAsKey in SharedGlobals_Teleop_UR5arm.Keyboard_KeysToTeleopControlsMapping_DictOfDicts:

            KeyToTeleopControlsMappingDict = SharedGlobals_Teleop_UR5arm.Keyboard_KeysToTeleopControlsMapping_DictOfDicts[AxisNameAsKey]

            KeyName = KeyToTeleopControlsMappingDict["KeyName"]
            OnPressCallbackFunctionNameString = KeyToTeleopControlsMappingDict["OnPressCallbackFunctionNameString"]
            OnReleaseCallbackFunctionNameString = KeyToTeleopControlsMappingDict["OnReleaseCallbackFunctionNameString"]

            if OnPressCallbackFunctionNameString in globals():
                keyboard.on_press_key(KeyName, globals()[OnPressCallbackFunctionNameString])

            if OnReleaseCallbackFunctionNameString in globals():
                keyboard.on_release_key(KeyName, globals()[OnReleaseCallbackFunctionNameString])

    ###############################################

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def DedicatedKeyboardListeningThread():

    print("Started DedicatedKeyboardListeningThread for UR5arm_ReubenPython2and3Class object.")
    SharedGlobals_Teleop_UR5arm.DedicatedKeyboardListeningThread_StillRunningFlag = 1

    SharedGlobals_Teleop_UR5arm.StartingTime_CalculatedFromDedicatedKeyboardListeningThread = getPreciseSecondsTimeStampString()

    ###############################################
    while SharedGlobals_Teleop_UR5arm.EXIT_PROGRAM_FLAG == 0:
        try:
            ###############################################
            SharedGlobals_Teleop_UR5arm.CurrentTime_CalculatedFromDedicatedKeyboardListeningThread = getPreciseSecondsTimeStampString() - SharedGlobals_Teleop_UR5arm.StartingTime_CalculatedFromDedicatedKeyboardListeningThread
            ###############################################

            ###############################################
            if SharedGlobals_Teleop_UR5arm.BeepNeedsToBePlayedFlag_RecordNewWaypoint_JointSpace == 1:
                if platform.system() == "Windows":
                    winsound.Beep(int(4000), int(500))
                else:
                    try:
                        shell_response = subprocess.check_output("paplay //home//pi//Desktop//Teleop_UR5arm_PythonDeploymentFiles//ParametersToBeLoaded//point.wav", shell=True)
                    except:
                        exceptions = sys.exc_info()[0]
                        print("ERROR BEEPING ON RASPBERRY PI, Exceptions: %s" % exceptions)

                SharedGlobals_Teleop_UR5arm.BeepNeedsToBePlayedFlag_RecordNewWaypoint_JointSpace = 0
            ###############################################

            ###############################################
            if SharedGlobals_Teleop_UR5arm.BeepNeedsToBePlayedFlag_RecordNewWaypoint_CartesianSpace == 1:
                if platform.system() == "Windows":
                    winsound.Beep(int(8000), int(500))
                else:
                    try:
                        shell_response = subprocess.check_output("paplay //home//pi//Desktop//Teleop_UR5arm_PythonDeploymentFiles//ParametersToBeLoaded//point.wav", shell=True)
                    except:
                        exceptions = sys.exc_info()[0]
                        print("ERROR BEEPING ON RASPBERRY PI, Exceptions: %s" % exceptions)

                SharedGlobals_Teleop_UR5arm.BeepNeedsToBePlayedFlag_RecordNewWaypoint_CartesianSpace = 0
            ###############################################

            ############################################### USE THE TIME.SLEEP() TO SET THE LOOP FREQUENCY
            ###############################################
            ###############################################
            if SharedGlobals_Teleop_UR5arm.DedicatedKeyboardListeningThread_TimeToSleepEachLoop > 0.0:
                time.sleep(SharedGlobals_Teleop_UR5arm.DedicatedKeyboardListeningThread_TimeToSleepEachLoop)
            ###############################################
            ###############################################
            ###############################################

        except:
            exceptions = sys.exc_info()[0]
            print("DedicatedKeyboardListeningThread, Exceptions: %s" % exceptions)
            traceback.print_exc()
    ###############################################

    print("Exited DedicatedKeyboardListeningThread.")
    SharedGlobals_Teleop_UR5arm.DedicatedKeyboardListeningThread_StillRunningFlag = 0
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def KeyPressResponse_RecordNewWaypoint_JointSpace(event):

    KeyPressResponse_RecordNewWaypoint_JointSpace_TextToPrint = ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(SharedGlobals_Teleop_UR5arm.UR5arm_MostRecentDict_JointAngleList_Deg, 0, 5)
    KeyPressResponse_RecordNewWaypoint_JointSpace_TextToPrint = KeyPressResponse_RecordNewWaypoint_JointSpace_TextToPrint.replace("+","")
    print(KeyPressResponse_RecordNewWaypoint_JointSpace_TextToPrint)

    SharedGlobals_Teleop_UR5arm.BeepNeedsToBePlayedFlag_RecordNewWaypoint_JointSpace = 1

    #print("KeyPressResponse_RecordNewWaypoint_JointSpace event fired!")
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def KeyPressResponse_RecordNewWaypoint_CartesianSpace(event):

    KeyPressResponse_RecordNewWaypoint_CartesianSpace_TextToPrint = ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(SharedGlobals_Teleop_UR5arm.UR5arm_MostRecentDict_ToolVectorActual, 0, 5)
    KeyPressResponse_RecordNewWaypoint_CartesianSpace_TextToPrint = KeyPressResponse_RecordNewWaypoint_CartesianSpace_TextToPrint.replace("+","")
    print(KeyPressResponse_RecordNewWaypoint_CartesianSpace_TextToPrint)

    SharedGlobals_Teleop_UR5arm.BeepNeedsToBePlayedFlag_RecordNewWaypoint_CartesianSpace = 1

    #print("KeyPressResponse_RecordNewWaypoint_CartesianSpace event fired!")
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def KeyPressResponse_ZEDcontrolClutch_START(event):

    SharedGlobals_Teleop_UR5arm.KeyPressResponse_ZEDcontrolClutch_State = 1

    #print("KeyPressResponse_ZEDcontrolClutch_START event fired!")
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def KeyPressResponse_ZEDcontrolClutch_STOP(event):

    SharedGlobals_Teleop_UR5arm.KeyPressResponse_ZEDcontrolClutch_State = 0

    #print("KeyPressResponse_ZEDcontrolClutch_STOP event fired!")
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def KeyPressResponse_IncrementURtoolTipInX_START(event):

    SharedGlobals_Teleop_UR5arm.KeyPressResponse_IncrementURtoolTipInX_NeedsToBeChangedFlag = 1

    #print("KeyPressResponse_IncrementURtoolTipInX_START event fired!")
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def KeyPressResponse_IncrementURtoolTipInX_STOP(event):

    SharedGlobals_Teleop_UR5arm.KeyPressResponse_IncrementURtoolTipInX_NeedsToBeChangedFlag = 0

    #print("KeyPressResponse_IncrementURtoolTipInX_STOP event fired!")
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def KeyPressResponse_DecrementURtoolTipInX_START(event):

    SharedGlobals_Teleop_UR5arm.KeyPressResponse_DecrementURtoolTipInX_NeedsToBeChangedFlag = 1

    #print("KeyPressResponse_DecrementURtoolTipInX_START event fired!")
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def KeyPressResponse_DecrementURtoolTipInX_STOP(event):

    SharedGlobals_Teleop_UR5arm.KeyPressResponse_DecrementURtoolTipInX_NeedsToBeChangedFlag = 0

    #print("KeyPressResponse_DecrementURtoolTipInX_STOP event fired!")
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def KeyPressResponse_IncrementURtoolTipInY_START(event):

    SharedGlobals_Teleop_UR5arm.KeyPressResponse_IncrementURtoolTipInY_NeedsToBeChangedFlag = 1

    #print("KeyPressResponse_IncrementURtoolTipInY_START event fired!")
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def KeyPressResponse_IncrementURtoolTipInY_STOP(event):

    SharedGlobals_Teleop_UR5arm.KeyPressResponse_IncrementURtoolTipInY_NeedsToBeChangedFlag = 0

    #print("KeyPressResponse_IncrementURtoolTipInY_STOP event fired!")
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def KeyPressResponse_DecrementURtoolTipInY_START(event):

    SharedGlobals_Teleop_UR5arm.KeyPressResponse_DecrementURtoolTipInY_NeedsToBeChangedFlag = 1

    #print("KeyPressResponse_DecrementURtoolTipInY_START event fired!")
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def KeyPressResponse_DecrementURtoolTipInY_STOP(event):

    SharedGlobals_Teleop_UR5arm.KeyPressResponse_DecrementURtoolTipInY_NeedsToBeChangedFlag = 0

    #print("KeyPressResponse_DecrementURtoolTipInY_STOP event fired!")
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def KeyPressResponse_IncrementURtoolTipInZ_START(event):

    SharedGlobals_Teleop_UR5arm.KeyPressResponse_IncrementURtoolTipInZ_NeedsToBeChangedFlag = 1

    #print("KeyPressResponse_IncrementURtoolTipInZ_START event fired!")
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def KeyPressResponse_IncrementURtoolTipInZ_STOP(event):

    SharedGlobals_Teleop_UR5arm.KeyPressResponse_IncrementURtoolTipInZ_NeedsToBeChangedFlag = 0

    #print("KeyPressResponse_IncrementURtoolTipInZ_STOP event fired!")
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def KeyPressResponse_DecrementURtoolTipInZ_START(event):

    SharedGlobals_Teleop_UR5arm.KeyPressResponse_DecrementURtoolTipInZ_NeedsToBeChangedFlag = 1

    #print("KeyPressResponse_DecrementURtoolTipInZ_START event fired!")
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def KeyPressResponse_DecrementURtoolTipInZ_STOP(event):

    SharedGlobals_Teleop_UR5arm.KeyPressResponse_DecrementURtoolTipInZ_NeedsToBeChangedFlag = 0

    #print("KeyPressResponse_DecrementURtoolTipInZ_STOP event fired!")
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def KeyPressResponse_OpenRobotiqGripper2F85_START(event):

    SharedGlobals_Teleop_UR5arm.KeyPressResponse_OpenRobotiqGripper2F85_NeedsToBeChangedFlag = 1

    #print("KeyPressResponse_OpenRobotiqGripper2F85_START event fired!")
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def KeyPressResponse_OpenRobotiqGripper2F85_STOP(event):

    SharedGlobals_Teleop_UR5arm.KeyPressResponse_OpenRobotiqGripper2F85_NeedsToBeChangedFlag = 0

    #print("KeyPressResponse_OpenRobotiqGripper2F85_STOP event fired!")
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def KeyPressResponse_CloseRobotiqGripper2F85_START(event):

    SharedGlobals_Teleop_UR5arm.KeyPressResponse_CloseRobotiqGripper2F85_NeedsToBeChangedFlag = 1

    #print("KeyPressResponse_CloseRobotiqGripper2F85_START event fired!")
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def KeyPressResponse_CloseRobotiqGripper2F85_STOP(event):

    SharedGlobals_Teleop_UR5arm.KeyPressResponse_CloseRobotiqGripper2F85_NeedsToBeChangedFlag = 0

    #print("KeyPressResponse_CloseRobotiqGripper2F85_STOP event fired!")
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def GUI_update_clock():
    global root
    global USE_GUI_FLAG
    global GUI_RootAfterCallbackInterval_Milliseconds
    global TKinter_LightRedColor
    global TKinter_LightGreenColor
    global TKinter_LightBlueColor
    global TKinter_LightYellowColor
    global TKinter_DefaultGrayColor

    global CurrentTime_CalculatedFromMainThread
    global DataStreamingFrequency_CalculatedFromMainThread

    global UR5arm_ReubenPython2and3ClassObject
    global UR5arm_OPEN_FLAG
    global SHOW_IN_GUI_UR5arm_MostRecentDict_FLAG
    global UR5arm_ToolVectorActual_ToBeSet
    global UR5arm_MostRecentDict_Label
    global UR5arm_MostRecentDict

    global RobotiqGripper2F85_Position_ToBeSet
    global RobotiqGripper2F85_Speed_ToBeSet
    global RobotiqGripper2F85_Force_ToBeSet

    global ZEDasHandController_ReubenPython2and3ClassObject
    global ZEDasHandController_OPEN_FLAG
    global SHOW_IN_GUI_ZEDasHandController_FLAG
    global ZEDasHandController_MostRecentDict
    global ZEDasHandController_MostRecentDict_Time
    global ZEDasHandController_Trigger_State
    global ZEDasHandController_AddToUR5armCurrentPositionList
    global ZEDasHandController_PositionList_ScalingFactorList
    global ZEDasHandController_RotationMatrixListsOfLists
    global ZEDasHandController_RollPitchYaw_AbtXYZ_List_ScalingFactorList
    global ZEDasHandControllerInfo_Label

    global RobotiqGripper2F85_ReubenPython2and3ClassObject
    global RobotiqGripper2F85_OPEN_FLAG
    global SHOW_IN_GUI_RobotiqGripper2F85_FLAG

    global KeyboardInfo_Label
    global Keyboard_KeysToTeleopControlsMapping_DictOfDicts_FormattedAsNicelyPrintedString

    global JoystickHID_ReubenPython2and3ClassObject
    global JOYSTICK_OPEN_FLAG
    global SHOW_IN_GUI_JOYSTICK_FLAG
    global Joystick_AddToUR5armCurrentPositionList
    global Joystick_AxisHatButtonOrBallTo6DOFposeMapping_ListOfDicts_FormattedAsNicelyPrintedString
    global JoystickInfo_Label
    global Joystick_ClutchState

    global MyPrint_ReubenPython2and3ClassObject
    global MYPRINT_OPEN_FLAG
    global SHOW_IN_GUI_MYPRINT_FLAG

    global DebuggingInfo_Label

    global ControlType

    global ControlType_StartingValue
    global ControlType_AcceptableValues
    global SharedGlobals_Teleop_UR5arm_MainThread_TimeToSleepEachLoop
    global ZEDasHandController_PositionList_ScalingFactorList
    global ZEDasHandController_RollPitchYaw_AbtXYZ_List_ScalingFactorList

    global LoopCounter_CalculatedFromGUIthread
    global CurrentTime_CalculatedFromGUIthread
    global StartingTime_CalculatedFromGUIthread
    global LastTime_CalculatedFromGUIthread
    global DataStreamingFrequency_CalculatedFromGUIthread
    global DataStreamingDeltaT_CalculatedFromGUIthread

    global CSVfileForTrajectoryData_SaveFlag
    global CSVfileForTrajectoryData_SaveFlag_Button
    global UR5arm_MostRecentDict_ToolVectorActual_MotionFromSnapshotAtTimeOfCreatingCSVfileForTrajectoryData

    if USE_GUI_FLAG == 1:
        if SharedGlobals_Teleop_UR5arm.EXIT_PROGRAM_FLAG == 0:
        #########################################################
        #########################################################

            #########################################################
            #########################################################
            CurrentTime_CalculatedFromGUIthread = getPreciseSecondsTimeStampString() - StartingTime_CalculatedFromGUIthread

            [LoopCounter_CalculatedFromGUIthread, LastTime_CalculatedFromGUIthread, DataStreamingFrequency_CalculatedFromGUIthread, DataStreamingDeltaT_CalculatedFromGUIthread] = UpdateFrequencyCalculation(LoopCounter_CalculatedFromGUIthread, CurrentTime_CalculatedFromGUIthread, LastTime_CalculatedFromGUIthread, DataStreamingFrequency_CalculatedFromGUIthread, DataStreamingDeltaT_CalculatedFromGUIthread)
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            DebuggingInfo_Label["text"] = "MainThread, Time: " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(CurrentTime_CalculatedFromMainThread, 0, 3) +\
                            "\t\t\tFrequency: " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DataStreamingFrequency_CalculatedFromMainThread, 0, 3) +\
                            "\nGUIthread, Time: " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(CurrentTime_CalculatedFromGUIthread, 0, 3) +\
                            "\t\t\tFrequency: " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DataStreamingFrequency_CalculatedFromGUIthread, 0, 3) +\
                            "\nControlType: " + ControlType + \
                            "\nUR5arm_MostRecentDict_JointAngleList_Deg: " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(SharedGlobals_Teleop_UR5arm.UR5arm_MostRecentDict_JointAngleList_Deg, 0, 5) +\
                            "\nUR5arm_MostRecentDict_JointAngleList_Rad: " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(SharedGlobals_Teleop_UR5arm.UR5arm_MostRecentDict_JointAngleList_Rad, 0, 5) +\
                            "\nUR5, ToolVectorActual: " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(SharedGlobals_Teleop_UR5arm.UR5arm_MostRecentDict_ToolVectorActual, 0, 5) +\
                            "\nUR5, ToolVectorActual_ToBeSet: " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(UR5arm_ToolVectorActual_ToBeSet, 0, 5) +\
                            "\nRobotiqGripper2F85, Position Speed Force: " + str([RobotiqGripper2F85_Position_ToBeSet, RobotiqGripper2F85_Speed_ToBeSet, RobotiqGripper2F85_Force_ToBeSet]) + \
                            "\nCSVfileForTrajectoryData_SaveFlag: " + str(CSVfileForTrajectoryData_SaveFlag) +\
                            "\nDifference UR5arm for CSV writing: " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(UR5arm_MostRecentDict_ToolVectorActual_MotionFromSnapshotAtTimeOfCreatingCSVfileForTrajectoryData, 0, 3)

            #########################################################
            #########################################################

            #########################################################
            #########################################################
            KeyboardInfo_Label["text"] = "Keyboard flags: " + str([SharedGlobals_Teleop_UR5arm.KeyPressResponse_DecrementURtoolTipInX_NeedsToBeChangedFlag,
                                                        SharedGlobals_Teleop_UR5arm.KeyPressResponse_IncrementURtoolTipInX_NeedsToBeChangedFlag,
                                                        SharedGlobals_Teleop_UR5arm.KeyPressResponse_DecrementURtoolTipInY_NeedsToBeChangedFlag,
                                                        SharedGlobals_Teleop_UR5arm.KeyPressResponse_IncrementURtoolTipInY_NeedsToBeChangedFlag,
                                                        SharedGlobals_Teleop_UR5arm.KeyPressResponse_DecrementURtoolTipInZ_NeedsToBeChangedFlag,
                                                        SharedGlobals_Teleop_UR5arm.KeyPressResponse_IncrementURtoolTipInZ_NeedsToBeChangedFlag,
                                                        SharedGlobals_Teleop_UR5arm.KeyPressResponse_OpenRobotiqGripper2F85_NeedsToBeChangedFlag,
                                                        SharedGlobals_Teleop_UR5arm.KeyPressResponse_CloseRobotiqGripper2F85_NeedsToBeChangedFlag]) + \
                            "\nKeyboard_AddToUR5armCurrentPositionList: " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(SharedGlobals_Teleop_UR5arm.Keyboard_AddToUR5armCurrentPositionList, 0, 3) +\
                            "\nKeyboard_KeysToTeleopControlsMapping_DictOfDicts: " + \
                            "\n" + Keyboard_KeysToTeleopControlsMapping_DictOfDicts_FormattedAsNicelyPrintedString
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            JoystickInfo_Label["text"] = "Joystick_AddToUR5armCurrentPositionList: " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(Joystick_AddToUR5armCurrentPositionList, 0, 3) +\
                            "\nJoystick_ClutchState: " + str(Joystick_ClutchState) + \
                            "\nJoystick_AxisHatButtonOrBallTo6DOFposeMapping_ListOfDicts: " + \
                            "\n" + Joystick_AxisHatButtonOrBallTo6DOFposeMapping_ListOfDicts_FormattedAsNicelyPrintedString
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            ZEDasHandControllerInfo_Label["text"] = "\nZEDasHandController_PositionList_ScalingFactorList: " + str(ZEDasHandController_PositionList_ScalingFactorList) + \
                            "\nZEDasHandController_RollPitchYaw_AbtXYZ_List_ScalingFactorList: " + str(ZEDasHandController_RollPitchYaw_AbtXYZ_List_ScalingFactorList) + \
                            "\nZEDasHandController_RotationMatrixListsOfLists: " + str(ZEDasHandController_RotationMatrixListsOfLists) + \
                            "\nZEDasHandController_AddToUR5armCurrentPositionList: " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(ZEDasHandController_AddToUR5armCurrentPositionList, 0, 3) + \
                            "\nZEDasHandController_Trigger_State: " + str(ZEDasHandController_Trigger_State)

            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if SHOW_IN_GUI_UR5arm_MostRecentDict_FLAG == 1:
                UR5arm_MostRecentDict_Label["text"] = ConvertDictToProperlyFormattedStringForPrinting(UR5arm_MostRecentDict, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 3, NumberOfTabsBetweenItems = 1)
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if CSVfileForTrajectoryData_SaveFlag == 1:
                CSVfileForTrajectoryData_SaveFlag_Button["bg"] = TKinter_LightGreenColor
                CSVfileForTrajectoryData_SaveFlag_Button["text"] = "Saving CSV"
            else:
                CSVfileForTrajectoryData_SaveFlag_Button["bg"] = TKinter_LightRedColor
                CSVfileForTrajectoryData_SaveFlag_Button["text"] = "NOT saving CSV"
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if ZEDasHandController_OPEN_FLAG == 1 and SHOW_IN_GUI_ZEDasHandController_FLAG == 1:
                ZEDasHandController_ReubenPython2and3ClassObject.GUI_update_clock()
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if RobotiqGripper2F85_OPEN_FLAG == 1 and SHOW_IN_GUI_RobotiqGripper2F85_FLAG == 1:
                RobotiqGripper2F85_ReubenPython2and3ClassObject.GUI_update_clock()
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if JOYSTICK_OPEN_FLAG == 1 and SHOW_IN_GUI_JOYSTICK_FLAG == 1:
                JoystickHID_ReubenPython2and3ClassObject.GUI_update_clock()
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if MYPRINT_OPEN_FLAG == 1 and SHOW_IN_GUI_MYPRINT_FLAG == 1:
                MyPrint_ReubenPython2and3ClassObject.GUI_update_clock()
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
            #########################################################
            #########################################################
        
        #########################################################
        #########################################################

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def GUI_Thread():
    global my_platform
    global root
    global root_Xpos
    global root_Ypos
    global root_width
    global root_height
    global GUItitleString
    global GUI_RootAfterCallbackInterval_Milliseconds
    global GUIbuttonWidth
    global GUIbuttonPadX
    global GUIbuttonPadY
    global GUIbuttonFontSize
    global USE_GUI_FLAG
    global TKinter_LightRedColor
    global TKinter_LightGreenColor
    global TKinter_LightBlueColor
    global TKinter_LightYellowColor
    global TKinter_DefaultGrayColor
    global SHOW_IN_GUI_UR5arm_MostRecentDict_FLAG

    ########################################################### KEY GUI LINE
    ###########################################################
    root = Tk()
    ###########################################################
    ###########################################################

    ###########################################################SET THE DEFAULT FONT FOR ALL WIDGETS CREATED AFTTER/BELOW THIS CALL
    ###########################################################
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(size=8)
    root.option_add("*Font", default_font)
    ###########################################################
    ###########################################################

    ###########################################################
    ###########################################################
    TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150)  # RGB
    TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150)  # RGB
    TKinter_LightBlueColor = '#%02x%02x%02x' % (150, 150, 255)  # RGB
    TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
    TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
    ###########################################################
    ###########################################################

    ###########################################################
    ###########################################################
    global TabControlObject
    global Tab_MainControls
    global Tab_UR5arm
    global Tab_RobotiqGripper2F85
    global Tab_KEYBOARD
    global Tab_JOYSTICK
    global Tab_ZEDasHandController
    global Tab_MyPrint

    TabControlObject = ttk.Notebook(root)

    Tab_MainControls = ttk.Frame(TabControlObject)
    TabControlObject.add(Tab_MainControls, text=' Main Controls ')

    Tab_UR5arm = ttk.Frame(TabControlObject)
    TabControlObject.add(Tab_UR5arm, text=' UR5arm ')

    Tab_RobotiqGripper2F85 = ttk.Frame(TabControlObject)
    TabControlObject.add(Tab_RobotiqGripper2F85, text=' Robotiq ')

    Tab_KEYBOARD = ttk.Frame(TabControlObject)
    TabControlObject.add(Tab_KEYBOARD, text=' Keyboard ')

    Tab_JOYSTICK = ttk.Frame(TabControlObject)
    TabControlObject.add(Tab_JOYSTICK, text=' Joystick ')

    Tab_ZEDasHandController = ttk.Frame(TabControlObject)
    TabControlObject.add(Tab_ZEDasHandController, text=' ZEDasHandController ')

    Tab_MyPrint = ttk.Frame(TabControlObject)
    TabControlObject.add(Tab_MyPrint, text=' MyPrint ')

    TabControlObject.pack(expand=1, fill="both") #CANNOT MIX PACK AND GRID IN THE SAME FRAME/TAB, SO ALL .GRID'S MUST BE CONTAINED WITHIN THEIR OWN FRAME/TAB.

    ############# #Set the tab header font
    TabStyle = ttk.Style()
    TabStyle.configure('TNotebook.Tab', font=('Helvetica', '12', 'bold'))
    #############

    ###########################################################
    ###########################################################

    ###########################################################
    ###########################################################
    global ExtraProgramControlGuiFrame
    ExtraProgramControlGuiFrame = Frame(Tab_MainControls)
    ExtraProgramControlGuiFrame["borderwidth"] = 2
    ExtraProgramControlGuiFrame["relief"] = "ridge"
    ExtraProgramControlGuiFrame.grid(row=0, column=0, padx=GUIbuttonPadX, pady=GUIbuttonPadY, rowspan=1, columnspan=1, sticky='w')
    ###########################################################
    ###########################################################

    ############################################
    ############################################
    global ExitProgramButton
    ExitProgramButton = Button(ExtraProgramControlGuiFrame, text="Exit Program", state="normal", width=GUIbuttonWidth, command=lambda i=1: ExitProgram_Callback())
    ExitProgramButton.grid(row=0, column=0, padx=GUIbuttonPadX, pady=GUIbuttonPadY, columnspan=1, rowspan=1,)
    ExitProgramButton.config(font=("Helvetica", GUIbuttonFontSize))
    ############################################
    ############################################

    ############################################
    ############################################
    global JSONfiles_NeedsToBeLoadedFlagButton
    JSONfiles_NeedsToBeLoadedFlagButton = Button(ExtraProgramControlGuiFrame, text="Load JSON files", state="normal", width=GUIbuttonWidth, command=lambda i=1: JSONfiles_NeedsToBeLoadedFlag_ButtonResponse())
    JSONfiles_NeedsToBeLoadedFlagButton.grid(row=0, column=1, padx=GUIbuttonPadX, pady=GUIbuttonPadY, columnspan=1, rowspan=1,)
    JSONfiles_NeedsToBeLoadedFlagButton.config(font=("Helvetica", GUIbuttonFontSize))
    ############################################
    ############################################

    ###########################################################
    ###########################################################
    global DebuggingInfo_Label
    DebuggingInfo_Label = Label(ExtraProgramControlGuiFrame, text="DebuggingInfo_Label", width=120, font=("Helvetica", 10))  #
    DebuggingInfo_Label.grid(row=1, column=0, padx=GUIbuttonPadX, pady=GUIbuttonPadY, columnspan=10, rowspan=1)
    ###########################################################
    ###########################################################

    ###########################################################
    ###########################################################
    global KeyboardInfo_Label
    KeyboardInfo_Label = Label(Tab_KEYBOARD, text="KeyboardInfo_Label", width=120, font=("Helvetica", 10))
    KeyboardInfo_Label.grid(row=0, column=0, padx=GUIbuttonPadX, pady=GUIbuttonPadY, columnspan=10, rowspan=1)
    ###########################################################
    ###########################################################

    ###########################################################
    ###########################################################
    global JoystickInfo_Label
    JoystickInfo_Label = Label(Tab_JOYSTICK, text="JoystickInfo_Label", width=120, font=("Helvetica", 10))
    JoystickInfo_Label.grid(row=1, column=0, padx=GUIbuttonPadX, pady=GUIbuttonPadY, columnspan=10, rowspan=1)
    ###########################################################
    ###########################################################

    ###########################################################
    ###########################################################
    global ZEDasHandControllerInfo_Label
    ZEDasHandControllerInfo_Label = Label(Tab_ZEDasHandController, text="ZEDasHandControllerInfo_Label", width=120, font=("Helvetica", 10))
    ZEDasHandControllerInfo_Label.grid(row=1, column=0, padx=GUIbuttonPadX, pady=GUIbuttonPadY, columnspan=10, rowspan=1)
    ###########################################################
    ###########################################################

    ###########################################################
    ###########################################################
    global ActuatorsControlGuiFrame
    ActuatorsControlGuiFrame = Frame(Tab_MainControls)
    ActuatorsControlGuiFrame["borderwidth"] = 2
    ActuatorsControlGuiFrame["relief"] = "ridge"
    ActuatorsControlGuiFrame.grid(row=2, column=0, padx=GUIbuttonPadX, pady=GUIbuttonPadY, rowspan=1, columnspan=1, sticky='w')
    ActuatorsControlGuiFrame_ButtonWidth = 22
    ActuatorsControlGuiFrame_FontSize = 20
    ActuatorsControlGuiFrame_CheckbuttonWidth = 20
    ###########################################################
    ###########################################################

    ###########################################################
    ###########################################################
    global UR5arm_MoveSafelyToStartingPose_Button
    UR5arm_MoveSafelyToStartingPose_Button = Button(ActuatorsControlGuiFrame, text='UR Home', state="normal", width=GUIbuttonWidth, bg=TKinter_LightGreenColor, font=("Helvetica", GUIbuttonFontSize), command=lambda i=1: UR5arm_MoveSafelyToStartingPose_ButtonResponse())
    UR5arm_MoveSafelyToStartingPose_Button.grid(row=3, column=0, padx=GUIbuttonPadX, pady=GUIbuttonPadY, columnspan=1, rowspan=1)
    ###########################################################
    ###########################################################

    ###########################################################
    ###########################################################
    global UR5arm_StopMotion_Button
    UR5arm_StopMotion_Button = Button(ActuatorsControlGuiFrame, text='UR Stop', state="normal", width=GUIbuttonWidth, bg=TKinter_LightRedColor, font=("Helvetica", GUIbuttonFontSize), command=lambda i=1: UR5arm_StopMotion_ButtonResponse())
    UR5arm_StopMotion_Button.grid(row=3, column=1, padx=GUIbuttonPadX, pady=GUIbuttonPadY, columnspan=1, rowspan=1)
    ###########################################################
    ###########################################################

    ###########################################################
    ###########################################################
    global UR5arm_MostRecentDict_Label
    UR5arm_MostRecentDict_Label = Label(Tab_UR5arm, text="UR5arm_MostRecentDict_Label", width=120, font=("Helvetica", 10))
    if SHOW_IN_GUI_UR5arm_MostRecentDict_FLAG == 1:
        UR5arm_MostRecentDict_Label.grid(row=0, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
    ###########################################################
    ###########################################################
    
    ###########################################################
    ###########################################################
    global CSVfileForTrajectoryData_SaveFlag_Button
    CSVfileForTrajectoryData_SaveFlag_Button = Button(ActuatorsControlGuiFrame, text='Save CSV', state="normal", width=GUIbuttonWidth, font=("Helvetica", GUIbuttonFontSize), command=lambda i=1: CSVfileForTrajectoryData_SaveFlag_ButtonResponse())
    CSVfileForTrajectoryData_SaveFlag_Button.grid(row=4, column=0, padx=GUIbuttonPadX, pady=GUIbuttonPadY, columnspan=1, rowspan=1)
    ###########################################################
    ###########################################################

    ###########################################################
    ###########################################################
    global SHOW_IN_GUI_UR5arm_ServoJparameterEntries_FLAG

    global UR5arm_ServoJtimeDurationSeconds_Label
    UR5arm_ServoJtimeDurationSeconds_Label = Label(ActuatorsControlGuiFrame, text="UR5arm_ServoJtimeDurationSeconds", width=50, font=("Helvetica", 12))

    if SHOW_IN_GUI_UR5arm_ServoJparameterEntries_FLAG == 1:
        UR5arm_ServoJtimeDurationSeconds_Label.grid(row=5, column=0, padx=1, pady=1, columnspan=1, rowspan=1)

    global UR5arm_ServoJtimeDurationSeconds_StringVar
    UR5arm_ServoJtimeDurationSeconds_StringVar = StringVar()
    UR5arm_ServoJtimeDurationSeconds_StringVar.set(str(UR5arm_ServoJtimeDurationSeconds))

    global UR5arm_ServoJtimeDurationSeconds_Entry
    UR5arm_ServoJtimeDurationSeconds_Entry = Entry(ActuatorsControlGuiFrame,
                                        font=("Helvetica", int(12)),
                                        state="normal",
                                        width=20,
                                        textvariable=UR5arm_ServoJtimeDurationSeconds_StringVar,
                                        justify='center')

    if SHOW_IN_GUI_UR5arm_ServoJparameterEntries_FLAG == 1:
        UR5arm_ServoJtimeDurationSeconds_Entry.grid(row=5, column=1, padx=0, pady=0, columnspan=1, rowspan=1)
    UR5arm_ServoJtimeDurationSeconds_Entry.bind('<Return>', lambda event: UR5arm_ServoJtimeDurationSeconds_EntryEventResponse(event))
    UR5arm_ServoJtimeDurationSeconds_Entry.bind('<Leave>', lambda event: UR5arm_ServoJtimeDurationSeconds_EntryEventResponse(event))
    UR5arm_ServoJtimeDurationSeconds_Entry.bind('<ButtonPress-1>', lambda event: UR5arm_ServoJtimeDurationSeconds_EntryEventResponse(event))
    ###########################################################
    ###########################################################

    ###########################################################
    ###########################################################
    global UR5arm_ServoJlookAheadTimeSeconds_Label
    UR5arm_ServoJlookAheadTimeSeconds_Label = Label(ActuatorsControlGuiFrame, text="UR5arm_ServoJlookAheadTimeSeconds", width=50, font=("Helvetica", 12))
    if SHOW_IN_GUI_UR5arm_ServoJparameterEntries_FLAG == 1:
        UR5arm_ServoJlookAheadTimeSeconds_Label.grid(row=6, column=0, padx=1, pady=1, columnspan=1, rowspan=1)

    global UR5arm_ServoJlookAheadTimeSeconds_StringVar
    UR5arm_ServoJlookAheadTimeSeconds_StringVar = StringVar()
    UR5arm_ServoJlookAheadTimeSeconds_StringVar.set(str(UR5arm_ServoJlookAheadTimeSeconds))

    global UR5arm_ServoJlookAheadTimeSeconds_Entry
    UR5arm_ServoJlookAheadTimeSeconds_Entry = Entry(ActuatorsControlGuiFrame,
                                        font=("Helvetica", int(12)),
                                        state="normal",
                                        width=20,
                                        textvariable=UR5arm_ServoJlookAheadTimeSeconds_StringVar,
                                        justify='center')

    if SHOW_IN_GUI_UR5arm_ServoJparameterEntries_FLAG == 1:
        UR5arm_ServoJlookAheadTimeSeconds_Entry.grid(row=6, column=1, padx=0, pady=0, columnspan=1, rowspan=1)
    UR5arm_ServoJlookAheadTimeSeconds_Entry.bind('<Return>', lambda event: UR5arm_ServoJlookAheadTimeSeconds_EntryEventResponse(event))
    UR5arm_ServoJlookAheadTimeSeconds_Entry.bind('<Leave>', lambda event: UR5arm_ServoJlookAheadTimeSeconds_EntryEventResponse(event))
    UR5arm_ServoJlookAheadTimeSeconds_Entry.bind('<ButtonPress-1>', lambda event: UR5arm_ServoJlookAheadTimeSeconds_EntryEventResponse(event))
    ###########################################################
    ###########################################################

    ###########################################################
    ###########################################################
    global UR5arm_ServoJgain_Label
    UR5arm_ServoJgain_Label = Label(ActuatorsControlGuiFrame, text="UR5arm_ServoJgain", width=50, font=("Helvetica", 12))
    if SHOW_IN_GUI_UR5arm_ServoJparameterEntries_FLAG == 1:
        UR5arm_ServoJgain_Label.grid(row=7, column=0, padx=1, pady=1, columnspan=1, rowspan=1)

    global UR5arm_ServoJgain_StringVar
    UR5arm_ServoJgain_StringVar = StringVar()
    UR5arm_ServoJgain_StringVar.set(str(UR5arm_ServoJgain))

    global UR5arm_ServoJgain_Entry
    UR5arm_ServoJgain_Entry = Entry(ActuatorsControlGuiFrame,
                                        font=("Helvetica", int(12)),
                                        state="normal",
                                        width=20,
                                        textvariable=UR5arm_ServoJgain_StringVar,
                                        justify='center')

    if SHOW_IN_GUI_UR5arm_ServoJparameterEntries_FLAG == 1:
        UR5arm_ServoJgain_Entry.grid(row=7, column=1, padx=0, pady=0, columnspan=1, rowspan=1)
    UR5arm_ServoJgain_Entry.bind('<Return>', lambda event: UR5arm_ServoJgain_EntryEventResponse(event))
    UR5arm_ServoJgain_Entry.bind('<Leave>', lambda event: UR5arm_ServoJgain_EntryEventResponse(event))
    UR5arm_ServoJgain_Entry.bind('<ButtonPress-1>', lambda event: UR5arm_ServoJgain_EntryEventResponse(event))
    ###########################################################
    ###########################################################

    ###########################################################
    ###########################################################
    global ControlTypeGuiFrame
    ControlTypeGuiFrame = Frame(ExtraProgramControlGuiFrame)
    ControlTypeGuiFrame.grid(row=2, column=0, padx=GUIbuttonPadX, pady=GUIbuttonPadY, rowspan=1, columnspan=1, sticky='w')
    ###########################################################
    ###########################################################

    ###########################################################
    ###########################################################
    global ControlType_Radiobutton_SelectionVar
    ControlType_Radiobutton_SelectionVar = StringVar()

    ControlType_Radiobutton_SelectionVar.set(ControlType_StartingValue)
    ###########################################################
    ###########################################################

    ###########################################################
    ###########################################################
    global ControlType_AcceptableValues

    global ControlType_RadioButtonObjectsList
    ControlType_RadioButtonObjectsList = list()
    for Index, ControlTypeString in enumerate(ControlType_AcceptableValues):
        ControlType_RadioButtonObjectsList.append(Radiobutton(ControlTypeGuiFrame,
                                                      text=ControlTypeString,
                                                      state="normal",
                                                      width=15,
                                                      anchor="w",
                                                      variable=ControlType_Radiobutton_SelectionVar,
                                                      value=ControlTypeString,
                                                      command=lambda name=ControlTypeString: ControlType_Radiobutton_Response(name)))
        ControlType_RadioButtonObjectsList[Index].grid(row=0, column=Index, padx=1, pady=1, columnspan=1, rowspan=1)
        #if ControlType_StartingValue == "ControlTypeString":
        #    ControlType_RadioButtonObjectsList[Index].select()
    ###########################################################
    ###########################################################

    ########################################################### THIS BLOCK MUST COME 2ND-TO-LAST IN def  GUI_Thread() IF USING TABS.
    ###########################################################
    root.protocol("WM_DELETE_WINDOW", ExitProgram_Callback)  # Set the callback function for when the window's closed.
    root.title(GUItitleString)
    root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
    root.geometry('%dx%d+%d+%d' % (
    root_width, root_height, root_Xpos, root_Ypos))  # set the dimensions of the screen and where it is placed
    root.mainloop()
    ###########################################################
    ###########################################################

    ###########################################################
    ########################################################### THIS BLOCK MUST COME LAST IN def  GUI_Thread() REGARDLESS OF CODE.
    root.quit()  # Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
    root.destroy()  # Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
    ###########################################################
    ###########################################################

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def UR5arm_ServoJtimeDurationSeconds_EntryEventResponse(event):
    global ActuatorsControlGuiFrame
    global UR5arm_ServoJtimeDurationSeconds_StringVar
    global UR5arm_ServoJtimeDurationSeconds_MinVal
    global UR5arm_ServoJtimeDurationSeconds_MaxVal
    global UR5arm_ServoJtimeDurationSeconds

    #################################################Take away focus so that we're not continuing to tpye into entry when logging waypoints.
    ActuatorsControlGuiFrame.focus_set()
    #################################################

    try:
        Value = float(UR5arm_ServoJtimeDurationSeconds_StringVar.get())

        UR5arm_ServoJtimeDurationSeconds = LimitTextEntryInput(UR5arm_ServoJtimeDurationSeconds_MinVal, UR5arm_ServoJtimeDurationSeconds_MaxVal, Value, UR5arm_ServoJtimeDurationSeconds_StringVar)
        print("UR5arm_ServoJtimeDurationSeconds_EntryEventResponse event fired, UR5arm_ServoJtimeDurationSeconds = " + str(UR5arm_ServoJtimeDurationSeconds))

    except:
        exceptions = sys.exc_info()[0]
        print("Variable_dictEntryEventResponse ERROR: Exceptions: %s" % exceptions)
        traceback.print_exc()
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def UR5arm_ServoJlookAheadTimeSeconds_EntryEventResponse(event):
    global ActuatorsControlGuiFrame
    global UR5arm_ServoJlookAheadTimeSeconds_StringVar
    global UR5arm_ServoJlookAheadTimeSeconds_MinVal
    global UR5arm_ServoJlookAheadTimeSeconds_MaxVal
    global UR5arm_ServoJlookAheadTimeSeconds

    #################################################Take away focus so that we're not continuing to tpye into entry when logging waypoints.
    ActuatorsControlGuiFrame.focus_set()
    #################################################

    try:
        Value = float(UR5arm_ServoJlookAheadTimeSeconds_StringVar.get())

        UR5arm_ServoJlookAheadTimeSeconds = LimitTextEntryInput(UR5arm_ServoJlookAheadTimeSeconds_MinVal, UR5arm_ServoJlookAheadTimeSeconds_MaxVal, Value, UR5arm_ServoJlookAheadTimeSeconds_StringVar)
        print("UR5arm_ServoJlookAheadTimeSeconds_EntryEventResponse event fired, UR5arm_ServoJlookAheadTimeSeconds = " + str(UR5arm_ServoJlookAheadTimeSeconds))

    except:
        exceptions = sys.exc_info()[0]
        print("Variable_dictEntryEventResponse ERROR: Exceptions: %s" % exceptions)
        traceback.print_exc()
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def UR5arm_ServoJgain_EntryEventResponse(event):
    global ActuatorsControlGuiFrame
    global UR5arm_ServoJgain_StringVar
    global UR5arm_ServoJgain_MinVal
    global UR5arm_ServoJgain_MaxVal
    global UR5arm_ServoJgain

    #################################################Take away focus so that we're not continuing to tpye into entry when logging waypoints.
    ActuatorsControlGuiFrame.focus_set()
    #################################################

    try:
        Value = float(UR5arm_ServoJgain_StringVar.get())

        UR5arm_ServoJgain = LimitTextEntryInput(UR5arm_ServoJgain_MinVal, UR5arm_ServoJgain_MaxVal, Value, UR5arm_ServoJgain_StringVar)
        print("UR5arm_ServoJgain_EntryEventResponse event fired, UR5arm_ServoJgain = " + str(UR5arm_ServoJgain))

    except:
        exceptions = sys.exc_info()[0]
        print("Variable_dictEntryEventResponse ERROR: Exceptions: %s" % exceptions)
        traceback.print_exc()
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def ControlType_Radiobutton_Response(name):
    global ControlType_Radiobutton_SelectionVar
    global ControlType
    global ControlType_NeedsToBeChangedFlag

    #print("name: " + name)

    ControlType = ControlType_Radiobutton_SelectionVar.get()
    ControlType_NeedsToBeChangedFlag = 1
    print("ControlType set to: " + ControlType)
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def JSONfiles_NeedsToBeLoadedFlag_ButtonResponse():
    global JSONfiles_NeedsToBeLoadedFlag

    JSONfiles_NeedsToBeLoadedFlag = 1

    MyPrint_ReubenPython2and3ClassObject.my_print("JSONfiles_NeedsToBeLoadedFlag_ButtonResponse event fired!")
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def UR5arm_MoveSafelyToStartingPose_ButtonResponse():
    global UR5arm_MoveSafelyToStartingPose_NeedsToBeChangedFlag

    UR5arm_MoveSafelyToStartingPose_NeedsToBeChangedFlag = 1

    MyPrint_ReubenPython2and3ClassObject.my_print("UR5arm_MoveSafelyToStartingPose_ButtonResponse event fired!")
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def UR5arm_StopMotion_ButtonResponse():
    global UR5arm_StopMotion_State_NeedsToBeChangedFlag

    UR5arm_StopMotion_State_NeedsToBeChangedFlag  = 1

    MyPrint_ReubenPython2and3ClassObject.my_print("UR5arm_StopMotion_ButtonResponse event fired!")
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def CSVfileForTrajectoryData_SaveFlag_ButtonResponse():
    global CSVfileForTrajectoryData_SaveFlag_NeedsToBeChangedFlag

    CSVfileForTrajectoryData_SaveFlag_NeedsToBeChangedFlag = 1

    MyPrint_ReubenPython2and3ClassObject.my_print("CSVfileForTrajectoryData_SaveFlag_ButtonResponse event fired!")
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def SetAllActuatorsStatesOnOrOffCleanlyFromMainLoop():
    global MyPrint_ReubenPython2and3ClassObject
    global UR5arm_StopMotion_State_NeedsToBeChangedFlag

    UR5arm_StopMotion_State_NeedsToBeChangedFlag = 1

    MyPrint_ReubenPython2and3ClassObject.my_print("SetAllActuatorsStatesOnOrOffCleanlyFromMainLoop event fired!")
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def UR5arm_AllowExternalCommandsFromMainProgram():
    global MyPrint_ReubenPython2and3ClassObject
    global UR5arm_AllowExternalCommandsFromMainProgram_Flag
    global UR5arm_WatchdogTimerDurationSeconds_ExpirationWillEndStandAloneProcess
    global UR5arm_ReubenPython2and3ClassObject

    UR5arm_AllowExternalCommandsFromMainProgram_Flag = 1

    if UR5arm_WatchdogTimerDurationSeconds_ExpirationWillEndStandAloneProcess > 0.0:
        UR5arm_ReubenPython2and3ClassObject.FunctionCallToStandAloneProcess("SetWatchdogTimerEnableState",
                                                                            [1],
                                                                            MultiprocessingQueue_Rx_MaxSize_Local=UR5arm_MultiprocessingQueue_Rx_MaxSize,
                                                                            IgnoreNewDataIfQueueIsFullFlag=1)

    MyPrint_ReubenPython2and3ClassObject.my_print("UR5arm_AllowExternalCommandsFromMainProgram event fired!")

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def UR5arm_BlockWhileExecuting_MoveSafelyToStartingPoseViaMultipointSequence():
    global UR5arm_OPEN_FLAG
    global UR5arm_MoveToHomeAtStartOfProgramFlag
    global UR5arm_ReubenPython2and3ClassObject
    global UR5arm_MultiprocessingQueue_Rx_MaxSize
    global UR5arm_PositionControl_ServoJ_MoveThroughListOfPoses_SafeReturnToStartingPoseFromAnywhere

    time.sleep(1.0) #Give the UR5arm a chance to open before we try to send it a MoveSafelyToStartingPoseViaMultipointSequence command.
    if UR5arm_OPEN_FLAG == 1:
        if UR5arm_MoveToHomeAtStartOfProgramFlag == 1: #MOVE TO START
            UR5arm_ReubenPython2and3ClassObject.FunctionCallToStandAloneProcess("MoveSafelyToStartingPoseViaMultipointSequence",
                                                                                [],
                                                                                MultiprocessingQueue_Rx_MaxSize_Local=UR5arm_MultiprocessingQueue_Rx_MaxSize,
                                                                                IgnoreNewDataIfQueueIsFullFlag=1)

            TimerCallbackFunctionWithFunctionAsArgument_SingleShot_NoParenthesesAfterFunctionName(UR5arm_PositionControl_ServoJ_MoveThroughListOfPoses_SafeReturnToStartingPoseFromAnywhere[0]["TimeDurationSec"], UR5arm_AllowExternalCommandsFromMainProgram, [])

        else: #DON'T MOVE
            UR5arm_AllowExternalCommandsFromMainProgram()

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
if __name__ == '__main__':

    ################################################
    ################################################
    global my_platform
    global ParametersToBeLoaded_Directory_TO_BE_USED
    global LogFile_Directory_TO_BE_USED

    my_platform = GetMyPlatform()

    if my_platform == "windows":
        ParametersToBeLoaded_Directory_TO_BE_USED = ParametersToBeLoaded_Directory_Windows
        LogFile_Directory_TO_BE_USED = LogFile_Directory_Windows

    elif my_platform == "linux":
        ParametersToBeLoaded_Directory_TO_BE_USED = ParametersToBeLoaded_Directory_LinuxNonRaspberryPi
        LogFile_Directory_TO_BE_USED = LogFile_Directory_LinuxNonRaspberryPi

    elif my_platform == "mac":
        ParametersToBeLoaded_Directory_TO_BE_USED = ParametersToBeLoaded_Directory_Mac
        LogFile_Directory_TO_BE_USED = LogFile_Directory_Mac

    else:
        "Teleop_UR5arm.py: ERROR, OS must be Windows, LinuxNonRaspberryPi, or Mac!"
        ExitProgram_Callback()

    print("ParametersToBeLoaded_Directory_TO_BE_USED: " + ParametersToBeLoaded_Directory_TO_BE_USED)
    print("LogFile_Directory_TO_BE_USED: " + LogFile_Directory_TO_BE_USED)
    ################################################
    ################################################

    ################################################
    ################################################
    global USE_GUI_FLAG_ARGV_OVERRIDE
    global SOFTWARE_LAUNCH_METHOD

    [USE_GUI_FLAG_ARGV_OVERRIDE, SOFTWARE_LAUNCH_METHOD] =  ParseARGV_USE_GUI_and_SOFTWARE_LAUNCH_METHOD()

    print("Teleop_UR5arm, USE_GUI_FLAG_ARGV_OVERRIDE: " + str(USE_GUI_FLAG_ARGV_OVERRIDE) + ", SOFTWARE_LAUNCH_METHOD: " + str(SOFTWARE_LAUNCH_METHOD))

    if SOFTWARE_LAUNCH_METHOD == -1:
        print("Teleop_UR5arm ERROR, must launch software via command terminal/BAT-file, not IDE!")
        time.sleep(5.0)
        sys.exit()
    ################################################
    ################################################

    ################################################
    ################################################
    AMflag = IsTheTimeCurrentlyAM()
    if AMflag == 1:
        AMorPMstring = "AM"
    else:
        AMorPMstring = "PM"

    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("Starting 'Teleop_UR5arm.py' at " + getTimeStampString() + AMorPMstring)
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    ################################################
    ################################################

    #################################################
    #################################################
    global JSONfiles_NeedsToBeLoadedFlag
    JSONfiles_NeedsToBeLoadedFlag = 0

    #################################################
    global UseClassesFlags_Directions
    global USE_GUI_FLAG
    global USE_KEYBOARD_FLAG
    global USE_MYPRINT_FLAG
    global USE_UR5arm_FLAG
    global USE_ZEDasHandController_FLAG
    global USE_RobotiqGripper2F85_FLAG
    global USE_JOYSTICK_FLAG
    global USE_PLOTTER_FLAG
    global SAVE_PROGRAM_LOGS_FLAG
    global SAVE_CSV_FILE_OF_TRAJECTORY_DATA_FLAG_AT_START_OF_PROGRAM

    LoadAndParseJSONfile_UseClassesFlags()
    #################################################

    #################################################
    global SHOW_IN_GUI_MYPRINT_FLAG
    global SHOW_IN_GUI_UR5arm_StandAloneProcess_FLAG
    global SHOW_IN_GUI_UR5arm_MostRecentDict_FLAG
    global SHOW_IN_GUI_UR5arm_ServoJparameterEntries_FLAG
    global SHOW_IN_GUI_ZEDasHandController_FLAG
    global SHOW_IN_GUI_RobotiqGripper2F85_FLAG
    global SHOW_IN_GUI_JOYSTICK_FLAG
    global GUItitleString
    global GUI_RootAfterCallbackInterval_Milliseconds
    global root_Xpos
    global root_Ypos
    global root_width
    global root_height
    global GUIbuttonWidth
    global GUIbuttonPadX
    global GUIbuttonPadY
    global GUIbuttonFontSize
    global UR5arm_RootWindowWidth
    global UR5arm_RootWindowHeight
    global UR5arm_RootWindowStartingX
    global UR5arm_RootWindowStartingY
    global UR5arm_RootWindowTitle
    global GUI_ROW_ZEDasHandController
    global GUI_COLUMN_ZEDasHandController
    global GUI_PADX_ZEDasHandController
    global GUI_PADY_ZEDasHandController
    global GUI_ROWSPAN_ZEDasHandController
    global GUI_COLUMNSPAN_ZEDasHandController
    global GUI_ROW_RobotiqGripper2F85
    global GUI_COLUMN_RobotiqGripper2F85
    global GUI_PADX_RobotiqGripper2F85
    global GUI_PADY_RobotiqGripper2F85
    global GUI_ROWSPAN_RobotiqGripper2F85
    global GUI_COLUMNSPAN_RobotiqGripper2F85
    global GUI_ROW_JOYSTICK
    global GUI_COLUMN_JOYSTICK
    global GUI_PADX_JOYSTICK
    global GUI_PADY_JOYSTICK
    global GUI_ROWSPAN_JOYSTICK
    global GUI_COLUMNSPAN_JOYSTICK
    global GUI_ROW_MYPRINT
    global GUI_COLUMN_MYPRINT
    global GUI_PADX_MYPRINT
    global GUI_PADY_MYPRINT
    global GUI_ROWSPAN_MYPRINT
    global GUI_COLUMNSPAN_MYPRINT

    LoadAndParseJSONfile_GUIsettings()
    #################################################

    #################################################
    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_GUIparametersDict
    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_setup_dict

    LoadAndParseJSONfile_Plotter()
    #################################################

    #################################################
    global UR5arm_Directions
    global UR5arm_ArmNameToUse

    global UR5arm_Arm_Specific_Details
    global UR5arm_ControllerBoxVersion
    global UR5arm_RealTimeClientInterfaceVersionNumberString
    global UR5arm_IPV4Address
    global UR5arm_ServoJtimeDurationSeconds
    global UR5arm_ServoJlookAheadTimeSeconds
    global UR5arm_ServoJGain

    global UR5arm_IPV4_NumberOfRxMessagesToBuffers
    global UR5arm_DedicatedTxThread_MaximumTxMessagesPerSecondFrequency
    global UR5arm_DedicatedTxThread_TxMessageToSend_Queue_MaxSize
    global UR5arm_Payload_MassKG_ToBeCommanded
    global UR5arm_Payload_CoGmetersList_ToBeCommanded
    global UR5arm_Velocity
    global UR5arm_Acceleration
    global UR5arm_MultiprocessingQueue_Rx_MaxSize
    global UR5arm_MultiprocessingQueue_Tx_MaxSize
    global UR5arm_MoveToHomeAtStartOfProgramFlag
    global UR5arm_WatchdogTimerDurationSeconds_ExpirationWillEndStandAloneProcess
    global UR5am_StandAloneProcess_TimeToSleepEachLoop
    global UR5arm_TimeDurationToWaitBetweenCreatingClassObjectAndReadingData_Seconds
    global UR5arm_PositionControl_ServoJ_MoveThroughListOfPoses_SafeReturnToStartingPoseFromAnywhere
    global UR5arm_EnableTx_State_AtStartupFlag
    global UR5arm_Zero_UR5arm_MostRecentDict_ToolVectorActual_WhenCreatingCSVfileForTrajectoryData_Flag

    LoadAndParseJSONfile_UR5()

    if UR5arm_ArmNameToUse not in UR5arm_Arm_Specific_Details:
        print("Teleop_UR5arm ERROR: UR5arm_ArmNameToUse = " + str(UR5arm_ArmNameToUse) + " not listed in UR5arm_Arm_Specific_Details.")
        ExitProgram_Callback()
    else:
        UR5arm_ControllerBoxVersion = UR5arm_Arm_Specific_Details[UR5arm_ArmNameToUse]["UR5arm_ControllerBoxVersion"]
        UR5arm_RealTimeClientInterfaceVersionNumberString = UR5arm_Arm_Specific_Details[UR5arm_ArmNameToUse]["UR5arm_RealTimeClientInterfaceVersionNumberString"]
        UR5arm_IPV4Address = UR5arm_Arm_Specific_Details[UR5arm_ArmNameToUse]["UR5arm_IPV4Address"]
        UR5arm_ServoJtimeDurationSeconds = UR5arm_Arm_Specific_Details[UR5arm_ArmNameToUse]["UR5arm_ServoJtimeDurationSeconds"]
        UR5arm_ServoJlookAheadTimeSeconds = UR5arm_Arm_Specific_Details[UR5arm_ArmNameToUse]["UR5arm_ServoJlookAheadTimeSeconds"]
        UR5arm_ServoJgain = UR5arm_Arm_Specific_Details[UR5arm_ArmNameToUse]["UR5arm_ServoJgain"]
    #################################################

    #################################################
    global RobotiqGripper2F85_Directions
    global RobotiqGripper2F85_DesiredSerialNumber
    global RobotiqGripper2F85_DesiredSlaveID
    global RobotiqGripper2F85_MainThread_TimeToSleepEachLoop
    global RobotiqGripper2F85_Position_Starting
    global RobotiqGripper2F85_Speed_Starting
    global RobotiqGripper2F85_Force_Starting

    LoadAndParseJSONfile_RobotiqGripper2F85()
    #################################################

    #################################################
    global Keyboard_Directions
    global Keyboard_KeysToTeleopControlsMapping_DictOfDicts

    LoadAndParseJSONfile_Keyboard()
    KeyboardMapKeysToCallbackFunctions()
    #################################################

    #################################################
    global Joystick_NameDesired
    global Joystick_IntegerIDdesired
    global Joystick_ShowJustDotMovingFlag
    global Joystick_Axis_Index_ToDisplayAsHorizontalAxisOn2DdotDisplay
    global Joystick_Axis_Index_ToDisplayAsVerticalAxisOn2DdotDisplay
    global Joystick_Clutch_Button_Index_ToDisplayAsDotColorOn2DdotDisplay
    global Joystick_PrintInfoForAllDetectedJoysticksFlag
    global Joystick_AxisHatButtonOrBallTo6DOFposeMapping_ListOfDicts
    global Joystick_UseClutchFlag

    LoadAndParseJSONfile_Joystick()
    #################################################

    #################################################
    global ZEDasHandController_Directions
    global ZEDasHandController_ZEDcoordinateSystem
    global ZEDasHandController_ZEDresolution
    global ZEDasHandController_ZEDfps
    global ZEDasHandController_MainThread_TimeToSleepEachLoop
    global ZEDasHandController_Position_ExponentialFilterLambda
    global ZEDasHandController_Rotation_ExponentialFilterLambda
    global ZEDasHandController_DataCollectionDurationInSecondsForZeroing
    global ZEDasHandController_RotationMatrixListsOfLists
    global ZEDasHandController_PositionList_ScalingFactorList
    global ZEDasHandController_RollPitchYaw_AbtXYZ_List_ScalingFactorList

    LoadAndParseJSONfile_ZEDasHandController()
    #################################################

    #################################################
    global ControlType_StartingValue
    global ControlType_AcceptableValues
    global Teleop_UR5arm_MainThread_TimeToSleepEachLoop

    LoadAndParseJSONfile_ControlLawParameters()

    if ControlType_StartingValue not in ControlType_AcceptableValues:
        print("ERROR: ControlType_StartingValue but be in " + str(ControlType_AcceptableValues))
    #################################################

    #################################################
    #################################################
    global root

    global TabControlObject
    global Tab_MainControls
    global Tab_ZEDasHandController
    global Tab_UR5arm
    global Tab_RobotiqGripper2F85
    global Tab_KEYBOARD
    global Tab_JOYSTICK
    global Tab_MyPrint

    global ControlType
    ControlType = ControlType_StartingValue

    global ControlType_NeedsToBeChangedFlag
    ControlType_NeedsToBeChangedFlag = 0
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPrint_ReubenPython2and3ClassObject

    global MYPRINT_OPEN_FLAG
    MYPRINT_OPEN_FLAG = -1
    #################################################
    #################################################

    #################################################
    #################################################
    global UR5arm_ReubenPython2and3ClassObject

    global UR5arm_OPEN_FLAG
    UR5arm_OPEN_FLAG = -1

    global UR5arm_MostRecentDict
    UR5arm_MostRecentDict = dict()

    #Defined in SharedGlobals_Teleop_UR5arm.py:
    #global UR5arm_MostRecentDict_JointAngleList_Deg
    #global UR5arm_MostRecentDict_JointAngleList_Rad
    #global UR5arm_MostRecentDict_ToolVectorActual

    global UR5arm_MostRecentDict_ToolVectorActual_AtTimeOfClutchIn
    UR5arm_MostRecentDict_ToolVectorActual_AtTimeOfClutchIn = [-11111.0]*6

    global UR5arm_MostRecentDict_ToolVectorActual_SnapshotAtTimeOfCreatingCSVfileForTrajectoryData
    UR5arm_MostRecentDict_ToolVectorActual_SnapshotAtTimeOfCreatingCSVfileForTrajectoryData = [-11111.0]*6

    global UR5arm_MostRecentDict_ToolVectorActual_MotionFromSnapshotAtTimeOfCreatingCSVfileForTrajectoryData
    UR5arm_MostRecentDict_ToolVectorActual_MotionFromSnapshotAtTimeOfCreatingCSVfileForTrajectoryData = [0.0]*6

    global UR5arm_MostRecentDict_ToolTipSpeedsCartestian_TCPspeedActual
    UR5arm_MostRecentDict_ToolTipSpeedsCartestian_TCPspeedActual = [-11111.0]*6

    global UR5arm_MostRecentDict_ToolTipSpeedsCartestian_LinearXYZnorm_MetersPerSec
    UR5arm_MostRecentDict_ToolTipSpeedsCartestian_LinearXYZnorm_MetersPerSec = -11111.0

    global UR5arm_MostRecentDict_DataStreamingFrequency_CalculatedFromDedicatedRxThread
    UR5arm_MostRecentDict_DataStreamingFrequency_CalculatedFromDedicatedRxThread = -11111.0

    global UR5arm_MostRecentDict_Time
    UR5arm_MostRecentDict_Time = -11111.0

    global UR5arm_MostRecentDict_ToolVectorActual_IsItInitializedFlag
    UR5arm_MostRecentDict_ToolVectorActual_IsItInitializedFlag = 0

    global UR5arm_ToolVectorActual_ToBeSet
    UR5arm_ToolVectorActual_ToBeSet = [-11111.0]*6

    global UR5arm_PositionControl_Waypoints_ToBeSet
    UR5arm_PositionControl_Waypoints_ToBeSet = dict()

    global UR5arm_PositionControl_NeedsToBeChangedFlag
    UR5arm_PositionControl_NeedsToBeChangedFlag = 0

    global UR5arm_MoveSafelyToStartingPose_NeedsToBeChangedFlag
    UR5arm_MoveSafelyToStartingPose_NeedsToBeChangedFlag = 0

    global UR5arm_StopMotion_State_NeedsToBeChangedFlag
    UR5arm_StopMotion_State_NeedsToBeChangedFlag = 0

    global UR5arm_AllowExternalCommandsFromMainProgram_Flag
    UR5arm_AllowExternalCommandsFromMainProgram_Flag = 0

    global UR5arm_ServoJtimeDurationSeconds_MinVal
    UR5arm_ServoJtimeDurationSeconds_MinVal = 0.001

    global UR5arm_ServoJtimeDurationSeconds_MaxVal
    UR5arm_ServoJtimeDurationSeconds_MaxVal = 60.0

    global UR5arm_ServoJlookAheadTimeSeconds_MinVal
    UR5arm_ServoJlookAheadTimeSeconds_MinVal = 0.03 #From URscript manual

    global UR5arm_ServoJlookAheadTimeSeconds_MaxVal
    UR5arm_ServoJlookAheadTimeSeconds_MaxVal = 0.2 #From URscript manual

    global UR5arm_ServoJgain_MinVal
    UR5arm_ServoJgain_MinVal = 100 #From URscript manual

    global UR5arm_ServoJgain_MaxVal
    UR5arm_ServoJgain_MaxVal = 2000 #From URscript manual

    #To limit inputs from JSON file.
    UR5arm_ServoJtimeDurationSeconds = LimitNumber_FloatOutputOnly(UR5arm_ServoJtimeDurationSeconds_MinVal, UR5arm_ServoJtimeDurationSeconds_MaxVal, UR5arm_ServoJtimeDurationSeconds)
    UR5arm_ServoJlookAheadTimeSeconds = LimitNumber_FloatOutputOnly(UR5arm_ServoJlookAheadTimeSeconds_MinVal, UR5arm_ServoJlookAheadTimeSeconds_MaxVal, UR5arm_ServoJlookAheadTimeSeconds)
    UR5arm_ServoJgain = LimitNumber_FloatOutputOnly(UR5arm_ServoJgain_MinVal, UR5arm_ServoJgain_MaxVal, UR5arm_ServoJgain)

    #################################################
    #################################################

    #################################################
    #################################################
    global ZEDasHandController_ReubenPython2and3ClassObject

    global ZEDasHandController_OPEN_FLAG
    ZEDasHandController_OPEN_FLAG = -1

    global ZEDasHandController_MostRecentDict
    ZEDasHandController_MostRecentDict = dict()

    global ZEDasHandController_MostRecentDict_TrackingState
    ZEDasHandController_MostRecentDict_TrackingState = ""

    global ZEDasHandController_MostRecentDict_ZEDcameraRotationVector
    ZEDasHandController_MostRecentDict_ZEDcameraRotationVector = [-11111.0] * 3

    global ZEDasHandController_MostRecentDict_NumberOfFramesGrabbed
    ZEDasHandController_MostRecentDict_NumberOfFramesGrabbed = -11111

    global ZEDasHandController_MostRecentDict_DataStreamingFrequency
    ZEDasHandController_MostRecentDict_DataStreamingFrequency = -11111.0

    global ZEDasHandController_MostRecentDict_Time
    ZEDasHandController_MostRecentDict_Time = -11111.0

    global ZEDasHandController_MostRecentDict_PosList_Raw
    ZEDasHandController_MostRecentDict_PosList_Raw = [-11111.0]*3

    global ZEDasHandController_MostRecentDict_RollPitchYaw_AbtXYZ_List_Radians_Raw
    ZEDasHandController_MostRecentDict_RollPitchYaw_AbtXYZ_List_Radians_Raw = [-11111.0]*3

    global ZEDasHandController_MostRecentDict_RollPitchYaw_AbtXYZ_List_Radians_Filtered
    ZEDasHandController_MostRecentDict_RollPitchYaw_AbtXYZ_List_Radians_Filtered = [-11111.0]*3

    global ZEDasHandController_MostRecentDict_RollPitchYaw_AbtXYZ_List_Degrees_Raw
    ZEDasHandController_MostRecentDict_RollPitchYaw_AbtXYZ_List_Degrees_Raw = [-11111.0]*3

    global ZEDasHandController_MostRecentDict_RollPitchYaw_AbtXYZ_List_Degrees_Filtered
    ZEDasHandController_MostRecentDict_RollPitchYaw_AbtXYZ_List_Degrees_Filtered = [-11111.0]*3

    global ZEDasHandController_PositionList
    ZEDasHandController_PositionList = [-11111.0] * 3

    global ZEDasHandController_PositionList_AtTimeOfClutchIn
    ZEDasHandController_PositionList_AtTimeOfClutchIn = [-11111.0] * 3

    global ZEDasHandController_RollPitchYaw_AbtXYZ_List_Degrees
    ZEDasHandController_RollPitchYaw_AbtXYZ_List_Degrees = [-11111.0] * 3

    global ZEDasHandController_RollPitchYaw_AbtXYZ_List_Degrees_AtTimeOfClutchIn
    ZEDasHandController_RollPitchYaw_AbtXYZ_List_Degrees_AtTimeOfClutchIn = [-11111.0] * 3

    global ZEDasHandController_RollPitchYaw_AbtXYZ_List_Radians
    ZEDasHandController_RollPitchYaw_AbtXYZ_List_Radians = [-11111.0] * 3

    global ZEDasHandController_RollPitchYaw_AbtXYZ_List_Radians_AtTimeOfClutchIn
    ZEDasHandController_RollPitchYaw_AbtXYZ_List_Radians_AtTimeOfClutchIn = [-11111.0] * 3

    global ZEDasHandController_Trigger_State
    ZEDasHandController_Trigger_State = -1

    global ZEDasHandController_Trigger_State_last
    ZEDasHandController_Trigger_State_last = -1

    global ZEDasHandController_AddToUR5armCurrentPositionList
    ZEDasHandController_AddToUR5armCurrentPositionList = [0.0]*3
    #################################################
    #################################################

    #################################################
    #################################################
    global RobotiqGripper2F85_ReubenPython2and3ClassObject

    global RobotiqGripper2F85_OPEN_FLAG
    RobotiqGripper2F85_OPEN_FLAG = -1

    global RobotiqGripper2F85_MostRecentDict
    RobotiqGripper2F85_MostRecentDict = dict()

    global RobotiqGripper2F85_MostRecentDict_SlaveIDreceivedFromGripper
    RobotiqGripper2F85_MostRecentDict_SlaveIDreceivedFromGripper = -11111

    global RobotiqGripper2F85_MostRecentDict_DataStreamingFrequency_CalculatedFromMainThread
    RobotiqGripper2F85_MostRecentDict_DataStreamingFrequency_CalculatedFromMainThread = -11111.0

    global RobotiqGripper2F85_MostRecentDict_Time
    RobotiqGripper2F85_MostRecentDict_Time = -11111.0

    global RobotiqGripper2F85_Position_ToBeSet
    RobotiqGripper2F85_Position_ToBeSet = RobotiqGripper2F85_Position_Starting
    
    global RobotiqGripper2F85_Speed_ToBeSet
    RobotiqGripper2F85_Speed_ToBeSet = RobotiqGripper2F85_Speed_Starting
    
    global RobotiqGripper2F85_Force_ToBeSet
    RobotiqGripper2F85_Force_ToBeSet = RobotiqGripper2F85_Force_Starting

    global RobotiqGripper2F85_PositionSpeedOrForce_NeedsToBeChangedFlag
    RobotiqGripper2F85_PositionSpeedOrForce_NeedsToBeChangedFlag = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global JoystickHID_ReubenPython2and3ClassObject

    global JOYSTICK_OPEN_FLAG
    JOYSTICK_OPEN_FLAG = -1

    global JOYSTICK_MostRecentDict
    JOYSTICK_MostRecentDict = dict()

    global JOYSTICK_MostRecentDict_Joystick_Axis_Value_List
    JOYSTICK_MostRecentDict_Joystick_Axis_Value_List = list()

    global JOYSTICK_MostRecentDict_Joystick_Button_Value_List
    JOYSTICK_MostRecentDict_Joystick_Button_Value_List = list()

    global JOYSTICK_MostRecentDict_Joystick_Button_LatchingRisingEdgeEvents_List
    JOYSTICK_MostRecentDict_Joystick_Button_LatchingRisingEdgeEvents_List = list()

    global JOYSTICK_MostRecentDict_Joystick_Hat_Value_List
    JOYSTICK_MostRecentDict_Joystick_Hat_Value_List = list()

    global JOYSTICK_MostRecentDict_Joystick_Hat_LatchingRisingEdgeEvents_List
    JOYSTICK_MostRecentDict_Joystick_Hat_LatchingRisingEdgeEvents_List = list()

    global JOYSTICK_MostRecentDict_Joystick_Ball_Value_List
    JOYSTICK_MostRecentDict_Joystick_Ball_Value_List = list()

    global JOYSTICK_MostRecentDict_DataStreamingFrequency
    JOYSTICK_MostRecentDict_DataStreamingFrequency = -11111.0

    global JOYSTICK_MostRecentDict_Time
    JOYSTICK_MostRecentDict_Time = -11111.0

    global Joystick_AddToUR5armCurrentPositionList
    Joystick_AddToUR5armCurrentPositionList = [0.0]*6

    global Joystick_ClutchState
    Joystick_ClutchState = 0
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject

    global PLOTTER_OPEN_FLAG
    PLOTTER_OPEN_FLAG = -1

    global MyPlotterPureTkinter_MostRecentDict
    MyPlotterPureTkinter_MostRecentDict = dict()

    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag
    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag = -1

    global LastTime_CalculatedFromMainThread_PLOTTER
    LastTime_CalculatedFromMainThread_PLOTTER = -11111.0
    #################################################
    #################################################

    #################################################
    #################################################
    global LoopCounter_CalculatedFromMainThread
    LoopCounter_CalculatedFromMainThread = 0

    global CurrentTime_CalculatedFromMainThread
    CurrentTime_CalculatedFromMainThread = -11111.0

    global StartingTime_CalculatedFromMainThread
    StartingTime_CalculatedFromMainThread = -11111.0

    global LastTime_CalculatedFromMainThread
    LastTime_CalculatedFromMainThread = -11111.0

    global DataStreamingFrequency_CalculatedFromMainThread
    DataStreamingFrequency_CalculatedFromMainThread = -1

    global DataStreamingDeltaT_CalculatedFromMainThread
    DataStreamingDeltaT_CalculatedFromMainThread = -1
    #################################################
    #################################################
    
    #################################################
    #################################################
    global LoopCounter_CalculatedFromGUIthread
    LoopCounter_CalculatedFromGUIthread = 0

    global CurrentTime_CalculatedFromGUIthread
    CurrentTime_CalculatedFromGUIthread = -11111.0

    global StartingTime_CalculatedFromGUIthread
    StartingTime_CalculatedFromGUIthread = -11111.0

    global LastTime_CalculatedFromGUIthread
    LastTime_CalculatedFromGUIthread = -11111.0

    global DataStreamingFrequency_CalculatedFromGUIthread
    DataStreamingFrequency_CalculatedFromGUIthread = -1

    global DataStreamingDeltaT_CalculatedFromGUIthread
    DataStreamingDeltaT_CalculatedFromGUIthread = -1
    #################################################
    #################################################

    #################################################
    #################################################
    global CSVfileForTrajectoryData_FileObject

    global CSVfileForTrajectoryData_SaveFlag_NeedsToBeChangedFlag
    CSVfileForTrajectoryData_SaveFlag_NeedsToBeChangedFlag = SAVE_CSV_FILE_OF_TRAJECTORY_DATA_FLAG_AT_START_OF_PROGRAM #If we want to record, then this will start it from state of 0.

    global CSVfileForTrajectoryData_SaveFlag
    CSVfileForTrajectoryData_SaveFlag = 0

    global CSVfileForTrajectoryData_DirectoryPath
    CSVfileForTrajectoryData_DirectoryPath = LogFile_Directory_Windows

    CreateNewDirectoryIfItDoesntExist(CSVfileForTrajectoryData_DirectoryPath)
    #################################################
    #################################################

    #################################################
    #################################################
    #All Keyboard variables defined in SharedGlobals_Teleop_UR5arm.py:
    #global DedicatedKeyboardListeningThread_StillRunningFlag
    #global KeyPressResponse_IncrementURtoolTipInX_NeedsToBeChangedFlag
    #etc.
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_KEYBOARD_FLAG == 1:
        DedicatedKeyboardListeningThread_ThreadingObject = threading.Thread(target=DedicatedKeyboardListeningThread, args=())
        DedicatedKeyboardListeningThread_ThreadingObject.setDaemon(True) #Means that thread is destroyed automatically when the main thread is destroyed.
        DedicatedKeyboardListeningThread_ThreadingObject.start()
    #################################################
    #################################################

    #################################################  KEY GUI LINE
    #################################################
    if USE_GUI_FLAG == 1:
        StartingTime_CalculatedFromGUIthread = getPreciseSecondsTimeStampString()
        print("Starting GUI thread...")

        global GUI_Thread_ThreadingObject
        GUI_Thread_ThreadingObject = threading.Thread(target=GUI_Thread)
        GUI_Thread_ThreadingObject.setDaemon(True)  # Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
        GUI_Thread_ThreadingObject.start()
        time.sleep(0.5)  # Allow enough time for 'root' to be created that we can then pass it into other classes.
    else:
        root = None
        Tab_MainControls = None
        Tab_UR5arm = None
        Tab_RobotiqGripper2F85 = None
        Tab_ZEDasHandController = None
        Tab_KEYBOARD = None
        Tab_JOYSTICK = None
        Tab_MyPrint = None
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPrint_ReubenPython2and3ClassObject_GUIparametersDict
    MyPrint_ReubenPython2and3ClassObject_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_MYPRINT_FLAG),
                                                                    ("root", Tab_MyPrint),
                                                                    ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                    ("GUI_ROW", GUI_ROW_MYPRINT),
                                                                    ("GUI_COLUMN", GUI_COLUMN_MYPRINT),
                                                                    ("GUI_PADX", GUI_PADX_MYPRINT),
                                                                    ("GUI_PADY", GUI_PADY_MYPRINT),
                                                                    ("GUI_ROWSPAN", GUI_ROWSPAN_MYPRINT),
                                                                    ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_MYPRINT),
                                                                    ("GUI_STICKY", "W")])

    global MyPrint_ReubenPython2and3ClassObject_LogFile_Directory_TO_BE_USED
    if SAVE_PROGRAM_LOGS_FLAG == 1:
        MyPrint_ReubenPython2and3ClassObject_LogFile_Directory_TO_BE_USED = LogFile_Directory_TO_BE_USED + "//Teleop_UR5arm_MyPrint_LogFile_" + str(int(round(getPreciseSecondsTimeStampString()))) +  ".txt"
    else:
        MyPrint_ReubenPython2and3ClassObject_LogFile_Directory_TO_BE_USED = "" #Meanings that no log will be save.

    global MyPrint_ReubenPython2and3ClassObject_setup_dict
    MyPrint_ReubenPython2and3ClassObject_setup_dict = dict([("NumberOfPrintLines", 20),
                                                            ("WidthOfPrintingLabel", 150),
                                                            ("PrintToConsoleFlag", 1),
                                                            ("LogFileNameFullPath", MyPrint_ReubenPython2and3ClassObject_LogFile_Directory_TO_BE_USED),
                                                            ("GUIparametersDict", MyPrint_ReubenPython2and3ClassObject_GUIparametersDict)])

    if USE_MYPRINT_FLAG == 1:
        try:
            MyPrint_ReubenPython2and3ClassObject = MyPrint_ReubenPython2and3Class(MyPrint_ReubenPython2and3ClassObject_setup_dict)
            MYPRINT_OPEN_FLAG = MyPrint_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPrint_ReubenPython2and3ClassObject __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    global UR5arm_ReubenPython2and3ClassObject_GUIparametersDict
    UR5arm_ReubenPython2and3ClassObject_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_UR5arm_StandAloneProcess_FLAG),
                                    ("EnableInternal_MyPrint_Flag", 1),
                                    ("GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents", 30),
                                    ("NumberOfPrintLines", 10),
                                    ("RootWindowWidth", UR5arm_RootWindowWidth),
                                    ("RootWindowHeight", UR5arm_RootWindowHeight),
                                    ("RootWindowStartingX", UR5arm_RootWindowStartingX),
                                    ("RootWindowStartingY", UR5arm_RootWindowStartingY),
                                    ("RootWindowTitle", UR5arm_RootWindowTitle)])

    global JointAngleCommandIncrementDecrement_CustomEntryLabels_ListOfDicts
    JointAngleCommandIncrementDecrement_CustomEntryLabels_ListOfDicts = [dict([("IncrementLabel", "Base, TOWARDS"),("DecrementLabel", " Base, AWAY")]),
                                                                        dict([("IncrementLabel", "Shoulder, AWAY"),("DecrementLabel", "Shoulder, TOWARDS")]),
                                                                        dict([("IncrementLabel", "Elbow, AWAY"),("DecrementLabel", "Elbow, TOWARDS")]),
                                                                        dict([("IncrementLabel", "Wrist Pitch, UP"),("DecrementLabel", "Wrist Pitch, DOWN")]),
                                                                        dict([("IncrementLabel", "Wrist Roll, TWIST DOWN"),("DecrementLabel", "Wrist Roll, TWIST UP")]),
                                                                        dict([("IncrementLabel", "Gripper Roll, UP"),("DecrementLabel", "Gripper Roll, DOWN")])]

    UR5arm_ReubenPython2and3ClassObject_setup_dict = dict([("GUIparametersDict", UR5arm_ReubenPython2and3ClassObject_GUIparametersDict),
                                                        ("NameToDisplay_UserSet", "UR5arm"),
                                                        ("RealTimeClientInterfaceVersionNumberString", UR5arm_RealTimeClientInterfaceVersionNumberString), #'<3.0' for test UR5CB2, '3.8' for test URCB3
                                                        ("ControllerBoxVersion", UR5arm_ControllerBoxVersion), #2, #3
                                                        ("IPV4_address", UR5arm_IPV4Address), #"192.168.1.100" "192.168.1.12"
                                                        ("IPV4_NumberOfRxMessagesToBuffers", UR5arm_IPV4_NumberOfRxMessagesToBuffers),
                                                        ("IPV4_TimeoutDurationSeconds", 5.0),
                                                        ("DedicatedRxThread_TimeToSleepEachLoop", 0.001),
                                                        ("DedicatedTxThread_MaximumTxMessagesPerSecondFrequency", UR5arm_DedicatedTxThread_MaximumTxMessagesPerSecondFrequency),
                                                        ("DedicatedTxThread_TxMessageToSend_Queue_MaxSize", UR5arm_DedicatedTxThread_TxMessageToSend_Queue_MaxSize),
                                                        ("StandAloneProcess_TimeToSleepEachLoop", UR5am_StandAloneProcess_TimeToSleepEachLoop),
                                                        ("PositionControl_ServoJ_MoveThroughListOfPoses_SafeReturnToStartingPoseFromAnywhere", list(UR5arm_PositionControl_ServoJ_MoveThroughListOfPoses_SafeReturnToStartingPoseFromAnywhere)),
                                                        ("StartingPoseJointAngleList_Deg", list(UR5arm_PositionControl_ServoJ_MoveThroughListOfPoses_SafeReturnToStartingPoseFromAnywhere)[0]["JointAngleList_Deg"]),
                                                        ("Payload_MassKG_ToBeCommanded", UR5arm_Payload_MassKG_ToBeCommanded),
                                                        ("Payload_CoGmetersList_ToBeCommanded", UR5arm_Payload_CoGmetersList_ToBeCommanded), #Determined experimentally on 12/16/21.
                                                        ("Acceleration", UR5arm_Acceleration),
                                                        ("Velocity", UR5arm_Velocity),
                                                        ("JointAngleCommandIncrementDecrement_ValueInDegrees", 1.0),
                                                        ("JointAngleCommandIncrementDecrement_CustomEntryLabels_ListOfDicts", JointAngleCommandIncrementDecrement_CustomEntryLabels_ListOfDicts),
                                                        ("ParentPID", os.getpid()),
                                                        ("WatchdogTimerDurationSeconds_ExpirationWillEndStandAloneProcess", UR5arm_WatchdogTimerDurationSeconds_ExpirationWillEndStandAloneProcess),
                                                        ("MultiprocessingQueue_Rx_MaxSize", UR5arm_MultiprocessingQueue_Rx_MaxSize),
                                                        ("MultiprocessingQueue_Tx_MaxSize", UR5arm_MultiprocessingQueue_Tx_MaxSize),
                                                        ("EnableTx_State_AtStartupFlag", UR5arm_EnableTx_State_AtStartupFlag)])
    if USE_UR5arm_FLAG == 1:
        try:
            UR5arm_ReubenPython2and3ClassObject = UR5arm_ReubenPython2and3Class(UR5arm_ReubenPython2and3ClassObject_setup_dict)

            #################################################
            UR5arm_OPEN_FLAG = 0
            CurrentTime_UR5arm_OpeningSleep = 0.0
            StartingTime_UR5arm_OpeningSleep = getPreciseSecondsTimeStampString()

            while CurrentTime_UR5arm_OpeningSleep < UR5arm_TimeDurationToWaitBetweenCreatingClassObjectAndReadingData_Seconds:
                time.sleep(0.1)
                print("CurrentTime_UR5arm_OpeningSleep: " + str(CurrentTime_UR5arm_OpeningSleep))

                CurrentTime_UR5arm_OpeningSleep = getPreciseSecondsTimeStampString() - StartingTime_UR5arm_OpeningSleep

                UR5arm_MostRecentDict_temp = UR5arm_ReubenPython2and3ClassObject.GetMostRecentDataDict()
                if len(UR5arm_MostRecentDict_temp) > 0 and "Time" in UR5arm_MostRecentDict_temp:
                    UR5arm_OPEN_FLAG = 1
                    print("Received first real data from GetMostRecentDataDict() @ CurrentTime_UR5arm_OpeningSleep: " + str(CurrentTime_UR5arm_OpeningSleep))
                    break
            #################################################

        except:
            exceptions = sys.exc_info()[0]
            print("UR5arm_ReubenPython2and3ClassObject __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    global ZEDasHandController_ReubenPython2and3ClassObject_GUIparametersDict
    ZEDasHandController_ReubenPython2and3ClassObject_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_ZEDasHandController_FLAG),
                                    ("root", Tab_ZEDasHandController),
                                    ("EnableInternal_MyPrint_Flag", 1),
                                    ("NumberOfPrintLines", 10),
                                    ("UseBorderAroundThisGuiObjectFlag", 0),
                                    ("GUI_ROW", GUI_ROW_ZEDasHandController),
                                    ("GUI_COLUMN", GUI_COLUMN_ZEDasHandController),
                                    ("GUI_PADX", GUI_PADX_ZEDasHandController),
                                    ("GUI_PADY", GUI_PADY_ZEDasHandController),
                                    ("GUI_ROWSPAN", GUI_ROWSPAN_ZEDasHandController),
                                    ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_ZEDasHandController)])

    global ZEDasHandController_ReubenPython2and3ClassObject_setup_dict
    ZEDasHandController_ReubenPython2and3ClassObject_setup_dict = dict([("GUIparametersDict", ZEDasHandController_ReubenPython2and3ClassObject_GUIparametersDict),
                                                                ("NameToDisplay_UserSet", "ZEDasHandController_ReubenPython2and3Class"),
                                                                ("MainThread_TimeToSleepEachLoop", ZEDasHandController_MainThread_TimeToSleepEachLoop),
                                                                ("Position_ExponentialFilterLambda", ZEDasHandController_Position_ExponentialFilterLambda),
                                                                ("Rotation_ExponentialFilterLambda", ZEDasHandController_Rotation_ExponentialFilterLambda),
                                                                ("DataCollectionDurationInSecondsForZeroing", ZEDasHandController_DataCollectionDurationInSecondsForZeroing),
                                                                ("ZEDcoordinateSystem", ZEDasHandController_ZEDcoordinateSystem),
                                                                ("ZEDresolution", ZEDasHandController_ZEDresolution),
                                                                ("ZEDfps", ZEDasHandController_ZEDfps)])

    if USE_ZEDasHandController_FLAG == 1:
        try:
            ZEDasHandController_ReubenPython2and3ClassObject = ZEDasHandController_ReubenPython2and3Class(ZEDasHandController_ReubenPython2and3ClassObject_setup_dict)
            ZEDasHandController_OPEN_FLAG = ZEDasHandController_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("ZEDasHandController_ReubenPython2and3ClassObject __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    global RobotiqGripper2F85_ReubenPython2and3ClassObject_GUIparametersDict
    RobotiqGripper2F85_ReubenPython2and3ClassObject_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_RobotiqGripper2F85_FLAG),
                                    ("root", Tab_RobotiqGripper2F85), #root Tab_RobotiqGripper2F85
                                    ("EnableInternal_MyPrint_Flag", 1),
                                    ("NumberOfPrintLines", 10),
                                    ("UseBorderAroundThisGuiObjectFlag", 0),
                                    ("GUI_ROW", GUI_ROW_RobotiqGripper2F85),
                                    ("GUI_COLUMN", GUI_COLUMN_RobotiqGripper2F85),
                                    ("GUI_PADX", GUI_PADX_RobotiqGripper2F85),
                                    ("GUI_PADY", GUI_PADY_RobotiqGripper2F85),
                                    ("GUI_ROWSPAN", GUI_ROWSPAN_RobotiqGripper2F85),
                                    ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_RobotiqGripper2F85)])

    global RobotiqGripper2F85_ReubenPython2and3ClassObject_setup_dict
    RobotiqGripper2F85_ReubenPython2and3ClassObject_setup_dict = dict([("GUIparametersDict", RobotiqGripper2F85_ReubenPython2and3ClassObject_GUIparametersDict),
                                                                        ("DesiredSerialNumber", RobotiqGripper2F85_DesiredSerialNumber), #CHANGE THIS TO MATCH YOUR UNIQUE USB-to-RS485serial converter
                                                                        ("DesiredSlaveID", RobotiqGripper2F85_DesiredSlaveID), #Gripper's default is 9
                                                                        ("NameToDisplay_UserSet", "Reuben's Test Robotiq 2F85 Gripper"),
                                                                        ("MainThread_TimeToSleepEachLoop", RobotiqGripper2F85_MainThread_TimeToSleepEachLoop),
                                                                        ("Position_Starting", RobotiqGripper2F85_Position_Starting),
                                                                        ("Speed_Starting", RobotiqGripper2F85_Speed_Starting),
                                                                        ("Force_Starting", RobotiqGripper2F85_Force_Starting),
                                                                        ("SendPositionSpeedForceCommandToGripper_Queue_MaxSize", 2),
                                                                        ("SendConfirmationToCommandFlag", 0)])

    if USE_RobotiqGripper2F85_FLAG == 1:
        try:
            RobotiqGripper2F85_ReubenPython2and3ClassObject = RobotiqGripper2F85_ReubenPython2and3Class(RobotiqGripper2F85_ReubenPython2and3ClassObject_setup_dict)
            RobotiqGripper2F85_OPEN_FLAG = RobotiqGripper2F85_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("RobotiqGripper2F85_ReubenPython2and3ClassObject __init__: Exceptions: %s" % exceptions, 0)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    global JoystickHID_ReubenPython2and3ClassObject_GUIparametersDict
    JoystickHID_ReubenPython2and3ClassObject_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_JOYSTICK_FLAG),
                                    ("root", Tab_JOYSTICK),
                                    ("EnableInternal_MyPrint_Flag", 1),
                                    ("NumberOfPrintLines", 10),
                                    ("UseBorderAroundThisGuiObjectFlag", 0),
                                    ("GUI_ROW", GUI_ROW_JOYSTICK),
                                    ("GUI_COLUMN", GUI_COLUMN_JOYSTICK),
                                    ("GUI_PADX", GUI_PADX_JOYSTICK),
                                    ("GUI_PADY", GUI_PADY_JOYSTICK),
                                    ("GUI_ROWSPAN", GUI_ROWSPAN_JOYSTICK),
                                    ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_JOYSTICK)])

    global JoystickHID_ReubenPython2and3ClassObject_setup_dict
    JoystickHID_ReubenPython2and3ClassObject_setup_dict = dict([("GUIparametersDict", JoystickHID_ReubenPython2and3ClassObject_GUIparametersDict),
                                                                ("NameToDisplay_UserSet", "JoystickHID_ReubenPython2and3Class"),
                                                                ("Joystick_NameDesired", Joystick_NameDesired),
                                                                ("Joystick_IntegerIDdesired", Joystick_IntegerIDdesired),
                                                                ("Joystick_ShowJustDotMovingFlag", Joystick_ShowJustDotMovingFlag),
                                                                ("Joystick_Axis_Index_ToDisplayAsHorizontalAxisOn2DdotDisplay", Joystick_Axis_Index_ToDisplayAsHorizontalAxisOn2DdotDisplay),
                                                                ("Joystick_Axis_Index_ToDisplayAsVerticalAxisOn2DdotDisplay", Joystick_Axis_Index_ToDisplayAsVerticalAxisOn2DdotDisplay),
                                                                ("Joystick_Button_Index_ToDisplayAsDotColorOn2DdotDisplay", Joystick_Clutch_Button_Index_ToDisplayAsDotColorOn2DdotDisplay),
                                                                ("MainThread_TimeToSleepEachLoop", 0.010),
                                                                ("Joystick_PrintInfoForAllDetectedJoysticksFlag", Joystick_PrintInfoForAllDetectedJoysticksFlag)])

    if USE_JOYSTICK_FLAG == 1:
        try:
            JoystickHID_ReubenPython2and3ClassObject = JoystickHID_ReubenPython2and3Class(JoystickHID_ReubenPython2and3ClassObject_setup_dict)
            JOYSTICK_OPEN_FLAG = JoystickHID_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("JoystickHID_ReubenPython2and3ClassObject __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_setup_dict["GUIparametersDict"] = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_GUIparametersDict
    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_setup_dict["ParentPID"] = os.getpid()

    if USE_PLOTTER_FLAG == 1:
        try:
            MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class(MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_setup_dict)
            PLOTTER_OPEN_FLAG = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject, exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MYPRINT_FLAG == 1 and MYPRINT_OPEN_FLAG != 1:
        print("Failed to open MyPrint_ReubenPython2and3ClassObject.")
        ExitProgram_Callback()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_UR5arm_FLAG == 1 and UR5arm_OPEN_FLAG != 1:
        print("Failed to open UR5arm_ReubenPython2and3Class.")
        ExitProgram_Callback()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_ZEDasHandController_FLAG == 1 and ZEDasHandController_OPEN_FLAG != 1:
        print("Failed to open ZEDasHandController_ReubenPython2and3Class.")
        ExitProgram_Callback()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_RobotiqGripper2F85_FLAG == 1 and RobotiqGripper2F85_OPEN_FLAG != 1:
        print("Failed to open RobotiqGripper2F85_ReubenPython2and3Class.")
        ExitProgram_Callback()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_JOYSTICK_FLAG == 1 and JOYSTICK_OPEN_FLAG != 1:
        print("Failed to open JoystickHID_ReubenPython2and3Class.")
        ExitProgram_Callback()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_PLOTTER_FLAG == 1 and PLOTTER_OPEN_FLAG != 1:
        print("Failed to open MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.")
        ExitProgram_Callback()
    #################################################
    #################################################

    #################################################
    #################################################
    UR5arm_BlockWhileExecuting_MoveSafelyToStartingPoseViaMultipointSequence()
    #################################################
    #################################################

    #################################################
    #################################################
    if MYPRINT_OPEN_FLAG == 1:
        MyPrint_ReubenPython2and3ClassObject.my_print("Starting main loop 'Teleop_UR5arm'.")
    else:
        print("Starting main loop 'Teleop_UR5arm'.")
    #################################################
    #################################################

    #################################################
    #################################################
    StartingTime_CalculatedFromMainThread = getPreciseSecondsTimeStampString()
    #################################################
    #################################################

    while(SharedGlobals_Teleop_UR5arm.EXIT_PROGRAM_FLAG == 0):
        ###################################################################################################### Start GET's
        ######################################################################################################
        ######################################################################################################
        ######################################################################################################
        ######################################################################################################

        ################################################### GETs
        ###################################################
        CurrentTime_CalculatedFromMainThread = getPreciseSecondsTimeStampString() - StartingTime_CalculatedFromMainThread
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        if CSVfileForTrajectoryData_SaveFlag_NeedsToBeChangedFlag == 1:

            if CSVfileForTrajectoryData_SaveFlag == 1: #Currently saving, need to close the file.
                CloseCSVfileForTrajectoryDataAndStopWritingData()

            else: #Currently NOT saving, need to open the file.
                CreateCSVfileForTrajectoryDataAndStartWritingData()

            CSVfileForTrajectoryData_SaveFlag_NeedsToBeChangedFlag = 0

        ###################################################
        ###################################################

        ################################################### GET's
        ###################################################
        if JSONfiles_NeedsToBeLoadedFlag == 1:
            LoadAndParseJSONfile_GUIsettings()
            LoadAndParseJSONfile_UR5()
            LoadAndParseJSONfile_ControlLawParameters()

            LoadAndParseJSONfile_Keyboard()
            KeyboardMapKeysToCallbackFunctions()

            LoadAndParseJSONfile_Joystick()
            LoadAndParseJSONfile_ZEDasHandController()

            '''
            UPDATE UR PARAMETERS HERE UPON RELOADING JSON FILE
            '''

            JSONfiles_NeedsToBeLoadedFlag = 0
        ###################################################
        ###################################################

        ################################################### GET's FOR STAND-ALONE-PROCESS
        ###################################################
        if UR5arm_OPEN_FLAG == 1:
            try:
                UR5arm_MostRecentDict_temp = UR5arm_ReubenPython2and3ClassObject.GetMostRecentDataDict()

                if len(UR5arm_MostRecentDict_temp) > 0 and "Time" in UR5arm_MostRecentDict_temp:
                    UR5arm_MostRecentDict = UR5arm_MostRecentDict_temp

                    UR5arm_MostRecentDict_ToolVectorActual_IsItInitializedFlag = 1

                    SharedGlobals_Teleop_UR5arm.UR5arm_MostRecentDict_JointAngleList_Deg = UR5arm_MostRecentDict["JointAngleList_Deg"]
                    SharedGlobals_Teleop_UR5arm.UR5arm_MostRecentDict_JointAngleList_Rad = UR5arm_MostRecentDict["JointAngleList_Rad"]
                    SharedGlobals_Teleop_UR5arm.UR5arm_MostRecentDict_ToolVectorActual = UR5arm_MostRecentDict["ToolVectorActual"]
                    UR5arm_MostRecentDict_ToolTipSpeedsCartestian_TCPspeedActual = UR5arm_MostRecentDict["ToolTipSpeedsCartestian_TCPspeedActual"]
                    UR5arm_MostRecentDict_ToolTipSpeedsCartestian_LinearXYZnorm_MetersPerSec = UR5arm_MostRecentDict["ToolTipSpeedsCartestian_LinearXYZnorm_MetersPerSec"]
                    UR5arm_MostRecentDict_DataStreamingFrequency_CalculatedFromDedicatedRxThread = UR5arm_MostRecentDict["DataStreamingFrequency_CalculatedFromDedicatedRxThread"]
                    UR5arm_MostRecentDict_Time = UR5arm_MostRecentDict["Time"]

                    #print("UR5arm_MostRecentDict_Time: " + str(UR5arm_MostRecentDict_Time))
            except:
                exceptions = sys.exc_info()[0]
                print("Teleop_UR5arm, UR5arm GET's, exceptions: %s" % exceptions)
                #traceback.print_exc()
        ###################################################
        ###################################################

        ################################################### GET's
        ###################################################
        if ZEDasHandController_OPEN_FLAG == 1:

            ZEDasHandController_MostRecentDict = ZEDasHandController_ReubenPython2and3ClassObject.GetMostRecentDataDict()

            if "Time" in ZEDasHandController_MostRecentDict:

                #####
                ZEDasHandController_MostRecentDict_TrackingState = ZEDasHandController_MostRecentDict["TrackingState"]
                ZEDasHandController_MostRecentDict_ZEDcameraRotationVector = ZEDasHandController_MostRecentDict["ZEDcameraRotationVector"]
                ZEDasHandController_MostRecentDict_NumberOfFramesGrabbed = ZEDasHandController_MostRecentDict["NumberOfFramesGrabbed"]
                ZEDasHandController_MostRecentDict_DataStreamingFrequency = ZEDasHandController_MostRecentDict["DataStreamingFrequency"]
                ZEDasHandController_MostRecentDict_Time = ZEDasHandController_MostRecentDict["Time"]

                ZEDasHandController_MostRecentDict_PosList_Raw = ZEDasHandController_MostRecentDict["PosList_Raw"]
                ZEDasHandController_MostRecentDict_PosList_Filtered = ZEDasHandController_MostRecentDict["PosList_Filtered"]
                ZEDasHandController_MostRecentDict_RollPitchYaw_AbtXYZ_List_Radians_Raw = ZEDasHandController_MostRecentDict["RollPitchYaw_AbtXYZ_List_Radians_Raw"]
                ZEDasHandController_MostRecentDict_RollPitchYaw_AbtXYZ_List_Radians_Filtered = ZEDasHandController_MostRecentDict["RollPitchYaw_AbtXYZ_List_Radians_Filtered"]
                ZEDasHandController_MostRecentDict_RollPitchYaw_AbtXYZ_List_Degrees_Raw = ZEDasHandController_MostRecentDict["RollPitchYaw_AbtXYZ_List_Degrees_Raw"]
                ZEDasHandController_MostRecentDict_RollPitchYaw_AbtXYZ_List_Degrees_Filtered = ZEDasHandController_MostRecentDict["RollPitchYaw_AbtXYZ_List_Degrees_Filtered"]
                #####

                #print("ZEDasHandController_MostRecentDict: " + str(ZEDasHandController_MostRecentDict))
                #print("ZEDasHandController_MostRecentDict_Time: " + str(ZEDasHandController_MostRecentDict_Time))

                #####
                ZEDasHandController_PositionList = ZEDasHandController_MostRecentDict_PosList_Filtered
                ZEDasHandController_RollPitchYaw_AbtXYZ_List_Degrees = ZEDasHandController_MostRecentDict_RollPitchYaw_AbtXYZ_List_Degrees_Filtered
                ZEDasHandController_RollPitchYaw_AbtXYZ_List_Radians = ZEDasHandController_MostRecentDict_RollPitchYaw_AbtXYZ_List_Radians_Filtered
                #####

                #####
                for Index in range(0,3):
                    ZEDasHandController_PositionList[Index] = ZEDasHandController_PositionList[Index]*ZEDasHandController_PositionList_ScalingFactorList[Index]
                    ZEDasHandController_RollPitchYaw_AbtXYZ_List_Radians[Index] = ZEDasHandController_RollPitchYaw_AbtXYZ_List_Radians[Index]*ZEDasHandController_RollPitchYaw_AbtXYZ_List_ScalingFactorList[Index]
                    ZEDasHandController_RollPitchYaw_AbtXYZ_List_Degrees[Index] = ZEDasHandController_RollPitchYaw_AbtXYZ_List_Degrees[Index]*ZEDasHandController_RollPitchYaw_AbtXYZ_List_ScalingFactorList[Index]
                #####

                #####
                ZEDasHandController_Trigger_State = SharedGlobals_Teleop_UR5arm.KeyPressResponse_ZEDcontrolClutch_State #SPACE bar
                #####

                #####
                if ZEDasHandController_Trigger_State == 1 and ZEDasHandController_Trigger_State_last == 0:
                    ZEDasHandController_PositionList_AtTimeOfClutchIn = list(ZEDasHandController_PositionList)
                    ZEDasHandController_RollPitchYaw_AbtXYZ_List_Radians_AtTimeOfClutchIn = list(ZEDasHandController_RollPitchYaw_AbtXYZ_List_Radians)
                    ZEDasHandController_RollPitchYaw_AbtXYZ_List_Degrees_AtTimeOfClutchIn = list(ZEDasHandController_RollPitchYaw_AbtXYZ_List_Degrees)

                    UR5arm_MostRecentDict_ToolVectorActual_AtTimeOfClutchIn = list(SharedGlobals_Teleop_UR5arm.UR5arm_MostRecentDict_ToolVectorActual)
                #####

                #####
                ZEDasHandController_Trigger_State_last = ZEDasHandController_Trigger_State
                #####

        ###################################################
        ###################################################

        ################################################### GET's
        ###################################################
        if RobotiqGripper2F85_OPEN_FLAG == 1:

            RobotiqGripper2F85_MostRecentDict = RobotiqGripper2F85_ReubenPython2and3ClassObject.GetMostRecentDataDict()

            if "Time" in RobotiqGripper2F85_MostRecentDict:
                RobotiqGripper2F85_MostRecentDict_SlaveIDreceivedFromGripper = RobotiqGripper2F85_MostRecentDict["SlaveIDreceivedFromGripper"]
                RobotiqGripper2F85_MostRecentDict_DataStreamingFrequency_CalculatedFromMainThread = RobotiqGripper2F85_MostRecentDict["DataStreamingFrequency_CalculatedFromMainThread"]
                RobotiqGripper2F85_MostRecentDict_Time = RobotiqGripper2F85_MostRecentDict["Time"]

                #print("RobotiqGripper2F85_MostRecentDict_Time: " + str(RobotiqGripper2F85_MostRecentDict_Time))
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        if JOYSTICK_OPEN_FLAG == 1:

            JOYSTICK_MostRecentDict = JoystickHID_ReubenPython2and3ClassObject.GetMostRecentDataDict()

            if "Time" in JOYSTICK_MostRecentDict:
                JOYSTICK_MostRecentDict_Joystick_Axis_Value_List = JOYSTICK_MostRecentDict["Joystick_Axis_Value_List"]
                JOYSTICK_MostRecentDict_Joystick_Button_Value_List = JOYSTICK_MostRecentDict["Joystick_Button_Value_List"]
                JOYSTICK_MostRecentDict_Joystick_Button_LatchingRisingEdgeEvents_List = JOYSTICK_MostRecentDict["Joystick_Button_LatchingRisingEdgeEvents_List"]
                JOYSTICK_MostRecentDict_Joystick_Hat_Value_List = JOYSTICK_MostRecentDict["Joystick_Hat_Value_List"]
                JOYSTICK_MostRecentDict_Joystick_Hat_LatchingRisingEdgeEvents_List = JOYSTICK_MostRecentDict["Joystick_Hat_LatchingRisingEdgeEvents_List"]
                JOYSTICK_MostRecentDict_Joystick_Ball_Value_List = JOYSTICK_MostRecentDict["Joystick_Ball_Value_List"]
                JOYSTICK_MostRecentDict_DataStreamingFrequency = JOYSTICK_MostRecentDict["DataStreamingFrequency"]
                JOYSTICK_MostRecentDict_Time = JOYSTICK_MostRecentDict["Time"]

                #print("JOYSTICK_MostRecentDict_Joystick_Axis_Value_List: " + str(JOYSTICK_MostRecentDict_Joystick_Axis_Value_List))
        ###################################################
        ###################################################

        ######################################################################################################
        ######################################################################################################
        ######################################################################################################
        ######################################################################################################
        ###################################################################################################### End GET's

        ###################################################################################################### Start Control Law
        ######################################################################################################
        ######################################################################################################
        ######################################################################################################
        ######################################################################################################

        ###################################################
        ###################################################
        ###################################################
        if ControlType_NeedsToBeChangedFlag == 1:
            dummy = 0
            ControlType_NeedsToBeChangedFlag = 0
        ###################################################
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        ###################################################
        #We can include JoystickControl here because the joystick-->robotiq code will overwrite these keyboard-generated values later.
        #However, if 'ParametersToBeLoaded_Joystick.json' doesn't map anything to the Robotiq (like with the SpaceMouse), then this keyboard code's values will still map to the Robotiq.
        if ControlType == "KeyboardControl" or ControlType == "JoystickControl" or ControlType == "ZEDcontrol":

            ###################################################
            ###################################################
            if SharedGlobals_Teleop_UR5arm.KeyPressResponse_OpenRobotiqGripper2F85_NeedsToBeChangedFlag  == 1:
                RobotiqGripper2F85_Position_ToBeSet = LimitNumber_FloatOutputOnly(0.0, 255.0, RobotiqGripper2F85_Position_ToBeSet + SharedGlobals_Teleop_UR5arm.Keyboard_KeysToTeleopControlsMapping_DictOfDicts["OpenRobotiqGripper2F85"]["IncrementSize"])

                RobotiqGripper2F85_PositionSpeedOrForce_NeedsToBeChangedFlag = 1
                #SharedGlobals_Teleop_UR5arm.KeyPressResponse_OpenRobotiqGripper2F85_NeedsToBeChangedFlag = 0 #HANDLED INSTEAD BY THE REVERSE KEY-PRESS
            ###################################################
            ###################################################

            ###################################################
            ###################################################
            if SharedGlobals_Teleop_UR5arm.KeyPressResponse_CloseRobotiqGripper2F85_NeedsToBeChangedFlag  == 1:
                RobotiqGripper2F85_Position_ToBeSet = LimitNumber_FloatOutputOnly(0.0, 255.0, RobotiqGripper2F85_Position_ToBeSet + SharedGlobals_Teleop_UR5arm.Keyboard_KeysToTeleopControlsMapping_DictOfDicts["CloseRobotiqGripper2F85"]["IncrementSize"])

                RobotiqGripper2F85_PositionSpeedOrForce_NeedsToBeChangedFlag = 1
                #SharedGlobals_Teleop_UR5arm.KeyPressResponse_CloseRobotiqGripper2F85_NeedsToBeChangedFlag = 0 #HANDLED INSTEAD BY THE REVERSE KEY-PRESS
            ###################################################
            ###################################################

        ###################################################
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        ###################################################
        if ControlType == "KeyboardControl":

            if UR5arm_MostRecentDict_ToolVectorActual_IsItInitializedFlag == 1:

                if SharedGlobals_Teleop_UR5arm.KeyPressResponse_IncrementURtoolTipInX_NeedsToBeChangedFlag == 1:
                    UR5arm_ToolVectorActual_ToBeSet = list(SharedGlobals_Teleop_UR5arm.UR5arm_MostRecentDict_ToolVectorActual)
                    UR5arm_ToolVectorActual_ToBeSet[0] = UR5arm_ToolVectorActual_ToBeSet[0] + SharedGlobals_Teleop_UR5arm.Keyboard_KeysToTeleopControlsMapping_DictOfDicts["Xincrement"]["IncrementSize"]
                    UR5arm_PositionControl_NeedsToBeChangedFlag = 1
                    #SharedGlobals_Teleop_UR5arm.KeyPressResponse_IncrementURtoolTipInX_NeedsToBeChangedFlag = 0 #HANDLED INSTEAD BY THE REVERSE KEY-PRESS

                if SharedGlobals_Teleop_UR5arm.KeyPressResponse_DecrementURtoolTipInX_NeedsToBeChangedFlag == 1:
                    UR5arm_ToolVectorActual_ToBeSet = list(SharedGlobals_Teleop_UR5arm.UR5arm_MostRecentDict_ToolVectorActual)
                    UR5arm_ToolVectorActual_ToBeSet[0] = UR5arm_ToolVectorActual_ToBeSet[0] + SharedGlobals_Teleop_UR5arm.Keyboard_KeysToTeleopControlsMapping_DictOfDicts["Xdecrement"]["IncrementSize"]
                    UR5arm_PositionControl_NeedsToBeChangedFlag = 1
                    #SharedGlobals_Teleop_UR5arm.KeyPressResponse_DecrementURtoolTipInX_NeedsToBeChangedFlag = 0 #HANDLED INSTEAD BY THE REVERSE KEY-PRESS

                if SharedGlobals_Teleop_UR5arm.KeyPressResponse_IncrementURtoolTipInY_NeedsToBeChangedFlag == 1:
                    UR5arm_ToolVectorActual_ToBeSet = list(SharedGlobals_Teleop_UR5arm.UR5arm_MostRecentDict_ToolVectorActual)
                    UR5arm_ToolVectorActual_ToBeSet[1] = UR5arm_ToolVectorActual_ToBeSet[1] + SharedGlobals_Teleop_UR5arm.Keyboard_KeysToTeleopControlsMapping_DictOfDicts["Yincrement"]["IncrementSize"]
                    UR5arm_PositionControl_NeedsToBeChangedFlag = 1
                    #SharedGlobals_Teleop_UR5arm.KeyPressResponse_IncrementURtoolTipInY_NeedsToBeChangedFlag = 0 #HANDLED INSTEAD BY THE REVERSE KEY-PRESS

                if SharedGlobals_Teleop_UR5arm.KeyPressResponse_DecrementURtoolTipInY_NeedsToBeChangedFlag == 1:
                    UR5arm_ToolVectorActual_ToBeSet = list(SharedGlobals_Teleop_UR5arm.UR5arm_MostRecentDict_ToolVectorActual)
                    UR5arm_ToolVectorActual_ToBeSet[1] = UR5arm_ToolVectorActual_ToBeSet[1] + SharedGlobals_Teleop_UR5arm.Keyboard_KeysToTeleopControlsMapping_DictOfDicts["Ydecrement"]["IncrementSize"]
                    UR5arm_PositionControl_NeedsToBeChangedFlag = 1
                    #SharedGlobals_Teleop_UR5arm.KeyPressResponse_DecrementURtoolTipInY_NeedsToBeChangedFlag = 0 #HANDLED INSTEAD BY THE REVERSE KEY-PRESS

                if SharedGlobals_Teleop_UR5arm.KeyPressResponse_IncrementURtoolTipInZ_NeedsToBeChangedFlag == 1:
                    UR5arm_ToolVectorActual_ToBeSet = list(SharedGlobals_Teleop_UR5arm.UR5arm_MostRecentDict_ToolVectorActual)
                    UR5arm_ToolVectorActual_ToBeSet[2] = UR5arm_ToolVectorActual_ToBeSet[2] + SharedGlobals_Teleop_UR5arm.Keyboard_KeysToTeleopControlsMapping_DictOfDicts["Zincrement"]["IncrementSize"]
                    UR5arm_PositionControl_NeedsToBeChangedFlag = 1
                    #SharedGlobals_Teleop_UR5arm.KeyPressResponse_IncrementURtoolTipInZ_NeedsToBeChangedFlag = 0 #HANDLED INSTEAD BY THE REVERSE KEY-PRESS

                if SharedGlobals_Teleop_UR5arm.KeyPressResponse_DecrementURtoolTipInZ_NeedsToBeChangedFlag == 1:
                    UR5arm_ToolVectorActual_ToBeSet = list(SharedGlobals_Teleop_UR5arm.UR5arm_MostRecentDict_ToolVectorActual)
                    UR5arm_ToolVectorActual_ToBeSet[2] = UR5arm_ToolVectorActual_ToBeSet[2] + SharedGlobals_Teleop_UR5arm.Keyboard_KeysToTeleopControlsMapping_DictOfDicts["Zdecrement"]["IncrementSize"]
                    UR5arm_PositionControl_NeedsToBeChangedFlag = 1
                    #SharedGlobals_Teleop_UR5arm.KeyPressResponse_DecrementURtoolTipInZ_NeedsToBeChangedFlag = 0 #HANDLED INSTEAD BY THE REVERSE KEY-PRESS

        ###################################################
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        ###################################################
        if ControlType == "JoystickControl":

            ###################################################
            ###################################################
            if UR5arm_MostRecentDict_ToolVectorActual_IsItInitializedFlag == 1 and JOYSTICK_OPEN_FLAG == 1:

                ###################################################
                if Joystick_UseClutchFlag == 1:
                    Joystick_ClutchState = JOYSTICK_MostRecentDict_Joystick_Button_Value_List[Joystick_Clutch_Button_Index_ToDisplayAsDotColorOn2DdotDisplay]
                else:
                    Joystick_ClutchState = 1
                ###################################################

                if Joystick_ClutchState == 1:

                    ###################################################
                    for Index in range(0,6):
                        AxisHatButtonOrBallTo6DOFposeMappingDict = Joystick_AxisHatButtonOrBallTo6DOFposeMapping_ListOfDicts[Index]

                        IncrementSize = AxisHatButtonOrBallTo6DOFposeMappingDict["IncrementSize"]
                        PrimaryAxisHatButtonOrBallIndex = AxisHatButtonOrBallTo6DOFposeMappingDict["PrimaryAxisHatButtonOrBallIndex"]
                        SecondaryAxisHatButtonOrBallIndex = AxisHatButtonOrBallTo6DOFposeMappingDict["SecondaryAxisHatButtonOrBallIndex"]

                        if AxisHatButtonOrBallTo6DOFposeMappingDict["AxisHatButtonOrBallType"] == "AXIS":
                            Joystick_AddToUR5armCurrentPositionList[Index] = IncrementSize*JOYSTICK_MostRecentDict_Joystick_Axis_Value_List[PrimaryAxisHatButtonOrBallIndex]

                        elif AxisHatButtonOrBallTo6DOFposeMappingDict["AxisHatButtonOrBallType"] == "HAT":
                            Joystick_AddToUR5armCurrentPositionList[Index] = IncrementSize*JOYSTICK_MostRecentDict_Joystick_Hat_Value_List[PrimaryAxisHatButtonOrBallIndex][SecondaryAxisHatButtonOrBallIndex]

                        else:
                            print("In JoystickControl, only AXIS and HAT can be used to control the UR5.") #Nothing other than an axis or hat can be used as an input currently (no buttons or balls).

                    ###################################################

                    #We're NOT using UR5arm_MostRecentDict_ToolVectorActual_AtTimeOfClutchIn because the joystick inputs rate-control, not absolute position.
                    UR5arm_ToolVectorActual_ToBeSet = list(SharedGlobals_Teleop_UR5arm.UR5arm_MostRecentDict_ToolVectorActual)

                    ###################################################
                    for Index in range(0,6):
                        UR5arm_ToolVectorActual_ToBeSet[Index] = UR5arm_ToolVectorActual_ToBeSet[Index]  + Joystick_AddToUR5armCurrentPositionList[Index]
                    ###################################################

                    UR5arm_PositionControl_NeedsToBeChangedFlag = 1

            else:
                UR5arm_ToolVectorActual_ToBeSet = list(SharedGlobals_Teleop_UR5arm.UR5arm_MostRecentDict_ToolVectorActual)
            ###################################################
            ###################################################

            ###################################################
            ###################################################
            if RobotiqGripper2F85_OPEN_FLAG == 1:

                ###################################################
                if len(Joystick_AxisHatButtonOrBallTo6DOFposeMapping_ListOfDicts) >= 7: #If 'ParametersToBeLoaded_Joystick.json' includes mapping to the Robotiq.
                    AxisHatButtonOrBallTo6DOFposeMappingDict = Joystick_AxisHatButtonOrBallTo6DOFposeMapping_ListOfDicts[6]

                    IncrementSize = AxisHatButtonOrBallTo6DOFposeMappingDict["IncrementSize"]
                    PrimaryAxisHatButtonOrBallIndex = AxisHatButtonOrBallTo6DOFposeMappingDict["PrimaryAxisHatButtonOrBallIndex"]
                    SecondaryAxisHatButtonOrBallIndex = AxisHatButtonOrBallTo6DOFposeMappingDict["SecondaryAxisHatButtonOrBallIndex"]

                    if AxisHatButtonOrBallTo6DOFposeMappingDict["AxisHatButtonOrBallType"] == "AXIS":
                        RobotiqGripper2F85_Position_ToBeSet = RobotiqGripper2F85_Position_ToBeSet + IncrementSize*JOYSTICK_MostRecentDict_Joystick_Axis_Value_List[PrimaryAxisHatButtonOrBallIndex]

                    elif AxisHatButtonOrBallTo6DOFposeMappingDict["AxisHatButtonOrBallType"] == "HAT":
                        RobotiqGripper2F85_Position_ToBeSet = RobotiqGripper2F85_Position_ToBeSet + IncrementSize*JOYSTICK_MostRecentDict_Joystick_Hat_Value_List[PrimaryAxisHatButtonOrBallIndex][SecondaryAxisHatButtonOrBallIndex]

                    elif AxisHatButtonOrBallTo6DOFposeMappingDict["AxisHatButtonOrBallType"] == "BUTTON":
                        #PrimaryAxisHatButtonOrBallIndex is 1 button (for opening), and SecondaryAxisHatButtonOrBallIndex is another button (for closing).
                        #If both are pressed at once, then nothing will happen as they cancel eachother out.
                        RobotiqGripper2F85_Position_ToBeSet = RobotiqGripper2F85_Position_ToBeSet + IncrementSize*JOYSTICK_MostRecentDict_Joystick_Button_Value_List[PrimaryAxisHatButtonOrBallIndex] - IncrementSize*JOYSTICK_MostRecentDict_Joystick_Button_Value_List[SecondaryAxisHatButtonOrBallIndex]

                    else:
                        print("In JoystickControl, only AXIS, HAT, and BUTTON can be specified to control the RobotiqGripper2F85.") #Nothing other than an axis or hat can be used as an input currently (no buttons or balls).

                    RobotiqGripper2F85_Position_ToBeSet = LimitNumber_FloatOutputOnly(0.0, 255.0, RobotiqGripper2F85_Position_ToBeSet)
                    RobotiqGripper2F85_PositionSpeedOrForce_NeedsToBeChangedFlag = 1
                ###################################################

            ###################################################
            ###################################################

        ###################################################
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        ###################################################
        if ControlType == "ZEDcontrol":

            if UR5arm_MostRecentDict_ToolVectorActual_IsItInitializedFlag == 1 and ZEDasHandController_OPEN_FLAG == 1 and ZEDasHandController_Trigger_State == 1: #dragon

                ZEDasHandController_AddToUR5armCurrentPositionList = numpy.array(ZEDasHandController_RotationMatrixListsOfLists).dot(numpy.array(ZEDasHandController_PositionList) - numpy.array(ZEDasHandController_PositionList_AtTimeOfClutchIn)).tolist()

                #We're locking to UR5arm_MostRecentDict_ToolVectorActual_AtTimeOfClutchIn, not updating based on actual each function.
                UR5arm_ToolVectorActual_ToBeSet = list(UR5arm_MostRecentDict_ToolVectorActual_AtTimeOfClutchIn)

                ###################################################
                ###################################################
                for Index in range(0,3):
                    UR5arm_ToolVectorActual_ToBeSet[Index] = UR5arm_ToolVectorActual_ToBeSet[Index]  + ZEDasHandController_AddToUR5armCurrentPositionList[Index]
                ###################################################
                ###################################################

                UR5arm_PositionControl_NeedsToBeChangedFlag = 1

            else:
                UR5arm_ToolVectorActual_ToBeSet = list(SharedGlobals_Teleop_UR5arm.UR5arm_MostRecentDict_ToolVectorActual)
                ZEDasHandController_AddToUR5armCurrentPositionList = [0.0]*3

        ###################################################
        ###################################################
        ###################################################

        ######################################################################################################
        ######################################################################################################
        ######################################################################################################
        ######################################################################################################
        ###################################################################################################### End Control Law

        ###################################################################################################### Start SET's
        ######################################################################################################
        ######################################################################################################
        ######################################################################################################
        ######################################################################################################

        ################################################### SET's
        ###################################################
        ###################################################
        if UR5arm_OPEN_FLAG == 1:

            ###################################################
            ###################################################
            if UR5arm_StopMotion_State_NeedsToBeChangedFlag == 1:
                UR5arm_ReubenPython2and3ClassObject.FunctionCallToStandAloneProcess("StopMotion_JointSpace",
                                                                                    [],
                                                                                    MultiprocessingQueue_Rx_MaxSize_Local=UR5arm_MultiprocessingQueue_Rx_MaxSize,
                                                                                    IgnoreNewDataIfQueueIsFullFlag=1)
                UR5arm_StopMotion_State_NeedsToBeChangedFlag = 0
            ###################################################
            ###################################################

            ################################################### unicorn
            ###################################################
            if UR5arm_AllowExternalCommandsFromMainProgram_Flag == 1:

                ###################################################
                if UR5arm_MoveSafelyToStartingPose_NeedsToBeChangedFlag == 1 and UR5arm_PositionControl_NeedsToBeChangedFlag == 0:
                    UR5arm_ReubenPython2and3ClassObject.FunctionCallToStandAloneProcess("MoveSafelyToStartingPoseViaMultipointSequence",
                                                                                        [],
                                                                                        MultiprocessingQueue_Rx_MaxSize_Local=UR5arm_MultiprocessingQueue_Rx_MaxSize,
                                                                                        IgnoreNewDataIfQueueIsFullFlag=1)

                    UR5arm_MoveSafelyToStartingPose_NeedsToBeChangedFlag = 0
                ###################################################

                ###################################################
                elif UR5arm_MoveSafelyToStartingPose_NeedsToBeChangedFlag == 0 and UR5arm_PositionControl_NeedsToBeChangedFlag == 1:
                    UR5arm_ReubenPython2and3ClassObject.FunctionCallToStandAloneProcess("PositionControl_ServoJ_MoveThroughListOfPoses",
                                                                                        [[dict([("PoseIsInToolSpaceFlag", 1), ("ToolTip6DOFpose", UR5arm_ToolVectorActual_ToBeSet), ("TimeDurationSec", UR5arm_ServoJtimeDurationSeconds), ("lookahead_time", UR5arm_ServoJlookAheadTimeSeconds), ("gain", UR5arm_ServoJgain)])]],
                                                                                        MultiprocessingQueue_Rx_MaxSize_Local=UR5arm_MultiprocessingQueue_Rx_MaxSize,
                                                                                        IgnoreNewDataIfQueueIsFullFlag=1)

                    UR5arm_PositionControl_NeedsToBeChangedFlag = 0
                ###################################################

                ###################################################
                else:
                    UR5arm_ReubenPython2and3ClassObject.FunctionCallToStandAloneProcess("KickWatchdogButDoNothing",
                                                                                        [0],
                                                                                        MultiprocessingQueue_Rx_MaxSize_Local=UR5arm_MultiprocessingQueue_Rx_MaxSize,
                                                                                        IgnoreNewDataIfQueueIsFullFlag=1)
                ###################################################

            else:
                UR5arm_ReubenPython2and3ClassObject.FunctionCallToStandAloneProcess("KickWatchdogButDoNothing",
                                                                                    [0],
                                                                                    MultiprocessingQueue_Rx_MaxSize_Local=UR5arm_MultiprocessingQueue_Rx_MaxSize,
                                                                                    IgnoreNewDataIfQueueIsFullFlag=1)

            ###################################################
            ###################################################

        ###################################################
        ###################################################
        ###################################################

        ################################################### SET's
        ###################################################
        if RobotiqGripper2F85_OPEN_FLAG == 1:
            if RobotiqGripper2F85_PositionSpeedOrForce_NeedsToBeChangedFlag == 1:
                RobotiqGripper2F85_ReubenPython2and3ClassObject.SendPositionSpeedForceCommandToGripper_ExternalClassFunction(int(RobotiqGripper2F85_Position_ToBeSet), int(RobotiqGripper2F85_Speed_ToBeSet), int(RobotiqGripper2F85_Force_ToBeSet), IgnoreNewDataIfQueueIsFullFlag=0)
                RobotiqGripper2F85_PositionSpeedOrForce_NeedsToBeChangedFlag = 0
        ###################################################
        ###################################################

        ################################################### SETs
        ###################################################
        if PLOTTER_OPEN_FLAG == 1:

            ####################################################
            MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.GetMostRecentDataDict()

            if "StandAlonePlottingProcess_ReadyForWritingFlag" in MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict:
                MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict["StandAlonePlottingProcess_ReadyForWritingFlag"]

                if MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag == 1:
                    if CurrentTime_CalculatedFromMainThread - LastTime_CalculatedFromMainThread_PLOTTER >= 0.040:
                        #MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.ExternalAddPointOrListOfPointsToPlot(["Channel0"], [CurrentTime_CalculatedFromMainThread], [Tension_ActualValue_grams])
                        #MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.ExternalAddPointOrListOfPointsToPlot(["Channel0", "Channel1"], [CurrentTime_CalculatedFromMainThread, CurrentTime_CalculatedFromMainThread], [PIDcontroller_Tension_MostRecentDict_ActualValueDot_ActualValueDot_Raw, PIDcontroller_Tension_MostRecentDict_ActualValueDot_ActualValueDot_Filtered])

                        MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.ExternalAddPointOrListOfPointsToPlot(["Channel0", "Channel1", "Channel2"], [CurrentTime_CalculatedFromMainThread]*3, ZEDasHandController_PositionList)



                        LastTime_CalculatedFromMainThread_PLOTTER = CurrentTime_CalculatedFromMainThread
            ####################################################

        ###################################################
        ###################################################

        ################################################# SET's
        #################################################
        if CSVfileForTrajectoryData_SaveFlag == 1:

            for Index in range(0, 6):
                UR5arm_MostRecentDict_ToolVectorActual_MotionFromSnapshotAtTimeOfCreatingCSVfileForTrajectoryData[Index] = SharedGlobals_Teleop_UR5arm.UR5arm_MostRecentDict_ToolVectorActual[Index] - UR5arm_MostRecentDict_ToolVectorActual_SnapshotAtTimeOfCreatingCSVfileForTrajectoryData[Index]

            CSVfileForTrajectoryData_LineToWrite = ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(CurrentTime_CalculatedFromMainThread, 0, 5) + \
                                                    ", " + \
                                                    ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(ZEDasHandController_MostRecentDict_PosList_Raw, 0, 5).replace("[","").replace("]","") + \
                                                    ", " +\
                                                    ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(UR5arm_MostRecentDict_ToolVectorActual_MotionFromSnapshotAtTimeOfCreatingCSVfileForTrajectoryData, 0, 5).replace("[","").replace("]","") + \
                                                    "\n"
            CSVfileForTrajectoryData_FileObject.write(CSVfileForTrajectoryData_LineToWrite)
        ###################################################
        ###################################################

        ######################################################################################################
        ######################################################################################################
        ######################################################################################################
        ######################################################################################################
        ###################################################################################################### End SET's

        ###################################################################################################### Update "last" values, calculate frequency, and sleep
        ######################################################################################################
        ######################################################################################################
        ######################################################################################################
        ######################################################################################################
        #PLACE TO UPDATE LAST_ VARIABLES

        [LoopCounter_CalculatedFromMainThread, LastTime_CalculatedFromMainThread, DataStreamingFrequency_CalculatedFromMainThread, DataStreamingDeltaT_CalculatedFromMainThread] = UpdateFrequencyCalculation(LoopCounter_CalculatedFromMainThread, CurrentTime_CalculatedFromMainThread, LastTime_CalculatedFromMainThread, DataStreamingFrequency_CalculatedFromMainThread, DataStreamingDeltaT_CalculatedFromMainThread)
        time.sleep(Teleop_UR5arm_MainThread_TimeToSleepEachLoop)

        ######################################################################################################
        ######################################################################################################
        ######################################################################################################
        ######################################################################################################
        ######################################################################################################

    ###################################################
    ###################################################
    ###################################################

    #################################################### THIS IS THE EXIT ROUTINE!
    ###################################################
    ###################################################
    print("Exiting main program 'Teleop_UR5arm'.")

    #################################################
    if CSVfileForTrajectoryData_SaveFlag == 1:
        print("Exiting CSV file by issuing CloseCSVfileForTrajectoryDataAndStopWritingData.")
        CloseCSVfileForTrajectoryDataAndStopWritingData()
    #################################################

    #################################################
    if MYPRINT_OPEN_FLAG == 1:
        MyPrint_ReubenPython2and3ClassObject.ExitProgram_Callback()
    #################################################

    #################################################
    if UR5arm_OPEN_FLAG == 1:
            #THE EFFECTIVENESS OF THIS EXIT FUNCTION CALL SEEMS TO DEPEND ON Teleop_UR5arm_MainThread_TimeToSleepEachLoop (how quickly the main thread is running).
            #Note sure why. When it's 0.001, then sometimes the UR5 standalone process doesn't get this exit signal. When it's larger (like 0.008), then it's not a problem.
            #WHAT CAUSES THIS?
            UR5arm_ReubenPython2and3ClassObject.FunctionCallToStandAloneProcess("ExitProgram_Callback",
                                                                                [],
                                                                                MultiprocessingQueue_Rx_MaxSize_Local=UR5arm_MultiprocessingQueue_Rx_MaxSize,
                                                                                IgnoreNewDataIfQueueIsFullFlag=1)
    #################################################

    #################################################
    if ZEDasHandController_OPEN_FLAG == 1:
        ZEDasHandController_ReubenPython2and3ClassObject.ExitProgram_Callback()
    #################################################

    #################################################
    if RobotiqGripper2F85_OPEN_FLAG == 1:
        RobotiqGripper2F85_ReubenPython2and3ClassObject.ExitProgram_Callback()
    #################################################

    #################################################
    if JOYSTICK_OPEN_FLAG == 1:
        JoystickHID_ReubenPython2and3ClassObject.ExitProgram_Callback()
    #################################################

    #################################################
    if PLOTTER_OPEN_FLAG == 1:
        MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.ExitProgram_Callback()
    #################################################

    ###################################################
    ###################################################
    ###################################################

#######################################################################################################################
#######################################################################################################################