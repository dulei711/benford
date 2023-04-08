import streamlit as st
import pandas as pd
import numpy as np
import math
from collections import OrderedDict
import seaborn as sns
import matplotlib.pyplot as plt


@st.cache
def read_file(file):
    df = pd.read_excel(file, engine='openpyxl')
    return df

@st.cache
def get_digit_frequency(data, position):
    if position == 'first':
        expected_freq_dict = OrderedDict([(d, math.log10(1 + 1 / d)) for d in range(1, 10)])
    elif position == 'second':
        expected_freq_dict = OrderedDict([(d, round(math.log10(1 + 1 / (10 * x + d)), 4)) for x in range(1, 10) for d in range(10)])
    elif position == 'third':
        expected_freq_dict = OrderedDict([(d, round(math.log10(1 + 1 / (100 * x + 10 * y + d)), 4)) for x in range(1, 10) for y in range(10) for d in range(10)])
    data = data.apply(lambda x: str(x))
    actual_freq = [0] * 9
    if data.str[position].str.isnumeric().any():
        actual_counts = data.str[position][data.str[position].str.isnumeric()].astype(int).value_counts(normalize=True).sort_index()
        for i, count in actual_counts.items():
            actual_freq[i-1] = count
    expected_freq = [expected_freq_dict[d] for d in range(1, 10)]
    return actual_freq, expected_freq


st.set_page_config(page_title="Newcomb-Benford's Law Anomaly Detection",
                   page_icon=":guardsman:",
                   layout="wide")

st.title("Newcomb-Benford's Law Anomaly Detection")

# upload file
uploaded_file = st.file_uploader("Upload a file", type=["xlsx", "xls"])

if uploaded_file is not None:
    df = read_file(uploaded_file)
    st.write(df)

    # column selection
    columns = list(df.columns)
    column = st.selectbox('Select a column', columns)

    # first digit analysis
    st.write('## First Digit Analysis')
    actual_freq, expected_freq = get_digit_frequency(df[column], 1)

    fig, ax = plt.subplots()
    sns.barplot(x=list(range(1, 10)), y=actual_freq)
    sns.lineplot(x=list(range(1, 10)), y=expected_freq, color='red', marker='o')
    ax.set(xlabel='Digit', ylabel='Frequency', title=f'First Digit Analysis ({column})')
    st.pyplot(fig)

    # second digit analysis
    st.write('## Second Digit Analysis')
    actual_freq, expected_freq = get_digit_frequency(df[column], 2)

    fig, ax = plt.subplots()
    sns.barplot(x=list(range(0, 10)), y=actual_freq)
    sns.lineplot(x=list(range(0, 10)), y=expected_freq, color='red', marker='o')
    ax.set(xlabel='Digit', ylabel='Frequency', title=f'Second Digit Analysis ({column})')
    st.pyplot(fig)

    # third digit analysis
    st.write('## Third Digit Analysis')
    actual_freq, expected_freq = get_digit_frequency(df[column], 3)

    fig, ax = plt.subplots()
    sns.barplot(x=list(range(0, 10)), y=actual_freq)
    sns.lineplot(x=list(range(0, 10)), y=expected_freq, color='red', marker='o')
    ax.set(xlabel='Digit', ylabel='Frequency', title=f'Third Digit Analysis ({column})')
    st.pyplot(fig)
