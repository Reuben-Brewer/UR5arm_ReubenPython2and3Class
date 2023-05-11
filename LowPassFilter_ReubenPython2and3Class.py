# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision H, 05/10/2023

Verified working on: Python 2.7, 3.8 for Windows 8.1, 10 64-bit, Ubuntu 20.04, and Raspberry Pi Buster (no Mac testing yet).
'''

__author__ = 'reuben.brewer'

###########################################################
import os
import sys
import time
import datetime
import math
import cmath
import ctypes
import collections
import numpy
import random
from random import randint
import inspect #To enable 'TellWhichFileWereIn'
import traceback
###########################################################

class LowPassFilter_ReubenPython2and3Class():

    ##########################################################################################################
    ##########################################################################################################
    def __init__(self, setup_dict):

        print("#################### LowPassFilter_ReubenPython2and3Class __init__ starting. ####################")

        #########################################################
        #########################################################
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "UseMedianFilterFlag" in setup_dict:
            self.UseMedianFilterFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseMedianFilterFlag", setup_dict["UseMedianFilterFlag"])
        else:
            self.UseMedianFilterFlag = 1

        print("LowPassFilter_ReubenPython2and3Class __init__: UseMedianFilterFlag: " + str(self.UseMedianFilterFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "UseExponentialSmoothingFilterFlag" in setup_dict:
            self.UseExponentialSmoothingFilterFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseExponentialSmoothingFilterFlag", setup_dict["UseExponentialSmoothingFilterFlag"])
        else:
            self.UseExponentialSmoothingFilterFlag = 1

        print("LowPassFilter_ReubenPython2and3Class __init__: UseExponentialSmoothingFilterFlag: " + str(self.UseExponentialSmoothingFilterFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "ExponentialSmoothingFilterLambda" in setup_dict:
            self.ExponentialSmoothingFilterLambda = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("ExponentialSmoothingFilterLambda", setup_dict["ExponentialSmoothingFilterLambda"], 0.0, 1.0)

        else:
            self.ExponentialSmoothingFilterLambda = 0.005

        print("LowPassFilter_ReubenPython2and3Class __init__: ExponentialSmoothingFilterLambda: " + str(self.ExponentialSmoothingFilterLambda))
        #########################################################
        #########################################################

        self.SignalInRaw = [0.0]*5
        self.SignalOutSmoothed = [0.0]*5

        self.MostRecentDataDict = dict()

        #########################################################
        #########################################################
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1
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
    def SwapTwoNumbersBasedOnSize(self, j, k):  # swaps values of j and k if j > k

        x = j
        y = k
        if j > k:
            # print "SWAPPED " + str(j) + " and " + str(k)
            x = k
            y = j

        # print [x, y]
        return [x, y]
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ComputeMedian5point_BoseNelson(self, a0, a1, a2, a3, a4):  # calculate the median from 5 adjacent points
        '''Network for N=5, using Bose-Nelson Algorithm.
          SWAP(0, 1); SWAP(3, 4); SWAP(2, 4);
          SWAP(2, 3); SWAP(0, 3); SWAP(0, 2);
          SWAP(1, 4); SWAP(1, 3); SWAP(1, 2);
        '''

        x0 = a0
        x1 = a1
        x2 = a2
        x3 = a3
        x4 = a4

        [x0, x1] = self.SwapTwoNumbersBasedOnSize(x0, x1)  # 0,1
        [x3, x4] = self.SwapTwoNumbersBasedOnSize(x3, x4)
        [x2, x4] = self.SwapTwoNumbersBasedOnSize(x2, x4)
        [x2, x3] = self.SwapTwoNumbersBasedOnSize(x2, x3)  # 2,3
        [x0, x3] = self.SwapTwoNumbersBasedOnSize(x0, x3)
        [x0, x2] = self.SwapTwoNumbersBasedOnSize(x0, x2)
        [x1, x4] = self.SwapTwoNumbersBasedOnSize(x1, x4)  # 1,4
        [x1, x3] = self.SwapTwoNumbersBasedOnSize(x1, x3)
        [x1, x2] = self.SwapTwoNumbersBasedOnSize(x1, x2)

        MedianValue = x2

        return MedianValue
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def AddDataPointFromExternalProgram(self, NewDataPoint):

        try:
            ###############################################
            NewDataPoint = float(NewDataPoint)

            self.SignalInRaw = list(numpy.roll(self.SignalInRaw, 1)) #MUST EXPLICITLY MAKE NEW LIST() FOR THIS TO WORK PROPERLY
            self.SignalInRaw[0] = NewDataPoint  #Add the incoming data point
    
            self.SignalOutSmoothed = list(numpy.roll(self.SignalOutSmoothed, 1)) #MUST EXPLICITLY MAKE NEW LIST() FOR THIS TO WORK PROPERLY

            # fmedian = median5(fval_prev4, fval_prev3, fval_prev2, fval_prev1, fval_new);
            MedianValue_BoseNelson = self.ComputeMedian5point_BoseNelson(self.SignalInRaw[4], self.SignalInRaw[3], self.SignalInRaw[2], self.SignalInRaw[1], self.SignalInRaw[0])
            #MedianValue_Numpy = numpy.median(self.SignalInRaw) MedianValue_Numpy is much slower than MedianValue_BoseNelson
            #print str(MedianValue_BoseNelson - MedianValue_Numpy)

            if self.UseMedianFilterFlag == 1:
                self.SignalOutSmoothed[0] = MedianValue_BoseNelson
            else:
                self.SignalOutSmoothed[0] = NewDataPoint

            if self.UseExponentialSmoothingFilterFlag == 1:
                #new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value
                self.SignalOutSmoothed[0] = self.ExponentialSmoothingFilterLambda * self.SignalInRaw[0] + (1.0 - self.ExponentialSmoothingFilterLambda) * self.SignalOutSmoothed[1]
            ###############################################

            ###############################################
            self.MostRecentDataDict = dict([("SignalInRaw", self.SignalInRaw[0]),
                                           ("SignalOutSmoothed", self.SignalOutSmoothed[0]),
                                           ("DataStreamingFrequency", -11111.0)]) #For backwards-compatibility, remove this later after we've updated our code.

            return self.MostRecentDataDict
            ###############################################

        except:
            exceptions = sys.exc_info()[0]
            print("AddDataPointFromExternalProgram: Exceptions: %s" % exceptions)
            return dict()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentDataDict(self):

        #deepcopy is not required as MostRecentDataDict only contains numbers (no lists, dicts, etc. that go beyond 1-level).
        return self.MostRecentDataDict.copy()
    ##########################################################################################################
    ##########################################################################################################


