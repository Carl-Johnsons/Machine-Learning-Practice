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

mkdir data
:: creating install_python_virtual_environment.bat
(
    echo @echo off
	echo echo creating python virtual environment
	echo python -m venv venv
	echo echo created successfully
) > install_python_virtual_environment.bat
:: creating requirements.txt
(
    echo # You need to access to the python virtual environment in order to run python notebook
    echo # .\venv\Scripts\activate.bat
    echo # pip install -r requirements.txt 
    echo tensorflow
    echo numpy
    echo matplotlib
    echo pandas
	echo ipython 
	echo ipykernel
) > requirements.txt
:: creating install_requirements.bat
(
    echo @echo off
    echo call .\venv\Scripts\activate.bat
    echo python.exe -m pip install --upgrade pip
    echo pip install -r requirements.txt
) > install_requirements.bat

:: creating install_all.bat
(
    echo @echo off
    echo call .\install_python_virtual_environment.bat
    echo call .\install_requirements.bat
    echo echo installed successfully
) > install_all.bat
call .\install_all.bat
call :CreateJupyterNotebook

EXIT /B 0

:CreateJupyterNotebook
mkdir notebook
cd .\notebook
(
    echo ^{
    echo "cells": ^[
    echo ^{
    echo "cell_type": "markdown",
    echo "metadata": ^{^},
    echo "source": ^[
    echo    "## Test"
    echo ^]
    echo ^},
    echo ^{
    echo "cell_type": "markdown",
    echo "metadata": ^{^},
    echo "source": ^[
        echo "## 1. Importing module"
    echo ^]
    echo ^},
    echo ^{
    echo "cell_type": "code",
    echo "execution_count": null,
    echo "metadata": ^{^},
    echo "outputs": ^[^],
    echo "source": ^[
        echo "import tensorflow as tf"
    echo ^]
    echo ^},
    echo ^{
    echo "cell_type": "markdown",
    echo "metadata": ^{^},
    echo "source": ^[
        echo "## 2. Test the tensorflow version"
    echo ^]
    echo ^},
    echo ^{
    echo "cell_type": "code",
    echo "execution_count": null,
    echo "metadata": ^{^},
    echo "outputs": ^[^],
    echo "source": ^[
        echo "print(tf.__version__)"
    echo ^]
    echo ^}
    echo ^],
    echo "metadata": ^{
    echo "kernelspec": ^{
    echo "display_name": "venv",
    echo "language": "python",
    echo "name": "python3"
    echo ^},
    echo "language_info": ^{
    echo "codemirror_mode": ^{
        echo "name": "ipython",
        echo "version": 3
    echo ^},
    echo "file_extension": ".py",
    echo "mimetype": "text/x-python",
    echo "name": "python",
    echo "nbconvert_exporter": "python",
    echo "pygments_lexer": "ipython3",
    echo "version": "3.11.0"
    echo ^}
    echo ^},
    echo "nbformat": 4,
    echo "nbformat_minor": 2
    echo ^}
) > %ProjectName%.ipynb
cd ..
EXIT /B 0