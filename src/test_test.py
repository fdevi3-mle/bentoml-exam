import json
from datetime import datetime, timedelta
from typing import Tuple

import jwt
import requests
import pytest
# The URL of the login and prediction endpoints
login_url = "http://127.0.0.1:3000/login"
predict_url = "http://127.0.0.1:3000/v1/models/admission_service/predict"


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

def make_prediction_with_token(query=None, token=None):
    if query is None:
        raise ValueError("Put a valid data json for prediction")
    qr = requests.post(
            predict_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            json=query
        )

    print("The response to the prediction:", qr.text)
    if qr.status_code!=200:
        print(qr.status_code)
    return token, qr




## Tests based on the JWT
# JWT Authentication Test:
#
# Verify that authentication fails if the JWT token is missing or invalid.
# Verify that authentication fails if the JWT token has expired.
# Verify that authentication succeeds with a valid JWT token.

# Login API Test:
#
# Verify that the API returns a valid JWT token for correct user credentials.
# Verify that the API returns a 401 error for incorrect user credentials.

#
# Prediction API Test:
#
# Verify that the API returns a 401 error if the JWT token is missing or invalid.
# Verify that the API returns a valid prediction for correct input data.
# Verify that the API returns an error for invalid input data.

#The first 3 tests are stupid as I just took the DS teams code and that code is crap so I will simulate a bad token

def test_good_token(credentials=good_credentials, data=good_data):
    ##generate token
    _token, status_code = get_jwt_token(credentials)
    t,qr = make_prediction_with_token(token=_token, query=data)
    assert qr.status_code==200, f"Expected 200 but got {qr.status_code}"

def test_token_missing(credentials=good_credentials, data=good_data):
    ##generate token
    _token, status_code = get_jwt_token(credentials)
    t,qr = make_prediction_with_token(token=None, query=data)
    assert qr.status_code ==401, f"Expected 401 but got {qr.status_code}"

def test_token_expired(credentials=good_credentials, data=good_data):
    ##generate token
    _token, status_code = get_jwt_token(credentials)
    t,qr = make_prediction_with_token(token=EXPIRED_TOKEN, query=data)
    assert qr.status_code ==401, f"Expected 401 but got {qr.status_code}"

# Login API Test:
## for some reason I need to query the "predict url" probably cause the authentication only happens at post at the predictions req
## Really bad design from DS , a simpler way is to look at FastAPI authentication,
## I am not doing it cause its a waste of time to redesign the whole service.py
## Also note that the bento.Service is depreceated showing lack of upkeep from the DS team
def test_good_credentials(credentials=good_credentials, data=good_data):
    ##generate token
    _token, status_code = get_jwt_token(credentials)
    t,qr = make_prediction_with_token(token=_token, query=data)
    assert qr.status_code==200, f"Expected 200 but got {qr.status_code}"


def test_bad_credentials(credentials=bad_credentials, data=good_data):
    ##generate token
    _token, status_code = get_jwt_token(credentials)
    t,qr = make_prediction_with_token(token=_token, query=data)
    assert qr.status_code ==401, f"Expected 401 but got {qr.status_code}"


# Prediction API Test:
#First test is as same as the invalid jwt test, not repeating

#Verify that the API returns a valid prediction for correct input data. --> same as good credentials
def test_good_data(credentials=good_credentials, data=good_data):
    ##generate token
    _token, status_code = get_jwt_token(credentials)
    t,qr = make_prediction_with_token(token=_token, query=data)
    dic = json.loads(qr.text)
    assert dic['prediction'][0] >0.5, f"Expected  > 0.5 but got {dic}"


def test_poor_data(credentials=good_credentials, data=poor_data):
    ##generate token
    _token, status_code = get_jwt_token(credentials)
    t,qr = make_prediction_with_token(token=_token, query=data)
    dic = json.loads(qr.text)
    assert dic['prediction'][0] <=0.5, f"Expected  < 0.5 but got {dic}"

def test_bad_data(credentials=good_credentials, data=bad_data):
    ##generate token
    _token, status_code = get_jwt_token(credentials)
    t,qr = make_prediction_with_token(token=_token, query=data)
    assert qr.status_code == 400, f"Expected 400 but got {qr.status_code}"
