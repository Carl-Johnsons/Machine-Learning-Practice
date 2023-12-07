@echo off
echo creating python virtual environment
python -m venv venv
echo created successfully
call .\venv\Scripts\activate.bat
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
exit
