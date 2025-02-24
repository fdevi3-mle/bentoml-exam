import os
#  Warnings
import warnings
from typing import Tuple, Annotated

import pandas as pd
from AutoClean import AutoClean
from sklearn.model_selection import train_test_split
from zenml import step

from utils import CSV_PATH, PROCESSED_PATH, get_csv_path

warnings.filterwarnings('ignore')
# Set random state
random_state = 42
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'



@step
def bento_data_loader()->Annotated[pd.DataFrame, "bento_raw_data"]:
    filepath = CSV_PATH
    if not os.path.exists(filepath):
        filepath = get_csv_path
    data = pd.read_csv(filepath,index_col='Serial No.')
    print(data.head(1))
    return data

@step
def bento_data_processor(data)->Annotated[pd.DataFrame,"bento_processed_data"]:
    pipeline = AutoClean(data, mode='auto', duplicates=True, missing_num='auto',  outliers=False, outlier_param=1.5, verbose=True)
    processed_data = pipeline.output
    print(processed_data.columns)
    return processed_data



@step
def bento_data_splitter(data)->Tuple[Annotated[pd.DataFrame, "X_train_bento"],Annotated[pd.DataFrame, "X_test_bento"],Annotated[pd.Series, "y_train_bento"],
Annotated[pd.Series,"y_test_bento"]]:
    y = data['Chance of Admit '] #nice job adding a dumb space
    X = data.drop(['Chance of Admit '], axis=1)

    scaler_features = ['GRE Score', 'TOEFL Score','University Rating', 'SOP',
       'LOR ', 'CGPA']
    values = [340,120,5,5,5,10]

    mapping = dict(zip(scaler_features,values))
    for key,value in mapping.items():
        X[key] = X[key]/value

    #split then scale
    X_train,X_test,y_train,y_test = train_test_split(X, y, test_size=0.2,
                                                        random_state=random_state)
    # #scaler
    # scaler = MinMaxScaler()
    # scaler_features = ['GRE Score', 'TOEFL Score', 'University Rating', 'SOP',
    #    'LOR ', 'CGPA'] ## one coudl consider Univers rating and sop as cat but whateverr
    # X_train[scaler_features] = scaler.fit_transform(X_train[scaler_features])
    # X_test[scaler_features] = scaler.transform(X_test[scaler_features])




    #Research is already encoded so let it be
    print(X_train.head(1))

    #save to file
    dic = {'X_train.csv':X_train,'X_test.csv':X_test,'y_train.csv':y_train,'y_test.csv':y_test}
    for key,value in dic.items():
        filepath = os.path.join(PROCESSED_PATH,key)
        value.to_csv(filepath,index=False)
    return X_train,X_test,y_train,y_test

