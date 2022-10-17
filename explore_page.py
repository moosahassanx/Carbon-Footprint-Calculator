from datetime import datetime, timedelta
from distutils.command.bdist import show_formats
from locale import getpreferredencoding
from operator import index
from xml.etree.ElementTree import tostring
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from predict_page import get_prediction

@st.cache(show_spinner=False)
def calculate_carbon_footprint(
    electricityTotal, 
    gasTotal, 
    entertainmentTotal, 
    foodTotal, 
    rentTotal, 
    miscellaneousTotal,
    electronicsTotal,
    industrialTotal,
    residencyTotal,
    healthTotal):
    carbonFootprint = 0

    carbonFootprint = carbonFootprint + electricityTotal * 105
    carbonFootprint = carbonFootprint + gasTotal * 105
    carbonFootprint = carbonFootprint + entertainmentTotal * 50
    carbonFootprint = carbonFootprint + foodTotal * 50
    carbonFootprint = carbonFootprint + rentTotal * 50
    carbonFootprint = carbonFootprint + miscellaneousTotal * 80
    carbonFootprint = carbonFootprint + electronicsTotal * 100
    carbonFootprint = carbonFootprint + industrialTotal * 80
    carbonFootprint = carbonFootprint + residencyTotal * 50
    carbonFootprint = carbonFootprint + healthTotal * 40

    return str(carbonFootprint)

def show_explore_page():
    st.title("Carbon Footprint Calculator")

    st.write("""
    ##### Calculate the carbon footprint by uploading JSON of bank transactions
    """)

    data_file = st.file_uploader("Upload JSON", type=["json"])
    if data_file is not None:

        # extract file information from the upload
        file_details = {
            "filename":data_file.name, 
            "filetype":data_file.type,
            "filesize":data_file.size
        }
        
        # displaying details of the upload
        st.write(file_details)
        
        # displaying transaction history of file upload
        d_f = pd.read_json(data_file, lines=True)
        st.write("""##### Transaction history:""")
        st.dataframe(d_f)

        # all the different categories
        electricityTotal = 0
        gasTotal = 0
        entertainmentTotal = 0
        foodTotal = 0
        rentTotal = 0
        miscellaneousTotal = 0
        electronicsTotal = 0
        industrialTotal = 0
        residencyTotal = 0
        healthTotal = 0

        with st.spinner('Categorising bank transaction descriptions...'):
            # displaying
            st.write("""##### Analysis:""")

            # iterate through each column in the dataframe
            for row in d_f.itertuples():
                # get total sum for each category
                if(get_prediction(row.description)["tag"] == "electricity"):
                    electricityTotal += row.amount * -1
                elif(get_prediction(row.description)["tag"] == "gas"):
                    gasTotal += row.amount * -1
                elif(get_prediction(row.description)["tag"] == "entertainment"):
                    entertainmentTotal += row.amount * -1
                elif(get_prediction(row.description)["tag"] == "food"):
                    foodTotal += row.amount * -1
                elif(get_prediction(row.description)["tag"] == "rent"):
                    rentTotal += row.amount * -1
                elif(get_prediction(row.description)["tag"] == "miscellaneous"):
                    miscellaneousTotal += row.amount * -1
                elif(get_prediction(row.description)["tag"] == "electronics"):
                    electronicsTotal += row.amount * -1
                elif(get_prediction(row.description)["tag"] == "industrial"):
                    industrialTotal += row.amount * -1
                elif(get_prediction(row.description)["tag"] == "residency"):
                    residencyTotal += row.amount * -1
                elif(get_prediction(row.description)["tag"] == "health"):
                    healthTotal += row.amount * -1
        st.success('Prediction finished.')

        labels = "Electricity", "Gas", "Entertainment", "Food", "Rent", "Miscellaneous", "Electronics", "Industrial", "Residency", "Health"
        sizes = [
            electricityTotal, 
            gasTotal, 
            entertainmentTotal, 
            foodTotal, 
            rentTotal, 
            miscellaneousTotal, 
            electronicsTotal, 
            industrialTotal,
            residencyTotal,
            healthTotal
        ]

        st.write("Transaction spread")
        fig2 = plt.figure(figsize=(10, 3))
        ax2 = fig2.add_axes([0, 0, 1, 1])
        ax2.bar(labels, sizes, width=0.5)
        st.pyplot(fig2)

        # # filter between dates
        # st.write("""
        # ### Date Range Filter
        # """)

        # startDate = st.date_input(      # start date
        #     "Input start date",
        #     datetime.today() - timedelta(days=365)
        # )
        # st.write("Start date: ", startDate)
        
        # endDate = st.date_input(        # end date
        #     "Input end date",
        # )
        # st.write("End date: ", endDate)

        ok = st.button("Calculate Carbon Footprint")

        if ok:
            st.write("Your carbon footprint is " + 
            calculate_carbon_footprint(
                electricityTotal,
                gasTotal,
                entertainmentTotal,
                foodTotal,
                rentTotal,
                miscellaneousTotal,
                electronicsTotal,
                industrialTotal,
                residencyTotal,
                healthTotal) 
            + " metric tonnes of CO\u00b2.".format())
