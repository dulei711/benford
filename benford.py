import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
from scipy.stats import kstest

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    def chi_square_test(df, column):
        categories = pd.unique(df[column])
        obs_freq = []
        for cat in categories:
            obs_freq.append(sum(df[column] == cat))
        exp_freq = [len(df[column]) / len(categories)] * len(categories)
        chi2, p, dof, ex = chi2_contingency([obs_freq, exp_freq])
        if p < 0.05:
            st.write("The column", column, "may contain fraudulent data (p-value =", p, ")")
        else:
            st.write("The column", column, "does not seem to contain fraudulent data (p-value =", p, ")")

    def benfords_law_test(df, column):
        observed_values = df[column].astype(str).str[0].value_counts().sort_index()
        expected_values = pd.Series([np.log10(1 + 1 / i) for i in range(1, 10)], index=[str(i) for i in range(1, 10)]) * len(df[column])
        test_statistic, p_value = kstest(observed_values, expected_values)
        if p_value < 0.05:
            st.write("The column", column, "may contain fraudulent data (p-value =", p_value, ")")
        else:
            st.write("The column", column, "does not seem to contain fraudulent data (p-value =", p_value, ")")

    column = st.selectbox("Select a column to analyze", df.columns)
    st.write("### Chi-Squared Test")
    chi_square_test(df, column)
    st.write("### Benford's Law Test")
    benfords_law_test(df, column)
