# Filename: AIFallPrediction.py
# Objective:
# Remarks:
# Developer: Mr Michael Tan Kok Liang
# Date: 12/08/2024

# PYTHONIC LIBRARIES
# -------------------
# Importing requisite libraries
import streamlit as st;
import streamlit_authenticator as stauth;
import numpy as np;
import pandas as pd;
from sklearn.model_selection import train_test_split;
from sklearn.ensemble import RandomForestClassifier;
import pickle;
import joblib;
import sklearn;
import time;

#---------------- USER CREDENTIALS CONFIGURATIONS --------------------------
import yaml;
from yaml.loader import SafeLoader;
# ===========================================================================

# ----------- DATE AND TIME OPERATIONS ------------
from datetime import date; # For current date computational display.
from datetime import datetime; # For current timestamp computational display.
import time;
# ===============================================

# -----------------------------  GLOBAL VARIABLES -----------------------------------
global today, now, current_weekday, current_weekday_datetime, d1, d2, d3, pathname, frames, timer1_running;
global pageTitle, pageIcon, pageLayout, pageSidebar, docHeader, docIcon, docMenuItems, healthCareImage, securityAccessImage;
global docSubHeader, homePageInfo, authenticator;

# --------------- Document Variables  --------------------------
pageTitle = "";
pageIcon = "";
pageLayout = "";
pageSidebar = "";
docHeader = "";
docSubHeader = "";
docIcon = "";
docMenuItems = "";
healthCareImage = "";
securityAccessImage = "";
homePageInfo = "";


# Current Weekday and Timestamp computation
# ------------------------------------------
today = date.today(); # Variable for displaying today's date.
now = datetime.now(); # Variable for displaying today's data and time.
current_weekday = ""; # Current Weekday.
current_weekday_datetime = "";
d1 = "";
d2 = "";
d3 = "";

# Extract today date
#today = date.today();
if today.weekday() == 0:
    current_weekday = "Monday";
elif today.weekday() == 1:
    current_weekday = "Tuesday";
elif today.weekday() == 2:
    current_weekday = "Wednesday";
elif today .weekday() == 3:
    current_weekday = "Thursday";
elif today.weekday() == 4:
    current_weekday = "Friday";
elif today.weekday() == 5:
    current_weekday = "Saturday";
else:
    current_weekday = "Sunday";

d1 = today.strftime("%d/%m/%Y"); # 03/11/2023
d2 = today.strftime("%d%m%Y"); # 03112023
d3 = now.strftime("%H%M%S"); # 103314
d4 = now.strftime("%H%M%S.%f"); # 103314.ms (includes ms)

current_weekday_datetime = current_weekday + ", " + d1 + " " + d3;

# Page configuration
st.set_page_config(
     page_title='AI Fall Prediction App',
     page_icon='🪄',
     layout='wide',
     initial_sidebar_state='expanded');
def readConfig(): # Reads YAML Configuration File.
    with open('data\\Credentials.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader);

        authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days'],
            config['pre-authorized']
        );

        return authenticator;

if __name__ == "__main__":
    authenticator = readConfig();

    st.write(f"Current Day, Date and Time: {current_weekday_datetime}");

    # Title of the app
    st.title('🪄 AI Fall Prediction App');

    # Load dataset
    # df = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/iris.csv');
    df = pd.read_csv("pages\cStick.csv");

    # Change the dataframe column datatype
    # ---------------------------------------
    df[['Pressure', 'Accelerometer']] = df[['Pressure', 'Accelerometer']].astype(float);

    # Input widgets -> Sidebar
    #--------------------------
    st.sidebar.subheader('Input features');
    distance = st.sidebar.slider('Distance', 15, 30, 60);
    pressure = st.sidebar.slider('Pressure', 0.2, 1.2, 2.0);
    hrv = st.sidebar.slider('HRV', 33, 65, 130);
    sugarlevel = st.sidebar.slider('Sugar Level', 45, 90, 180);
    spo2 = st.sidebar.slider('SpO2', 25, 50, 100);
    accelerometer = st.sidebar.slider('Accelerometer', 0.2, 1.2, 2.0);
    st.write("");
    st.write("");

    if st.session_state['authentication_status']:
        st.write("");
        st.write("");
        test = authenticator.logout("Logout", "sidebar");
    if st.session_state['authentication_status'] is None:
        st.switch_page("AIFallPrediction.py");  # Navigates to the dashboard subpage.
        st.warning('Please enter your username and password');

    # Separate to X and y
    # df.rename(columns=lambda x: x.strip(), inplace=True);
    X = df.drop('Decision', axis=1); # Why? Because the last column is the prediction classifier.
    y = df.Decision;

    # Data splitting -> Splits the original dataset into the training and testing dataset.
    #---------------
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42);

    # Model building  -> using RandomForestClassifier
    # ---------------
    rf = RandomForestClassifier(max_depth=2, max_features=4, n_estimators=200, random_state=42);

    # Model Training
    #-----------------
    rf.fit(X_train, y_train);

    # Apply model to make predictions
    #y_pred = rf.predict([[distance, pressure, hrv, sugarlevel, spo2, accelerometer]]);

   # Saves the Trained Model output  -> Using sklearn joblib
   #----------------------------------
    scikit_ver = sklearn.__version__; # Displays the current scikit-learn's version
    joblib.dump(rf, f"model_{scikit_ver}.pkl"); # and create the version based model accordingly.

  # Loads the saved model
  #----------------------
    mj = joblib.load(f"model_{scikit_ver}.pkl"); # Loads the model for output prediction use.

  # Prediction using the loaded saved model.
  #------------------------------------------
    y_pred = mj.predict([[distance, pressure, hrv, sugarlevel, spo2, accelerometer]]);

    # Print EDA
    st.subheader('Brief EDA');
    st.write('The data is grouped by the class and the variable mean is computed for each class.');
    groupby_species_mean = df.groupby('Decision').mean();
    st.write(groupby_species_mean);
    st.line_chart(groupby_species_mean.T);
    # Print input features
    st.subheader('Input features')
    input_feature = pd.DataFrame([[distance, pressure, hrv, sugarlevel, spo2, accelerometer]],
                                 columns=['Distance', 'Pressure', 'HRV', 'SugarLevel', 'SpO2', 'Accelerometer']);
    st.write(input_feature);

    # Print prediction output
    st.subheader('Output');
    if(y_pred[0]==0):
        y_pred[0] = "No Fall";
    elif(y_pred[0]==1):
        y_pred[0] = "Slip or Trip";
    elif(y_pred[0]==2):
        y_pred[0] = "Fall";

   # Displays the predicted value.
   #-------------------------------
    st.metric('Predicted class', y_pred[0], '');

    st.html(
        "<p><h5><center>An AI Healthcare Solution Project. Proudly developed with ❤️ using Streamlit. 😎</center></h5></p>" );


