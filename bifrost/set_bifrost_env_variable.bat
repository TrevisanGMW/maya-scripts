@echo off
@title =  Create Environment Variable for Bifrost
SET BifrostVar=%~dp0bifrost_lib_config.json
:MENU
cls
color 0A
@echo.
@echo.
@echo.       This script auto creates the BIFROST_LIB_CONFIG_FILES environment variable for Bifrost.
@echo.       Put the ".bat" file in the folder where your "bifrost_lib_config.json" is and run it.
@echo.
@echo.
@echo. 	  1 = Overwrite Current Bifrost Variable (1st Var)
@echo. 	  2 = Add to Current Bifrost Variable (2nd, 3rd, etc..)
@echo. 	  3 = Open System Properties
@echo. 	  4 = Print BIFROST_LIB_CONFIG_FILES variable
@echo.
@echo.
@echo off
SET /P M=Type 1, 2, 3 or 4 then press ENTER:
IF %M%==1 GOTO OVERWRITE
IF %M%==2 GOTO ADD
IF %M%==3 GOTO SYSDM
IF %M%==4 GOTO PRINT
GOTO EOF

:OVERWRITE
SETX BIFROST_LIB_CONFIG_FILES "%BifrostVar%"
pause
GOTO EOF

:ADD
SET NewVar=%BIFROST_LIB_CONFIG_FILES%;%BifrostVar%
SETX BIFROST_LIB_CONFIG_FILES "%NewVar%"
pause
GOTO EOF

:PRINT
@echo.
@echo.
@echo.   %BIFROST_LIB_CONFIG_FILES%
@echo.
@echo.
pause
GOTO MENU

:SYSDM
sysdm.cpl
GOTO MENU

:EOF
exit