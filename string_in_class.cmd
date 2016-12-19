@echo off
setlocal
set script="%~dp0%string_in_class.py"
python %script% %*
endlocal
