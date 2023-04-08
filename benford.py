import pandas as pd
import numpy as np
import streamlit as st

def check_fraud(values):
    # Compute the observed frequencies of the first digits
    first_digits = np.array([int(str(n)[0]) for n in values])
    observed_frequencies = np.bincount(first_digits)[1:]

    # Compute the expected frequencies according to the Newcomb-Benford law
    indices = np.arange(1, 10)
    expected_frequencies = np.log10(1 + 1 / indices)

    # Normalize the expected frequencies to match the number of values
    expected_frequencies *= len(values)
    
    # Compute the chi-square statistic and compare it to the critical value
    chi_square = np.sum((observed_frequencies - expected_frequencies) ** 2 / expected_frequencies)
    critical_value = 15.51
    return chi_square > critical_value

# Set up the Streamlit app
st.title("Newcomb-Benford Law Fraud Detection")
st.write("Upload an Excel file and select a column to check for fraud on the first, second, and third digits.")
file = st.file_uploader("Choose a file")
if file is not None:
    df = pd.read_excel(file, engine="openpyxl")
    column_names = df.columns.tolist()
    column_to_check = st.selectbox("Select a column to check for fraud", column_names)
    if st.button("Check for fraud"):
        values_to_check = df[column_to_check].values
        is_fraudulent = check_fraud(values_to_check)
        if is_fraudulent:
            st.write(f"Fraud detected in column {column_to_check}!")
        else:
            st.write(f"No fraud detected in column {column_to_check}.")
