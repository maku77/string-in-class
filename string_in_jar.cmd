@echo off
setlocal
set script="%~dp0%string_in_jar.py"
python %script% %*
endlocal
