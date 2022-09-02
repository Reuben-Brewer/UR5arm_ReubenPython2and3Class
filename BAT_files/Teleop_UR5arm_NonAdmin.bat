REM This is a comment. First we CD into the disk drive (like "C" or "G"), so that our fullpath python commands will work.
REM This is a comment. Second we CD into the specific code working directory so that running this BAT file from the command prompt will keep us in the same directory.
REM This is a comment. We could issue the fullpath python command without this second CD into the specific folder, but then we'd be changed to "C:" or "G:" instead of our code directory.

SET CurrentDiskDrive=%CD:~0,3%
SET CurrentDirectoryFullPath=%~dp0

ECHO "CurrentDiskDrive:%CurrentDiskDrive%"
ECHO "CurrentDirectoryFullPath:%CurrentDirectoryFullPath%"

CD %CurrentDiskDrive%
CD %CurrentDirectoryFullPath%

python "%CurrentDirectoryFullPath%Teleop_UR5arm.py" "software_launch_method":"BATfile"

TIMEOUT 1