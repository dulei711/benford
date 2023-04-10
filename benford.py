import streamlit as st
import pandas as pd
import numpy as np
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
    # create the figure and subplots
    fig, axs = plt.subplots(3, 1, figsize=(20, 10))
    # plot the first digit data
    axs[0].bar(range(1, 10), first_digit_freq, alpha=0.5, label='Expected Frequency')
    axs[0].bar(first_digit_counts.index.astype(int), first_digit_freq_obs, alpha=0.5, label='Observed Frequency')
    axs[0].set_xlabel('First Digit')
    axs[0].set_ylabel('Frequency')
    axs[0].legend()
    axs[0].set_title('Benford\'s Law Analysis: First Digit')
    axs[0].axvline(x=6.5, color='red', linestyle='--')
    # plot the two digit data
    axs[1].bar(range(10, 100), two_digit_freq, alpha=0.5, label='Expected Frequency')
    axs[1].bar(two_digit_counts.index.astype(int), two_digit_freq_obs, alpha=0.5, label='Observed Frequency')
    axs[1].set_xlabel('Two Digits')
    axs[1].set_ylabel('Frequency')
    axs[1].legend()
    axs[1].set_title('Benford\'s Law Analysis: Two Digits')
    axs[1].axvline(x=58, color='red', linestyle='--')
    # plot the three digit data
    axs[2].bar(range(100, 1000), three_digit_freq, alpha=0.5, label='Expected Frequency')
    axs[2].bar(three_digit_counts.index.astype(int), three_digit_freq_obs, alpha=0.5, label='Observed Frequency')
    axs[2].set_xlabel('Three Digits')
    axs[2].set_ylabel('Frequency')
    axs[2].legend()
    axs[2].set_title('Benford\'s Law Analysis: Three Digits')
    axs[2].axvline(x=499, color='red', linestyle='--')
    # set the overall title and layout
    plt.suptitle('Benford\'s Law Analysis')
    plt.tight_layout()
    # display the plot
    st.pyplot(fig)


st.title("## Benford's Law Test")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    column = st.selectbox("Select a column:", df.columns)
    if st.button("Run"):
        benfords_law_test(df, column)
