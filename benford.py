import pandas as pd
import numpy as np
from scipy.stats import chisquare
import streamlit as st

def get_first_digit(n):
    return int(str(n)[0])

def get_second_digit(n):
    return int(str(n)[1])

def get_third_digit(n):
    return int(str(n)[2])

def check_fraud(numbers):
    # Get the first, second, and third digit of each number
    first_digits = np.vectorize(get_first_digit)(numbers)
    second_digits = np.vectorize(get_second_digit)(numbers)
    third_digits = np.vectorize(get_third_digit)(numbers)

    # Get the expected frequencies according to Newcomb-Benford's law
    expected_frequencies = np.array([np.log10(1 + 1 / d) for d in range(1, 10)])
    expected_frequencies = np.multiply(expected_frequencies, len(first_digits))

    # Get the observed frequencies for the first digit
    observed_frequencies, _ = np.histogram(first_digits, bins=np.arange(1, 11))

    # Test if the observed frequencies for the first digit follow the expected frequencies using a chi-square test
    _, p_value = chisquare(observed_frequencies, expected_frequencies)

    # If the p-value is less than the significance level, assume fraud
    if p_value < 0.05:
        return True
    
    # Get the observed frequencies for the second digit
    observed_frequencies, _ = np.histogram(second_digits, bins=np.arange(1, 11))

    # Test if the observed frequencies for the second digit follow the expected frequencies using a chi-square test
    _, p_value = chisquare(observed_frequencies, expected_frequencies)

    # If the p-value is less than the significance level, assume fraud
    if p_value < 0.05:
        return True
    
    # Get the observed frequencies for the third digit
    observed_frequencies, _ = np.histogram(third_digits, bins=np.arange(1, 11))

    # Test if the observed frequencies for the third digit follow the expected frequencies using a chi-square test
    _, p_value = chisquare(observed_frequencies, expected_frequencies)

    # If the p-value is less than the significance level, assume fraud
    if p_value < 0.05:
        return True

    return False

# Set page title
st.set_page_config(page_title="Fraud Detection App")

# Add title and subtitle
st.title("Fraud Detection App")
st.write("This app detects fraud based on the Newcomb-Benford's law applied to the first, second, and third digits of a number in an Excel file.")

# Allow user to upload Excel file
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Load the Excel file
    df = pd.read_excel(uploaded_file)

    # Show the user the available columns in the Excel file
    available_columns = list(df.columns)
    column_to_check = st.selectbox("Select a column to check for fraud", available_columns)
    
    if st.button("Run"):
        # Show a message while the fraud detection is running
        with st.spinner("Detecting fraud..."):
            # Apply the check_fraud function to the selected column
            fraud_mask = np.apply_along_axis(check_fraud, axis=0, arr=df[column_to_check].values)

        # Show the user the results of the fraud detection
        st.write("Fraud detected in the following rows:")
        st.write(df[fraud_mask])
