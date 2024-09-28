import streamlit as st
import pandas as pd

# Streamlit App Title
st.title("Series Generator for Data Inputs")

# Input Fields
st.header("Input Fields")

# Optional Input Fields
plant_abbr = st.text_input("Plant Abbreviation (Optional)", value="").upper() or None
section_abbr = st.text_input("Section Abbreviation (Optional)", value="").upper() or None
data_source = st.text_input("Data Source (Optional)", value="") or None

# Replace dashes with underscores in the Data Source Abbreviation
data_source_abbr = st.text_input("Data Source Abbreviation (Optional)", value="").replace("-", "_").upper() or None

stream_name = st.text_input("Stream Name (Optional)", value="") or None
stream_abbr = st.text_input("Stream Abbreviation (Optional)", value="").upper() or None

# Engineering Unit Description and Abbreviation
eng_unit_desc = st.text_input("Engineering Unit Description (Optional)", value="") or None
eng_unit_abbr = st.text_input("Engineering Unit Abbreviation", value="%")

# Dropdown for Aggregation input with the values from the screenshot
aggregation = st.selectbox("Aggregation", [
    "max", "min", "mean", "mean_nan", "count", "total", "weighted_average",
    "latest_value", "calculation"
])

# Free text input for Process instead of dropdown
process = st.text_input("Process (Optional)", value="") or None

# Adjust the Engineering Unit abbreviation for "Percentage" case
if eng_unit_abbr == "%":
    name_suffix = "PER"
else:
    name_suffix = eng_unit_abbr  # Use the entered abbreviation as the suffix if not Percentage

# Generate series on button click
if st.button("Generate Series"):
    # Initialize list to hold the series data
    series_data = []

    # Generate series name conditionally based on the presence of inputs
    series_name_parts = [
        plant_abbr,
        section_abbr,
        data_source_abbr,
        stream_abbr,
        name_suffix
    ]
    # Filter out any None values from the list
    series_name = "_".join(filter(None, series_name_parts)).upper()
    description = f"{stream_name or ''} {eng_unit_desc or ''}".strip()

    # Append the generated series data to a dictionary
    series_data.append({
        "name": series_name,
        "description": description,
        "is_calculation": "FALSE",
        "fill_method": "",
        "source_series": "",
        "target_series": "",
        "sample_period": "",
        "weighted_average_series": "",
        "aggregation": aggregation,
        "name_formula": "",
        "engineering_unit": eng_unit_abbr,  # Keep % for Engineering Unit in engineering_unit column
        "series_type": "",
        "process": process
    })

    # Convert the series data to a DataFrame for display
    df = pd.DataFrame(series_data)

    # Display the generated DataFrame
    st.subheader("Generated Series Data")
    st.dataframe(df)

    # Download the DataFrame as a CSV file
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='generated_series.csv',
        mime='text/csv',
    )