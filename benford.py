import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chisquare
import matplotlib as plt

def benfords_law_test(df, column):    
    # calculate the expected frequencies for the first digit using Benford's Law
    first_digit_freq = np.log10(1 + 1 / np.arange(1, 10))
    two_digit_freq = np.array([np.log10(1 + 1 / (10 * i + j)) for i in range(1, 10) for j in range(0, 10)])
    three_digit_freq = np.array([np.log10(1 + 1 / (100 * i + 10 * j + k)) for i in range(1, 10) for j in range(0, 10) for k in range(0, 10)])
    # count the occurrences of each first, two, and three digit combination in the numbers column
    first_digit_counts = df[column].astype(str).str[0].value_counts()
    two_digit_counts = df[column].astype(str).str[:2].value_counts()
    three_digit_counts = df[column].astype(str).str[:3].value_counts()
    # normalize the counts to get the observed frequencies
    first_digit_freq_obs = first_digit_counts / first_digit_counts.sum()
    two_digit_freq_obs = two_digit_counts / two_digit_counts.sum()
    three_digit_freq_obs = three_digit_counts / three_digit_counts.sum()
    # create lists of digit ranges and expected/observed frequencies for each chart
    digit_ranges = [range(1, 10), range(10, 100), range(100, 1000)]
    expected_freqs = [first_digit_freq, two_digit_freq, three_digit_freq]
    observed_freqs = [first_digit_freq_obs, two_digit_freq_obs, three_digit_freq_obs]
    #plot with matplotlib
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(25,10))
    for i, ax in enumerate(axes):
        ax.bar(digit_ranges[i], expected_freqs[i], alpha=0.5, color='b', label='Expected Frequency')
        ax.bar(digit_ranges[i], observed_freqs[i], alpha=0.5, color='r', label='Observed Frequency')
        ax.set_xlabel('Digits')
        ax.set_ylabel('Frequency')
        ax.set_title(f'Benford\'s Law Analysis: {i+1} Digits')
        ax.legend(loc='best')
    plt.tight_layout()
    st.pyplot(fig)

    
st.title("## Benford's Law Test")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    column = st.selectbox("Select a column:", df.columns)
    if st.button("Run"):
        benfords_law_test(df, column)
