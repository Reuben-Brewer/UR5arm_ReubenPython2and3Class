# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision B, 05/10/2023

Verified working on: Python 3.8 for Windows 10 64-bit, Ubuntu 20.04, and Raspberry Pi Buster (no Mac testing yet).
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
from copy import * #for deepcopy(dict)

###########################################################

class LowPassFilterForDictsOfLists_ReubenPython2and3Class():

    ##########################################################################################################
    ##########################################################################################################
    def __init__(self, setup_dict):

        print("#################### LowPassFilterForDictsOfLists_ReubenPython2and3Class __init__ starting. ####################")

        self.setup_dict = setup_dict

        #########################################################
        #########################################################
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DictOfVariableFilterSettings" in self.setup_dict:
            self.DictOfVariableFilterSettings = self.setup_dict["DictOfVariableFilterSettings"]

            '''
            #STILL NEED TO IMPLEMENT A CHECK OF ALL VALUES
            self.UseMedianFilterFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseMedianFilterFlag", self.setup_dict["UseMedianFilterFlag"])
            self.UseExponentialSmoothingFilterFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseExponentialSmoothingFilterFlag", self.setup_dict["UseExponentialSmoothingFilterFlag"])
            self.ExponentialSmoothingFilterLambda = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("ExponentialSmoothingFilterLambda", self.setup_dict["ExponentialSmoothingFilterLambda"], 0.0, 1.0)
            '''

        else:
            self.DictOfVariableFilterSettings = dict()

        print("LowPassFilterForDictsOfLists_ReubenPython2and3Class __init__: DictOfVariableFilterSettings: " + str(self.DictOfVariableFilterSettings))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.VariablesDict = dict()
        #########################################################
        #########################################################

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
    def AddDictOfVariableFilterSettingsFromExternalProgram(self, NewDictOfVariableFilterSettings):

        for VariableNameString in NewDictOfVariableFilterSettings:
            if VariableNameString not in self.DictOfVariableFilterSettings:
                self.DictOfVariableFilterSettings[VariableNameString] = deepcopy(NewDictOfVariableFilterSettings[VariableNameString])

        #print("AddDictOfVariableFilterSettingsFromExternalProgram: " + str(self.DictOfVariableFilterSettings))
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
    ##########################################################################################################
    def AddDataDictFromExternalProgram(self, DataDictOfNewPointsForMultipleVariables):

        #print("AddDataDictFromExternalProgram: self.DictOfVariableFilterSettings = " + str(self.DictOfVariableFilterSettings))

        ##########################################################################################################
        ##########################################################################################################
        for VariableNameString in DataDictOfNewPointsForMultipleVariables:

            ##########################################################################################################
            if VariableNameString in self.DictOfVariableFilterSettings:

                ###############################################
                ###############################################
                UpdatedValuesList = DataDictOfNewPointsForMultipleVariables[VariableNameString]
                if isinstance(UpdatedValuesList, list) == 0:
                    UpdatedValuesList = [UpdatedValuesList]
                ###############################################
                ###############################################

                ###############################################
                ###############################################
                if VariableNameString not in self.VariablesDict:

                    ###############################################
                    LengthOfList = len(UpdatedValuesList)
                    StartingValueOfSignalList = [0.0]*5
                    self.VariablesDict[VariableNameString] = dict([("__SignalInRawHistoryList", list([StartingValueOfSignalList]*LengthOfList)),
                                                                   ("__SignalOutFilteredHistoryList", list([StartingValueOfSignalList]*LengthOfList)),
                                                                   ("Raw_MostRecentValuesList", [0.0]*LengthOfList),
                                                                   ("Filtered_MostRecentValuesList", [0.0]*LengthOfList),
                                                                   ("UseMedianFilterFlag", self.DictOfVariableFilterSettings[VariableNameString]["UseMedianFilterFlag"]),
                                                                   ("UseExponentialSmoothingFilterFlag", self.DictOfVariableFilterSettings[VariableNameString]["UseExponentialSmoothingFilterFlag"]),
                                                                   ("ExponentialSmoothingFilterLambda", self.DictOfVariableFilterSettings[VariableNameString]["ExponentialSmoothingFilterLambda"])])
                    ###############################################

                ###############################################
                ###############################################

                ###############################################
                ###############################################
                else:

                    ###############################################
                    for Index, Value in enumerate(UpdatedValuesList):
                        self.UpdateOneVariableWithNewValue(VariableNameString, Index, Value)
                    ###############################################

                ###############################################
                ###############################################

            ##########################################################################################################

            ##########################################################################################################
            else:
                print("AddDataDictFromExternalProgram, error: " + VariableNameString + " not in self.DictOfVariableFilterSettings")
                return dict()
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        return deepcopy(self.VariablesDict)
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateOneVariableWithNewValue(self, VariableNameStr, ListIndex, NewValue):

        try:

            #print("UpdateOneVariableWithNewValue: " + str(VariableNameStr) + ", ListIndex = " + ", NewValue = " + str(NewValue))

            ###############################################
            ###############################################
            ###############################################
            NewValue = float(NewValue)

            ###############################################
            ###############################################
            self.VariablesDict[VariableNameStr]["__SignalInRawHistoryList"][ListIndex] = list(numpy.roll(self.VariablesDict[VariableNameStr]["__SignalInRawHistoryList"][ListIndex], 1)) #MUST EXPLICITLY MAKE NEW LIST() FOR THIS TO WORK PROPERLY
            self.VariablesDict[VariableNameStr]["__SignalInRawHistoryList"][ListIndex][0] = NewValue  #Add the incoming data point
            ###############################################
            ###############################################

            ###############################################
            ###############################################

            ###############################################
            self.VariablesDict[VariableNameStr]["__SignalOutFilteredHistoryList"][ListIndex] = list(numpy.roll(self.VariablesDict[VariableNameStr]["__SignalOutFilteredHistoryList"][ListIndex], 1)) #MUST EXPLICITLY MAKE NEW LIST() FOR THIS TO WORK PROPERLY
            ###############################################

            ###############################################
            # fmedian = median5(fval_prev4, fval_prev3, fval_prev2, fval_prev1, fval_new);
            MedianValue_BoseNelson = self.ComputeMedian5point_BoseNelson(self.VariablesDict[VariableNameStr]["__SignalInRawHistoryList"][ListIndex][4],
                                                                         self.VariablesDict[VariableNameStr]["__SignalInRawHistoryList"][ListIndex][3],
                                                                         self.VariablesDict[VariableNameStr]["__SignalInRawHistoryList"][ListIndex][2],
                                                                         self.VariablesDict[VariableNameStr]["__SignalInRawHistoryList"][ListIndex][1],
                                                                         self.VariablesDict[VariableNameStr]["__SignalInRawHistoryList"][ListIndex][0])
            #MedianValue_Numpy = numpy.median(self.__SignalInRawHistoryList) MedianValue_Numpy is much slower than MedianValue_BoseNelson
            #print str(MedianValue_BoseNelson - MedianValue_Numpy)

            if self.VariablesDict[VariableNameStr]["UseMedianFilterFlag"] == 1:
                self.VariablesDict[VariableNameStr]["__SignalOutFilteredHistoryList"][ListIndex][0] = MedianValue_BoseNelson
            else:
                self.VariablesDict[VariableNameStr]["__SignalOutFilteredHistoryList"][ListIndex][0] = NewValue
            ###############################################

            ###############################################
            if self.VariablesDict[VariableNameStr]["UseExponentialSmoothingFilterFlag"] == 1:
                #new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value
                self.VariablesDict[VariableNameStr]["__SignalOutFilteredHistoryList"][ListIndex][0] = self.VariablesDict[VariableNameStr]["ExponentialSmoothingFilterLambda"] * self.VariablesDict[VariableNameStr]["__SignalInRawHistoryList"][ListIndex][0] + (1.0 - self.VariablesDict[VariableNameStr]["ExponentialSmoothingFilterLambda"]) * self.VariablesDict[VariableNameStr]["__SignalOutFilteredHistoryList"][ListIndex][1]
            ###############################################

            ###############################################
            self.VariablesDict[VariableNameStr]["Raw_MostRecentValuesList"][ListIndex] = self.VariablesDict[VariableNameStr]["__SignalInRawHistoryList"][ListIndex][0]
            self.VariablesDict[VariableNameStr]["Filtered_MostRecentValuesList"][ListIndex] = self.VariablesDict[VariableNameStr]["__SignalOutFilteredHistoryList"][ListIndex][0]
            ###############################################

            ###############################################
            ###############################################

            ###############################################
            ###############################################
            ###############################################

        except:
            exceptions = sys.exc_info()[0]
            print("UpdateOneVariableWithNewValue, exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentDataDict(self):

        return deepcopy(self.VariablesDict.copy()) #deepcopy is required we're returning a dict of dicts.
    ##########################################################################################################
    ##########################################################################################################


