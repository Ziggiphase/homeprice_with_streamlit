import streamlit as st
import pickle
#import joblib
import numpy as np

def load_model():
    with open("hp_model.pkl", 'rb') as f:
        model = pickle.load(f)
    with open("encoder.pkl", 'rb') as f:
        encoder = pickle.load(f)
    with open("scaler.pkl", 'rb') as f:
        scaler = pickle.load(f)
    
    return model, encoder, scaler

# def load_model():
#     model = joblib.load('model.joblib')
#     encoder = joblib.load('encoder.joblib')
#     return model, encoder

model, encoder, scaler = load_model()


def show_predict_page():
    st.title("Minna House Price Prediction")
    st.write("##### House info is needed for house prediction")
    
    Locations = ["Urban", "SubUrban", "Rural"]
    location = st.selectbox("Location", Locations)
    Bathroom = st.slider("Bathroom", 0, 3, 1)
    Bedroom = st.slider("Bedroom", 0, 8, 1)
    Age = st.slider("Age", 0, 152, 1)
    Area = st.text_input("Enter Area Size")

    yes = st.button("Calculate Home Price")
    if yes:
        #x = np.array([[Age, Bedroom, Bathroom, Area, location]])
        cols = [Age, Bedroom, Bathroom, Area]
        location = encoder.transform([location])
        location = location[0]
        cols.append(location)
        location = cols[4]
        arr_cols = np.array(cols)
        scaled_cols = arr_cols[:4]
        scaled_cols = scaler.transform([scaled_cols])
        new_cols = np.insert(scaled_cols, 4, [location])
        new_cols = np.array([new_cols])
        
        #a = np.array(x)
        #x[:, 4] = encoder.transform(x[:, 4])
        #x = x.astype(float)
        #st.write(x)
        pred_price = model.predict(new_cols)
        st.subheader(f"The estimated price is {round(pred_price[0])} £")