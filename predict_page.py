import streamlit as st
import pickle
import numpy as np
import random
import torch
import pandas as pd
import matplotlib.pyplot as plt

# Loading training data
@st.cache
def load_data():
    df = pd.read_json('ready-dataset.json')
    df.to_json(orient="records", lines=True)    
    return df

df = load_data()

# Load the model
from transformers import AutoModelForSequenceClassification
new_model = AutoModelForSequenceClassification.from_pretrained('./model/')

from transformers import AutoTokenizer
new_tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')

# Predictions function
# Get predictions
import torch
import numpy as np

def get_prediction(text):
    encoding = new_tokenizer(text, return_tensors='pt', padding='max_length', truncation=True, max_length=128)
    # encoding = {k: v.to(trainer.model.device) for k,v in encoding.items()}

    outputs = new_model(**encoding)

    logits = outputs.logits

    sigmoid = torch.nn.Sigmoid()
    probs = sigmoid(logits.squeeze().cpu())
    probs = probs.detach().numpy()
    label = np.argmax(probs, axis=-1)

    if label == 0:
        return {
            'tag': 'electricity',
            'probability': probs[0]
        }
    if label == 1:
        return {
            'tag': 'gas',
            'probability': probs[1]
        }
    if label == 2:
        return {
            'tag': 'entertainment',
            'probability': probs[1]
        }
    if label == 3:
        return {
            'tag': 'food',
            'probability': probs[1]
        }
    if label == 4:
        return {
            'tag': 'rent',
            'probability': probs[1]
        }
    if label == 5:
        return {
            'tag': 'miscellaneous',
            'probability': probs[1]
        }
    if label == 6:
        return {
            'tag': 'electronics',
            'probability': probs[1]
        }
    if label == 7:
        return {
            'tag': 'industrial',
            'probability': probs[1]
        }
    if label == 8:
        return {
            'tag': 'residency',
            'probability': probs[1]
        }
    if label == 9:
        return {
            'tag': 'health',
            'probability': probs[1]
        }
    

def show_predict_page():
    # Input bar
    st.title("Machine Learning Model")
    st.write("""##### Test the multi-class text classification 🤗 model.""")
    description = st.text_input("Enter bank description: ")

    ok = st.button("Predict")

    if ok:
        with st.spinner('Predicting text...'):
            ml_prediction = get_prediction(description)
            st.write(ml_prediction)

    # Accuracy test
    st.markdown("""---""")
    st.write("""##### Run Accuracy Test""")
    st.write("Check the accuracy in real time. Clicking run will execute a command which will compare each predicted values against tagged values and give a calculation of accuracy as a percentage.")
    st.write("~ 4-6 mins.")
    checkAccuracy = st.button("Run")
    if checkAccuracy:
        st.write(df)

        st.write("Running tests...")
        my_bar = st.progress(0)


        length = len(df.index)

        correct = 0
        for index, row in df.iterrows():
            predictTag = get_prediction(row['description'])
            if(str(predictTag['tag']) == row['tag']):
                correct = correct + 1
            my_bar.progress((index / length))

        accuracy = str(round((correct / length) * 100, 2))
        st.write("Accuracy: " + accuracy + "%")

    # Pie chart
    st.markdown("""---""")
    data = df["tag"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")       # equal aspect ratio ensures that pie is drawn as a circle
    st.write("""
    ##### Training Dataset Analysis
    """)
    st.pyplot(fig1)
