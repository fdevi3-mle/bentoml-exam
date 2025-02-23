import os
#  Warnings
import warnings
from typing import Annotated

import bentoml
from bentoml import bentos
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import RandomizedSearchCV
from zenml import step
from zenml.integrations.bentoml.steps import bento_builder_step

warnings.filterwarnings('ignore')
# Set random state
random_state = 42
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


##I assume you want to load the csv but
@step
def train_model_bento(X_train, X_test, y_train, y_test)->Annotated[RandomForestRegressor,"RandomForestRegressorBento"]:

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

    bento_model = bentoml.sklearn.save_model(
        "admission_model",
        best_est,
        custom_objects={
            "feature_names": X_train.columns.tolist(),
            "target_name": "Chance of Admit"
        },
        metadata={
            "version": "v1",
            "best_params": random_search.best_params_,
            "best_score": random_search.best_score_
        }
    )
    return best_est