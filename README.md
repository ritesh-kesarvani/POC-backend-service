# POC-backend-service

This repository contains a Proof of Concept (POC) backend service built with Python.

## Prerequisites

1. Python 3.x installed on your system
2. pip available in your PATH

## Setup Instructions

Follow the steps below to set up and run the service locally.

1. Create a virtual environment using the following command:

```
python -m venv <env name>
```

2. Activate the Virtual Environment

```
<env name>\Scripts\activate
```

3. Install the required Python packages:

```
pip install -r requirements.txt
```

4. Create a .env file by copying the provided example file:

```
copy .env.example .env
```

5. Open the .env file and fill in the required database configuration details as per your environment.

6. Start the backend service using the following command:

```
python application/app.py
```

7. The service should now be running successfully.
8. You can hit the below endpoint to check if the service is running fine or not

```
http://127.0.0.1:5000/healthcheck
```

### Notes: Ensure the virtual environment is activated before running the application.
