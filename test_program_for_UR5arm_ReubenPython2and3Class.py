# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision C, 08/29/2022

Verified working on: Python 3.8 for Windows 10 64-bit and Raspberry Pi Buster (no Mac testing yet).
'''

__author__ = 'reuben.brewer'

#########################################################
from UR5arm_ReubenPython2and3Class import *
from MyPrint_ReubenPython2and3Class import *
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

##########################################################################################################
##########################################################################################################
def getPreciseSecondsTimeStampString():
    ts = time.time()

    return ts
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def TellWhichFileWereIn():

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
def IsInputList(input, print_result_flag = 0):

    result = isinstance(input, list)

    if print_result_flag == 1:
        print("IsInputList: " + str(result))

    return result
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
def ForceControlTestButtonResponse():
    global ForceControlCommandNeedsToBeSentFlag

    ForceControlCommandNeedsToBeSentFlag = 1

    print("ForceControlTestButtonResponse, event fired!")
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_update_clock():
    global root
    global EXIT_PROGRAM_FLAG
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_GUI_FLAG
    global Data_Label
    global UR5arm_MostRecentDict_Label

    global UR5arm_ReubenPython2and3ClassObject
    global UR5arm_OPEN_FLAG
    global SHOW_IN_GUI_UR5arm_FLAG
    global UR5arm_MostRecentDict

    global MyPrint_ReubenPython2and3ClassObject
    global MYPRINT_OPEN_FLAG
    global SHOW_IN_GUI_MYPRINT_FLAG

    if USE_GUI_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
        #########################################################
        #########################################################

            #########################################################
            Data_Label_TextToDisplay = ConvertDictToProperlyFormattedStringForPrinting(UR5arm_MostRecentDict, NumberOfDecimalsPlaceToUse=5, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 1)
            Data_Label["text"] = Data_Label_TextToDisplay
            #########################################################

            #########################################################
            UR5arm_MostRecentDict_Label["text"] = ConvertDictToProperlyFormattedStringForPrinting(UR5arm_MostRecentDict, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 3, NumberOfTabsBetweenItems = 1)
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
def GUI_Thread():
    global root
    global root_Xpos
    global root_Ypos
    global root_width
    global root_height
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_TABS_IN_GUI_FLAG

    ################################################# KEY GUI LINE
    #################################################
    root = Tk()
    #################################################
    #################################################

    #################################################
    #################################################
    global TabControlObject
    global Tab_UR5arm
    global Tab_MainControls
    global Tab_MyPrint

    if USE_TABS_IN_GUI_FLAG == 1:
        #################################################
        TabControlObject = ttk.Notebook(root)

        Tab_UR5arm = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_UR5arm, text='  UR5arm  ')

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
        Tab_UR5arm = root
        Tab_MainControls = root
        Tab_MyPrint = root
        #################################################

    #################################################
    #################################################

    #################################################
    global ForceControlTestButton
    ForceControlTestButton = Button(Tab_MainControls, text='ForceControlTest', state="normal", width=20, command=lambda i=1: ForceControlTestButtonResponse())
    ForceControlTestButton.grid(row=0, column=0, padx=5, pady=1)
    #################################################

    #################################################
    global Data_Label
    Data_Label = Label(Tab_MainControls, text="Data_Label", width=150)
    Data_Label.grid(row=1, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
    #################################################

    #################################################
    global UR5arm_MostRecentDict_Label
    UR5arm_MostRecentDict_Label = Label(Tab_UR5arm, text="UR5arm_MostRecentDict_Label", width=120, font=("Helvetica", 10))
    UR5arm_MostRecentDict_Label.grid(row=0, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
    #################################################

    ################################################# THIS BLOCK MUST COME 2ND-TO-LAST IN def GUI_Thread() IF USING TABS.
    root.protocol("WM_DELETE_WINDOW", ExitProgram_Callback)  # Set the callback function for when the window's closed.
    root.title("test_program_for_UR5arm_ReubenPython2and3Class")
    root.geometry('%dx%d+%d+%d' % (root_width, root_height, root_Xpos, root_Ypos)) # set the dimensions of the screen and where it is placed
    root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
    root.mainloop()
    #################################################

    #################################################  THIS BLOCK MUST COME LAST IN def GUI_Thread() REGARDLESS OF CODE.
    root.quit() #Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
    root.destroy() #Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
    #################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
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
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    global USE_GUI_FLAG
    USE_GUI_FLAG = 1

    global USE_TABS_IN_GUI_FLAG
    USE_TABS_IN_GUI_FLAG = 1

    global USE_UR5arm_FLAG
    USE_UR5arm_FLAG = 1

    global USE_MYPRINT_FLAG
    USE_MYPRINT_FLAG = 1

    global USE_SINUSOIDAL_INPUT_FLAG
    USE_SINUSOIDAL_INPUT_FLAG = 0
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    global SHOW_IN_GUI_UR5arm_FLAG
    SHOW_IN_GUI_UR5arm_FLAG = 1

    global SHOW_IN_GUI_MYPRINT_FLAG
    SHOW_IN_GUI_MYPRINT_FLAG = 1
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    global GUI_ROW_MYPRINT
    global GUI_COLUMN_MYPRINT
    global GUI_PADX_MYPRINT
    global GUI_PADY_MYPRINT
    global GUI_ROWSPAN_MYPRINT
    global GUI_COLUMNSPAN_MYPRINT
    GUI_ROW_MYPRINT = 2

    GUI_COLUMN_MYPRINT = 0
    GUI_PADX_MYPRINT = 1
    GUI_PADY_MYPRINT = 10
    GUI_ROWSPAN_MYPRINT = 1
    GUI_COLUMNSPAN_MYPRINT = 1
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0

    global CurrentTime_MainLoopThread
    CurrentTime_MainLoopThread = -11111.0

    global StartingTime_MainLoopThread
    StartingTime_MainLoopThread = -11111.0

    global TimeToSleep_MainLoop_Thread
    TimeToSleep_MainLoop_Thread = 0.010

    global root

    global root_Xpos
    root_Xpos = 900

    global root_Ypos
    root_Ypos = 0

    global root_width
    root_width = 1920 - root_Xpos

    global root_height
    root_height = 1020 - root_Ypos

    global Tab_UR5arm
    global TabControlObject
    global Tab_MainControls
    global Tab_MyPrint

    global GUI_RootAfterCallbackInterval_Milliseconds
    GUI_RootAfterCallbackInterval_Milliseconds = 30

    global SINUSOIDAL_MOTION_INPUT_ROMtestTimeToPeakAngle
    SINUSOIDAL_MOTION_INPUT_ROMtestTimeToPeakAngle = 2.0

    global SINUSOIDAL_MOTION_INPUT_MinValue_PositionControl
    SINUSOIDAL_MOTION_INPUT_MinValue_PositionControl = -0.1

    global SINUSOIDAL_MOTION_INPUT_MaxValue_PositionControl
    SINUSOIDAL_MOTION_INPUT_MaxValue_PositionControl = 0.1

    global ForceControlCommandNeedsToBeSentFlag
    ForceControlCommandNeedsToBeSentFlag = 0
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    global UR5arm_ReubenPython2and3ClassObject

    global UR5arm_OPEN_FLAG
    UR5arm_OPEN_FLAG = -1

    global UR5arm_MostRecentDict
    UR5arm_MostRecentDict = dict()

    global UR5arm_MostRecentDict_JointAngleList_Deg
    UR5arm_MostRecentDict_JointAngleList_Deg = [-11111.0]*6

    global UR5arm_MostRecentDict_JointAngleList_Rad
    UR5arm_MostRecentDict_JointAngleList_Rad = [-11111.0]*6

    global UR5arm_MostRecentDict_ToolVectorActual
    UR5arm_MostRecentDict_ToolVectorActual = [-11111.0]*6

    global UR5arm_MostRecentDict_ToolTipSpeedsCartestian_TCPspeedActual
    UR5arm_MostRecentDict_ToolTipSpeedsCartestian_TCPspeedActual = [-11111.0]*6

    global UR5arm_MostRecentDict_ToolTipSpeedsCartestian_LinearXYZnorm_MetersPerSec
    UR5arm_MostRecentDict_ToolTipSpeedsCartestian_LinearXYZnorm_MetersPerSec = -11111.0

    global UR5arm_MostRecentDict_DataStreamingFrequency_CalculatedFromDedicatedRxThread
    UR5arm_MostRecentDict_DataStreamingFrequency_CalculatedFromDedicatedRxThread = -11111.0

    global UR5arm_MostRecentDict_Time
    UR5arm_MostRecentDict_Time = -11111.0

    global UR5arm_WatchdogTimerDurationSeconds_ExpirationWillEndStandAloneProcess
    UR5arm_WatchdogTimerDurationSeconds_ExpirationWillEndStandAloneProcess = 2.0

    global UR5arm_MultiprocessingQueue_Rx_MaxSize
    UR5arm_MultiprocessingQueue_Rx_MaxSize = 3

    global UR5arm_MultiprocessingQueue_Tx_MaxSize
    UR5arm_MultiprocessingQueue_Tx_MaxSize = 3

    global UR5arm_TimeDurationToWaitBetweenCreatingClassObjectAndReadingData_Seconds
    UR5arm_TimeDurationToWaitBetweenCreatingClassObjectAndReadingData_Seconds = 5.0
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    global MyPrint_ReubenPython2and3ClassObject

    global MYPRINT_OPEN_FLAG
    MYPRINT_OPEN_FLAG = -1
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## KEY GUI LINE
    ##########################################################################################################
    ##########################################################################################################
    if USE_GUI_FLAG == 1:
        print("Starting GUI thread...")
        GUI_Thread_ThreadingObject = threading.Thread(target=GUI_Thread)
        GUI_Thread_ThreadingObject.setDaemon(True) #Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
        GUI_Thread_ThreadingObject.start()
        time.sleep(0.5)  #Allow enough time for 'root' to be created that we can then pass it into other classes.
    else:
        root = None
        Tab_UR5arm = None
        Tab_MainControls = None
        Tab_MyPrint = None
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    global UR5arm_ReubenPython2and3ClassObject_GUIparametersDict
    UR5arm_ReubenPython2and3ClassObject_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_UR5arm_FLAG),
                                    ("EnableInternal_MyPrint_Flag", 1),
                                    ("GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents", 30),
                                    ("NumberOfPrintLines", 10),
                                    ("RootWindowWidth", 1000),
                                    ("RootWindowHeight", 1000),
                                    ("RootWindowStartingX", 100),
                                    ("RootWindowStartingY", 100),
                                    ("RootWindowTitle", "UR5arm")])

    global HomeStraightUpPose_Deg
    HomeStraightUpPose_Deg = [0.0, -90.0, 0.0, -90.0, 0.0, 0.0]

    #    #''' CB3_S
    global UR5arm_PositionControl_MoveJ_MoveThroughListOfPoses_SafeReturnToStartingPoseFromAnywhere
    UR5arm_PositionControl_MoveJ_MoveThroughListOfPoses_SafeReturnToStartingPoseFromAnywhere = list([dict([("JointAngleList_Deg", [-12.463, -78.767, 79.495, -89.215, -89.185, -24.887]), ("TimeDurationSec", 5.0)]),
                                                                                                dict([("JointAngleList_Deg", [-12.463, -78.767, 79.495, -89.215, -89.185, -24.887]), ("TimeDurationSec", 5.0)])])
    #'''

    ''' CB3_K
    global UR5arm_PositionControl_MoveJ_MoveThroughListOfPoses_SafeReturnToStartingPoseFromAnywhere
    UR5arm_PositionControl_MoveJ_MoveThroughListOfPoses_SafeReturnToStartingPoseFromAnywhere = list([dict([("JointAngleList_Deg", [88.310, -115.040, 88.510, 21.571, 82.274, 41.313]), ("TimeDurationSec", 5.0)]),
                                                                                                dict([("JointAngleList_Deg", [88.310, -115.040, 88.510, 21.571, 82.274, 41.313]), ("TimeDurationSec", 5.0)])])
    '''

    '''
    global UR5arm_PositionControl_MoveJ_MoveThroughListOfPoses_SafeReturnToStartingPoseFromAnywhere
    UR5arm_PositionControl_MoveJ_MoveThroughListOfPoses_SafeReturnToStartingPoseFromAnywhere = list([dict([("JointAngleList_Deg", [0.0, -90.0, 0.0, -90.0, 0.0, 0.0]), ("TimeDurationSec", 5.0)]),
                                                                                                dict([("JointAngleList_Deg", [0.0, -90.0, 0.0, -90.0, 0.0, 0.0]), ("TimeDurationSec", 5.0)])])
    '''

    global JointAngleCommandIncrementDecrement_CustomEntryLabels_ListOfDicts
    JointAngleCommandIncrementDecrement_CustomEntryLabels_ListOfDicts = [dict([("IncrementLabel", "Base, +"),("DecrementLabel", " Base, -")]),
                                                                        dict([("IncrementLabel", "Shoulder, +"),("DecrementLabel", "Shoulder, -")]),
                                                                        dict([("IncrementLabel", "Elbow, +"),("DecrementLabel", "Elbow, -")]),
                                                                        dict([("IncrementLabel", "Wrist Pitch, +"),("DecrementLabel", "Wrist Pitch, -")]),
                                                                        dict([("IncrementLabel", "Wrist Roll, +"),("DecrementLabel", "Wrist Roll, -")]),
                                                                        dict([("IncrementLabel", "Gripper Roll, +"),("DecrementLabel", "Gripper Roll, -")])]

    global UR5arm_ReubenPython2and3ClassObject_setup_dict
    UR5arm_ReubenPython2and3ClassObject_setup_dict = dict([("GUIparametersDict", UR5arm_ReubenPython2and3ClassObject_GUIparametersDict),
                                                        ("NameToDisplay_UserSet", "Reuben's UR5arm test"),
                                                        ("RealTimeClientInterfaceVersionNumberString","5.10"), #'<3.0' for test UR5CB2, '3.8' for test URCB3_K, '5.10' for CB3_S
                                                        ("ControllerBoxVersion", 3), #2, #3
                                                        ("IPV4_address", "192.168.0.110",), #"192.168.1.100" for CB2_S, "192.168.1.12" for CB3_K, #"192.168.0.110" for CB3_S
                                                        ("IPV4_NumberOfRxMessagesToBuffers", 50),
                                                        ("IPV4_TimeoutDurationSeconds", 5.0),
                                                        ("DedicatedRxThread_TimeToSleepEachLoop", 0.001),
                                                        ("DedicatedTxThread_MaximumTxMessagesPerSecondFrequency", 100.0),
                                                        ("DedicatedTxThread_TxMessageToSend_Queue_MaxSize", 1),
                                                        ("StandAloneProcess_TimeToSleepEachLoop", 0.007),
                                                        ("PositionControl_ServoJ_MoveThroughListOfPoses_SafeReturnToStartingPoseFromAnywhere", UR5arm_PositionControl_MoveJ_MoveThroughListOfPoses_SafeReturnToStartingPoseFromAnywhere),
                                                        ("StartingPoseJointAngleList_Deg", [0.0, -90.0, 0.0, -90.0, 0.0, 0.0]),
                                                        ("Payload_MassKG_ToBeCommanded", 1.660),
                                                        ("Payload_CoGmetersList_ToBeCommanded", [0.000, 0.020, 0.200]),
                                                        ("Acceleration", 1.05),
                                                        ("Velocity", 1.25),
                                                        ("JointAngleCommandIncrementDecrement_ValueInDegrees", 1.0),
                                                        ("JointAngleCommandIncrementDecrement_CustomEntryLabels_ListOfDicts", JointAngleCommandIncrementDecrement_CustomEntryLabels_ListOfDicts),
                                                        ("ParentPID", os.getpid()),
                                                        ("UR5arm_WatchdogTimerDurationSeconds_ExpirationWillEndStandAloneProcess", UR5arm_WatchdogTimerDurationSeconds_ExpirationWillEndStandAloneProcess),
                                                        ("MultiprocessingQueue_Rx_MaxSize", UR5arm_MultiprocessingQueue_Rx_MaxSize),
                                                        ("MultiprocessingQueue_Tx_MaxSize", UR5arm_MultiprocessingQueue_Tx_MaxSize),
                                                        ("EnableTx_State_AtStartupFlag", 1)])

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
            ExitProgram_Callback()
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if USE_MYPRINT_FLAG == 1:

        MyPrint_ReubenPython2and3ClassObject_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_MYPRINT_FLAG),
                                                                        ("root", Tab_MyPrint), #root
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
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if USE_UR5arm_FLAG == 1 and UR5arm_OPEN_FLAG != 1:
        print("Failed to open UR5arm_ReubenPython2and3Class.")
        ExitProgram_Callback()
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if USE_MYPRINT_FLAG == 1 and MYPRINT_OPEN_FLAG != 1:
        print("Failed to open MyPrint_ReubenPython2and3ClassObject.")
        ExitProgram_Callback()
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    print("Starting main loop 'test_program_for_UR5arm_ReubenPython2and3Class.")
    StartingTime_MainLoopThread = getPreciseSecondsTimeStampString()

    UR5arm_ReubenPython2and3ClassObject.FunctionCallToStandAloneProcess("MoveSafelyToStartingPoseViaMultipointSequence", [], MultiprocessingQueue_Rx_MaxSize_Local = UR5arm_MultiprocessingQueue_Rx_MaxSize, IgnoreNewDataIfQueueIsFullFlag = 1)
    time.sleep(5.0)
    if UR5arm_WatchdogTimerDurationSeconds_ExpirationWillEndStandAloneProcess > 0.0:
        UR5arm_ReubenPython2and3ClassObject.FunctionCallToStandAloneProcess("SetWatchdogTimerEnableState", [1])

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    while(EXIT_PROGRAM_FLAG == 0):
        try:
            ##########################################################################################################
            ##########################################################################################################
            CurrentTime_MainLoopThread = getPreciseSecondsTimeStampString() - StartingTime_MainLoopThread
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            if USE_UR5arm_FLAG == 1:

                ########################################################################################################## GET's
                if UR5arm_OPEN_FLAG == 1:

                    UR5arm_MostRecentDict_temp = UR5arm_ReubenPython2and3ClassObject.GetMostRecentDataDict()

                    if len(UR5arm_MostRecentDict_temp) > 0 and "Time" in UR5arm_MostRecentDict_temp:
                        UR5arm_MostRecentDict = UR5arm_MostRecentDict_temp

                        #print("UR5arm_MostRecentDict: " + str(UR5arm_MostRecentDict) + ", type(UR5arm_MostRecentDict): " + str(type(UR5arm_MostRecentDict)))
                        #print("UR5arm_MostRecentDict: " + str(UR5arm_MostRecentDict))

                        UR5arm_MostRecentDict_JointAngleList_Deg = UR5arm_MostRecentDict["JointAngleList_Deg"]
                        UR5arm_MostRecentDict_JointAngleList_Rad = UR5arm_MostRecentDict["JointAngleList_Rad"]
                        UR5arm_MostRecentDict_ToolVectorActual = UR5arm_MostRecentDict["ToolVectorActual"]
                        UR5arm_MostRecentDict_ToolTipSpeedsCartestian_TCPspeedActual = UR5arm_MostRecentDict["ToolTipSpeedsCartestian_TCPspeedActual"]
                        UR5arm_MostRecentDict_ToolTipSpeedsCartestian_LinearXYZnorm_MetersPerSec = UR5arm_MostRecentDict["ToolTipSpeedsCartestian_LinearXYZnorm_MetersPerSec"]
                        UR5arm_MostRecentDict_DataStreamingFrequency_CalculatedFromDedicatedRxThread = UR5arm_MostRecentDict["DataStreamingFrequency_CalculatedFromDedicatedRxThread"]
                        UR5arm_MostRecentDict_Time = UR5arm_MostRecentDict["Time"]

                        #print("UR5arm_MostRecentDict_Time: " + str(UR5arm_MostRecentDict_Time))
                ##########################################################################################################

                ########################################################################################################## SET's
                if UR5arm_OPEN_FLAG == 1:

                    if USE_SINUSOIDAL_INPUT_FLAG == 1:
                        time_gain = math.pi / (2.0 * SINUSOIDAL_MOTION_INPUT_ROMtestTimeToPeakAngle)
                        SIN_POSITION_INPUT_TO_COMMAND = (SINUSOIDAL_MOTION_INPUT_MaxValue_PositionControl + SINUSOIDAL_MOTION_INPUT_MinValue_PositionControl)/2.0 + 0.5*abs(SINUSOIDAL_MOTION_INPUT_MaxValue_PositionControl - SINUSOIDAL_MOTION_INPUT_MinValue_PositionControl)*math.sin(1.0*time_gain*CurrentTime_MainLoopThread)
                        COS_POSITION_INPUT_TO_COMMAND = (SINUSOIDAL_MOTION_INPUT_MaxValue_PositionControl + SINUSOIDAL_MOTION_INPUT_MinValue_PositionControl)/2.0 + 0.5*abs(SINUSOIDAL_MOTION_INPUT_MaxValue_PositionControl - SINUSOIDAL_MOTION_INPUT_MinValue_PositionControl)*math.cos(1.0*time_gain*CurrentTime_MainLoopThread)

                        #ToolTip6DOFpose_ToBeSet = [+0.445, +0.191, +0.526+SINUSOIDAL_POSITION_INPUT_TO_COMMAND, -1.569, +0.033, +0.068]
                        ToolTip6DOFpose_ToBeSet = [+0.181 + SIN_POSITION_INPUT_TO_COMMAND, -0.191, +0.742 + COS_POSITION_INPUT_TO_COMMAND, +0.015, -2.229, +2.212]

                        UR5arm_ReubenPython2and3ClassObject.FunctionCallToStandAloneProcess("PositionControl_ServoJ_MoveThroughListOfPoses",
                                                                                            [[dict([("PoseIsInToolSpaceFlag", 1), ("ToolTip6DOFpose", ToolTip6DOFpose_ToBeSet), ("TimeDurationSec", 0.03), ("lookahead_time", 0.2),("gain", 100)])]],
                                                                                            MultiprocessingQueue_Rx_MaxSize_Local = UR5arm_MultiprocessingQueue_Rx_MaxSize,
                                                                                            IgnoreNewDataIfQueueIsFullFlag = 1)
                    else:
                        UR5arm_ReubenPython2and3ClassObject.FunctionCallToStandAloneProcess("KickWatchdogButDoNothing",
                                                                                            [0],
                                                                                            MultiprocessingQueue_Rx_MaxSize_Local=UR5arm_MultiprocessingQueue_Rx_MaxSize,
                                                                                            IgnoreNewDataIfQueueIsFullFlag=1)

                        if ForceControlCommandNeedsToBeSentFlag == 1:
                            #def ForceControl(self, Force_XYZlist, Speed_MagnitudeMetersPerSec, StoppingDecellerationMetersPerSecSquared, DurationForWhichToApplyForceInSeconds = -11111.0, ZeroForceReadingsBeforeMoveFlag = 0):
                            Force_XYZlist = [-1.0, 0.0, 0.0]
                            Speed_MagnitudeMetersPerSec = 0.1
                            StoppingDecellerationMetersPerSecSquared = 0.5
                            DurationForWhichToApplyForceInSeconds = 1.0
                            ZeroForceReadingsBeforeMoveFlag = 1
                            print("goat")
                            UR5arm_ReubenPython2and3ClassObject.FunctionCallToStandAloneProcess("ForceControl",
                                                                                            [Force_XYZlist, Speed_MagnitudeMetersPerSec, StoppingDecellerationMetersPerSecSquared, DurationForWhichToApplyForceInSeconds, ZeroForceReadingsBeforeMoveFlag],
                                                                                            MultiprocessingQueue_Rx_MaxSize_Local=UR5arm_MultiprocessingQueue_Rx_MaxSize,
                                                                                            IgnoreNewDataIfQueueIsFullFlag=1)
                            ForceControlCommandNeedsToBeSentFlag = 0
                ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            time.sleep(TimeToSleep_MainLoop_Thread) #IF YOU MAKE THIS TIME.SLEEP TOO SHORT (LIKE 0.001), THEN THE ARM WON'T HAVE TIME TO MOVE.
            ##########################################################################################################
            ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("test_program_for_UR5arm_ReubenPython2and3Class, Exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## THIS IS THE EXIT ROUTINE!
    ##########################################################################################################
    ##########################################################################################################
    print("Exiting main program 'test_program_for_UR5arm_ReubenPython2and3Class.")

    ##########################################################################################################
    ##########################################################################################################
    if UR5arm_OPEN_FLAG == 1:
        UR5arm_ReubenPython2and3ClassObject.FunctionCallToStandAloneProcess("ExitProgram_Callback",
                                                                            [],
                                                                            MultiprocessingQueue_Rx_MaxSize_Local=UR5arm_MultiprocessingQueue_Rx_MaxSize,
                                                                            IgnoreNewDataIfQueueIsFullFlag=1)
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    if MYPRINT_OPEN_FLAG == 1:
        MyPrint_ReubenPython2and3ClassObject.ExitProgram_Callback()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################