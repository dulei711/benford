import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
from scipy.stats import kstest
import matplotlib.pyplot as plt

def p_value(observed_values, expected_values, digit):
    test_statistic, p_value = kstest(observed_values, expected_values)
    if p_value < 0.05:
        st.write("The column", column, "may contain fraudulent data (p-value =", p_value, ") on the ", digit, "digit")
    else:
        st.write("The column", column, "does not seem to contain fraudulent data (p-value =", p_value, ") on the ", digit, "digit")

def benfords_law_test(df, column):    
    number_counts = df[column].value_counts()
    count_df = pd.DataFrame({'Number': number_counts.index, 'Count': number_counts.values})
    count_df['Observed Frequency'] = count_df['Count'] / count_df['Count'].sum()
    count_df['Expected Frequency'] = np.log10(1 + 1/count_df['Number']) / np.log10(10)
    st.dataframe(count_df)
    
st.title("## Benford's Law Test")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    column = st.selectbox("Select a column:", df.columns)
    if st.button("Run"):
        benfords_law_test(df, column)
