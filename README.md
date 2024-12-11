# RUL-Predictor
Web application that calculates remaining useful life of a system using CMAPPS dataset

CMAPSS : Commercial Modular Aero-Propulsion System Simulation dataset will be used
Each data set is divided into a train and a test set
Each time-series data set is a data set obtained from another engine
A dataset is data from the same type of engine
The four data sets are multivariate time-series data obtained with different operational conditions (ONE, SIX)    and fault modes (ONE, TWO), respectively.
There are three operational settings that affect engine performance
For each test data, RUL (Remaining Useful Life) values are provided
In the training set, the degradation increases until it reaches the predefined threshold, which is deemed bad for operating the engine
In the test set, the time series data is terminated before it is completely degraded
For each data set, there is a column of 26 sensors.
For this project, use all the four train and test sets.
  1.	The user must be able to send sensor data during the operation of the asset and get an estimate of the remaining useful life
 2.	The user must be able to specify the training set to be used to train the model.  By default, this should include the entire training set.
 3.    In addition to this default behavior, the user must be able to specify specific assets to train on by providing unique identifiers for the assets.
 4.	The user must be able to specify the training set to be used to train the model.  By default, this should include the entire training set.
 From the technical point of view, we will setup a web app to serve ML models learned from the CMAPSS dataset, as shown in the figure
 1.	The models must be built using all the four training datasets
 2.	The models must be served using a Flask-based Web app.  It can be stood up locally for this project.
# 3.	The client application must be able to send sensor data to receive the RUL prediction.
