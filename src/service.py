#  Warnings
import warnings
from datetime import datetime, timedelta

import bentoml
import jwt
import numpy as np
from bentoml.io import JSON
from pydantic import BaseModel, Field
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

warnings.filterwarnings('ignore')

# Secret key and algorithm for JWT authentication
JWT_SECRET_KEY = "bob"
JWT_ALGORITHM = "HS256"

# User credentials for authentication
USERS = {
    "bob": "builder",
    "test": "test"
}

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path == "/v1/models/admission_service/predict":
            token = request.headers.get("Authorization")
            if not token:
                return JSONResponse(status_code=401, content={"detail": "Missing authentication token"})

            try:
                token = token.split()[1]  # Remove 'Bearer ' prefix
                payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            except jwt.ExpiredSignatureError:
                return JSONResponse(status_code=401, content={"detail": "Token has expired"})
            except jwt.InvalidTokenError:
                return JSONResponse(status_code=401, content={"detail": "Invalid token"})

            request.state.user = payload.get("sub")

        response = await call_next(request)
        return response


# ['Serial No.', 'GRE Score', 'TOEFL Score', 'University Rating', 'SOP',
#  'LOR ', 'CGPA', 'Research', 'Chance of Admit ']
##TODO convert to literal
# Pydantic model to validate input data
class AdmissionModel(BaseModel):
    GRE_Score: float = Field(description="GRE Score",ge=0,le=340)
    TOEFL_Score: float = Field(description="TOEFL Score",ge=0,le=120)
    University_Rating: float = Field(description="University Ranking")
    SOP: float = Field(description="Statement of Purpose",ge=0,le=5)
    LOR: float = Field(description="Letter of Recommendation",ge=0,le=5)
    CGPA: float = Field(description="Cumulative GPA",ge=0,le=10)
    Research: int = Field(description="Cumulative GPA",ge=0,le=1)


# Load the model from Model Store
admission_model_runner = bentoml.sklearn.get("admission_model:latest").to_runner()

# Create service API
admission_service = bentoml.Service("admission_service", runners=[admission_model_runner])

# Add JWT authentication middleware
admission_service.add_asgi_middleware(JWTAuthMiddleware)

# Create an API endpoint for the service
@admission_service.api(input=JSON(), output=JSON())
def login(credentials: dict) -> dict:
    username = credentials.get("username")
    password = credentials.get("password")

    if username in USERS and USERS[username] == password:
        token = create_jwt_token(username)
        return {"token": token}
    else:
        return JSONResponse(status_code=401, content={"detail": "Invalid credentials"})

# Create an API endpoint for the service
@admission_service.api(
    input=JSON(pydantic_model=AdmissionModel),
    output=JSON(),
    route='v1/models/admission_service/predict'
)

async def predict(input_data: AdmissionModel, ctx: bentoml.Context) -> dict:
    request = ctx.request
    user = request.state.user if hasattr(request.state, 'user') else None

    # Convert input data to numpy array in correct order
    # also scale it , its a very crude scaler that takes the max value only
    input_series = np.array([
        input_data.GRE_Score/340,
        input_data.TOEFL_Score/120,
        input_data.University_Rating/5,
        input_data.SOP/5,
        input_data.LOR/5,
        input_data.CGPA/10,
        input_data.Research,
    ])
    print(input_series)

    result = await admission_model_runner.predict.async_run(input_series.reshape(1, -1))

    return {
        "prediction": result.tolist(),
        "user": user
    }

# Function to create a JWT token
def create_jwt_token(user_id: str):
    expiration = datetime.utcnow()  + timedelta(hours=1)
    payload = {
        "sub": user_id,
        "exp": expiration
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token