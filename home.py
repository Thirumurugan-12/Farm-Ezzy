import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor
import streamlit as st
import json
import requests
import google.generativeai as gen_ai
from streamlit_lottie import st_lottie 

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
    
gen_ai.configure(api_key="AIzaSyC5RiRjeKWNQkrUJxKWjfBr4w1oF12Wr8Y")
model = gen_ai.GenerativeModel('gemini-1.0-pro')

st.set_page_config(
    page_title="Farm Ezy - Crop Prediction",
    page_icon="🌾",
    layout="wide"
)
st.title("Farm Ezy - Crop Prediction🌾")

lottie_coding = load_lottiefile("Animation - 1714254170675.json") 
st_lottie(
    lottie_coding,
    speed=1,
    reverse=False,
    loop=True,
    quality="high", 
    #renderer="canvas",
    height=None,
    width=None,
    key=None,
)

# Load the CSV file
@st.cache_data
def load_data():
    return pd.read_csv('cpdata.csv')

# Load data
data = load_data()

# Create dummy variable for target i.e label
label = pd.get_dummies(data.label).iloc[:, 1:]
data = pd.concat([data, label], axis=1)
data.drop('label', axis=1, inplace=True)

train = data.iloc[:, 0:4].values
test = data.iloc[:, 4:].values

# Divide the data into training and test set
X_train, X_test, y_train, y_test = train_test_split(train, test, test_size=0.3)

# Train the model
clf = DecisionTreeRegressor()
clf.fit(X_train, y_train)

# User input
st.sidebar.title("Enter Environmental Factors")
air_humidity = st.sidebar.number_input('Air Humidity (g.m-3)')
air_temp = st.sidebar.number_input('Air Temp( °C)')
soil_humidity = st.sidebar.number_input('Soil Humidity(m3/m-3)')
soil_ph = st.sidebar.number_input('Soil pH (0-14)')
rainfall = st.sidebar.number_input('Rainfall(mm)')

if air_humidity != 0 and air_temp != 0 and soil_humidity != 0 and soil_ph != 0 and rainfall != 0:
    # Standardize the features
    sc = StandardScaler()
    user_input = sc.fit_transform([[air_humidity, air_temp, soil_humidity, soil_ph]])

    # Prediction
    predictions = clf.predict(user_input)

    crops = ['wheat', 'mungbean', 'Tea', 'millet', 'maize', 'lentil', 'jute', 'cofee', 'cotton', 'ground nut', 'peas',
             'rubber', 'sugarcane', 'tobacco', 'kidney beans', 'moth beans', 'coconut', 'blackgram', 'adzuki beans',
             'pigeon peas', 'chick peas', 'banana', 'grapes', 'apple', 'mango', 'muskmelon', 'orange', 'papaya',
             'watermelon', 'pomegranate']

    # Display prediction
    for i in range(len(predictions[0])):
        if predictions[0][i] == 1:
            predicted_crop = crops[i]
            break
    else:
        predicted_crop = "Incorrect Parameters"  # Default crop if none of the crops match

    st.write('The predicted crop is:', predicted_crop)
    st.write(model.generate_content(f"For the given environmental factors, the best crop to grow is:{predicted_crop}").text)
else:
    st.write("Please input all environmental factors to predict the crop.")
