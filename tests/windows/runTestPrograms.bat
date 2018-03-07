@ECHO off 

ECHO "------------------ program tests ------------------"

SET "CURRENT_PATH=%~dp0"


CALL runVisual.bat 
IF %errorlevel% neq 0 EXIT /b %errorlevel%

CALL runGcc.bat libstdc++11
IF %errorlevel% neq 0 EXIT /b %errorlevel%

CALL runGcc.bat libstdc++
IF %errorlevel% neq 0 EXIT /b %errorlevel%


CD %CURRENT_PATH%
