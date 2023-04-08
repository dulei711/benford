import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chisquare
import math

def first_digit(x):
    return int(str(x)[0])

def second_digit(x):
    return int(str(x)[1])

def third_digit(x):
    return int(str(x)[2])

def get_expected_counts(n):
    return [n * (math.log10(1 + 1/d) - math.log10(1 + 1/(d+1))) for d in range(1, 10)]

def analyze_data(df,column):
    data = df[column].dropna()
    n = len(data)
    first_digits = data.apply(first_digit)
    second_digits = data.apply(second_digit)
    third_digits = data.apply(third_digit)

    observed_counts_first = [sum(first_digits == d) for d in range(1, 10)]
    expected_counts_first = get_expected_counts(n)
    chi_square_first = chisquare(observed_counts_first, expected_counts_first)

    observed_counts_second = [sum(second_digits == d) for d in range(1, 10)]
    expected_counts_second = get_expected_counts(n)
    chi_square_second = chisquare(observed_counts_second, expected_counts_second)

    observed_counts_third = [sum(third_digits == d) for d in range(1, 10)]
    expected_counts_third = get_expected_counts(n)
    chi_square_third = chisquare(observed_counts_third, expected_counts_third)

    return {
        'observed_counts_first': observed_counts_first,
        'expected_counts_first': expected_counts_first,
        'chi_square_first': chi_square_first,
        'observed_counts_second': observed_counts_second,
        'expected_counts_second': expected_counts_second,
        'chi_square_second': chi_square_second,
        'observed_counts_third': observed_counts_third,
        'expected_counts_third': expected_counts_third,
        'chi_square_third': chi_square_third
    }

def plot_chart(counts, title):
    fig, ax = plt.subplots()
    ax.bar(range(1, 10), counts)
    ax.set_xlabel('Digit')
    ax.set_ylabel('Count')
    ax.set_title(title)
    st.pyplot(fig)

st.set_page_config(page_title='Fraud Detection using Newcomb Benford Law', page_icon=':guardsman:', layout='wide')

st.title('Fraud Detection using Newcomb Benford Law')
st.sidebar.title('Input Data')

uploaded_file = st.sidebar.file_uploader('Choose an Excel file', type=['xlsx'])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    column = st.selectbox("Select Column",df.columns)

    st.write('**Data sample:**')
    st.dataframe(df[column].head())

    st.write('**Analysis:**')
    result = analyze_data(df,column)
    st.write('First Digit Analysis:')
    st.write(f'Chi-Square Statistic: {result["chi_square_first"].statistic}')
    st.write(f'p-value: {result["chi_square_first"].pvalue}')
    plot_chart(result['observed_counts_first'], 'First Digit Counts')

    st.write('Second Digit Analysis:')
    st.write(f'Chi-Square Statistic: {result["chi_square_second"].statistic}')
    st.write(f'p-value: {result["chi_square_second"].pvalue}')
    plot_chart(result['observed_counts_second'], 'Second Digit Counts')

    st.write('Third Digit Analysis:')
    st.write(f'Chi-Square Statistic: {result["chi_square_third"].statistic}')
    st.write(f'p-value: {result["chi_square_third"].pvalue}')
    plot_chart(result['observed_counts_third'], 'Third Digit Counts')
