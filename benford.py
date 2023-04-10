import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def benfords_law_test(df, column):    
    number_counts = df[column].value_counts()
    count_df = pd.DataFrame({'Number': number_counts.index, 'Count': number_counts.values})
    count_df['Observed Frequency'] = count_df['Count'] / count_df['Count'].sum()
    count_df['Expected Frequency'] = np.log10(1 + 1/count_df['Number']) / np.log10(10)
    st.table(count_df)
    
st.title("## Benford's Law Test")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    column = st.selectbox("Select a column:", df.columns)
    if st.button("Run"):
        benfords_law_test(df, column)
