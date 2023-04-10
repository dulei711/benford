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
    
    # plot a bar chart for each digit
    fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(12, 8))
    fig.suptitle('Benford\'s Law Distribution for {}'.format(column))
    for i, ax in enumerate(axes.flat):
        digit = i + 1
        if digit == 2:
            freq = two_digit_freq
            freq_obs = two_digit_freq_obs
            xlabels = [str(i) + str(j) for i in range(1, 10) for j in range(0, 10)]
        elif digit == 3:
            freq = three_digit_freq
            freq_obs = three_digit_freq_obs
            xlabels = [str(i) + str(j) + str(k) for i in range(1, 10) for j in range(0, 10) for k in range(0, 10)]
        else:
            freq = first_digit_freq
            freq_obs = first_digit_freq_obs
            xlabels = np.arange(1, 10)
        
        ax.bar(xlabels, freq, width=0.8, alpha=0.5, label='Expected')
        ax.bar(xlabels, freq_obs, width=0.4, alpha=0.8, label='Observed')
        ax.set_title('Digit {}'.format(digit))
        ax.legend()
    
    plt.tight_layout()
    st.pyplot(fig)
    
st.title("## Benford's Law Test")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    column = st.selectbox("Select a column:", df.columns)
    if st.button("Run"):
        benfords_law_test(df, column)
