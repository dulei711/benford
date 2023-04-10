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
    
    # create a figure with 3 subplots
    # create a figure with 3 subplots
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))
    plt.subplots_adjust(hspace=0.4)
    
    # plot the first digit results
    axs[0].bar(first_digit_counts.index.astype(int), first_digit_freq_obs.values, color='b', alpha=0.5)
    axs[0].plot(range(1, 10), first_digit_freq, color='r', marker='o')
    axs[0].set_xticks(range(1, 10))
    axs[0].set_title('First Digit')
    axs[0].set_ylabel('Frequency')
    axs[0].legend(['Expected', 'Observed'])

    # plot the two digit results
    axs[1].bar(two_digit_counts.index.astype(int), two_digit_freq_obs.values, color='b', alpha=0.5)
    axs[1].plot(range(10, 100), two_digit_freq, color='r', marker='o')
    axs[1].set_xticks(range(10, 100, 10))
    axs[1].set_title('Two Digits')
    axs[1].set_ylabel('Frequency')
    axs[1].legend(['Expected', 'Observed'])

    # plot the three digit results
    axs[2].bar(three_digit_counts.index.astype(int), three_digit_freq_obs.values, color='b', alpha=0.5)
    axs[2].plot(range(100, 1000), three_digit_freq, color='r', marker='o')
    axs[2].set_xticks(range(100, 1000, 100))
    axs[2].set_title('Three Digits')
    axs[2].set_ylabel('Frequency')
    axs[2].legend(['Expected', 'Observed'])
    st.pyplot(fig)
    
st.title("## Benford's Law Test")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    column = st.selectbox("Select a column:", df.columns)
    if st.button("Run"):
        benfords_law_test(df, column)
