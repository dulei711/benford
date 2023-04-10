import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def benfords_law_test(df, column):    
    number_counts = df[column].value_counts()
    st.dataframe(number_counts)
    count_df = pd.DataFrame({'Number': number_counts.index, 'Count': number_counts.values})
    count_df['Observed Frequency'] = count_df['Count'] / count_df['Count'].sum()
    count_df['Expected Frequency'] = np.log10(1 + 1/count_df['Number']) / np.log10(10)

    # Plot the observed and expected frequencies
    plt.plot(count_df['Number'], count_df['Observed Frequency'], 'bo-', label='Observed Frequency')
    plt.plot(count_df['Number'], count_df['Expected Frequency'], 'r^-', label='Expected Frequency')
    plt.xscale('log')
    plt.xlabel('Number')
    plt.ylabel('Frequency')
    plt.title('Benford\'s Law Test')
    plt.legend()
    plt.show()
    st.pyplot(fig)
    
st.title("## Benford's Law Test")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    column = st.selectbox("Select a column:", df.columns)
    if st.button("Run"):
        benfords_law_test(df, column)
