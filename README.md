# DjangoDoctor
- This application has strict version requirements due to `pycaret`. It is recommended that you use Python version 3.11.0 which can be installed using `pyenv`.
- Find the instructions for installing pyenv [here](https://github.com/pyenv/pyenv)

## Setup process
1. Create virtual environment
``` bash
python3 -m venv venv311
or
py -m venv venv311
or
python -m venv venv311
```

2. Activate the virtual environment
- Windows
``` bash
.\venv311\Scripts\activate
```
- Mac/Linux
``` bash
source venv311/bin/activate
```
3.Then start by installing this,"pip install numpy==1.24.4 scipy==1.11.4 pandas==2.1.4 scikit-learn==1.4.2",To avoid errors of pre compiling builder versions then:
Install dependancies
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
