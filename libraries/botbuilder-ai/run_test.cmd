@ECHO OFF


cd C:\Users\v-asho\Desktop\Python\botbuilder-python\libraries\botbuilder-ai

python -m compileall .
IF %ERRORLEVEL% NEQ 0 (
  ECHO [Error] build failed!
  exit /b %errorlevel%
)

python -O -m compileall .
IF %ERRORLEVEL% NEQ 0 (
  ECHO [Error] build failed!
  exit /b %errorlevel%
)

pip install .
IF %ERRORLEVEL% NEQ 0 (
  ECHO [Error] DIALOGS Install failed!
  exit /b %errorlevel%
)

python -m unittest discover ./tests
IF %ERRORLEVEL% NEQ 0 (
  ECHO [Error] Test failed!
  exit /b %errorlevel%
