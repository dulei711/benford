import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chisquare

# Define a function to calculate the first digit of a number
def first_digit(n):
    return int(str(n)[0])

# Define a function to calculate the second digit of a number
def second_digit(n):
    return int(str(n)[1])

# Define a function to calculate the third digit of a number
def third_digit(n):
    return int(str(n)[2])

# Define a function to apply the Newcomb-Benford Law to a series of numbers
def apply_newcomb_benford_law(data, digit):
    # Calculate the frequency of each digit
    digit_counts = data.apply(digit).value_counts(normalize=True)
    # Calculate the expected frequency based on Newcomb-Benford Law
    expected_counts = np.log10(1 + 1 / np.arange(1, 10))
    expected_counts *= data.shape[0]
    # Calculate the chi-square statistic
    chi_square = chisquare(digit_counts, expected_counts)
    # Return the digit frequencies and the chi-square statistic
    return digit_counts, chi_square

# Define the Streamlit app
st.set_page_config(page_title="Newcomb Benford's Law Fraud Detection", page_icon=":guardsman:", layout="wide")
st.title("Newcomb Benford's Law Fraud Detection")
st.write("This app analyzes fraud using Newcomb Benford's Law on the first, second, and third digits of numbers in a dataset.")

# Upload a dataset
st.sidebar.title("Upload a Dataset")
uploaded_file = st.sidebar.file_uploader(label="Choose a CSV or Excel file", type=["csv", "xlsx"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) if uploaded_file.type == "text/csv" else pd.read_excel(uploaded_file, engine="openpyxl")
    st.sidebar.write("Dataset Summary:")
    st.sidebar.write(df.describe())
    df_column = st.selectbox('Select the Column to evaluate:', df.columns)
    
    # Analyze the first digit
    st.sidebar.title("First Digit Analysis")
    first_digit_counts, first_digit_chi_square = apply_newcomb_benford_law(df_column, first_digit)
    st.sidebar.write("First Digit Counts:")
    st.sidebar.write(first_digit_counts)
    st.sidebar.write("Chi-Square Statistic:")
    st.sidebar.write(first_digit_chi_square.statistic)

    # Analyze the second digit
    st.sidebar.title("Second Digit Analysis")
    second_digit_counts, second_digit_chi_square = apply_newcomb_benford_law(df_column, second_digit)
    st.sidebar.write("Second Digit Counts:")
    st.sidebar.write(second_digit_counts)
    st.sidebar.write("Chi-Square Statistic:")
    st.sidebar.write(second_digit_chi_square.statistic)

    # Analyze the third digit
    st.sidebar.title("Third Digit Analysis")
    third_digit_counts, third_digit_chi_square = apply_newcomb_benford_law(df_column, third_digit)
    st.sidebar.write("Third Digit Counts:")
    st.sidebar.write(third_digit_counts)
    st.sidebar.write("Chi-Square Statistic:")
    st.sidebar.write(third_digit_chi_square.statistic)

    # Display the dataset and digit frequencies
    st.write("Dataset:")
    st.write(df)
    st.write("Digit Frequencies:")
    st.write(pd.DataFrame({
        "First Digit": first_digit_counts,
        "Second Digit": second_digit_counts,
        "Third Digit": third_digit_counts}))
