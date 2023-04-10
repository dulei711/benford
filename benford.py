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
    
    # create a figure with three subplots
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 10))
    
    # plot a bar chart comparing the expected and observed frequencies for the first digit
    ax = axes[0]
    x = np.arange(1, 10)
    ax.bar(x, first_digit_freq, color='blue', alpha=0.5, label='Expected')
    ax.bar(x, first_digit_freq_obs, color='orange', alpha=0.5, label='Observed')
    ax.set_xticks(x)
    ax.set_xticklabels(x)
    ax.set_xlabel('First Digit')
    ax.set_ylabel('Frequency')
    ax.set_title('Benford\'s Law for First Digit')
    ax.legend()
    
    # plot a bar chart comparing the expected and observed frequencies for the two digits
    ax = axes[1]
    x = np.arange(10, 100)
    ax.bar(x, two_digit_freq, color='blue', alpha=0.5, label='Expected')
    ax.bar(x, two_digit_freq_obs, color='orange', alpha=0.5, label='Observed')
    ax.set_xticks(x[::10])
    ax.set_xticklabels(x[::10])
    ax.set_xlabel('Two Digits')
    ax.set_ylabel('Frequency')
    ax.set_title('Benford\'s Law for Two Digits')
    ax.legend()
    
    # plot a bar chart comparing the expected and observed frequencies for the three digits
    ax = axes[2]
    x = np.arange(100, 1000)
    ax.bar(x, three_digit_freq, color='blue', alpha=0.5, label='Expected')
    ax.bar(x, three_digit_freq_obs, color='orange', alpha=0.5, label='Observed')
    ax.set_xticks(x[::100])
    ax.set_xticklabels(x[::100])
    ax.set_xlabel('Three Digits')
    ax.set_ylabel('Frequency')
    ax.set_title('Benford\'s Law for Three Digits')
    ax.legend()
    
    plt.tight()
    st.pyplot(fig)
    
st.title("## Benford's Law Test")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    column = st.selectbox("Select a column:", df.columns)
    if st.button("Run"):
        benfords_law_test(df, column)
