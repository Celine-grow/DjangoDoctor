DjangoDoctor
This is a Django-based backend system for doctors that supports one-way messaging to patients and integrates with an external cost prediction model for treatment estimation.

⚠️ Note: This application has strict version requirements due to dependencies like pycaret. It is highly recommended to use Python 3.11.0, which can be installed using pyenv.
👉 Install pyenv instructions

🚀 Setup Instructions
1. Create a Virtual Environment
bash
Copy
Edit
# For Linux/Mac
python3 -m venv venv311

# For Windows
py -m venv venv311
2. Activate the Environment
bash
Copy
Edit
# Windows
.\venv311\Scripts\activate

# Mac/Linux
source venv311/bin/activate
3. Install Core Dependencies
Install core versions first to avoid build issues:

bash
Copy
Edit
pip install numpy==1.24.4 scipy==1.11.4 pandas==2.1.4 scikit-learn==1.4.2
Then install the full requirements:

bash
Copy
Edit
pip install -r requirements.txt
4. Run Migrations
bash
Copy
Edit
python manage.py migrate
💬 Doctor-to-Patient Messaging System
This feature enables doctors to send messages to patients (one-way communication).

✅ How It Works
When a patient registers on the Cystella system (Patient System), they are automatically registered on the Doctor System (patients.html).

Doctors can select a patient and click "Message Patient" to open a messaging interface.

The message is sent to this backend, which forwards it to the Cystella Patient API.

📡 Requirements
Patient System Server (Cystella) must be running to receive and display messages.

If the Cystella server is down, the message will not be delivered (will silently fail or return a server error).

⚙️ API Endpoint Configuration
In the Doctor system’s views.py specifically message_patient view, ensure the api_url uses your local IP address (not 127.0.0.1), for example:

python
Copy
Edit
api_url = 'http://<your-local-ip>:8000/api/auth/receive_message/'
To run the server:

bash
Copy
Edit
python manage.py runserver 0.0.0.0:8000
📊 Model Integration – Cost Prediction
The system integrates with a separate FastAPI-based Cost Prediction Service that provides treatment cost estimations based on selected region and treatment options.

🔗 Setup Requirements
Clone and set up the Cost Prediction repository (as guided in its own README).

Install dependencies, load or train the model, and run the FastAPI service.

You should see output like:

pgsql
Copy
Edit
INFO:     Started server process [15372]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
⚠️ Important
The prediction service must be running for this Django app to successfully request and display cost estimations.

If the model is offline, cost estimation features will not work.

✅ Final Checklist
 Python 3.11.0 installed via pyenv

 Virtual environment set up and activated

 Base dependencies installed (numpy, pandas, etc.)

 requirements.txt installed

 Migrations done

 Patient System running

 Cost Prediction API running

 Local IP configured correctly in views.py
