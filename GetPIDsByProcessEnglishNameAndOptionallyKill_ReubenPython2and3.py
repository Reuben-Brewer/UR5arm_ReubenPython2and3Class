# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision F, 05/10/2023

Verified working on: Python 2.7, 3.8 for Windows 8.1, 10 64-bit and Raspberry Pi Buster (no Mac testing yet).
'''

__author__ = 'reuben.brewer'

#########################################################
import os
import sys
import platform
import pexpect
import subprocess
import traceback
#########################################################

#########################################################
if sys.version_info[0] < 3:
    from builtins import raw_input as input
else:
    from future.builtins import input as input #"sudo pip3 install future" (Python 3) AND "sudo pip install future" (Python 2)
#########################################################

##########################################################################################################
##########################################################################################################
def GetMyPlatformOS():

    my_platform = ""

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

    return my_platform
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GetCurrentPythonFileNameString(IncludeFullPathFlag = 0):

    FileName = ""

    try:
        if IncludeFullPathFlag == 1:
            FileName = str(os.path.realpath(__file__))

        else:
            FileName = str(os.path.basename(__file__))

    except:
        pass
        # exceptions = sys.exc_info()[0]
        # print("GetCurrentPythonFileNameString, exceptions: %s" % exceptions, 0)
        # traceback.print_exc()

    return FileName
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GetPIDsByProcessEnglishName(ProcessName = ""):
    print("GetPIDsByProcessEnglishName: Current PID of this program is " + str(os.getpid()))

    my_platform = GetMyPlatformOS()

    PID_DictWithPIDasKey = dict()
    PID_DictWithEXEenglishNameAsKey = dict()

    #################################
    if my_platform == "windows":

        if ProcessName != "":
            shell_command_to_issue = 'tasklist /FI \"IMAGENAME eq "' + ProcessName + '.exe\"'
        else:
            shell_command_to_issue = 'tasklist'

        shell_response_bytes = subprocess.check_output(shell_command_to_issue)
        shell_response_str = str(shell_response_bytes)  # Need to convert bytes to str in Python 3

        ###############
        if sys.version_info[0] < 3:
            shell_response_ListOfStr = shell_response_str.split("\r\n")
        else:
            shell_response_ListOfStr = shell_response_str.split("\\r\\n")#PYTHON 3 DIFFERS IN HOW IT SPLITS BASED ON \r\n

        #print("\n $$$$ shell_response_ListOfStr: " + str(shell_response_ListOfStr) + "$$$$")

        for line_str in shell_response_ListOfStr:
            #print("\n$$$$ line_str:" + line_str + "$$$$")

            line_ListOfStr = line_str.split(" ")
            #print("\n$$$$ line_ListOfStr:" + str(line_ListOfStr) + "$$$$")
            #print(str(len(line_ListOfStr)))

            for line_ListOfStr_IndividualTab in line_ListOfStr:
                try:
                    #print("line_ListOfStr_IndividualTab: " + str(line_ListOfStr_IndividualTab))
                    PID_int = int(line_ListOfStr_IndividualTab)

                    EXEenglishNameAsKey = line_ListOfStr[0] #.replace('\\r\\n',"")

                    ######
                    if EXEenglishNameAsKey.find(GetCurrentPythonFileNameString()) == -1: #Shouldn't find the name of the current file anywhere
                        if PID_int != os.getpid():  # Exclude the python program that's currently running this script
                            PID_DictWithPIDasKey[PID_int] = EXEenglishNameAsKey

                            if EXEenglishNameAsKey not in PID_DictWithEXEenglishNameAsKey:
                                PID_DictWithEXEenglishNameAsKey[EXEenglishNameAsKey] = list([PID_int])
                            else:
                                PID_DictWithEXEenglishNameAsKey[EXEenglishNameAsKey].append(PID_int)

                            #print(EXEenglishNameAsKey + ", PID = " + str(PID_int))
                    ######

                    break
                except:
                    pass
    #################################

    #################################
    elif my_platform == "linux" or my_platform == "pi":
        if ProcessName != "":
            shell_command_to_issue = "ps axo command:200,pid | grep \"" + ProcessName + "\"" #'a' = show processes for all users, 'u' = display the process's user/owner, 'x' = also show processes not attached to a terminal
        else:
            shell_command_to_issue = "ps axo command:200,pid" #'a' = show processes for all users, 'u' = display the process's user/owner, 'x' = also show processes not attached to a terminal

        print("shell_command_to_issue: " + shell_command_to_issue)

        '''
        Has to use 'ps' because 'pgrep' had some issues:
        shell_command_to_issue = "pgrep \"" + ProcessName + "\"" #WORKS
        shell_response = pexpect.run(shell_command_to_issue) #ERROR, PEXPECT CAN'T HANDLE | PIPES, and pexpect.spawn('/bin/bash', ['-c', shell_command_to_issue]) didn't work.
        '''

        shell_response = subprocess.check_output(shell_command_to_issue, shell=True)
        shell_response_str = str(shell_response)
        # print("\n$$$$" + "shell_response_str: " + str(shell_response_str) + "$$$$")

        ###############
        if sys.version_info[0] < 3:
            shell_response_ListOfStr = shell_response_str.split("\n")
        else:
            shell_response_ListOfStr = shell_response_str.split("\\n")#PYTHON 3 DIFFERS IN HOW IT SPLITS BASED ON \r\n, DON'T USE .splitlines() HAS ISSUES IN PYTHON3

        # print("\n$$$$" + "shell_response_ListOfStr: " + str(shell_response_ListOfStr) + "$$$$")
        # print(str(len(shell_response_ListOfStr)))

        for line_str in shell_response_ListOfStr:
            line_str = line_str.replace("\\r", "").replace("\\n", "").replace("b'", "").replace("'", "")  # There's a leading "b'" and a trailing "'" that need to be removed.
            # print("\n$$$$ line_str: " + line_str + "\n$$$$")

            try:
                # "cat /proc/sys/kernel/pid_max" tells us that the maximum length of a PID 32768,
                # which is why we know that the last 5 characters will be enough for the PID

                PID_int = int(line_str[-5:])
                EXEenglishNameAsKey = line_str[:-5].strip()

                ######
                if EXEenglishNameAsKey.find(GetCurrentPythonFileNameString()) == -1: #Shouldn't find the name of the current file anywhere
                    if PID_int != os.getpid(): #Exclude the python program that's currently running this script
                        PID_DictWithPIDasKey[PID_int] = EXEenglishNameAsKey

                        if EXEenglishNameAsKey not in PID_DictWithEXEenglishNameAsKey:
                            PID_DictWithEXEenglishNameAsKey[EXEenglishNameAsKey] = list([PID_int])
                        else:
                            PID_DictWithEXEenglishNameAsKey[EXEenglishNameAsKey].append(PID_int)

                        #print(EXEenglishNameAsKey + ", PID = " + str(PID_int))
                ######

            except:
                pass
                # exceptions = sys.exc_info()[0]
                # print("GetPIDsByProcessEnglishName, exceptions: %s" % exceptions, 0)
                # traceback.print_exc()
    #################################

    return [PID_DictWithPIDasKey, PID_DictWithEXEenglishNameAsKey]
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def KillProcessByPIDlist(PID_list, UseSigkillForceCloseImmediatelyFlag = 0):

    my_platform = GetMyPlatformOS()

    if isinstance(PID_list, list) == 0:
        PID_list = list(PID_list)

    for PID in PID_list:
        cmd = ""

        #################################
        if my_platform == "windows":
            cmd = "Taskkill /PID " + str(PID) + " /F"
        #################################

        #################################
        elif my_platform == "linux" or my_platform == "pi":
            if UseSigkillForceCloseImmediatelyFlag == 1:
                cmd = "kill -9 " + str(PID)  # '-9' forces closed, same as -sigkill
            else:
                cmd = "kill " + str(PID)  # Allows the process to terminate cleanly.
        #################################

        print("Issuing cmd: " + cmd)
        subprocess.Popen(cmd, shell=True)

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    ############################################
    ############################################
    KillFlag = 0
    UseSigkillForceCloseImmediatelyFlag = 0
    ProcessNameToFindAndKill = ""

    try:
        if len(sys.argv) >= 2:
            ARGV_1 = sys.argv[1].strip().lower()

            print("ARGV_1: " + str(ARGV_1))
            ProcessNameToFindAndKill = ARGV_1

        if len(sys.argv) >= 3:
            ARGV_2 = sys.argv[2].strip().lower()
            print("ARGV_2: " + str(ARGV_2))

            if ARGV_2.lower().find("kill") != -1:
                KillFlag = 1
            else:
                KillFlag = 0

            if ARGV_2.lower().find("sigkill") != -1:
                UseSigkillForceCloseImmediatelyFlag = 1
            else:
                UseSigkillForceCloseImmediatelyFlag = 0

        print("UseSigkillForceCloseImmediatelyFlag: " + str(UseSigkillForceCloseImmediatelyFlag))
    except:
        exceptions = sys.exc_info()[0]
        print("Parsing ARGV_1, exceptions: %s" % exceptions, 0)
        traceback.print_exc()
    ############################################
    ############################################

    [PID_DictWithPIDasKey, PID_DictWithEXEenglishNameAsKey] = GetPIDsByProcessEnglishName(ProcessNameToFindAndKill)
    #[PID_DictWithPIDasKey, PID_DictWithEXEenglishNameAsKey] = GetPIDsByProcessEnglishName(ProcessNameToFindAndKill)
    #[PID_DictWithPIDasKey, PID_DictWithEXEenglishNameAsKey] = GetPIDsByProcessEnglishName("")

    print("$$$$$$$$$$$$")
    print("PID_DictWithPIDasKey: " + str(PID_DictWithPIDasKey))
    print("$$$$$$$$$$$$")
    print("PID_DictWithEXEenglishNameAsKey: " + str(PID_DictWithEXEenglishNameAsKey))
    print("$$$$$$$$$$$$")

    ############################################
    ############################################
    ListOfProcessesToKill = list()
    for PIDint in PID_DictWithPIDasKey:
        print("PID: " + str(PIDint) + ": " + PID_DictWithPIDasKey[PIDint])
        ListOfProcessesToKill.append(PIDint)

    print("ListOfProcessesToKill: " + str(ListOfProcessesToKill))
    ############################################
    ############################################

    ############################################
    ############################################
    if KillFlag == 1:
        KillProcessByPIDlist(ListOfProcessesToKill, UseSigkillForceCloseImmediatelyFlag) #the 2nd argument allows us to include "SIGKILL"
    else:
        input("Without a 'kill' flag in ARGV, we'll find PIDs and wait for you to press any key to exit (without killing!)...")
    ############################################
    ############################################


##########################################################################################################
##########################################################################################################