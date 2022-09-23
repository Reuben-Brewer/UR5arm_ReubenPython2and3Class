#!/bin/sh
#IF THIS SCRIPT CAN'T BE FOUND OR RUN IN THE COMMAND TERMINAL, TYPE "dos2unix filename.sh" to remove ^M characters that are preenting it from running.

CurrentTimeVariable=`date +%s`
echo "CurrentTimeVariable in seconds = $CurrentTimeVariable"

LogFileFullPath="Teleop_UR5arm_ExecutionLog_$CurrentTimeVariable.txt"
echo "LogFileFullPath = $LogFileFullPath"

echo "Running Launch_Teleop_UR5arm_Admin.sh" | tee -a $LogFileFullPath

echo "Launch_Teleop_UR5arm_Admin.sh running Teleop_UR5arm.py" | tee -a $LogFileFullPath
sudo python3 -u Teleop_UR5arm.py "SOFTWARE_LAUNCH_METHOD:BASH" | tee -a $LogFileFullPath

exit
