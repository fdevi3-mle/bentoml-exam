import requests
import os

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(CURRENT_PATH,'data')
PROCESSED_PATH = os.path.join(DATA_PATH,'processed')
RAW_PATH = os.path.join(DATA_PATH,'raw')
SRC_PATH = os.path.join(CURRENT_PATH,'src')
MODEL_PATH = os.path.join(CURRENT_PATH,'models')

ADMISSION_FILENAME = 'admission.csv'
CSV_PATH = os.path.join(RAW_PATH,ADMISSION_FILENAME)
FEATURES = ['Serial No.', 'GRE Score', 'TOEFL Score', 'University Rating', 'SOP',
       'LOR ', 'CGPA', 'Research', 'Chance of Admit ']

CSV_URL = 'https://assets-datascientest.s3.eu-west-1.amazonaws.com/MLOPS/bentoml/admission.csv'

def get_data(data_path=CURRENT_PATH, filename=ADMISSION_FILENAME, url=CSV_URL):
    print(f"Downloading file{filename} from {url}")
    filepath = os.path.join(RAW_PATH,filename)
    response = requests.get(url)
    if response.status_code == 200:
        with open(filepath, 'wb') as file:
            file.write(response.content)
    else:
        print(f'Error accessing the object {url}:', response.status_code)
    return filepath

def get_csv_path():
    if os.path.exists(CSV_PATH):
        return CSV_PATH
    else:
        return get_data()


if __name__=="__main__":
    print(get_csv_path())