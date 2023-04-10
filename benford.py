import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chisquare
from bokeh.io import output_notebook, show
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


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
    
    # create the first digit plot
    source1 = ColumnDataSource(dict(x=range(1, 10), y=first_digit_freq, y_obs=first_digit_freq_obs))
    p1 = figure(title="Benford's Law Analysis: First Digit", x_axis_label="First Digit", y_axis_label="Frequency", tooltips=[("Expected Frequency", "@y"), ("Observed Frequency", "@y_obs")])
    p1.vbar(x='x', top='y', width=0.5, color='blue', alpha=0.5, legend_label='Expected Frequency', source=source1)
    p1.vbar(x='x', top='y_obs', width=0.5, color='red', alpha=0.5, legend_label='Observed Frequency', source=source1)
    p1.legend.location = "top_right"

    # create the two digits plot
    source2 = ColumnDataSource(dict(x=range(10, 100), y=two_digit_freq, y_obs=two_digit_freq_obs))
    p2 = figure(title="Benford's Law Analysis: Two Digits", x_axis_label="Two Digits", y_axis_label="Frequency", tooltips=[("Expected Frequency", "@y"), ("Observed Frequency", "@y_obs")])
    p2.vbar(x='x', top='y', width=0.5, color='blue', alpha=0.5, legend_label='Expected Frequency', source=source2)
    p2.vbar(x='x', top='y_obs', width=0.5, color='red', alpha=0.5, legend_label='Observed Frequency', source=source2)
    p2.legend.location = "top_right"

    # create the three digits plot
    source3 = ColumnDataSource(dict(x=range(100, 1000), y=three_digit_freq, y_obs=three_digit_freq_obs))
    p3 = figure(title="Benford's Law Analysis: Three Digits", x_axis_label="Three Digits", y_axis_label="Frequency", tooltips=[("Expected Frequency", "@y"), ("Observed Frequency", "@y_obs")])
    p3.vbar(x='x', top='y', width=0.5, color='blue', alpha=0.5, legend_label='Expected Frequency', source=source3)
    p3.vbar(x='x', top='y_obs', width=0.5, color='red', alpha=0.5, legend_label='Observed Frequency', source=source3)
    p3.legend.location = "top_right"
    
    # update layout and display plot
    st.bokeh_chart(pio.to_bokeh(fig))

st.title("## Benford's Law Test")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    column = st.selectbox("Select a column:", df.columns)
    if st.button("Run"):
        benfords_law_test(df, column)
