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
    fig, axs = plt.subplots(3, 1, figsize=(20, 10))
    
    # First position
    observed_values_1 = df[column].astype(str).str[0].value_counts().sort_index()
    expected_values_1 = pd.Series([np.log10(1 + 1 / i) for i in range(1, 10)], index=[str(i) for i in range(1, 10)]) * len(df[column])
    p_value(observed_values_1, expected_values_1, "first")
    st.dataframe = observed_values_1
    
    # Second position
    observed_values_2 = df[column].astype(str).str[:2].value_counts().sort_values()
    expected_values_2 = pd.Series([np.log10(1 + 1 / i) for i in range(1, 100)], index=[str(i) for i in range(0, 99)]) * len(df[column])
    p_value(observed_values_2, expected_values_2, "second")
    st.dataframe(observed_values_2)
    
    # Third position
    observed_values_3 = df[column].astype(str).str[:3].value_counts().sort_values()
    expected_values_3 = pd.Series([np.log10(1 + 1 / i) for i in range(1, 1000)], index=[str(i) for i in range(0, 999)]) * len(df[column])                    
    p_value(observed_values_3, expected_values_3, "third")
    st.dataframe = observed_values_3

    
st.title("## Benford's Law Test")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    column = st.selectbox("Select a column:", df.columns)
    if st.button("Run"):
        benfords_law_test(df, column)
