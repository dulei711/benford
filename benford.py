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
    
    # create a figure with 3 subplots
    fig, axes = plt.subplots(3, 1, figsize=(20, 10))
    fig.subplots_adjust(hspace=0.4)

    # plot the first digit frequencies
    ax1 = axes[0]
    ax1.bar(first_digit_counts.index.astype(int), first_digit_freq_obs, color='b', alpha=0.5, label='Observed')
    ax1.plot(first_digit_counts.index.astype(int), first_digit_freq, color='r', label='Expected')
    ax1.set_title('First Digit Frequencies')
    ax1.set_xlabel('First Digit')
    ax1.set_ylabel('Frequency')
    ax1.legend()

    # plot the two digit frequencies
    ax2 = axes[1]
    ax2.bar(two_digit_counts.index.astype(int), two_digit_freq_obs, color='g', alpha=0.5, label='Observed')
    ax2.plot(two_digit_counts.index.astype(int), two_digit_freq, color='r', label='Expected')
    ax2.set_title('Two Digit Frequencies')
    ax2.set_xlabel('Two Digits')
    ax2.set_ylabel('Frequency')
    ax2.legend()

    # plot the three digit frequencies
    ax3 = axes[2]
    ax3.bar(three_digit_counts.index.astype(int), three_digit_freq_obs, color='m', alpha=0.5, label='Observed')
    ax3.plot(three_digit_counts.index.astype(int), three_digit_freq, color='r', label='Expected')
    ax3.set_title('Three Digit Frequencies')
    ax3.set_xlabel('Three Digits')
    ax3.set_ylabel('Frequency')
    ax3.legend()    
    st.pyplot(fig)
    
st.title("## Benford's Law Test")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    column = st.selectbox("Select a column:", df.columns)
    if st.button("Run"):
        benfords_law_test(df, column)
