import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import OrderedDict
import math

st.set_page_config(page_title='Newcomb-Benford Law', page_icon=':bar_chart:', layout='wide')

st.write('# Newcomb-Benford Law')
st.write('This app uses the Newcomb-Benford Law to detect anomalies in the first three digits of a column in an Excel file. To get started, please upload an Excel file below.')

uploaded_file = st.file_uploader('Upload Excel file', type=['xlsx'])
if uploaded_file is not None:
    st.write('## Configuration')
    st.write('## Data Preview')
    df = pd.read_excel(uploaded_file)
    column = st.selectbox("Select Column",df.columns)
    st.write(df.head())

    # first digit analysis
    st.write('## First Digit Analysis')
    digit_position = 'First'
    data = df[column].astype(str).str[0].astype(int)
    first_digit_df = pd.DataFrame({'Digit': range(1, 10)})
    first_digit_df['Actual Frequency'] = data.value_counts(normalize=True).sort_index().values
    expected_freq_dict = OrderedDict([(d, round(math.log10(1 + 1 / d), 4)) if d != 9 else 0.1197 for d in range(1, 10)])
    first_digit_df['Expected Frequency'] = [expected_freq_dict[d] for d in range(1, 10)]

    # chart
    fig, ax = plt.subplots()
    sns.barplot(x='Digit', y='Frequency', data=pd.DataFrame({'Digit': range(1, 10), 'Frequency': first_digit_df['Actual Frequency']}))
    sns.lineplot(x='Digit', y='Expected Frequency', data=first_digit_df, color='red', marker='o')
    ax.set(xlabel='Digit', ylabel='Frequency', title=f'First Digit Analysis ({column})')
    st.pyplot(fig)

    # second digit analysis
    st.write('## Second Digit Analysis')
    digit_position = 'Second'
    data = df[column].astype(str).str[1].astype(int)
    second_digit_df = pd.DataFrame({'Digit': range(0, 10)})
    second_digit_df
