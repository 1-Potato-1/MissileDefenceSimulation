python -m venv venv
call venv\Scripts\activate
pip install poetry==1.0.0
pip install PyInstaller==4.3
poetry install
REM opencv has conflicting dependencies, so can't complete conflict resolution
pip3 install opencv-python

python main.py parameters.json

deactivate