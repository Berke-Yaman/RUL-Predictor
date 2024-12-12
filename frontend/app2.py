### To Start The App: From the powershell go
# C:\Users\berke\OneDrive\Masaüstü\DERS DOSYALARI\Masters\TELE 6500\Project\frontend>
# use the line python -m flask --app app2 run --debug 
# then search http://127.0.0.1:5000/index.html on google.

# Importing libraries, modules
from flask import Flask, redirect, url_for, render_template, request, flash
from markupsafe import escape

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import io

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import os

# Creating the app
app = Flask(__name__)
app.secret_key = "SECRET KEY"

# Organizing the raw data
index_names = ['unit_nr', 'time_cycles']
setting_names = ['setting_1', 'setting_2', 'setting_3']
sensor_names = ['s_{}'.format(i) for i in range(1,22)] 
col_names = index_names + setting_names + sensor_names

# Feature Selection
drop_sensors = ['s_1','s_5','s_6','s_9','s_10','s_14','s_16','s_18','s_19']
drop_labels = index_names+setting_names+drop_sensors

# Reading the Data
train = pd.read_csv(('train_FD001.txt'), sep='\s+', header=None, names=col_names)
test = pd.read_csv(('test_FD001.txt'), sep='\s+', header=None, names=col_names)
y_test = pd.read_csv(('RUL_FD001.txt'), sep='\s+', header=None, names=['RUL'])

train1 = pd.read_csv(('train_FD002.txt'), sep='\s+', header=None, names=col_names)
test1 = pd.read_csv(('test_FD002.txt'), sep='\s+', header=None, names=col_names)
y_test1 = pd.read_csv(('RUL_FD002.txt'), sep='\s+', header=None, names=['RUL'])

train2 = pd.read_csv(('train_FD003.txt'), sep='\s+', header=None, names=col_names)
test2 = pd.read_csv(('test_FD003.txt'), sep='\s+', header=None, names=col_names)
y_test2 = pd.read_csv(('RUL_FD003.txt'), sep='\s+', header=None, names=['RUL'])

train3 = pd.read_csv(('train_FD004.txt'), sep='\s+', header=None, names=col_names)
test3 = pd.read_csv(('test_FD004.txt'), sep='\s+', header=None, names=col_names)
y_test3 = pd.read_csv(('RUL_FD004.txt'), sep='\s+', header=None, names=['RUL'])

# Merging data for the default 
default_train = pd.concat([train, train1, train2, train3], ignore_index=True)
default_test = pd.concat([test, test1, test2, test3], ignore_index=True)
default_y_test = pd.concat([y_test, y_test1, y_test2, y_test3], ignore_index=True)

# Function to Calculate RUL
def add_remaining_useful_life(df):
    # Get the total number of cycles for each unit
    grouped_by_unit = df.groupby(by="unit_nr")
    max_cycle = grouped_by_unit["time_cycles"].max()
    
    # Merge the max cycle back into the original frame
    result_frame = df.merge(max_cycle.to_frame(name='max_cycle'), left_on='unit_nr', right_index=True)
    
    # Calculate remaining useful life for each row
    remaining_useful_life = result_frame["max_cycle"] - result_frame["time_cycles"]
    result_frame["RUL"] = remaining_useful_life
    
    # drop max_cycle 
    result_frame = result_frame.drop("max_cycle", axis=1)
    return result_frame

# Chosen Model
lm = LinearRegression()

@app.route("/index.html", methods = ["POST","GET"])
def index():
    if request.method == "GET": 
        RUL = "" #Results
        return render_template('index.html', RUL=RUL)
    elif request.method == "POST":
        Test_Data = request.files.get("file_upload") # Get testing data from user
        Train_mod = request.form.get("Choose_Training_Set") # Get training data from user
        Train_mod = int(Train_mod) if Train_mod else None 
        
        # Manage tge training data according to user input
        if Train_mod == 1:
            train_data = train
        elif Train_mod == 2:
            train_data = train1
        elif Train_mod == 3:
            train_data = train2
        elif Train_mod == 4:
            train_data = train3
        else:
            train_data = default_train

        if not Test_Data:
            RUL = "Please upload a valid CSV file."
            return render_template('index.html', RUL=RUL) 
        else:
          # Reading the test data from user
          Test_Data = pd.read_csv(Test_Data, sep='\s+', header=None, names=col_names)
          # Calculating RUL for chosen training set
          train_data = train = add_remaining_useful_life(train_data)
          # Fitting the model
          X_train = train_data.drop(drop_labels, axis=1)
          y_train = X_train.pop('RUL')
          X_test = Test_Data.groupby('unit_nr').last().reset_index().drop(drop_labels, axis=1)
          lm.fit(X_train, y_train)
          # Predicting RUL
          y_hat_test = lm.predict(X_test)

            
            
          prediction = y_hat_test[0]
          RUL = f"Predicted RUL: {prediction:.2f} hours"
        
        return render_template('index.html', RUL=RUL)
