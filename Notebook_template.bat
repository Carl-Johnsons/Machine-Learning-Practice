@echo off
:: for input within the if block
setlocal enabledelayedexpansion

:: input project name
set /p ProjectName="Project name: "

IF EXIST .\%ProjectName%  (
    set /p answer="Directory %ProjectName% is existed. Delete this directory? (y/n) "

    :: use !! instead of %% to use variable delayed expansion
    IF "!answer!" == "y" (
        :: /Q to not ask any question
        rmdir /S /Q .\%ProjectName%
        echo delete existed %ProjectName% successfully
        call :CreateDirectory
    ) ELSE IF "!answer!" == "n" (
        echo Aborting operation
    ) ELSE ( 
        echo Invalid input 
    )
) ELSE (
    call :CreateDirectory
)

EXIT /B %ERRORLEVEL% 

:CreateDirectory
mkdir %ProjectName%
echo creating %ProjectName% directory successfully
cd .\%ProjectName%
:: creating jupyter notebook
mkdir notebook
cd .\notebook
echo. > %ProjectName%.ipynb
cd ..
:: creating requirements.txt
mkdir data
(
    echo # You need to access to the python virtual environment in order to run python notebook
    echo # .\venv\Scripts\activate.bat
    echo # pip install -r requirements.txt 
    echo tensorflow
    echo numpy
    echo matplotlib
    echo pandas
) > requirements.txt
:: creating install_requirements.bat
(
    echo @echo off
	echo echo creating python virtual environment
	echo python -m venv venv
	echo echo created successfully
    echo call .\venv\Scripts\activate.bat
    echo python.exe -m pip install --upgrade pip
    echo pip install -r requirements.txt
    echo exit
) > install_requirements.bat


echo installing default python package for virtual environment
call .\install_requirements.bat
echo installed successfully

pause
EXIT /B 0