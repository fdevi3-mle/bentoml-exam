from typing import Tuple,Annotated
import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from zenml import step, ArtifactConfig
from zenml.logger import get_logger
#  Warnings
import warnings
from AutoClean import AutoClean

from utils import CSV_PATH, PROCESSED_PATH, get_data, get_csv_path

warnings.filterwarnings('ignore')
# Set random state
random_state = 42
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


##I assume you want to load the csv but
@step
def train_model_bento(X_train, X_test, y_train, y_test):

    #Just use a grid search for the best regresrro
    params = {
        'n_estimators': [100, 200, 300],
        'max_depth': [2, 5,10],
        'max_features': ['auto', 'sqrt']
    }
    random_search = RandomizedSearchCV(RandomForestRegressor(random_state=random_state),cv=3,n_jobs=-1,
                                       verbose=2,scoring='neg_mean_squared_error',param_distributions=params)
    random_search.fit(X_train, y_train)
    print(f"The best parameters: {random_search.best_params_}")

    best_est = random_search.best_estimator_
    y_pred = best_est.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test,y_pred)

    print(f"R-squared Score {r2}")
    print(f"Mean Squared Erros {mse}")
    print(f"Mean Absolute Error {mae}")