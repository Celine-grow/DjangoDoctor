# DjangoDoctor
- This application has strict version requirements due to `pycaret`. It is recommended that you use Python version 3.11.0 which can be installed using `pyenv`.
- Find the instructions for installing pyenv [here](https://github.com/pyenv/pyenv)

## Setup process
1. Create virutal environment
``` bash
python3 -m venv venv
```

2. Activate the virtual environment
- Windows
``` bash
venv\Scripts\activate
```
- Mac/Linux
``` bash
source venv/bin/activate
```

3. Install dependancies
``` bash
pip3 install -r requirements.txt
```

4. Perform migrations
``` bash
python3 manage.py migrate
```

4. Run application
``` bash
python3 manage.py runserver
```
