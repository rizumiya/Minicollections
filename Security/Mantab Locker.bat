@echo off
title Folder Locker

REM Mendapatkan waktu saat ini
for /F "tokens=1-2 delims=: " %%a in ("%TIME%") do (
    set "hour=%%a"
    set "minute=%%b"
)

REM Membentuk kata kunci dari waktu HH:MM
set "lock_key=%hour%%minute%"

REM Menampilkan waktu dan kata kunci
echo Waktu saat ini: %hour%:%minute%
echo Kata kunci: %lock_key%

:menu
cls
echo =============== Folder Locker ===============
echo.
echo 1. Kunci Folder
echo 2. Buka Folder
echo 3. Keluar
echo.
set /p choice=Masukkan pilihan (1-3): 

if "%choice%"=="1" goto lock
if "%choice%"=="2" goto unlock
if "%choice%"=="3" goto exit

:lock
cls
echo =============== Kunci Folder ===============
echo.
set /p folder=Masukkan path folder yang ingin dikunci: 
echo.

echo attrib +h +s "%folder%" >> "%temp%\lock.bat"
echo echo Folder dikunci! >> "%temp%\lock.bat"

start /min "" cmd /c "%temp%\lock.bat"
timeout /t 2 >nul
del "%temp%\lock.bat"

echo.
echo Folder telah dikunci!
pause
goto exit


:unlock
cls
echo =============== Buka Folder ===============
echo.
set /p folder=Masukkan path folder yang ingin dibuka: 
echo.
set /p password=Masukkan kata kunci: 

if "%password%"=="%lock_key%" (
    echo attrib -h -s "%folder%" > "%temp%\unlock.bat"
    echo echo Folder dibuka! >> "%temp%\unlock.bat"

    start /min "" cmd /c "%temp%\unlock.bat"
    timeout /t 2 >nul
    del "%temp%\unlock.bat"

    echo.
    echo Folder telah dibuka!
) else (
    echo.
    echo Kata kunci yang Anda masukkan salah!
    echo Folder tidak dapat dibuka.
)
pause
goto exit

:exit
exit
