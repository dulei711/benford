import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chisquare

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
    # plot the two digit data
    axs[1].bar(range(10, 100), two_digit_freq, alpha=0.5, label='Expected Frequency')
    axs[1].bar(two_digit_counts.index.astype(int), two_digit_freq_obs, alpha=0.5, label='Observed Frequency')
    axs[1].set_xlabel('Two Digits')
    axs[1].set_ylabel('Frequency')
    axs[1].legend()
    axs[1].set_title('Benford\'s Law Analysis: Two Digits')
    # plot the three digit data
    axs[2].bar(range(100, 1000), three_digit_freq, alpha=0.5, label='Expected Frequency')
    axs[2].bar(three_digit_counts.index.astype(int), three_digit_freq_obs, alpha=0.5, label='Observed Frequency')
    axs[2].set_xlabel('Three Digits')
    axs[2].set_ylabel('Frequency')
    axs[2].legend()
    axs[2].set_title('Benford\'s Law Analysis: Three Digits')
    # set the overall title and layout
    plt.suptitle('Benford\'s Law Analysis')
    plt.tight_layout()
    # display the plot
    st.pyplot(fig)
    
    # calculate chi-squared tests and p-values
    first_digit_chi2, first_digit_pval = chisquare(first_digit_freq_obs, first_digit_freq)
    two_digit_chi2, two_digit_pval = chisquare(two_digit_freq_obs, two_digit_freq)
    three_digit_chi2, three_digit_pval = chisquare(three_digit_freq_obs, three_digit_freq)
    # print the expected and observed frequencies and chi-squared test results for the first, two, and three digits
    st.text('First Digit:')
    st.table(pd.DataFrame({'Expected Frequency': first_digit_freq, 'Observed Frequency': first_digit_freq_obs, 'Chi-Squared Test': first_digit_chi2, 'p-value': first_digit_pval}))
    st.text('Two Digits:')
    st.table(pd.DataFrame({'Expected Frequency': two_digit_freq, 'Observed Frequency': two_digit_freq_obs, 'Chi-Squared Test': two_digit_chi2, 'p-value': two_digit_pval}))
    st.text('Three Digits:')
    st.table(pd.DataFrame({'Expected Frequency': three_digit_freq, 'Observed Frequency': three_digit_freq_obs, 'Chi-Squared Test': three_digit_chi2, 'p-value': three_digit_pval}))

st.title("## Benford's Law Test")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    column = st.selectbox("Select a column:", df.columns)
    if st.button("Run"):
        benfords_law_test(df, column)
