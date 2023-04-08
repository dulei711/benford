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

    
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Function to calculate the frequency of each digit from 0 to 9
def calc_freq(data):
    freqs = []
    for i in range(10):
        freq = len(data[data.astype(str).str.startswith(str(i))])/len(data)
        freqs.append(freq)
    return freqs

# Define the Streamlit app
# Add a title to the app
st.title("Newcomb-Benford's Law Fraud Detection")

# Upload an Excel file and select a column to analyze
file = st.file_uploader("Upload an Excel file", type=["xls", "xlsx"])
if file is not None:
    df = pd.read_excel(file)
    column = st.selectbox("Select a column to analyze", df.columns.tolist())

    # Calculate the frequencies of each digit from 0 to 9 using Newcomb-Benford's Law
    freqs = calc_freq(df[column])

    # Create a bar chart for each digit to compare the observed frequencies with the expected ones
    for i in range(10):
        fig, ax = plt.subplots()
        ax.bar([0, 1], [freqs[i], 0.1], label=["Observed", "Expected"])
        ax.set_xlabel("Frequency")
        ax.set_ylabel("Digit " + str(i))
        ax.set_title("Newcomb-Benford's Law Frequencies")
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["Observed", "Expected"])
        ax.set_ylim([0, 0.5])
        st.pyplot(fig)
