'''import streamlit as st
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
    expected_values_1 = pd.Series([np.log10(1 + 1 / i) for i in range(1, 10)], index=[str(i) for i in range(1, 10)]) * len(df[column])
    p_value(observed_values_1, expected_values_1, "first")
    st.table(observed_values_1)
    
    # Second position
    observed_values_2 = df[column].astype(str).str[:2].value_counts().sort_values()
    expected_values_2 = pd.Series([np.log10(1 + 1 / i) for i in range(1, 100)], index=[str(i) for i in range(0, 99)]) * len(df[column])
    p_value(observed_values_2, expected_values_2, "second")
    st.table(observed_values_2)
    
    # Third position
    observed_values_3 = df[column].astype(str).str[:3].value_counts().sort_values()
    expected_values_3 = pd.Series([np.log10(1 + 1 / i) for i in range(1, 1000)], index=[str(i) for i in range(0, 999)]) * len(df[column])                    
    p_value(observed_values_3, expected_values_3, "third")
    st.table(observed_values_3)
'''

import pandas as pd
import numpy as np
import streamlit as st
from scipy.stats import chisquare

def benfords_law_test(df, column):    
    # First position
    observed_values_1 = df[column].astype(str).str[0].value_counts().sort_index()
    expected_values_1 = pd.Series([np.log10(1 + 1 / i) for i in range(1, 10)], index=[str(i) for i in range(1, 10)]) * len(df[column])
    p_value_1 = chisquare(observed_values_1, expected_values_1)[1]
    
    # Second position
    observed_values_2 = df[column].astype(str).str[:2].value_counts().sort_index()
    expected_values_2 = pd.Series([np.log10(1 + 1 / i) for i in range(1, 100)], index=[str(i).zfill(2) for i in range(1, 100)]) * len(df[column])
    p_value_2 = chisquare(observed_values_2, expected_values_2)[1]
    
    # Third position
    observed_values_3 = df[column].astype(str).str[:3].value_counts().sort_index()
    expected_values_3 = pd.Series([np.log10(1 + 1 / i) for i in range(1, 1000)], index=[str(i).zfill(3) for i in range(1, 1000)]) * len(df[column])
    p_value_3 = chisquare(observed_values_3, expected_values_3)[1]
    
    # Create a dataframe for the comparison of observed and expected frequencies
    df_comparison = pd.DataFrame({
        'Digit': [f'{i}' for i in range(1,10)] + [f'{i:02}' for i in range(10,100)] + [f'{i:03}' for i in range(100,1000)],
        'Observed Frequency': list(observed_values_1.values) + list(observed_values_2.values) + list(observed_values_3.values),
        'Expected Frequency': list(expected_values_1.values) + list(expected_values_2.values) + list(expected_values_3.values)
    })
    
    # Add a column for the p-values
    df_comparison['p-value'] = [p_value_1] * 9 + [p_value_2] * 90 + [p_value_3] * 900
    
    return df_comparison

    
st.title("## Benford's Law Test")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    column = st.selectbox("Select a column:", df.columns)
    if st.button("Run"):
        benfords_law_test(df, column)
