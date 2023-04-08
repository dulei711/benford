import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chi2
import matplotlib.pyplot as plt

def benfords_law(data):
    # Calculate the frequency distribution of the first, second, and third digits
    first_digits = data.apply(lambda x: int(str(x)[0]))
    second_digits = data.apply(lambda x: int(str(x)[1]) if len(str(x)) >= 2 else 0)
    third_digits = data.apply(lambda x: int(str(x)[2]) if len(str(x)) >= 3 else 0)
    
    digit_counts = [first_digits.value_counts().sort_index(), 
                    second_digits.value_counts().sort_index(), 
                    third_digits.value_counts().sort_index()]
    
    digit_counts = [counts / counts.sum() for counts in digit_counts]

    # Calculate the expected frequency distribution according to Benford's Law
    expected_counts = np.log10(1 + 1 / np.arange(1, 10))
    expected_counts /= expected_counts.sum()
    expected_counts = [np.tile(expected_counts, (9, 1)).T ** (i - 1) for i in range(1, 4)]
    expected_counts = [counts / counts.sum() for counts in expected_counts]

    # Calculate the difference between the observed and expected frequency distributions
    chi_squared = sum(((counts - expected_counts[i]) ** 2 / expected_counts[i]).sum() for i, counts in enumerate(digit_counts))
    p_value = 1 - chi2.cdf(chi_squared, 24)

    return digit_counts, expected_counts, chi_squared, p_value

st.set_page_config(page_title="Fraud Detection with Benford's Law", page_icon=":guardsman:")

st.title("Fraud Detection with Benford's Law")

# Creating a file uploader widget
file = st.file_uploader("Upload file", type=['csv', 'xls', 'xlsx', 'txt'])

# Checking if a file is uploaded or not
if file is not None:
    # If the file is a CSV
    if file.type == 'text/csv':
        df = pd.read_csv(file)
    # If the file is an Excel spreadsheet
    elif file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        df = pd.read_excel(file)
    # If the file is a TXT file
    elif file.type == 'text/plain':
        df = pd.read_csv(file, sep='\t', header=None)
    # For all other file types
    else:
        st.write("File type not supported")
    
    st.write("Sample data:")
    st.write(df.head())
    column_data = st.selectbox('Select the column to evaluate fraud!', df.columns)
    if st.button("Run"):
        # Analyze data with Benford's Law
        digit_counts, expected_counts, chi_squared, p_value = benfords_law(column_data)

        # Display results
        st.write('First Digit Counts:')
        st.write(digit_counts[0])

        st.write('First Digit Expected Counts:')
        st.write(expected_counts[0])

        st.write('Second Digit Counts:')
        st.write(digit_counts[1])

        st.write('Second Digit Expected Counts:')
        st.write(expected_counts[1])

        st.write('Third Digit Counts:')
        st.write(digit_counts[2])

        st.write('Third Digit Expected Counts:')
        st.write(expected_counts[2])

        st.write('Chi-Squared:')
        st.write(chi_squared)

        st.write('P-Value:')
        st.write(p_value)

        # Plot results
        fig, axs = plt.subplots(1, 3, figsize=(10, 4))
        for i, ax in enumerate(axs):
            ax.bar(range(1, 10), digit_counts[i], label='Observed', color='C0')
            ax.plot(range(1, 10), expected_counts[i], label='Expected', color='C1', marker='o')
            ax.set_xlabel(f'{["First", "Second", "Third"][i]} Digit')
            ax.set_ylabel('Frequency')
            ax.set_title(f'Benford\'s Law Analysis ({["First", "Second", "Third"][i]} Digit)')
            ax.legend()

        st.pyplot(fig)
else:
    st.write("No File uploaded")
