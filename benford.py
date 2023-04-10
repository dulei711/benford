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
    # First position
    observed_values_1 = df[column].astype(str).str[0].value_counts().sort_index()
    expected_values_1 = pd.Series([np.log10(1 + 1 / i) for i in observed_values1) * len(df[column])
    p_value(observed_values_1, expected_values_1, "first")
        
    # Second position
    observed_values_2 = df[column].astype(str).str[:2].value_counts().sort_values()
    expected_values_2 = pd.Series([np.log10(1 + 1 / i) for i in observed_values2) * len(df[column])
    p_value(observed_values_2, expected_values_2, "second")
        
    # Third position
    observed_values_3 = df[column].astype(str).str[:3].value_counts().sort_values()
    expected_values_3 = pd.Series([np.log10(1 + 1 / i) for i in observed_values3) * len(df[column])
    p_value(observed_values_3, expected_values_3, "third")
        
    # Compile results into a DataFrame
    observed_values = pd.concat([observed_values_1, observed_values_2, observed_values_3], axis=1)
    observed_values.columns = ['First Digit', 'First 2 Digits', 'First 3 Digits']
    
    expected_values = pd.concat([expected_values_1, expected_values_2, expected_values_3], axis=1)
    expected_values.columns = ['First Digit', 'First 2 Digits', 'First 3 Digits']
    
    freq_df = pd.concat([observed_values, expected_values], axis=1)
    freq_df = freq_df.fillna(0)
    freq_df = freq_df.astype(int)
    freq_df.index.name = 'Digit'
    freq_df['Difference'] = freq_df['First Digit'] - freq_df['First Digit'].apply(lambda x: round(x))
    
    return st.dataframe(freq_df)

st.title("## Benford's Law Test")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    column = st.selectbox("Select a column:", df.columns)
    if st.button("Run"):
        benfords_law_test(df, column)
