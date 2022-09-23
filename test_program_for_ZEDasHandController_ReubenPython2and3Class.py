# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision E, 09/21/2022

Verified working on: Python 3.8 for Windows 10 64-bit and Ubuntu 20.04.
'''

__author__ = 'reuben.brewer'

#########################################################
#https://github.com/Reuben-Brewer/ZEDasHandController_ReubenPython2and3Class
from ZEDasHandController_ReubenPython2and3Class import *
#########################################################

#########################################################
#https://github.com/Reuben-Brewer/MyPrint_ReubenPython2and3Class
from MyPrint_ReubenPython2and3Class import *
#########################################################

#########################################################
#https://github.com/Reuben-Brewer/MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class
from MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class import *
#########################################################

#########################################################
import os
import sys
import platform
import time
import datetime
import threading
import collections
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

###########################################################################################################
##########################################################################################################
def getPreciseSecondsTimeStampString():
    ts = time.time()

    return ts
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def getTimeStampString():

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%m_%d_%Y---%H_%M_%S')

    return st
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def CreateNewDirectoryIfItDoesntExist(directory):
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
def GUI_update_clock():
    global root
    global EXIT_PROGRAM_FLAG
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_GUI_FLAG

    global ZEDasHandController_ReubenPython2and3ClassObject
    global ZEDasHandController_OPEN_FLAG
    global SHOW_IN_GUI_ZEDasHandController_FLAG
    global ZEDasHandController_MostRecentDict

    global MyPrint_ReubenPython2and3ClassObject
    global MYPRINT_OPEN_FLAG
    global SHOW_IN_GUI_MYPRINT_FLAG

    global ZEDasHandController_Label

    if USE_GUI_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
        #########################################################
        #########################################################

            #########################################################
            ZEDasHandController_Label["text"] = ConvertDictToProperlyFormattedStringForPrinting(ZEDasHandController_MostRecentDict, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3)
            #########################################################

            #########################################################
            if ZEDasHandController_OPEN_FLAG == 1 and SHOW_IN_GUI_ZEDasHandController_FLAG == 1:
                ZEDasHandController_ReubenPython2and3ClassObject.GUI_update_clock()
            #########################################################

            #########################################################
            if MYPRINT_OPEN_FLAG == 1 and SHOW_IN_GUI_MYPRINT_FLAG == 1:
                MyPrint_ReubenPython2and3ClassObject.GUI_update_clock()
            #########################################################

            root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
        #########################################################
        #########################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ExitProgram_Callback():
    global EXIT_PROGRAM_FLAG

    print("ExitProgram_Callback event fired!")

    EXIT_PROGRAM_FLAG = 1
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
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

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
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
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_Thread():
    global root
    global root_Xpos
    global root_Ypos
    global root_width
    global root_height
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_TABS_IN_GUI_FLAG
    global ZEDasHandController_Label

    ################################################# KEY GUI LINE
    #################################################
    root = Tk()
    #################################################
    #################################################

    #################################################
    #################################################
    global TabControlObject
    global Tab_MainControls
    global Tab_ZEDasHandController
    global Tab_MyPrint

    if USE_TABS_IN_GUI_FLAG == 1:
        #################################################
        TabControlObject = ttk.Notebook(root)

        Tab_ZEDasHandController = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_ZEDasHandController, text='   ZEDasHandController   ')

        Tab_MainControls = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_MainControls, text='   Main Controls   ')

        Tab_MyPrint = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_MyPrint, text='   MyPrint Terminal   ')

        TabControlObject.pack(expand=1, fill="both")  # CANNOT MIX PACK AND GRID IN THE SAME FRAME/TAB, SO ALL .GRID'S MUST BE CONTAINED WITHIN THEIR OWN FRAME/TAB.

        ############# #Set the tab header font
        TabStyle = ttk.Style()
        TabStyle.configure('TNotebook.Tab', font=('Helvetica', '12', 'bold'))
        #############
        
        #################################################
    else:
        #################################################
        Tab_MainControls = root
        Tab_ZEDasHandController = root
        Tab_MyPrint = root
        #################################################

    #################################################
    #################################################

    #################################################
    #################################################
    ZEDasHandController_Frame = Frame(Tab_MainControls)
    ZEDasHandController_Frame.grid(row=0, column=0, padx=1, pady=1, columnspan=10, rowspan=1)
    #################################################
    #################################################

    #################################################
    #################################################
    Buttons_Frame = Frame(ZEDasHandController_Frame)
    Buttons_Frame.grid(row=0, column=0, padx=1, pady=1, columnspan=10, rowspan=1)
    #################################################
    #################################################

    #################################################
    #################################################
    ZEDasHandController_Label = Label(ZEDasHandController_Frame, text="ZEDasHandController_Label", width=100)
    ZEDasHandController_Label.grid(row=1, column=0, padx=1, pady=1, columnspan=1, rowspan=1, sticky="w")
    #################################################
    #################################################

    #################################################
    #################################################
    ZeroPosition_Button = Button(Buttons_Frame, text="Zero Position", state="normal", width=15, command=lambda: ZeroPosition_ButtonResponse())
    ZeroPosition_Button.grid(row=0, column=1, padx=10, pady=10, rowspan=1, columnspan=1)
    #################################################
    #################################################

    #################################################
    #################################################
    ZeroRotation_Button = Button(Buttons_Frame, text="Zero Rotation", state="normal", width=15, command=lambda: ZeroRotation_ButtonResponse())
    ZeroRotation_Button.grid(row=0, column=2, padx=10, pady=10, rowspan=1, columnspan=1)
    #################################################
    #################################################

    ################################################# THIS BLOCK MUST COME 2ND-TO-LAST IN def  GUI_Thread() IF USING TABS.
    #################################################
    root.protocol("WM_DELETE_WINDOW", ExitProgram_Callback)  # Set the callback function for when the window's closed.
    root.title("test_program_for_ZEDasHandController_ReubenPython2and3Class")
    root.geometry('%dx%d+%d+%d' % (root_width, root_height, root_Xpos, root_Ypos)) # set the dimensions of the screen and where it is placed
    root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
    root.mainloop()
    #################################################
    #################################################

    #################################################  THIS BLOCK MUST COME LAST IN def  GUI_Thread() REGARDLESS OF CODE.
    #################################################
    root.quit() #Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
    root.destroy() #Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
    #################################################
    #################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ZeroPosition_ButtonResponse():
    global ZEDasHandController_OPEN_FLAG
    global ZEDasHandController_ReubenPython2and3ClassObject
    
    if ZEDasHandController_OPEN_FLAG == 1:
        ZEDasHandController_ReubenPython2and3ClassObject.ZeroPosition()
        print("ZeroPosition_ButtonResponse: Event fired !")
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ZeroRotation_ButtonResponse():
    global ZEDasHandController_OPEN_FLAG
    global ZEDasHandController_ReubenPython2and3ClassObject

    if ZEDasHandController_OPEN_FLAG == 1:
        ZEDasHandController_ReubenPython2and3ClassObject.ZeroRotation()
        print("ZeroRotation_ButtonResponse: Event fired !")
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    #################################################
    #################################################
    global my_platform

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
    #################################################
    #################################################

    #################################################
    #################################################
    global USE_GUI_FLAG
    USE_GUI_FLAG = 1

    global USE_TABS_IN_GUI_FLAG
    USE_TABS_IN_GUI_FLAG = 1

    global USE_ZEDasHandController_FLAG
    USE_ZEDasHandController_FLAG = 1

    global USE_MYPRINT_FLAG
    USE_MYPRINT_FLAG = 0

    global USE_PLOTTER_FLAG_XYZ
    USE_PLOTTER_FLAG_XYZ = 1
    
    global USE_PLOTTER_FLAG_RollPitchYaw
    USE_PLOTTER_FLAG_RollPitchYaw = 1

    global SAVE_CSV_FILE_OF_TRAJECTORY_DATA_FLAG_AT_START_OF_PROGRAM
    SAVE_CSV_FILE_OF_TRAJECTORY_DATA_FLAG_AT_START_OF_PROGRAM = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global SHOW_IN_GUI_ZEDasHandController_FLAG
    SHOW_IN_GUI_ZEDasHandController_FLAG = 1

    global SHOW_IN_GUI_MYPRINT_FLAG
    SHOW_IN_GUI_MYPRINT_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global GUI_ROW_ZEDasHandController
    global GUI_COLUMN_ZEDasHandController
    global GUI_PADX_ZEDasHandController
    global GUI_PADY_ZEDasHandController
    global GUI_ROWSPAN_ZEDasHandController
    global GUI_COLUMNSPAN_ZEDasHandController
    GUI_ROW_ZEDasHandController = 1

    GUI_COLUMN_ZEDasHandController = 0
    GUI_PADX_ZEDasHandController = 1
    GUI_PADY_ZEDasHandController = 1
    GUI_ROWSPAN_ZEDasHandController = 1
    GUI_COLUMNSPAN_ZEDasHandController = 1

    global GUI_ROW_MYPRINT
    global GUI_COLUMN_MYPRINT
    global GUI_PADX_MYPRINT
    global GUI_PADY_MYPRINT
    global GUI_ROWSPAN_MYPRINT
    global GUI_COLUMNSPAN_MYPRINT
    GUI_ROW_MYPRINT = 2

    GUI_COLUMN_MYPRINT = 0
    GUI_PADX_MYPRINT = 1
    GUI_PADY_MYPRINT = 1
    GUI_ROWSPAN_MYPRINT = 1
    GUI_COLUMNSPAN_MYPRINT = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0

    global CurrentTime_MainLoopThread
    CurrentTime_MainLoopThread = -11111.0

    global StartingTime_MainLoopThread
    StartingTime_MainLoopThread = -11111.0

    global root

    global root_Xpos
    root_Xpos = 900

    global root_Ypos
    root_Ypos = 0

    global root_width
    root_width = 1920 - root_Xpos

    global root_height
    root_height = 1020 - root_Ypos

    global TabControlObject
    global Tab_MainControls
    global Tab_ZEDasHandController
    global Tab_MyPrint

    global GUI_RootAfterCallbackInterval_Milliseconds
    GUI_RootAfterCallbackInterval_Milliseconds = 30
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
    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_XYZ

    global PLOTTER_OPEN_FLAG_XYZ
    PLOTTER_OPEN_FLAG_XYZ = -1

    global LastTime_MainLoopThread_PLOTTER_XYZ
    LastTime_MainLoopThread_PLOTTER_XYZ = -11111.0
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_RollPitchYaw

    global PLOTTER_OPEN_FLAG_RollPitchYaw
    PLOTTER_OPEN_FLAG_RollPitchYaw = -1

    global LastTime_MainLoopThread_PLOTTER_RollPitchYaw
    LastTime_MainLoopThread_PLOTTER_RollPitchYaw = -11111.0
    #################################################
    #################################################

    #################################################  KEY GUI LINE
    #################################################
    if USE_GUI_FLAG == 1:
        print("Starting GUI thread...")
        GUI_Thread_ThreadingObject = threading.Thread(target=GUI_Thread)
        GUI_Thread_ThreadingObject.setDaemon(True) #Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
        GUI_Thread_ThreadingObject.start()
        time.sleep(0.5)  #Allow enough time for 'root' to be created that we can then pass it into other classes.
    else:
        root = None
        Tab_MainControls = None
        Tab_ZEDasHandController = None
        Tab_MyPrint = None
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
                                                                ("NameToDisplay_UserSet", "Reuben's ZEDasHandController_ReubenPython2and3Class Test"),
                                                                ("MainThread_TimeToSleepEachLoop", 0.001),
                                                                ("Position_ExponentialFilterLambda", 0.9),
                                                                ("Rotation_ExponentialFilterLambda", 0.9),
                                                                ("DataCollectionDurationInSecondsForZeroing", 1.0),
                                                                ("ZEDcoordinateSystem", "RIGHT_HANDED_Z_UP"),
                                                                ("ZEDresolution", "HD720"),
                                                                ("ZEDfps", 60)])

    # NOTE: Positional tracking uses image and depth information to estimate the position of the camera in 3D space.
    # To improve tracking results, use high FPS video modes such as HD720 and WVGA.

    '''
    self.ZEDcoordinateSystemOptions = ["RIGHT_HANDED_Y_DOWN",   #default
                                    "LEFT_HANDED_Y_UP",             #Unity
                                    "RIGHT_HANDED_Y_UP",            #OpenGL
                                    "LEFT_HANDED_Z_UP",             #Unreal Engine
                                    "RIGHT_HANDED_Z_UP"]            #ROS
    '''

    '''
    self.ZEDresolutionOptions = ["HD2K",    #2208*1242 (x2), available framerates: 15 fps.
                                "HD1080",   #1920*1080 (x2), available framerates: 15, 30 fps.
                                "HD720",    #1280*720 (x2), available framerates: 15, 30, 60 fps.
                                "VGA"]  #672*376 (x2), available framerates: 15, 30, 60, 100 fps.
    '''

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
    if USE_MYPRINT_FLAG == 1:

        MyPrint_ReubenPython2and3ClassObject_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_MYPRINT_FLAG),
                                                                        ("root", Tab_MyPrint),
                                                                        ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                        ("GUI_ROW", GUI_ROW_MYPRINT),
                                                                        ("GUI_COLUMN", GUI_COLUMN_MYPRINT),
                                                                        ("GUI_PADX", GUI_PADX_MYPRINT),
                                                                        ("GUI_PADY", GUI_PADY_MYPRINT),
                                                                        ("GUI_ROWSPAN", GUI_ROWSPAN_MYPRINT),
                                                                        ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_MYPRINT)])

        MyPrint_ReubenPython2and3ClassObject_setup_dict = dict([("NumberOfPrintLines", 10),
                                                                ("WidthOfPrintingLabel", 200),
                                                                ("PrintToConsoleFlag", 1),
                                                                ("LogFileNameFullPath", os.getcwd() + "//TestLog.txt"),
                                                                ("GUIparametersDict", MyPrint_ReubenPython2and3ClassObject_GUIparametersDict)])

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
    global MyPlotterPureTkinter_MostRecentDict_XYZ
    MyPlotterPureTkinter_MostRecentDict_XYZ = dict()

    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag_XYZ
    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag_XYZ = -1



    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_GUIparametersDict_XYZ = dict([("EnableInternal_MyPrint_Flag", 1),
                                                                                                ("NumberOfPrintLines", 10),
                                                                                                ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                                                ("GraphCanvasWidth", 890),
                                                                                                ("GraphCanvasHeight", 500),
                                                                                                ("GraphCanvasWindowStartingX", 0),
                                                                                                ("GraphCanvasWindowStartingY", 0),
                                                                                                ("GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents", 20)])

    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_setup_dict_XYZ
    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_setup_dict_XYZ = dict([("GUIparametersDict", MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_GUIparametersDict_XYZ),
                                                                                        ("ParentPID", os.getpid()),
                                                                                        ("WatchdogTimerExpirationDurationSeconds_StandAlonePlottingProcess", 5.0),
                                                                                        ("MarkerSize", 3),
                                                                                        ("CurvesToPlotNamesAndColorsDictOfLists", dict([("NameList", ["X", "Y", "Z"]),("ColorList", ["Red", "Green", "Blue"])])),
                                                                                        ("NumberOfDataPointToPlot", 50),
                                                                                        ("XaxisNumberOfTickMarks", 10),
                                                                                        ("YaxisNumberOfTickMarks", 10),
                                                                                        ("XaxisNumberOfDecimalPlacesForLabels", 3),
                                                                                        ("YaxisNumberOfDecimalPlacesForLabels", 3),
                                                                                        ("XaxisAutoscaleFlag", 1),
                                                                                        ("YaxisAutoscaleFlag", 1),
                                                                                        ("X_min", 0.0),
                                                                                        ("X_max", 20.0),
                                                                                        ("Y_min", -0.0015),
                                                                                        ("Y_max", 0.0015),
                                                                                        ("XaxisDrawnAtBottomOfGraph", 0),
                                                                                        ("XaxisLabelString", "Time (sec)"),
                                                                                        ("YaxisLabelString", "XYZ"),
                                                                                        ("ShowLegendFlag", 1)])

    if USE_PLOTTER_FLAG_XYZ == 1:
        try:
            MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_XYZ = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class(MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_setup_dict_XYZ)
            PLOTTER_OPEN_FLAG_XYZ = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_XYZ.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_XYZ, exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPlotterPureTkinter_MostRecentDict_RollPitchYaw
    MyPlotterPureTkinter_MostRecentDict_RollPitchYaw = dict()

    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag_RollPitchYaw
    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag_RollPitchYaw = -1

    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_GUIparametersDict_RollPitchYaw = dict([("EnableInternal_MyPrint_Flag", 1),
                                                                                                ("NumberOfPrintLines", 10),
                                                                                                ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                                                ("GraphCanvasWidth", 890),
                                                                                                ("GraphCanvasHeight", 500),
                                                                                                ("GraphCanvasWindowStartingX", 0),
                                                                                                ("GraphCanvasWindowStartingY", 510),
                                                                                                ("GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents", 20)])

    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_setup_dict_RollPitchYaw
    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_setup_dict_RollPitchYaw = dict([("GUIparametersDict", MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_GUIparametersDict_RollPitchYaw),
                                                                                        ("ParentPID", os.getpid()),
                                                                                        ("WatchdogTimerExpirationDurationSeconds_StandAlonePlottingProcess", 5.0),
                                                                                        ("MarkerSize", 3),
                                                                                        ("CurvesToPlotNamesAndColorsDictOfLists", dict([("NameList", ["Roll", "Pitch", "Yaw"]),("ColorList", ["Red", "Green", "Blue"])])),
                                                                                        ("NumberOfDataPointToPlot", 50),
                                                                                        ("XaxisNumberOfTickMarks", 10),
                                                                                        ("YaxisNumberOfTickMarks", 10),
                                                                                        ("XaxisNumberOfDecimalPlacesForLabels", 3),
                                                                                        ("YaxisNumberOfDecimalPlacesForLabels", 3),
                                                                                        ("XaxisAutoscaleFlag", 1),
                                                                                        ("YaxisAutoscaleFlag", 1),
                                                                                        ("X_min", 0.0),
                                                                                        ("X_max", 20.0),
                                                                                        ("Y_min", -0.0015),
                                                                                        ("Y_max", 0.0015),
                                                                                        ("XaxisDrawnAtBottomOfGraph", 0),
                                                                                        ("XaxisLabelString", "Time (sec)"),
                                                                                        ("YaxisLabelString", "RollPitchYaw (Degrees)"),
                                                                                        ("ShowLegendFlag", 1)])

    if USE_PLOTTER_FLAG_RollPitchYaw == 1:
        try:
            MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_RollPitchYaw = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class(MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_setup_dict_RollPitchYaw)
            PLOTTER_OPEN_FLAG_RollPitchYaw = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_RollPitchYaw.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_RollPitchYaw, exceptions: %s" % exceptions)
            traceback.print_exc()
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
    if USE_MYPRINT_FLAG == 1 and MYPRINT_OPEN_FLAG != 1:
        print("Failed to open MyPrint_ReubenPython2and3ClassObject.")
        ExitProgram_Callback()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_PLOTTER_FLAG_XYZ == 1 and PLOTTER_OPEN_FLAG_XYZ != 1:
        print("Failed to open MyPlotterPureTkinterClass_Object_XYZ.")
        ExitProgram_Callback()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_PLOTTER_FLAG_RollPitchYaw == 1 and PLOTTER_OPEN_FLAG_RollPitchYaw != 1:
        print("Failed to open MyPlotterPureTkinterClass_Object_RollPitchYaw.")
        ExitProgram_Callback()
    #################################################
    #################################################

    #################################################
    #################################################
    print("Starting main loop 'test_program_for_ZEDasHandController_ReubenPython2and3Class.")
    StartingTime_MainLoopThread = getPreciseSecondsTimeStampString()

    #################################################
    if SAVE_CSV_FILE_OF_TRAJECTORY_DATA_FLAG_AT_START_OF_PROGRAM == 1:
        CSVfileDirectoryPath = os.getcwd() + "//Logs"
        CreateNewDirectoryIfItDoesntExist(CSVfileDirectoryPath)
        CSVfilepathFull = CSVfileDirectoryPath + "//ZEDlog_" + getTimeStampString() + ".csv"
        print("CSVfilepathFull: " + CSVfilepathFull)

        CSVfileToWriteTo = open(CSVfilepathFull, "a") #Will append to file if it exists, create new file with this as first entry if file doesn't exist.
        CSVfileToWriteTo.write("X, Y, Z" + "\n")
    #################################################

    while(EXIT_PROGRAM_FLAG == 0):

        ###################################################
        ###################################################
        CurrentTime_MainLoopThread = getPreciseSecondsTimeStampString() - StartingTime_MainLoopThread
        ###################################################
        ###################################################

        ################################################### GET's
        ###################################################
        if ZEDasHandController_OPEN_FLAG == 1:

            ZEDasHandController_MostRecentDict = ZEDasHandController_ReubenPython2and3ClassObject.GetMostRecentDataDict()

            if "Time" in ZEDasHandController_MostRecentDict:

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

                #print("ZEDasHandController_MostRecentDict: " + str(ZEDasHandController_MostRecentDict))
                #print("ZEDasHandController_MostRecentDict_Time: " + str(ZEDasHandController_MostRecentDict_Time))
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        if SAVE_CSV_FILE_OF_TRAJECTORY_DATA_FLAG_AT_START_OF_PROGRAM == 1:
            LineToWrite = ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(ZEDasHandController_MostRecentDict_PosList_Raw, 0, 5).replace("[","").replace("]","") + "\n"
            CSVfileToWriteTo.write(LineToWrite)
        ###################################################
        ###################################################

        ####################################################
        ####################################################
        if PLOTTER_OPEN_FLAG_XYZ == 1:

            ####################################################
            MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_XYZ = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_XYZ.GetMostRecentDataDict()

            if "StandAlonePlottingProcess_ReadyForWritingFlag" in MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_XYZ:
                MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag_XYZ = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_XYZ["StandAlonePlottingProcess_ReadyForWritingFlag"]

                if MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag_XYZ == 1:
                    if CurrentTime_MainLoopThread - LastTime_MainLoopThread_PLOTTER_XYZ >= 0.050:

                        #####
                        #MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_XYZ.ExternalAddPointOrListOfPointsToPlot(["X", "Y", "Z"], [CurrentTime_MainLoopThread]*3, ZEDasHandController_MostRecentDict_PosList_Raw)
                        MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_XYZ.ExternalAddPointOrListOfPointsToPlot(["X", "Y", "Z"], [CurrentTime_MainLoopThread]*3, ZEDasHandController_MostRecentDict_PosList_Filtered)

                        #MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_XYZ.ExternalAddPointOrListOfPointsToPlot(["X", "Y"], [CurrentTime_MainLoopThread]*2, [ZEDasHandController_MostRecentDict_PosList_Raw[0], ZEDasHandController_MostRecentDict_PosList_Filtered[0]])
                        #MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_XYZ.ExternalAddPointOrListOfPointsToPlot(["X", "Y"], [CurrentTime_MainLoopThread]*2, [ZEDasHandController_MostRecentDict_PosList_Raw[1], ZEDasHandController_MostRecentDict_PosList_Filtered[1]])
                        #MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_XYZ.ExternalAddPointOrListOfPointsToPlot(["X", "Y"], [CurrentTime_MainLoopThread]*2, [ZEDasHandController_MostRecentDict_PosList_Raw[2], ZEDasHandController_MostRecentDict_PosList_Filtered[2]])
                        #####

                        #####
                        LastTime_MainLoopThread_PLOTTER_XYZ = CurrentTime_MainLoopThread
                        #####

            ####################################################

        ####################################################
        ####################################################

        ####################################################
        ####################################################
        if PLOTTER_OPEN_FLAG_RollPitchYaw == 1:

            ####################################################
            MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_RollPitchYaw = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_RollPitchYaw.GetMostRecentDataDict()

            if "StandAlonePlottingProcess_ReadyForWritingFlag" in MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_RollPitchYaw:
                MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag_RollPitchYaw = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_RollPitchYaw["StandAlonePlottingProcess_ReadyForWritingFlag"]

                if MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag_RollPitchYaw == 1:
                    if CurrentTime_MainLoopThread - LastTime_MainLoopThread_PLOTTER_RollPitchYaw >= 0.050:

                        #####
                        #MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_RollPitchYaw.ExternalAddPointOrListOfPointsToPlot(["Roll", "Pitch", "Yaw"], [CurrentTime_MainLoopThread]*3, ZEDasHandController_MostRecentDict_RollPitchYaw_AbtXYZ_List_Degrees_Raw)
                        MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_RollPitchYaw.ExternalAddPointOrListOfPointsToPlot(["Roll", "Pitch", "Yaw"], [CurrentTime_MainLoopThread]*3, ZEDasHandController_MostRecentDict_RollPitchYaw_AbtXYZ_List_Degrees_Filtered)

                        #MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_RollPitchYaw.ExternalAddPointOrListOfPointsToPlot(["Roll", "Pitch"], [CurrentTime_MainLoopThread]*2, [ZEDasHandController_MostRecentDict_RollPitchYaw_AbtXYZ_List_Degrees_Raw[0], ZEDasHandController_MostRecentDict_RollPitchYaw_AbtXYZ_List_Degrees_Filtered[0]])
                        #MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_RollPitchYaw.ExternalAddPointOrListOfPointsToPlot(["Roll", "Pitch"], [CurrentTime_MainLoopThread]*2, [ZEDasHandController_MostRecentDict_RollPitchYaw_AbtXYZ_List_Degrees_Raw[1], ZEDasHandController_MostRecentDict_RollPitchYaw_AbtXYZ_List_Degrees_Filtered[1]])
                        #MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_RollPitchYaw.ExternalAddPointOrListOfPointsToPlot(["Roll", "Pitch"], [CurrentTime_MainLoopThread]*2, [ZEDasHandController_MostRecentDict_RollPitchYaw_AbtXYZ_List_Degrees_Raw[2], ZEDasHandController_MostRecentDict_RollPitchYaw_AbtXYZ_List_Degrees_Filtered[2]])
                        #####

                        #####
                        LastTime_MainLoopThread_PLOTTER_RollPitchYaw = CurrentTime_MainLoopThread
                        #####

            ####################################################

        ####################################################
        ####################################################

        time.sleep(1.0/60.0)
    #################################################
    #################################################

    ################################################# THIS IS THE EXIT ROUTINE!
    #################################################
    print("Exiting main program 'test_program_for_ZEDasHandController_ReubenPython2and3Class.")

    #################################################
    if SAVE_CSV_FILE_OF_TRAJECTORY_DATA_FLAG_AT_START_OF_PROGRAM == 1:
        CSVfileToWriteTo.close()
    #################################################

    #################################################
    if ZEDasHandController_OPEN_FLAG == 1:
        ZEDasHandController_ReubenPython2and3ClassObject.ExitProgram_Callback()
    #################################################

    #################################################
    if MYPRINT_OPEN_FLAG == 1:
        MyPrint_ReubenPython2and3ClassObject.ExitProgram_Callback()
    #################################################

    #################################################
    if PLOTTER_OPEN_FLAG_XYZ == 1:
        MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_XYZ.ExitProgram_Callback()
    #################################################

    #################################################
    if PLOTTER_OPEN_FLAG_RollPitchYaw == 1:
        MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_RollPitchYaw.ExitProgram_Callback()
    #################################################

    #################################################
    #################################################

##########################################################################################################
##########################################################################################################