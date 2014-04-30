:: command to build huge Vim with OLE, Python, Lua

@echo off

:: following vars only available in this bat file
setlocal

set SDK_INCLUDE_DIR=C:\Program Files (x86)\Microsoft SDKs\Windows\v7.1A\Include

:: build GUI version
nmake -f Make_mvc.mak FEATURES=HUGE MBYTE=yes CSCOPE=yes SNIFF=no NETBEANS=no CPUNR=pentium4 DEBUG=no MAP=yes PYTHON=C:\Python27 PYTHON_VER=27 DYNAMIC_PYTHON=yes LUA=C:\LUA LUA_VER=52 DYNAMIC_LUA=yes USERNAME="Liang Feng <liang.feng98 AT gmail DOT com>" USERDOMAIN=China GUI=yes OLE=yes IME=yes GIME=yes %*

:: build console version
nmake -f Make_mvc.mak FEATURES=HUGE MBYTE=yes CSCOPE=yes SNIFF=no NETBEANS=no CPUNR=pentium4 DEBUG=no MAP=yes PYTHON=C:\Python27 PYTHON_VER=27 DYNAMIC_PYTHON=yes LUA=C:\LUA LUA_VER=52 DYNAMIC_LUA=yes USERNAME="Liang Feng <liang.feng98 AT gmail DOT com>" USERDOMAIN=China %*

if "%1" == "clean" goto :End

:: Copy any new Vim exe & runtime files to current install.
set SRC="C:\Users\liangfeng\personal\projects\download\vim_src"
set DST="C:\Program Files (x86)\Vim\vim74"

xcopy %SRC%\runtime %DST% /D /E /H /I /Y
xcopy %SRC%\src\xxd\xxd.exe %DST%\* /D /Y
xcopy %SRC%\src\*.exe %DST%\* /D /Y
xcopy %SRC%\src\*.pdb %DST%\* /D /Y
xcopy %SRC%\src\*.map %DST%\* /D /Y
REM  xcopy %SRC%\src\GvimExt\gvimext.dll %DST%\* /D /Y

:End

endlocal
