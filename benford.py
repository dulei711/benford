import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to calculate the frequency of the first, second, and third digits
def calc_freq(data):
    # Get the first digit of each number
    first_digit = data.apply(lambda x: int(str(x)[0]) if str(x)[0].isdigit() else None)
    # Get the second digit of each number
    second_digit = data.apply(lambda x: int(str(x)[1]) if str(x)[1].isdigit() else None)
    # Get the third digit of each number
    third_digit = data.apply(lambda x: int(str(x)[2]) if str(x)[2].isdigit() else None)
    
    # Calculate the frequency of each digit
    freq_1 = len(first_digit[first_digit == 1])/len(first_digit.dropna())
    freq_2 = len(second_digit[second_digit == 2])/len(second_digit.dropna())
    freq_3 = len(third_digit[third_digit == 3])/len(third_digit.dropna())
    
    return freq_1, freq_2, freq_3


# Function to load the Excel file and apply the frequency calculation function
def load_data(file):
    df = pd.read_excel(file)
    st.write(df.head())

    # Get the column with the numbers to be analyzed
    column_name = st.selectbox("Select the column with the numbers", options=df.columns)
    data = df[column_name]

    # Calculate the frequency of the first, second, and third digits
    freq_1, freq_2, freq_3 = calc_freq(data)

    # Display the frequencies
    st.write(f"Frequency of first digit: {freq_1:.2f}")
    st.write(f"Frequency of second digit: {freq_2:.2f}")
    st.write(f"Frequency of third digit: {freq_3:.2f}")

    # Create a chart of the frequencies
    fig, ax = plt.subplots()
    ax.bar(['First digit', 'Second digit', 'Third digit'], [freq_1, freq_2, freq_3])
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

# Set up the Streamlit app
st.set_page_config(page_title="Fraud Detection with Newcomb-Benford's Law", page_icon=":money_with_wings:")

st.write("# Fraud Detection with Newcomb-Benford's Law")

# Allow the user to upload an Excel file
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

# Load the data and display the frequencies and chart
if uploaded_file is not None:
    load_data(uploaded_file)
else:
    st.warning("Please upload a file.")
