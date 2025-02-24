from zenml import pipeline
from zenml.client import Client

from src.prepare_data import bento_data_loader, bento_data_processor, bento_data_splitter
from src.train_model import train_model_bento

# Zenml Client
client = Client()
Client().activate_stack(
    "default"
)
@pipeline(enable_cache=True)  # This function combines steps together
def bentoml_pipeline():
    print("Hi")
    dataframe = bento_data_loader()
    processed_data = bento_data_processor(dataframe)
    X_train,X_test,y_train,y_test = bento_data_splitter(processed_data)
    model=train_model_bento(X_train,X_test,y_train,y_test)



if __name__ == "__main__":

    bentoml_pipeline()  # call this to run the pipeline

