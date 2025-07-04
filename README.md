cd MergePD
git clone 
python -m venv venv
./venv/Scripts/activate
pip install sentencepiece-0.2.0-cp312-cp312-win_amd64.whl
pip install -r requirements.txt
python app.py
switch to http://127.0.0.1:5500/
