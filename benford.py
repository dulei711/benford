import streamlit as st
import pandas as pd
import math
from scipy.stats import chisquare
import matplotlib.pyplot as plt
import seaborn as sns

# set page title and icon
st.set_page_config(page_title='Newcomb Benford Law', page_icon=':bar_chart:', layout='wide')

# page header
st.write('# Newcomb Benford Law')

# file upload and column selection
file = st.file_uploader('Upload Excel file', type=['xlsx', 'xls'])
if file is not None:
    df = pd.read_excel(file)
    column = st.selectbox('Select a column to analyze', df.columns)

    # first digit analysis
    st.write('## First Digit Analysis')
    digit_position = 'First'
    data = df[column].astype(str).str[0].astype(int)
    first_digit_df = pd.DataFrame({'Digit': range(1, 10)})
    first_digit_df['Actual Frequency'] = data.value_counts(normalize=True).sort_index().values
    first_digit_df['Expected Frequency'] = [math.log10(1 + 1/d) for d in range(1, 10)]

    # update expected frequency dictionary based on position
    expected_freq_dict = {d: math.log10(1 + 1/d) for d in range(1, 10)}
    if digit_position == 'Second':
        expected_freq_dict = {d: 2 * freq for d, freq in expected_freq_dict.items()}
    elif digit_position == 'Third':
        expected_freq_dict = {d: 3 * freq for d, freq in expected_freq_dict.items()}

    # chi-square test
    st.write('### Chi-Square Test')
    st.write('Null Hypothesis: The observed and expected frequencies are not significantly different.')
    st.write('Alternative Hypothesis: The observed and expected frequencies are significantly different.')
    alpha = st.number_input('Significance level (alpha)', value=0.05, step=0.01, format='%g')
    chi2, p = chisquare(first_digit_df['Actual Frequency'], f_exp=first_digit_df['Expected Frequency'])
    st.write(f'Chi-square statistic: {chi2:.4f}')
    st.write(f'p-value: {p:.4f}')
    if p < alpha:
        st.write('Reject the null hypothesis.')
    else:
        st.write('Fail to reject the null hypothesis.')

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
    second_digit_df['Actual Frequency'] = data.value_counts(normalize=True).sort_index().values
    second_digit_df['Expected Frequency'] = [2 * freq for d, freq in expected_freq_dict.items()]

    # chart
    fig, ax = plt.subplots()
    sns.barplot(x='Digit', y='Frequency', data=pd.DataFrame({'Digit': range(0, 10), 'Frequency': second_digit_df['Actual Frequency']}))
    sns.lineplot(x='Digit', y='Expected Frequency', data=second_digit_df, color='red', marker='o')
    ax.set(xlabel='Digit', ylabel='Frequency', title=f'Second Digit Analysis ({column})')
    st.pyplot(fig)

    # third digit analysis
    st.write('## Third Digit Analysis')
    digit_position = 'Third'
    data = df[column].astype(str).str[2].astype(int)
    third_digit_df = pd.DataFrame({'Digit': range(0, 10)})
    third_digit_df['Actual Frequency'] = data.value_counts(normalize=True).sort_index().values
    third_digit_df['Expected Frequency'] = [3 * freq for d, freq in expected_freq_dict.items()]

    # chart
    fig, ax = plt.subplots()
    sns.barplot(x='Digit', y='Frequency', data=pd.DataFrame({'Digit': range(0, 10), 'Frequency': third_digit_df['Actual Frequency']}))
    sns.lineplot(x='Digit', y='Expected Frequency', data=third_digit_df, color='red', marker='o')
    ax.set(xlabel='Digit', ylabel='Frequency', title=f'Third Digit Analysis ({column})')
    st.pyplot(fig)
