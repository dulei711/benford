import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
import math

import math

def get_digit_frequency(data, position):
    # Check if data is a Series, and convert to str if necessary
    if not isinstance(data, pd.Series):
        data = pd.Series(data)
    data = data.astype(str)
    
    # Select the specified position of the digit
    selected_digits = data.str[position - 1]
    
    # Filter out non-numeric values and convert to int
    selected_digits = selected_digits[selected_digits.str.isnumeric()]
    selected_digits = selected_digits.astype(int)
    
    # Count the frequency of each digit
    freq_dict = dict(Counter(selected_digits))
    
    # Compute the expected frequency of each digit
    expected_freq_dict = {d: math.log10(1 + 1/(10*d + i)) for i in range(10) for d in range(1, 10)}
    expected_freq_dict[0] = math.log10(2)
    
    # Convert the frequency dictionaries to lists
    actual_freq = [freq_dict.get(d, 0) for d in range(0, 10)]
    expected_freq = [expected_freq_dict[d] for d in range(0, 10)]
    
    return actual_freq, expected_freq




def plot_frequency_comparison(column, position):
    actual_freq, expected_freq = get_digit_frequency(df[column], position)
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 6))
    
    # Plot actual frequency
    sns.barplot(x=list(range(0, 10)), y=actual_freq, ax=ax1)
    ax1.set(title=f'Actual Frequency for Column "{column}" at Digit Position {position}',
            xlabel='Digit', ylabel='Frequency')
    
    # Plot expected frequency
    sns.lineplot(x=list(range(0, 10)), y=expected_freq, ax=ax2)
    ax2.set(title=f'Expected Frequency for Column "{column}" at Digit Position {position}',
            xlabel='Digit', ylabel='Frequency')
    
    # Set y-axis limit to be the maximum frequency value between actual and expected
    max_freq = max(max(actual_freq), max(expected_freq))
    ax1.set_ylim(0, max_freq)
    ax2.set_ylim(0, max_freq)
    
    # Show the plot
    st.pyplot(fig)

st.set_page_config(page_title="Newcomb-Benford Law Anomaly Detection")
st.title("Newcomb-Benford Law Anomaly Detection")

uploaded_file = st.file_uploader("Choose a file to upload")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # Get the column names and ask user which column to analyze
    column_names = list(df.columns)
    column = st.selectbox("Select a column to analyze", column_names)
    
    # Ask user which digit position to analyze
    position = st.slider("Select a digit position to analyze (1 = first digit)", 1, len(str(df[column].max())))
    
    if st.button("RUN"):
        # Generate the frequency comparison plot
        plot_frequency_comparison(column, position)
