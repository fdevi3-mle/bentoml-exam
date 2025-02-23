## BentoML Exam
The exam is divided into two parts (one mandatory and one optional), you will work on a dataset concerning student admissions to universities. This dataset contains information to predict the chance of admission of a student to a university. The variables are as follows:

+ GRE Score: Score obtained on the GRE test (scored out of 340)
+ TOEFL Score: Score obtained on the TOEFL test (scored out of 120)
+ University Rating: University rating (scored out of 5)
+ SOP: Statement of Purpose (scored out of 5)
+ LOR: Letter of Recommendation (scored out of 5)
+ CGPA: Cumulative Grade Point Average (scored out of 10)
+ Research: Research experience (0 or 1)
+ Chance of Admit: Chance of admission (scored out of 1)
For the mandatory part 1, you will need to complete the following steps:

## Step 1
Prepare your work environment and load the data.
Create a linear regression model and test its performance.
Set up a prediction API.
Create a bento & containerization with Docker.
For the optional part 2 (which is absolutely not required for the validation of this exam), you will need to use bentoml to implement a deployment case using multiple runners. The only purpose of this part is to allow you to practice freely while enabling you to create a real architecture.

Part 1: Mandatory Part
1.1. Preparing the Work Environment
Retrieving the Work Repository
First, to properly start the project, you will need to retrieve the basic architecture. To do this, you need to fork the repository at: https://github.com/DataScientest-Studio/examen_bentoml

Once you have forked the repository, you can clone the repository to your machine. You will then have a folder containing the following structure:

├── examen_bentoml          
│   ├── data       
│   │   ├── processed      
│   │   └── raw           
│   ├── models      
│   ├── src       
│   └── README.md
Loading the Data
Now, you will need to load the data into the data/raw folder. For this, you should use the following link: https://assets-datascientest.s3.eu-west-1.amazonaws.com/MLOPS/bentoml/admission.csv

Creating the Virtual Environment
To work properly, set up a virtual environment that you will name according to your choice. This will allow you to work in an isolated environment and not disturb your Python installation.

1.2. Creating the Model
In this part, you will need to complete the steps of data preparation, modeling, and model performance evaluation. As you have seen in your courses, you will need to split the data into a training set and a test set, normalize the data if necessary, create a regression model to address the problem posed at the beginning of the notebook before finally evaluating the model's performance.

Data Preparation
Create a Python script prepare_data.py in the src folder that loads the data, cleans it, and divides it into a training set and a test set. You can use the pandas and scikit-learn libraries for this.

The target variable in the initial dataset is Chance of Admit, feel free to remove variables that you logically judge unnecessary for your modeling.

Following this, you should obtain the following files: X_test, X_train, y_test, y_train and save them in the data/processed folder.

Modeling
Once your datasets are cleaned and ready for modeling, you can create a regression model of your choice to predict the target variable.

Create a Python script train_model.py in the src folder that loads the training data, creates a regression model, and trains it.

After training your model on the training data, test and display its performance on the test data. You can use the metric of your choice (R2, RMSE, MAE, ...).

Finally, if your model's performance is satisfactory following the successive tests you will have done, you must save your model in the BentoML Model Store.

After saving, verify that your model is properly registered using the appropriate BentoML command.

1.3. Setting up the Prediction API
During this step, you will create a prediction API that will predict the chance of admission of a student to a university.

For this, create a Python script service.py in the src folder that loads the saved model, creates a secure prediction API, and launches it through the BentoML service.

The API must be accessible via an HTTP POST request on a port of your machine. It must take as input all the variables necessary for prediction and return the prediction of the chance of admission for a student.

Regarding endpoints, you must create a login endpoint to secure access to the API (you are free to choose the security method you want) and an endpoint named predict to make predictions, but you are not limited to a single endpoint if you want to add other interesting features to your API.

Don't forget to test your API by doing inference on test data of your choice.

1.4. Creating a bento & containerization with Docker
In this final step, you will create a bento that will contain your model and your API. You will then need to containerize this bento with Docker.

As you have seen in the courses, a bento is an archive of files containing all the source code for your model training and the APIs you have defined to serve it, the saved binary models, data files, Dockerfiles, dependencies, and additional configurations.

To create a bento, you must first create a bentofile.yaml file at the root of your project. This file will contain the information mentioned above. Don't forget to properly specify the folders or files to include in your bento.

Here is an example of a bentofile.yaml for reference (don't copy this code as is, adapt it to your project, it won't work otherwise):

service: 
  name: admissions_prediction
  version: 1.0.0
labels:
  owner: "DataScientest"
  project: "Admissions Prediction"
    description: "Predict the chance of admission of a student in a university"
include:
  - '*.py'
python:
    packages:
      - scikit-learn
      - pandas
Finally, use the BentoML commands we saw in class to containerize your bento and create a Docker image that will contain your model and your API.

Don't forget to test your Docker image by running it locally and making requests to your API.

When you are finished, you will need to compress your Docker image and make it available for evaluation. For this, you can use the following command:

# BE CAREFUL to respect the naming convention below
docker save -o bento_image.tar <your_name>_<your_image_name>
⚠️⚠️⚠️ To respect this naming convention <your_name>_<your_image_name>, you will need to be careful to properly configure your bentoml service. Incorrect naming may result in evaluation failure.

1.5. Unit Tests
To test the proper functioning of the service created in part 4, you must write unit tests. Here are some essential unit tests you can perform:

