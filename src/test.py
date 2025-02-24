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
# Secret key and algorithm for JWT authentication
JWT_SECRET_KEY = "hacker"
JWT_ALGORITHM = "HS256"


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

    # Data to be sent to the prediction endpoint
    data = {
        "Serial_No": 12345,
        "GRE_Score": 140,
        "TOEFL_Score": 20,
        "University_Rating": 5,
        "SOP": 5.0,
        "LOR": 5.0,
        "CGPA": 9.0, ##this one is highly weighted
        "Research": 0
    }

    # Send a POST request to the prediction
    response = requests.post(
        predict_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        json=data
    )

    print("Réponse de l'API de prédiction:", response.text)
else:
    print("Erreur lors de la connexion:", login_response.text)


# Function to create a JWT token
def create_jwt_token(user_id: str):
    expiration = datetime.utcnow()  + timedelta(hours=1)
    payload = {
        "sub": user_id,
        "exp": expiration
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def create_bad_jwt_token(user_id: str):
    expiration = datetime.utcnow()  + timedelta(seconds=1)
    payload = {
        "sub": user_id,
        "exp": expiration
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


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

## Tests based on the JWT
# JWT Authentication Test:
#
# Verify that authentication fails if the JWT token is missing or invalid.
# Verify that authentication fails if the JWT token has expired.
# Verify that authentication succeeds with a valid JWT token.

def test_jwt_authentication_invalid_token():
    # Simulate a valid JWT token
    username = bad_credentials.get("username")
    token = create_jwt_token(username)
    response = requests.get(
        login_url,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code != 200, f" not Expected 200, but got {response.status_code}"

def test_jwt_authentication_valid_token():
    # Simulate a valid JWT token
    username = good_credentials.get("username")
    token = create_jwt_token(username)
    response = requests.get(
        login_url,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, f" not Expected 200, but got {response.status_code}"



def test_good_credentials(credentials=good_credentials):
    a,b = get_jwt_token(credentials)
    assert b==200 , f"Expected 200 but got {b}"

def test_bad_credentials(credentials=bad_credentials):
    a,b = get_jwt_token(credentials)
    assert b!=200 , f"Did not Expect 200 but got {b}" ## Too lazy to check what was the bad status code done by DAtascentest
