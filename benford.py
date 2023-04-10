import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chisquare
import matplotlib.pyplot as plt
import seaborn as sns

# set the style to seaborn-darkgrid
sns.set_style("darkgrid")

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
    
    # create plots comparing the observed and expected frequencies
    fig, ax = plt.subplots(3, 1, figsize=(8, 12))

    # plot for first digits
    expected_first = ax[0].bar(np.arange(1, 10), first_digit_freq, alpha=0.5, label='Expected')
    observed_first = ax[0].bar(first_digit_counts.index.astype(np,int), first_digit_freq_obs.loc[first_digit_counts.index.astype(str)], alpha=0.5, label='Observed')
    ax[0].set_xlabel('First Digit')
    ax[0].set_ylabel('Frequency')
    ax[0].set_title('First Digit Frequencies')
    ax[0].legend()

    # plot for two digits
    expected_two = ax[1].bar(np.arange(10, 100), two_digit_freq, alpha=0.5, label='Expected')
    observed_two = ax[1].bar(two_digit_counts.index.astype(np,int), two_digit_freq_obs.loc[two_digit_counts.index.astype(str)], alpha=0.5, label='Observed')
    ax[1].set_xlabel('Two Digits')
    ax[1].set_ylabel('Frequency')
    ax[1].set_title('Two Digits Frequencies')
    ax[1].legend()

    # plot for three digits
    expected_three = ax[2].bar(np.arange(100, 1000), three_digit_freq, alpha=0.5, label='Expected')
    observed_three = ax[2].bar(three_digit_counts.index.astype(np,int), three_digit_freq_obs.loc[three_digit_counts.index.astype(str)], alpha=0.5, label='Observed')
    ax[2].set_xlabel('Three Digits')
    ax[2].set_ylabel('Frequency')
    ax[2].set_title('Three Digits Frequencies')
    ax[2].legend()

    plt.tight_layout()
    st.pyplot(fig)
    
st.title("## Benford's Law Test")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    column = st.selectbox("Select a column:", df.columns)
    if st.button("Run"):
        benfords_law_test(df, column)
