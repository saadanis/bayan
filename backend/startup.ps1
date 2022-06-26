py -m pip install --user virtualenv
py -m venv env
.\env\Scripts\activate
py -m pip install -r requirements.txt --no-cache-dir
$env:FLASK_APP = "./index.py"
flask run -p 8000