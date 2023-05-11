# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision E, 05/10/2023

Verified working on: Python 3.8 for Windows 10 64-bit (haven't tested on Ubuntu, Raspberry Pi, or Mac yet).
'''

__author__ = 'reuben.brewer'

#########################################################
import os
import sys
import traceback
import time
import datetime
from collections import OrderedDict
from copy import deepcopy
import glob #For getting a list of files in a directory with a certain extension

import pandas
#########################################################

#########################################################
#MUST USE VERSION 224 (https://stackoverflow.com/questions/58612306/how-to-fix-importerror-dll-load-failed-while-importing-win32api/60611014#60611014)
#Latest version is 228 but gives us a DLL error.
#"pip install pywin32==224"
import win32com.client #for commanding Excel as a program
#########################################################

#########################################################
#For writing excel files.
#"pip install xlwt==1.2.0"
import xlwt
#########################################################

#########################################################
#For copying excel file when we create the excel file. HAVE TO INSTALL SEPARATELY FROM XLWT/XLRD.
#"pip install xlutils==1.7.1"
from xlutils.copy import copy
#########################################################

#########################################################
#For reading excel files.
#"pip install xlrd==1.0.0"
import xlrd
#########################################################

#########################################################
#http://xlsxwriter.readthedocs.io/chart.html FOR MAKING CHARTS
#XlsxWriter can only create new files. It cannot read or modify existing files. Can only handle xlsx files, not xls
#"pip install xlsxwriter==0.9.6" verified working, but doesn't support setting the chart size.
#"pip install xlsxwriter==1.3.3" INSTALLED 08/28/20 (had to manually delete older version from /lib/site-packages because it was distutils-managed. Works overall, but the function ".set_size" doesn't do anything.
import xlsxwriter
#########################################################

##########################################################################################################
##########################################################################################################
def OpenXLSsndCopyDataToLists(FileName_full_path):

    DataOrderedDict = OrderedDict()

    try:

        ##########################################################################################################
        xlrd_workbook = xlrd.open_workbook(FileName_full_path)

        sheet_names = xlrd_workbook.sheet_names()
        #print('Sheet Names', sheet_names)

        xlrd_sheet = xlrd_workbook.sheet_by_name(sheet_names[0])
        #print(xlrd_sheet.name)

        ##########################################################################################################

        ##########################################################################################################
        header_variable_name_list = []
        ListOfColumnDataLists = []
        for column in range(0, xlrd_sheet.ncols):  # Iterate through columns
            cell_value = xlrd_sheet.cell_value(0, column)  # Get cell object by row, col
            cell_value_as_string = str(cell_value).strip()
            header_variable_name_list.append(cell_value_as_string)
            ListOfColumnDataLists.append([])
        print("Detected the following variable names: " + str(header_variable_name_list))
        #print(ListOfColumnDataLists)
        ##########################################################################################################

        ##########################################################################################################
        for row in range(1, xlrd_sheet.nrows): # Iterate through rows starting at index 1 so that we don't capture the header
            for column in range(0, xlrd_sheet.ncols):  # Iterate through columns
                cell_value = xlrd_sheet.cell_value(row, column)  # Get cell object by row, col
                ListOfColumnDataLists[column].append(cell_value)
        ##########################################################################################################

        ##########################################################################################################
        for column in range(0, xlrd_sheet.ncols):  # Iterate through columns
            DataOrderedDict[header_variable_name_list[column]] = ListOfColumnDataLists[column]
        ##########################################################################################################

        return DataOrderedDict

    except:
        exceptions = sys.exc_info()[0]
        print("OpenXLSsndCopyDataToLists, exceptions: %s" % exceptions)
        traceback.print_exc()
        return DataOrderedDict

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def CreateExcelChart(FileName_to_save_full_path, DataOrderedDictToWrite):

    #print("FileName_to_save_full_path: " + FileName_to_save_full_path)

    workbook = xlsxwriter.Workbook(FileName_to_save_full_path)
    worksheet = workbook.add_worksheet()

    ##########################################################################################################
    alphabetString = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI", "AJ", "AK", "AL", "AM", "AN", "AO", "AP", "AQ", "AR", "AS", "AT", "AU", "AV", "AW", "AX", "AY", "AZ"]
    numerical_index = 0
    NumberOfDataRows = -1
    for key in DataOrderedDictToWrite:
        starting_cell_string_identifier = alphabetString[numerical_index] + "1"
        #print("DataOrderedDictToWrite[key]: " + str(DataOrderedDictToWrite[key]))
        worksheet.write_column(starting_cell_string_identifier, [key] + DataOrderedDictToWrite[key]) #
        NumberOfDataRows = len(DataOrderedDictToWrite[key])
        worksheet.set_column(numerical_index, numerical_index, 20) #set column width of current column to 20
        numerical_index = numerical_index + 1
    ##########################################################################################################
        
    #"Time, ZEDmini_X, ZEDmini_Y, ZEDmini_Z, UR5arm_X, UR5arm_Y, UR5arm_Z, UR5arm_Rx, UR5arm_Ry, UR5arm_Rz"

    Time_ExcelColumnLetter = "A"

    ZEDmini_X_ExcelColumnLetter = "B"

    ZEDmini_Y_ExcelColumnLetter = "C"

    ZEDmini_Z_ExcelColumnLetter = "D"

    UR5arm_X_ExcelColumnLetter = "E"

    UR5arm_Y_ExcelColumnLetter = "F"

    UR5arm_Z_ExcelColumnLetter = "G"

    UR5arm_Rx_ExcelColumnLetter = "H"

    UR5arm_Ry_ExcelColumnLetter = "I"

    UR5arm_Rz_ExcelColumnLetter = "J"

    ZEDmini_vs_UR5arm_Xaxis_Chart_sheet = workbook.add_chartsheet("ZEDmini_vs_UR5arm_Xaxis")
    ZEDmini_vs_UR5arm_Xaxis_Chart = workbook.add_chart({'type': 'scatter'}) #http://xlsxwriter.readthedocs.io/example_chart_scatter.html
    ZEDmini_vs_UR5arm_Xaxis_Chart.add_series({'name': 'Time_vs_ZEDmini_Xaxis','categories': "=Sheet1!$" + Time_ExcelColumnLetter + "$2:$" + Time_ExcelColumnLetter + "$"+str(NumberOfDataRows+1),'values': "=Sheet1!$" + ZEDmini_X_ExcelColumnLetter + "$2:$" + ZEDmini_X_ExcelColumnLetter + "$" + str(NumberOfDataRows+1)}) #X VALUES FIRST, THEN Y
    ZEDmini_vs_UR5arm_Xaxis_Chart.add_series({'name': 'Time_vs_UR5arm_Xaxis','categories': "=Sheet1!$" + Time_ExcelColumnLetter + "$2:$" + Time_ExcelColumnLetter + "$"+str(NumberOfDataRows+1),'values': "=Sheet1!$" + UR5arm_X_ExcelColumnLetter + "$2:$" + UR5arm_X_ExcelColumnLetter + "$" + str(NumberOfDataRows+1)}) #X VALUES FIRST, THEN Y
    ZEDmini_vs_UR5arm_Xaxis_Chart.set_title ({'name': 'Time vs ZEDmini, UR5arm (Xaxis)'})
    ZEDmini_vs_UR5arm_Xaxis_Chart.set_x_axis({'name': 'Time'})
    ZEDmini_vs_UR5arm_Xaxis_Chart.set_y_axis({'name': 'Xaxis Value'})
    ZEDmini_vs_UR5arm_Xaxis_Chart_sheet.set_chart(ZEDmini_vs_UR5arm_Xaxis_Chart)
    
    ZEDmini_vs_UR5arm_Yaxis_Chart_sheet = workbook.add_chartsheet("ZEDmini_vs_UR5arm_Yaxis")
    ZEDmini_vs_UR5arm_Yaxis_Chart = workbook.add_chart({'type': 'scatter'}) #http://xlsxwriter.readthedocs.io/example_chart_scatter.html
    ZEDmini_vs_UR5arm_Yaxis_Chart.add_series({'name': 'Time_vs_ZEDmini_Yaxis','categories': "=Sheet1!$" + Time_ExcelColumnLetter + "$2:$" + Time_ExcelColumnLetter + "$"+str(NumberOfDataRows+1),'values': "=Sheet1!$" + ZEDmini_Y_ExcelColumnLetter + "$2:$" + ZEDmini_Y_ExcelColumnLetter + "$" + str(NumberOfDataRows+1)}) #X VALUES FIRST, THEN Y
    ZEDmini_vs_UR5arm_Yaxis_Chart.add_series({'name': 'Time_vs_UR5arm_Yaxis','categories': "=Sheet1!$" + Time_ExcelColumnLetter + "$2:$" + Time_ExcelColumnLetter + "$"+str(NumberOfDataRows+1),'values': "=Sheet1!$" + UR5arm_Y_ExcelColumnLetter + "$2:$" + UR5arm_Y_ExcelColumnLetter + "$" + str(NumberOfDataRows+1)}) #X VALUES FIRST, THEN Y
    ZEDmini_vs_UR5arm_Yaxis_Chart.set_title ({'name': 'Time vs ZEDmini, UR5arm (Yaxis)'})
    ZEDmini_vs_UR5arm_Yaxis_Chart.set_x_axis({'name': 'Time'})
    ZEDmini_vs_UR5arm_Yaxis_Chart.set_y_axis({'name': 'Yaxis Value'})
    ZEDmini_vs_UR5arm_Yaxis_Chart_sheet.set_chart(ZEDmini_vs_UR5arm_Yaxis_Chart)
    
    ZEDmini_vs_UR5arm_Zaxis_Chart_sheet = workbook.add_chartsheet("ZEDmini_vs_UR5arm_Zaxis")
    ZEDmini_vs_UR5arm_Zaxis_Chart = workbook.add_chart({'type': 'scatter'}) #http://xlsxwriter.readthedocs.io/example_chart_scatter.html
    ZEDmini_vs_UR5arm_Zaxis_Chart.add_series({'name': 'Time_vs_ZEDmini_Zaxis','categories': "=Sheet1!$" + Time_ExcelColumnLetter + "$2:$" + Time_ExcelColumnLetter + "$"+str(NumberOfDataRows+1),'values': "=Sheet1!$" + ZEDmini_Z_ExcelColumnLetter + "$2:$" + ZEDmini_Z_ExcelColumnLetter + "$" + str(NumberOfDataRows+1)}) #X VALUES FIRST, THEN Y
    ZEDmini_vs_UR5arm_Zaxis_Chart.add_series({'name': 'Time_vs_UR5arm_Zaxis','categories': "=Sheet1!$" + Time_ExcelColumnLetter + "$2:$" + Time_ExcelColumnLetter + "$"+str(NumberOfDataRows+1),'values': "=Sheet1!$" + UR5arm_Z_ExcelColumnLetter + "$2:$" + UR5arm_Z_ExcelColumnLetter + "$" + str(NumberOfDataRows+1)}) #X VALUES FIRST, THEN Y
    ZEDmini_vs_UR5arm_Zaxis_Chart.set_title ({'name': 'Time vs ZEDmini, UR5arm (Zaxis)'})
    ZEDmini_vs_UR5arm_Zaxis_Chart.set_x_axis({'name': 'Time'})
    ZEDmini_vs_UR5arm_Zaxis_Chart.set_y_axis({'name': 'Zaxis Value'})
    ZEDmini_vs_UR5arm_Zaxis_Chart_sheet.set_chart(ZEDmini_vs_UR5arm_Zaxis_Chart)

    workbook.close()
    time.sleep(0.05)

    pywin32_FileName_xls = FileName_to_save_full_path
    pywin32_FileName_xls = pywin32_FileName_xls.replace("/", "\\") #This line is needed or else the Excel file will give you an error.

    xl = win32com.client.Dispatch("Excel.Application")
    xl.DisplayAlerts = False
    wb = xl.Workbooks.Open(pywin32_FileName_xls)
    wb.SaveAs(pywin32_FileName_xls, FileFormat = 56)
    wb.Close()
    xl.Quit()
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def animate(i):
    global DataOrderedDictFromOriginalFile
    global line

    line.set_data(DataOrderedDictFromOriginalFile["x"][i], DataOrderedDictFromOriginalFile["y"][i], DataOrderedDictFromOriginalFile["z"][i])  # update the data.

    return line
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    global DataOrderedDictFromOriginalFile
    global line

    global FileDirectory

    ##########################################################################################################
    try:
        if len(sys.argv) >= 2:
            ARGV_1 = sys.argv[1]

            print("ARGV_1: " + str(ARGV_1))
            FileDirectory = ARGV_1

        else:
            FileDirectory = os.getcwd()

    except:
        exceptions = sys.exc_info()[0]
        print("Parsing ARGV_1, exceptions: %s" % exceptions, 0)
        traceback.print_exc()

    print("Using FileDirectory = " + str(FileDirectory))
    ##########################################################################################################

    ##########################################################################################################

    #########################################################
    print("$$$$$$$$$$$$$$$$")
    print("RUN THIS PROGRAM FROM COMMAND LINE LIKE THIS: 'python ExcelPlot_CSVfileForTrajectoryData.py CSV-FILE-DIRECTORY-FULL-PATH'")
    print("$$$$$$$$$$$$$$$$")
    #########################################################

    #########################################################
    if FileDirectory.find(":") == -1:
        print("ERROR: You must specify the FULL path, starting from the disk drive like 'C:'")
        exit()()
    #########################################################

    #########################################################
    FileSuffixForChartFile = "_with_chart.xls"

    FileList_csv = glob.glob(FileDirectory + '/*.csv')
    FileList_xls = glob.glob(FileDirectory + '/*.xls')

    print("Found " + str(len(FileList_csv)) + " .csv files and " + str(len(FileList_xls)) + " .xls files.")
    #print("FileList_csv: " + str(FileList_csv))
    #print("FileList_xls: " + str(FileList_xls))
    #########################################################
    
    ##########################################################################################################
    for FileName_csv in FileList_csv:
        FileName_xls = FileName_csv.replace(".csv", ".xls")
        FileName_WITH_CHART_xls = FileName_csv.replace(".csv", FileSuffixForChartFile)

        ################################
        if FileName_xls not in FileList_xls: #Make sure we haven't already converted this csv to a xls file.
            print("Converting CSV file to xls file for " + FileName_csv)
            read_file = pandas.read_csv(FileName_csv)
            read_file.to_excel(FileName_xls, index=None, header=True)
        else:
            print("xls file '" + FileName_xls + "' already exists so skipping csv-xls conversion.")
        ################################

        ################################
        if FileName_WITH_CHART_xls not in FileList_xls: #Make sure we haven't already created a chart file for this csv.

            print("Creating xls chart file for " + FileName_csv)

            DataOrderedDictFromOriginalFile = OpenXLSsndCopyDataToLists(FileName_xls)

            CreateExcelChart(FileName_WITH_CHART_xls, DataOrderedDictFromOriginalFile)

        else:
            print("xls chart file already exists so skipping for " + FileName_csv)
        ################################


    ##########################################################################################################

##########################################################################################################
##########################################################################################################

