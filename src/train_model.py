import os
#  Warnings
import warnings
from typing import Annotated

import bentoml
from scipy.stats import loguniform
from sklearn.linear_model import ElasticNetCV
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import RandomizedSearchCV
from zenml import step

warnings.filterwarnings('ignore')
# Set random state
random_state = 42
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


##I assume you want to load the csv but
@step
def train_model_bento(X_train, X_test, y_train, y_test)->Annotated[ElasticNetCV,"admission_model"]:

    #Just use a grid search for the best regresrro
    params = {
        'l1_ratio' :[0.1, 0.5, 0.7, 0.9, 0.95, 0.99, 1.0],
        'n_alphas':[100,200,300,500],
        'max_iter':[1000,2000,3000,5000],
        'cv':[3,5]
    }
    random_search = RandomizedSearchCV(ElasticNetCV(positive=True,fit_intercept=False,random_state=random_state),cv=5,n_jobs=-1,
                                       verbose=2,scoring='neg_mean_squared_error',param_distributions=params,random_state=random_state)
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