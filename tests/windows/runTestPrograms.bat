@ECHO off 

ECHO "------------------ program tests ------------------"

SET "CURRENT_PATH=%~dp0"

CALL startConanServer.bat
IF %errorlevel% neq 0 EXIT /b %errorlevel%


CALL runVisual.bat 
IF %errorlevel% neq 0 EXIT /b %errorlevel%

CALL runGcc.bat libstdc++11
IF %errorlevel% neq 0 EXIT /b %errorlevel%

CALL runGcc.bat libstdc++
IF %errorlevel% neq 0 EXIT /b %errorlevel%

CALL stopConanServer.bat
IF %errorlevel% neq 0 EXIT /b %errorlevel%

CD %CURRENT_PATH%
