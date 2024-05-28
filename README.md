## About
Python Service Boilerplate

## Installation
```bash
pip install virtualenv
virtualenv -p python3.11 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
uvicorn main:app --reload --host {HOST} --port {PORT}
```
<i>Note: use command above if you want to hot reload</i><br />
or

```bash
python main.py
```

## Generator
```bash
python generator.py
```

## Author
<a href="https://github.com/kiritoo9">kiritoo9</a>

## Version
1.1