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
    "Serial_No": 12345,
    "GRE_Score": 140,
    "TOEFL_Score": 20,
    "University_Rating": 5,
    "SOP": 3.0,
    "LOR": 1.0,
    "CGPA": 3.0,  ##this one is highly weighted
    "Research": 0
}

good_data = {
    "Serial_No": 12545,
    "GRE_Score": 340,
    "TOEFL_Score": 110,
    "University_Rating": 5,
    "SOP": 5.0,
    "LOR": 5.0,
    "CGPA": 9.0,
    "Research": 0
}

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



def get_jwt_token(credentials):
    lr = requests.post(
        login_url,
        headers={"Content-Type": "application/json"},
        json=credentials
    )
    if lr.status_code == 200:
        tk = lr.json().get("token")
        print("Token JWT :", tk)
        return tk, lr.status_code
    else:
        print(lr.status_code)
        return None,lr.status_code

def make_prediction_with_token(credentials, result=None, token=None):
    if result is None:
        raise ValueError("Put a valid data json for prediction")
    lr = requests.post(
        login_url,
        headers={"Content-Type": "application/json"},
        json=credentials
    )
    if lr.status_code == 200:
        tk = lr.json().get("token")
        print("Token JWT :", tk)
        qr = requests.post(
            predict_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            json=result
        )

        print("The response to the prediction:", qr.text)

    else:
        print(lr.status_code)
        print(f"Some stupidity with login at the {lr.url} with a status code {lr.status_code} ")

    return tk, lr.status_code , qr.status_code




## Tests based on the JWT
# JWT Authentication Test:
#
# Verify that authentication fails if the JWT token is missing or invalid.
# Verify that authentication fails if the JWT token has expired.
# Verify that authentication succeeds with a valid JWT token.

#The first 3 tests are stupid as I just took the DS teams code and that code is crap so I will simulate a bad token

def test_something(credentials=good_credentials, data=good_data):
    a,b,c = make_prediction_with_token(credentials, data)
    assert b==200, f"Expected 200 but got {b}"



def test_good_credentials(credentials=good_credentials):
    a,b = get_jwt_token(credentials)
    assert b==200 , f"Expected 200 but got {b}"

def test_bad_credentials(credentials=bad_credentials):
    a,b = get_jwt_token(credentials)
    assert b!=200 , f"Did not Expect 200 but got {b}" ## Too lazy to check what was the bad status code done by DAtascentest
