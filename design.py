import streamlit as st
import pandas as pd
import numpy as np
from keras.models import load_model
import cv2 as cv

import nutrition_api as api

st.title('Nutritionist AI')

st.sidebar.title('Menu')
st.sidebar.subheader('Select a page')
app_mode = st.sidebar.selectbox('Choose the app mode', ['Home', 'Calories Calculator', 'Food Planner', 'Calories Calculator(Image)'])

if app_mode == 'Home':
    st.subheader('Home')
    st.write('This is the home page')

elif app_mode == 'Calories Calculator':
    st.subheader('Calories Calculator')
    food = st.text_input('Enter food name')
    if st.button('Get Calories') and food:
        data = api.get_nutrition_info({'query': food})
        st.write('Amount of Calories:', data[0]["calories"])

elif app_mode == 'Food Planner':
    st.subheader('Food Planner')
    max_calories = st.number_input('Enter your maximum calories intake per day:')
    breakfast = st.text_input('Enter breakfast food name')
    lunch = st.text_input('Enter lunch food name')
    dinner = st.text_input('Enter dinner food name')
    if st.button('Get Calories') and breakfast and lunch and dinner and max_calories:
        breakfast_data = api.get_nutrition_info({'query': breakfast})
        lunch_data = api.get_nutrition_info({'query': lunch})
        dinner_data = api.get_nutrition_info({'query': dinner})
        total_calories = breakfast_data[0]["calories"] + lunch_data[0]["calories"] + dinner_data[0]["calories"]
        st.write('Total Calories:', total_calories)
        if total_calories > max_calories:
            st.write('You have exceeded your maximum calories intake per day')
        else:
            st.write('You have not exceeded your maximum calories intake per day')

elif app_mode == 'Calories Calculator(Image)':
    st.subheader('Calories Calculator(Image)')

    model = load_model('keras_model.h5')
    labels = open('labels.txt', 'r').readlines()
    # Change underscore to space
    labels = [label.replace('_', ' ') for label in labels]
    # Remove digits from labels
    for index, label in enumerate(labels):
        labels[index] = ''.join([i for i in label if not i.isdigit()])
        index+=1
    # Remove first space
    labels = [label.replace(' ', '', 1) for label in labels]
    # Remove new line character
    labels = [label.replace('\n', '') for label in labels]

    picture = st.camera_input('Take a picture of your food')
    if st.button('Get Calories') and picture:
        with open('picture.jpg', 'wb') as f:
            f.write(picture.getbuffer())
        
        # Grab the webcameras image.
        image = cv.imread('picture.jpg')
        # Resize the raw image into (224-height,224-width) pixels.
        image = cv.resize(image, (224, 224), interpolation=cv.INTER_AREA)
        # Make the image a numpy array and reshape it to the models input shape.
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
        # Normalize the image array
        image = (image / 127.5) - 1
        # Have the model predict what the current image is. Model.predict
        # returns an array of percentages. Example:[0.2,0.8] meaning its 20% sure
        # it is the first label and 80% sure its the second label.
        probabilities = model.predict(image)
        predicted_food = labels[np.argmax(probabilities)]
        # Print what the highest value probabilitie label
        st.write('Food identified:', predicted_food)
        print(predicted_food)
        # Calculate the calories
        calories = api.get_nutrition_info({'query': predicted_food})
        st.write('Amount of Calories:', calories[0]["calories"])