import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chisquare
import matplotlib.pyplot as plt

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
    
    # plot the expected vs observed frequencies for the first digit
    fig, ax = plt.subplots()
    ax.plot(np.arange(1, 10), first_digit_freq, 'ro-', label='Expected')
    ax.bar(np.arange(1, 10), first_digit_freq_obs, alpha=0.5, label='Observed')
    ax.set_xlabel('First Digit')
    ax.set_ylabel('Frequency')
    ax.set_title('Benford\'s Law Test for First Digit in ' + column)
    ax.legend()
    st.pyplot(fig)

    # plot the expected vs observed frequencies for the two digits
    fig, ax = plt.subplots()
    ax.plot(np.arange(10, 100), two_digit_freq, 'ro-', label='Expected')
    ax.bar(np.arange(10, 100), two_digit_freq_obs, alpha=0.5, label='Observed')
    ax.set_xlabel('Two Digits')
    ax.set_ylabel('Frequency')
    ax.set_title('Benford\'s Law Test for Two Digits in ' + column)
    ax.legend()
    st.pyplot(fig)

    # plot the expected vs observed frequencies for the three digits
    fig, ax = plt.subplots()
    ax.plot(np.arange(100, 1000), three_digit_freq, 'ro-', label='Expected')
    ax.bar(np.arange(100, 1000), three_digit_freq_obs, alpha=0.5, label='Observed')
    ax.set_xlabel('Three Digits')
    ax.set_ylabel('Frequency')
    ax.set_title('Benford\'s Law Test for Three Digits in ' + column)
    ax.legend()
    st.pyplot(fig)
    
st.title("## Benford's Law Test")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    column = st.selectbox("Select a column:", df.columns)
    if st.button("Run"):
        benfords_law_test(df, column)
