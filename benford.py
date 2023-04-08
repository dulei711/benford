import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def calculate_expected_frequencies(df, column_name):
    data = df[column_name]
    # Get the first digit of each value
    first_digits = data.apply(lambda x: int(str(x)[0]))
    # Calculate the expected frequency for each digit
    expected_freq = np.log10(1 + 1/np.arange(1, 10))
    expected_freq = np.round(expected_freq / np.sum(expected_freq), 4)
    expected_freq_dict = dict(zip(range(1, 10), expected_freq))
    # Calculate the actual frequency for each digit
    actual_freq_dict = dict(first_digits.value_counts(normalize=True))
    # Merge the expected and actual frequencies into a single dataframe
    freq_df = pd.DataFrame({'Digit': range(1, 10),
                            'Expected Frequency': expected_freq,
                            'Actual Frequency': [actual_freq_dict.get(d, 0) for d in range(1, 10)]})
    return freq_df

st.title('Newcomb Benford\'s Law Anomaly Detection')

# Ask the user to upload an excel file
uploaded_file = st.file_uploader('Upload an Excel file', type=['xlsx', 'xls'])

if uploaded_file is not None:
    # Read the data from the uploaded file into a pandas dataframe
    df = pd.read_excel(uploaded_file)
    # Ask the user to select a column from the dataframe
    column_name = st.selectbox('Select a column', options=list(df.columns))
    # Calculate the expected and actual frequencies for each digit
    freq_df = calculate_expected_frequencies(df, column_name)
    # Plot a bar chart comparing the expected and actual frequencies
    fig, ax = plt.subplots()
    freq_df.plot(x='Digit', y=['Expected Frequency', 'Actual Frequency'], kind='bar', ax=ax)
    ax.set_xlabel('Digit')
    ax.set_ylabel('Frequency')
    ax.set_title(f'Newcomb Benford\'s Law for {column_name}')
    st.pyplot(fig)
