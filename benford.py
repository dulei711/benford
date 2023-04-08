import streamlit as st
import pandas as pd
import openpyxl
import numpy as np
import matplotlib.pyplot as plt

def newcomb_benford(column):
    # Calculate the first, second, and third digits of the column
    first_digit = abs(column)//10**(int(np.log10(abs(column))))
    second_digit = abs(column)//10**(int(np.log10(abs(column)))-1)%10
    third_digit = abs(column)//10**(int(np.log10(abs(column)))-2)%10
    
    # Calculate the expected frequencies based on Newcomb Benford's law
    first_freq = np.log10(1 + 1/first_digit)
    second_freq = np.log10(1 + 1/(10*first_digit + second_digit))
    third_freq = np.log10(1 + 1/(100*first_digit + 10*second_digit + third_digit))
    
    return [first_freq, second_freq, third_freq]

def analyze_excel_file(file):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(file, engine='openpyxl')
    
    # Get the column to analyze
    col = st.selectbox('Select a column to analyze:', df.columns)
    
    # Calculate the observed and expected frequencies for the first, second, and third digits of the column
    obs_freq = df[col].apply(lambda x: newcomb_benford(x)).sum()
    exp_freq = np.log10(np.arange(1, 10)).repeat(3)
    
    # Create a bar chart to compare the observed and expected frequencies
    '''
    fig, ax = plt.subplots()
    ax.bar(np.arange(1, 10)-0.2, obs_freq, width=0.4, color='orange', label='Observed')
    ax.bar(np.arange(1, 10)+0.2, exp_freq, width=0.4, color='blue', label='Expected')
    ax.set_xlabel('Digit')
    ax.set_ylabel('Frequency (log10)')
    ax.set_title('Newcomb Benford\'s Law Analysis')
    ax.legend()
    
    # Show the chart in the Streamlit app
    st.pyplot(fig)
    '''

st.set_page_config(page_title='Fraud Detection with Newcomb Benford\'s Law')

# Add a title to the app
st.title('Fraud Detection with Newcomb Benford\'s Law')

# Add a file uploader to the app
file = st.file_uploader('Upload an Excel file', type=['xlsx'])

if st.button("Run"):
    # Analyze the Excel file if a file has been uploaded
    if file is not None:
        analyze_excel_file(file)
