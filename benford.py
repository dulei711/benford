import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chisquare
import plotly.graph_objects as go
import plotly.io as pio

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
    
    # create subplots
    fig = make_subplots(rows=3, cols=1, subplot_titles=("Benford's Law Analysis: First Digit", "Benford's Law Analysis: Two Digits", "Benford's Law Analysis: Three Digits"), shared_xaxes=True)
    # add bar traces for first digit
    fig.add_trace(go.Bar(x=range(1, 10), y=first_digit_freq, name='Expected Frequency', marker=dict(opacity=0.5)), row=1, col=1)
    fig.add_trace(go.Bar(x=first_digit_counts.index.astype(int), y=first_digit_freq_obs, name='Observed Frequency', marker=dict(opacity=0.5)), row=1, col=1)
    fig.update_xaxes(title_text="First Digit", row=1, col=1)
    fig.update_yaxes(title_text="Frequency", row=1, col=1)    
    # add bar traces for two digits
    fig.add_trace(go.Bar(x=range(10, 100), y=two_digit_freq, name='Expected Frequency', marker=dict(opacity=0.5)), row=2, col=1)
    fig.add_trace(go.Bar(x=two_digit_counts.index.astype(int), y=two_digit_freq_obs, name='Observed Frequency', marker=dict(opacity=0.5)), row=2, col=1)
    fig.update_xaxes(title_text="Two Digits", row=2, col=1)
    fig.update_yaxes(title_text="Frequency", row=2, col=1)    
    # add bar traces for three digits
    fig.add_trace(go.Bar(x=range(100, 1000), y=three_digit_freq, name='Expected Frequency', marker=dict(opacity=0.5)), row=3, col=1)
    fig.add_trace(go.Bar(x=three_digit_counts.index.astype(int), y=three_digit_freq_obs, name='Observed Frequency', marker=dict(opacity=0.5)), row=3, col=1)
    fig.update_xaxes(title_text="Three Digits", row=3, col=1)
    fig.update_yaxes(title_text="Frequency", row=3, col=1)
    st.plotly_chart(fig, use_container_width=True)

st.title("## Benford's Law Test")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    column = st.selectbox("Select a column:", df.columns)
    if st.button("Run"):
        benfords_law_test(df, column)
