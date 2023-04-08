import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chisquare

def calculate_expected_frequencies(df, column_name, digit_position):
    data = df[column_name]
    # Get the digit at the specified position for each value
    digits = data.apply(lambda x: str(x)[digit_position-1] if len(str(x)) >= digit_position else np.nan)
    digits = digits.dropna().astype(int)
    # Calculate the expected frequency for each digit based on the position
    if digit_position == 1:
        expected_freq = np.log10(1 + 1/np.arange(1, 10))
    elif digit_position == 2:
        expected_freq = np.log10(1 + 1/np.arange(10, 100))
        expected_freq = np.round(expected_freq / np.sum(expected_freq), 4)
        expected_freq_dict = dict(zip(range(10, 100), expected_freq))
    elif digit_position == 3:
        expected_freq = np.log10(1 + 1/np.arange(100, 1000))
        expected_freq = np.round(expected_freq / np.sum(expected_freq), 4)
        expected_freq_dict = dict(zip(range(100, 1000), expected_freq))
    # Convert the dictionary to a dataframe and rename the index column
    freq_df = pd.DataFrame.from_dict(expected_freq_dict, orient='index', columns=['Expected Frequency'])
    freq_df.index.name = 'Digit'
    # Calculate the actual frequency for each digit
    actual_freq_dict = dict(digits.value_counts(normalize=True))
    # Merge the expected and actual frequencies into a single dataframe
    freq_df = freq_df.merge(pd.DataFrame({'Digit': range(1, 10),
                                           'Actual Frequency': [actual_freq_dict.get(d, 0) for d in range(1, 10)]}),
                             on='Digit')
    return freq_df

def plot_frequencies(df):
    fig, ax = plt.subplots()
    ax.bar(df.index, df['Actual Frequency'], label='Actual')
    ax.plot(df.index, df['Expected Frequency'], color='red', label='Expected')
    ax.legend()
    ax.set_xlabel('Digit')
    ax.set_ylabel('Frequency')
    ax.set_title('Newcomb-Benford Law')
    st.pyplot(fig)

# Upload a file and get the column name
uploaded_file = st.file_uploader('Upload a file', type=['xlsx'])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.write('### Data Preview')
    st.write(df.head())
    column_name = st.selectbox('Select a column', options=df.columns)
    st.write(f'### Column: {column_name}')

    # Calculate the expected and actual frequencies for the first, second, and third digits
    st.write('### First Digit Analysis')
    first_digit_df = calculate_expected_frequencies(df, column_name, 1)
    st.write(first_digit_df)
    plot_frequencies(first_digit_df)

    st.write('### Second Digit Analysis')
    second_digit_df = calculate_expected_frequencies(df, column_name, 2)
    st.write(second_digit_df)
    plot_frequencies(second_digit_df)

    st.write('### Third Digit Analysis')
    third_digit_df = calculate_expected_frequencies(df, column_name, 3)
    st.write(third_digit_df)
    plot_frequencies(third_digit_df)

    # Perform the chi-square test on the first digit analysis
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
