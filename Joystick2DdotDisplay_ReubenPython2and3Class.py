# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision H, 09/22/2023

Verified working on: Python 2.7, 3.8 for Windows 8.1, 10 64-bit, Ubuntu 20.04, and Raspberry Pi Buster (no Mac testing yet).
'''

__author__ = 'reuben.brewer'

#################################################
import os
import sys
import platform
import time, datetime
import math
import collections
import inspect #To enable 'TellWhichFileWereIn'
import threading
import traceback
#################################################

#################################################
if sys.version_info[0] < 3:
    from Tkinter import * #Python 2
    import tkFont
    import ttk
else:
    from tkinter import * #Python 3
    import tkinter.font as tkFont #Python 3
    from tkinter import ttk
#################################################

#################################################
if sys.version_info[0] < 3:
    import Queue  # Python 2
else:
    import queue as Queue  # Python 3
#################################################

#################################################
if sys.version_info[0] < 3:
    from builtins import raw_input as input
else:
    from future.builtins import input as input
################################################# #"sudo pip3 install future" (Python 3) AND "sudo pip install future" (Python 2)

#################################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
#################################################

class Joystick2DdotDisplay_ReubenPython2and3Class(Frame): #Subclass the Tkinter Frame

    #######################################################################################################################
    #######################################################################################################################
    def __init__(self, setup_dict): #Subclass the Tkinter Frame

        print("#################### Joystick2DdotDisplay_ReubenPython2and3Class __init__ starting. ####################")

        #########################################################
        #########################################################
        self.GUI_ready_to_be_updated_flag = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = -1

        self.Input_Xvalue = 0
        self.Input_Yvalue = 0
        self.DotHighlightedLikeButtonPress_State = 0
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

        print("Joystick2DdotDisplay_ReubenPython2and3Class __init__: The OS platform is: " + self.my_platform)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "GUIparametersDict" in setup_dict:
            self.GUIparametersDict = setup_dict["GUIparametersDict"]

            ##########################################
            if "root" in self.GUIparametersDict:
                self.root = self.GUIparametersDict["root"]
            else:
                print("Joystick2DdotDisplay_ReubenPython2and3Class __init__: ERROR, must pass in 'root'")
                return
            ##########################################

            ##########################################
            if "GUI_ROW" in self.GUIparametersDict:
                self.GUI_ROW = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROW", self.GUIparametersDict["GUI_ROW"], 0.0, 1000.0))
            else:
                self.GUI_ROW = 0

            print("Joystick2DdotDisplay_ReubenPython2and3Class __init__: GUI_ROW: " + str(self.GUI_ROW))
            ##########################################

            ##########################################
            if "GUI_COLUMN" in self.GUIparametersDict:
                self.GUI_COLUMN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMN", self.GUIparametersDict["GUI_COLUMN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMN = 0

            print("Joystick2DdotDisplay_ReubenPython2and3Class __init__: GUI_COLUMN: " + str(self.GUI_COLUMN))
            ##########################################

            ##########################################
            if "GUI_PADX" in self.GUIparametersDict:
                self.GUI_PADX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADX", self.GUIparametersDict["GUI_PADX"], 0.0, 1000.0))
            else:
                self.GUI_PADX = 0

            print("Joystick2DdotDisplay_ReubenPython2and3Class __init__: GUI_PADX: " + str(self.GUI_PADX))
            ##########################################

            ##########################################
            if "GUI_PADY" in self.GUIparametersDict:
                self.GUI_PADY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADY", self.GUIparametersDict["GUI_PADY"], 0.0, 1000.0))
            else:
                self.GUI_PADY = 0

            print("Joystick2DdotDisplay_ReubenPython2and3Class __init__: GUI_PADY: " + str(self.GUI_PADY))
            ##########################################

            ##########################################
            if "GUI_ROWSPAN" in self.GUIparametersDict:
                self.GUI_ROWSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROWSPAN", self.GUIparametersDict["GUI_ROWSPAN"], 0.0, 1000.0))
            else:
                self.GUI_ROWSPAN = 1

            print("Joystick2DdotDisplay_ReubenPython2and3Class __init__: GUI_ROWSPAN: " + str(self.GUI_ROWSPAN))
            ##########################################

            ##########################################
            if "GUI_COLUMNSPAN" in self.GUIparametersDict:
                self.GUI_COLUMNSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMNSPAN", self.GUIparametersDict["GUI_COLUMNSPAN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMNSPAN = 1

            print("Joystick2DdotDisplay_ReubenPython2and3Class __init__: GUI_COLUMNSPAN: " + str(self.GUI_COLUMNSPAN))
            ##########################################

            ##########################################
            if "GUI_STICKY" in self.GUIparametersDict:
                self.GUI_STICKY = str(self.GUIparametersDict["GUI_STICKY"])
            else:
                self.GUI_STICKY = "w"

            print("Joystick2DdotDisplay_ReubenPython2and3Class __init__: GUI_STICKY: " + str(self.GUI_STICKY))
            ##########################################

        else:
            self.GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("Joystick2DdotDisplay_ReubenPython2and3Class __init__: No GUIparametersDict present, setting USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))

        #print("GUIparametersDict = " + str(self.GUIparametersDict))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "JoystickXYboxCanvas_HeightAndWidth" in setup_dict:
            self.JoystickXYboxCanvas_HeightAndWidth = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("JoystickXYboxCanvas_HeightAndWidth", setup_dict["JoystickXYboxCanvas_HeightAndWidth"], 100.0, 1000.0))
        else:
            self.JoystickXYboxCanvas_HeightAndWidth = 150

        print("JoystickHID_ReubenPython2and3Class __init__: JoystickXYboxCanvas_HeightAndWidth: " + str(self.JoystickXYboxCanvas_HeightAndWidth))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DisplayZeroCrosshairsFlag" in setup_dict:
            self.DisplayZeroCrosshairsFlag = self.PassThrough0and1values_ExitProgramOtherwise("DisplayZeroCrosshairsFlag", setup_dict["DisplayZeroCrosshairsFlag"])
        else:
            self.DisplayZeroCrosshairsFlag = 0

        print("Joystick2DdotDisplay_ReubenPython2and3Class __init__: DisplayZeroCrosshairsFlag: " + str(self.DisplayZeroCrosshairsFlag))
        #########################################################
        #########################################################
    
        #########################################################
        #########################################################
        self.myFrame = Frame(self.root)

        self.myFrame.grid(row = self.GUI_ROW,
                          column = self.GUI_COLUMN,
                          padx = self.GUI_PADX,
                          pady = self.GUI_PADY,
                          rowspan = self.GUI_ROWSPAN,
                          columnspan= self.GUI_COLUMNSPAN,
                          sticky = self.GUI_STICKY)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.JoystickXYboxCanvas_BorderWidth = 1

        ### Create and draw canvas
        self.JoystickXYboxCanvas = Canvas(self.myFrame,
                                         width=self.JoystickXYboxCanvas_HeightAndWidth,
                                         height=self.JoystickXYboxCanvas_HeightAndWidth) #bg="white", highlightbackground="black"

        self.JoystickXYboxCanvas["highlightthickness"] = 0  #IMPORTANT Remove light grey border around the Canvas
        self.JoystickXYboxCanvas["bd"] = 0 #IMPORTANT Setting "bd", along with "highlightthickness" to 0 makes the Canvas be in the (0,0) pixel location instead of offset by those thicknesses
        self.JoystickXYboxCanvas.grid(row=0, column=1, padx=0, pady=0, columnspan=1, rowspan=50)
        ###

        ### Create black outline around canvas
        self.JoystickXYboxCanvas.create_rectangle(0.5*self.JoystickXYboxCanvas_BorderWidth,
                                                 0.5 * self.JoystickXYboxCanvas_BorderWidth,
                                                 self.JoystickXYboxCanvas_HeightAndWidth - 0.5 * self.JoystickXYboxCanvas_BorderWidth -1, #The -1 accounts for indexing at 0
                                                 self.JoystickXYboxCanvas_HeightAndWidth - 0.5 * self.JoystickXYboxCanvas_BorderWidth -1, #The -1 accounts for indexing at 0
                                                 outline="black",
                                                 fill="white",
                                                 width=self.JoystickXYboxCanvas_BorderWidth)
        ###

        ### Create cicle
        self.JoystickXYboxCanvas_PointerCircle_Radius = 5
        self.JoystickXYboxCanvas_PointerCircle = self.CreateAndDrawCircleOnCanvas_CanvasCoord(self.JoystickXYboxCanvas, 0, 0, self.JoystickXYboxCanvas_PointerCircle_Radius, "red")
        ###

        #########################################################
        #########################################################

        #########################################################
        #########################################################
        time.sleep(0.1)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.GUI_ready_to_be_updated_flag = 1
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
    def UpdateDotCoordinatesAndDotColor(self, X, Y, DotHighlightedLikeButtonPress_State = 0):
        self.Input_Xvalue = self.LimitNumber_FloatOutputOnly(-1.0, 1.0, X)
        self.Input_Yvalue = self.LimitNumber_FloatOutputOnly(-1.0, 1.0, Y)

        if DotHighlightedLikeButtonPress_State in [0, 1]:
            self.DotHighlightedLikeButtonPress_State = DotHighlightedLikeButtonPress_State
        else:
            self.DotHighlightedLikeButtonPress_State = 0

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CreateAndDrawCircleOnCanvas_CanvasCoord(self, myCanvas, CenterX_CanvasCoord, CenterY_CanvasCoord, Radius, Color = "black"):

        CircleBoundingBoxCoordinates_CanvasCoord = self.GetCircleBoundingBoxCoordinatesListOnCanvas_CanvasCoord(CenterX_CanvasCoord, CenterY_CanvasCoord, Radius)

        CircleObjectToReturn = myCanvas.create_oval(CircleBoundingBoxCoordinates_CanvasCoord[0],
                                                    CircleBoundingBoxCoordinates_CanvasCoord[1],
                                                    CircleBoundingBoxCoordinates_CanvasCoord[2],
                                                    CircleBoundingBoxCoordinates_CanvasCoord[3],
                                                    outline=Color,
                                                    fill=Color,
                                                    width=0)
        return CircleObjectToReturn
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetCircleBoundingBoxCoordinatesListOnCanvas_CanvasCoord(self, CenterX_CanvasCoord, CenterY_CanvasCoord, Radius):

        coordinates_list = [CenterX_CanvasCoord - Radius,
                            CenterY_CanvasCoord - Radius,
                            CenterX_CanvasCoord + Radius,
                            CenterY_CanvasCoord + Radius]

        return coordinates_list
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ConvertMathPointToJoystickCanvasCoordinates(self, PointListXY):

        ####
        x = PointListXY[0]
        y = PointListXY[1]

        W = self.JoystickXYboxCanvas_HeightAndWidth
        H = self.JoystickXYboxCanvas_HeightAndWidth

        X_min = -1.0
        X_max = 1.0

        Y_min = -1.0
        Y_max = 1.0

        GraphBoxOutline_X0 = 0
        GraphBoxOutline_Y0 = 0
        ####

        ####
        m_Xaxis = ((W - GraphBoxOutline_X0)/(X_max - X_min))
        b_Xaxis = W - m_Xaxis*X_max

        X_out = m_Xaxis*x + b_Xaxis
        ####

        ####
        m_Yaxis = ((H - GraphBoxOutline_Y0) / (Y_max - Y_min))
        b_Yaxis = H - m_Yaxis * Y_max

        Y_out = m_Yaxis * y + b_Yaxis
        ####

        ####
        X_out = X_out
        Y_out = self.JoystickXYboxCanvas.winfo_height() - Y_out #Flip y-axis
        ####

        return [X_out, Y_out]
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_update_clock(self):

            #######################################################
            #######################################################
            #######################################################
            if self.GUI_ready_to_be_updated_flag == 1:

                #######################################################
                #######################################################
                try:

                    ### Debug drawing functions
                    #self.CreateAndDrawCircleOnCanvas_CanvasCoord(self.JoystickXYboxCanvas, 0, 0, self.JoystickXYboxCanvas_PointerCircle_Radius, "green")
                    #PointCoords_CanvasCoord = self.ConvertMathPointToJoystickCanvasCoordinates([0, 0])
                    #PointCoords_CanvasCoord = self.ConvertMathPointToJoystickCanvasCoordinates([0, 1])
                    #PointCoords_CanvasCoord = self.ConvertMathPointToJoystickCanvasCoordinates([1, 1])
                    ### Debug drawing functions

                    #######################################################
                    PointCoords_CanvasCoord = self.ConvertMathPointToJoystickCanvasCoordinates([self.Input_Xvalue, self.Input_Yvalue])

                    CircleBoundingBoxCoordinates_CanvasCoord = self.GetCircleBoundingBoxCoordinatesListOnCanvas_CanvasCoord(PointCoords_CanvasCoord[0],
                                                                                                               PointCoords_CanvasCoord[1],
                                                                                                               self.JoystickXYboxCanvas_PointerCircle_Radius)

                    self.JoystickXYboxCanvas.coords(self.JoystickXYboxCanvas_PointerCircle,
                                                       CircleBoundingBoxCoordinates_CanvasCoord[0],
                                                       CircleBoundingBoxCoordinates_CanvasCoord[1],
                                                       CircleBoundingBoxCoordinates_CanvasCoord[2],
                                                       CircleBoundingBoxCoordinates_CanvasCoord[3])
                    #######################################################
                    
                    #######################################################
                    if self.DotHighlightedLikeButtonPress_State == 1:
                        self.JoystickXYboxCanvas.itemconfig(self.JoystickXYboxCanvas_PointerCircle, fill='green', outline="green")
                    else:
                        self.JoystickXYboxCanvas.itemconfig(self.JoystickXYboxCanvas_PointerCircle, fill='red', outline="red")
                    #######################################################
                    
                    #######################################################
                    if self.DisplayZeroCrosshairsFlag == 1:
                        
                        HorizontalLineCoords_BottomOfLine_CanvasCoord = self.ConvertMathPointToJoystickCanvasCoordinates([-1.0, 0.0])
                        HorizontalLineCoords_TopOfLine_CanvasCoord = self.ConvertMathPointToJoystickCanvasCoordinates([1.0, 0.0])
                        
                        VerticalLineCoords_BottomOfLine_CanvasCoord = self.ConvertMathPointToJoystickCanvasCoordinates([0.0, -1.0])
                        VerticalLineCoords_TopOfLine_CanvasCoord = self.ConvertMathPointToJoystickCanvasCoordinates([0.0, 1.0])
                        
                        self.JoystickXYboxCanvas.create_line(HorizontalLineCoords_BottomOfLine_CanvasCoord[0],
                                                             HorizontalLineCoords_BottomOfLine_CanvasCoord[1],
                                                             HorizontalLineCoords_TopOfLine_CanvasCoord[0],
                                                             HorizontalLineCoords_TopOfLine_CanvasCoord[1],
                                                             fill="black", width=1) #dash=(10)
                        
                        self.JoystickXYboxCanvas.create_line(VerticalLineCoords_BottomOfLine_CanvasCoord[0],
                                                             VerticalLineCoords_BottomOfLine_CanvasCoord[1],
                                                             VerticalLineCoords_TopOfLine_CanvasCoord[0],
                                                             VerticalLineCoords_TopOfLine_CanvasCoord[1],
                                                             fill="black", width=1) #dash=(10)
                    #######################################################

                except:
                    exceptions = sys.exc_info()[0]
                    print("Joystick2DdotDisplay_ReubenPython2and3Class GUI_update_clock ERROR: Exceptions: %s" % exceptions)
                    traceback.print_exc()
                #######################################################
                #######################################################

            #######################################################
            #######################################################
            #######################################################

    ##########################################################################################################
    ##########################################################################################################