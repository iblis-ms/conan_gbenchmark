@ECHO off 

SET "CURRENT_PATH=%~dp0"

CD %REPO_BASE_DIR%
start conan_server
timeout 10 > NUL

CD %CURRENT_PATH%
CALL stopConanServer.bat

IF EXIST "%HOME%\.conan\data\GBenchmark" RD /q /s "%HOME%\.conan\data\GBenchmark"

IF EXIST "%HOME%\.conan_server\data\GBenchmark" RD /q /s "%HOME%\.conan_server\data\GBenchmark"

CD %REPO_BASE_DIR%
start conan_server

COPY %CURRENT_PATH%\..\server.conf %HOMEPATH%\.conan_server\server.conf
CALL conan export iblis_ms/stable

SET FOUND_LOCAL_SERVER=
FOR /f %%a in ('conan remote list ^| findstr /i http://localhost:9300') DO (
    SET FOUND_LOCAL_SERVER=true
)

IF "%FOUND_LOCAL_SERVER%"=="" ( 
  CALL conan remote add local http://localhost:9300
) 

CALL conan user -p demo -r local demo
CALL conan upload GBenchmark/1.1.0@iblis_ms/stable --all -r=local --force

CD %CURRENT_PATH%
