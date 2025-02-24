import requests

# The URL of the login and prediction endpoints
login_url = "http://127.0.0.1:3000/login"
predict_url = "http://127.0.0.1:3000/v1/models/admission_predictor/predict"

# Données de connexion
credentials = {
    "username": "test",
    "password": "test"
}

# Send a POST request to the login endpoint
login_response = requests.post(
    login_url,
    headers={"Content-Type": "application/json"},
    json=credentials
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
