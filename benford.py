import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import log10, floor

def first_digit(num):
    return int(str(num)[0])

def second_digit(num):
    return int(str(num)[1])

def third_digit(num):
    return int(str(num)[2])

def get_first_digits(data):
    return data.apply(first_digit)

def get_second_digits(data):
    return data.apply(second_digit)

def get_third_digits(data):
    return data.apply(third_digit)

def get_newcomb_benford_law(digit):
    return np.array([log10(1 + 1/d) for d in range(1, 10)]).cumsum() + log10(1/2)

def plot_newcomb_benford_law(data, digit):
    digits = [get_first_digits, get_second_digits, get_third_digits]
    titles = ["First Digit", "Second Digit", "Third Digit"]
    db = digits[digit](data)
    counts = db.value_counts(normalize=True).sort_index()
    expected_counts = get_newcomb_benford_law(digit)
    fig, ax = plt.subplots()
    ax.bar(counts.index, counts.values, label="Actual")
    ax.plot(range(1, 10), 10**expected_counts, "o-", label="Expected")
    ax.set_xticks(range(1, 10))
    ax.set_xticklabels(range(1, 10))
    ax.set_title(f"{titles[digit]} Distribution")
    ax.set_xlabel("Digit")
    ax.set_ylabel("Frequency")
    ax.legend()
    st.pyplot(fig)

st.title("Newcomb-Benford's Law for Fraud Detection")
st.write("This app analyzes an Excel file column using Newcomb-Benford's Law to detect fraud and displays an awesome chart of the analysis.")
st.write("Upload an Excel file:")
uploaded_file = st.file_uploader("", type=["xlsx"])
if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)
    column = st.selectbox("Select a column:", data.columns)
    digit = st.selectbox("Select a digit:", ["First Digit", "Second Digit", "Third Digit"])
    if digit == "First Digit":
        plot_newcomb_benford_law(data[column], 0)
    elif digit == "Second Digit":
        plot_newcomb_benford_law(data[column], 1)
    elif digit == "Third Digit":
        plot_newcomb_benford_law(data[column], 2)
