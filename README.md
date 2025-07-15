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


Extra Information

1.Doctor-to-Patient Messaging System
This feature allows doctors to send messages to individual patients. The implementation is one-way only:
🔒 Patients cannot message each other, or message doctors — only receive messages.

✅ How it Works
Doctors select a patient from the dashboard and click “Chat”.

They are directed to the messaging interface where they can write and send messages.

The message is sent to the backend, then forwarded to the Patient System's API endpoint for that user.

📡 Requirements
Patient System Server Must Be Running

The Patient System  must be actively running. i.e cystella 

Otherwise, the message cannot be delivered to the patient and will fail silently or return a server error.

Correct API Endpoint Configuration

In the Doctor System’s views.py, make sure the messaging API i.e message_patient  api_url endpoint uses your local IP address (not 127.0.0.1):
api_url = 'http://<your-local-ip>:8000/api/auth/receive_message/'
For example:

Start the Doctor Backend Server:

python manage.py runserver 0.0.0.0:8000
Send a message as a doctor and confirm:

Message appears in the patient message list.

No errors appear in either server console.

2.Model Intergration

💡 Cost Prediction Integration
This system integrates with a separate Cost Prediction Model service to generate treatment cost estimates based on selected region and treatment options.

🔗 Prerequisite Setup
To enable the cost prediction functionality in this app, you must first:

Clone and set up the Cost Prediction Model service
Follow the setup instructions in the Cost Prediction Repository  — it includes steps to:

Install dependencies

Load or train the machine learning model

Run the FastAPI service

Start the prediction model API server
Once you have followed all the guidelines there ,your server will be up and running something like,
INFO: Started server process [15372]
INFO: Waiting for application startup.
INFO: Application startup complete.
INFO: Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO: 127.0.0.1:50132 - "POST /generate_report HTTP/1.1" 422 Unprocessable Entity
INFO: 127.0.0.1:50143 - "POST /generate_report HTTP/1.1" 200 OK”


⚠️ Important: The prediction service must be running for the doctor system to successfully make cost estimation requests.
