python app.py
python3 -m venv xfiv-edificio-python
sleep 5
source xfiv-edificio-python/bin/activate
pip install -r requirements.txt
sleep 5
uvicorn index:app --reload --host 0.0.0.0 --port 3003 --workers 1