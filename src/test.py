import json
from datetime import datetime, timedelta
from typing import Tuple

import jwt
import requests
import pytest
# The URL of the login and prediction endpoints
login_url = "http://127.0.0.1:3000/login"
predict_url = "http://127.0.0.1:3000/v1/models/admission_predictor/predict"

# Données de connexion
good_credentials = {
    "username": "test",
    "password": "test"
}
bad_credentials = {
    "username": "hacker",
    "password": "hacker"
}

poor_data = {
    "GRE_Score": 140,
    "TOEFL_Score": 80,
    "University_Rating": 5,
    "SOP": 3.0,
    "LOR": 1.0,
    "CGPA": 3.0,  ##this one is highly weighted
    "Research": 1
}

good_data = {
    "GRE_Score": 340,
    "TOEFL_Score": 110,
    "University_Rating": 5,
    "SOP": 5.0,
    "LOR": 5.0,
    "CGPA": 9.0,
    "Research": 1
}

bad_data = {
    "GRE_Score": 340,
    "TOEFL_Score": 110,
    "University_Rating": "Ola, Como estas",
    "Research": 1
}


#EXPIRED
EXPIRED_TOKEN='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNzQwNDI2NDgwfQ.bK6YLIyjqzl_NSqyHely44ajn2RR9na0ASH0o-B7J-M'

# Send a POST request to the login endpoint
login_response = requests.post(
    login_url,
    headers={"Content-Type": "application/json"},
    json=good_credentials
)

# Check if the login was successful
if login_response.status_code == 200:
    token = login_response.json().get("token")
    print("Token JWT :", token)

    # Send a POST request to the prediction
    response = requests.post(
        predict_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        json=good_data
    )

    print("The response to the prediction:", response.text)
else:
    print(login_response.status_code)
    print(login_response.content)
    print(login_response.url)
    print(f"Some stupidity with login at the {login_response.url} with a status code {login_response.status_code} ")
