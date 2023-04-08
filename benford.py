import pandas as pd
import numpy as np
import streamlit as st
from streamlit_pandas_profiling import st_profile_report
from newcomb_benford import detect

def load_data():
    file = st.file_uploader("Upload file", type=["xlsx", "xls"])
    if file is not None:
        df = pd.read_excel(file)
        return df

def analyze_data(data, column):
    first_digits = [int(str(i)[0]) for i in data[column] if i > 0]
    second_digits = [int(str(i)[1]) for i in data[column] if i > 0 and len(str(i)) >= 2]
    third_digits = [int(str(i)[2]) for i in data[column] if i > 0 and len(str(i)) >= 3]

    results = {
        "First Digit": detect(first_digits),
        "Second Digit": detect(second_digits),
        "Third Digit": detect(third_digits),
    }

    return results

st.title("Fraud Detection using Newcomb-Benford's Law")
st.write("This app uses Newcomb-Benford's Law to detect fraud in data.")

# Load data
df = load_data()
if df is not None:
    st.write("Data Preview:")
    st.write(df.head())

    # Select column to analyze
    columns = list(df.columns)
    column = st.selectbox("Select column to analyze:", options=columns)

    # Analyze data
    results = analyze_data(df, column)

    # Display results
    st.write("Results:")
    st.write(results)

    # Display chart
    st.write("Chart:")
    chart_data = pd.DataFrame.from_dict(results, orient="index")
    st.bar_chart(chart_data)
