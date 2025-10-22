import pandas as pd
import matplotlib.pyplot as plt
import base64
import numpy as np
from docx import Document
import os

# Write a function to generate a list of integers from 0 to 10

# Functions:
#
#       create_pie_charts
#       image_to_base64
#       count_pass_fail
#       perform_validation


def create_pie_charts(df, year, path):

    """Create a pie chart for the Basic SCR composition for a given year and save it to the specified path.
    
    Args:
        df (pd.DataFrame): DataFrame containing the SCR data.
        year (str): The year for which the pie chart is to be created (e.g., '2024').
        path (str): The file path where the pie chart image will be saved.
    Returns:
        None
    """

    # Select the first 4 rows of the dataframe, these include the BSCR modules:
    df_bscr_modules = df.head(4)

    # Labels from the '€m' column and values from the '2024' column
    labels = df_bscr_modules['€m']
    values = df_bscr_modules[year]

    # Create the pie chart
    plt.figure(figsize=(5, 5))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 8})

    # Display the chart
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save the chart as a png file (file name depends on whether the period is the current year or previous year):    
    plt.savefig(path)

    plt.close()

    return None


def image_to_base64(img_path):

    """Convert an image file to a base64 encoded string.
    Args:
        img_path (str): The file path of the image to be converted.

    Returns:
        str: Base64 encoded string of the image.
    """

    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def count_pass_fail(value, threshold):

    """Count pass/fail based on a threshold.
    Args:
        value (float): The value to be evaluated.
        threshold (float): The threshold for pass/fail evaluation.      
    Returns:
        str: 'pass' if value <= threshold, 'fail' if value > threshold, np.nan for non-numeric values.
    """

    if isinstance(value, (int, float)):
        if value > threshold:
            return 'fail'
        else:
            return 'pass'
    return np.nan  # Non-numeric values are ignored


def perform_validation(scr_table_df, current_year, previous_year):

    """Perform validation on the SCR table DataFrame.

    Args:
        scr_table_df (pd.DataFrame): DataFrame containing the SCR table data.
        current_year (str): The current year column name (e.g., '2024').
        previous_year (str): The previous year column name (e.g., '2023').
    Returns:
        pd.DataFrame: DataFrame indicating discrepancies in the SCR table.
    """

    # Retrieve the SCR results imported from Excel and change the Movement % column to numeric:
    scr_table_input = scr_table_df.copy()

    # Convert 'Movement %' from string percentage to float
    scr_table_input['Movement %'] = (
        scr_table_input['Movement %']
        .str.rstrip('%')        # Remove the '%' sign
        .astype(float) / 100    # Convert to float and divide by 100
    )

    # Initialise scr_table_expected as a DataFrame
    scr_table_expected = pd.DataFrame(scr_table_input)

    # Define input_cells mask with the same shape as scr_table_expected, initialized to False
    input_cells = pd.DataFrame(False, index=scr_table_expected.index, columns=scr_table_expected.columns)

    # Specifiy input cells - these cannot be checked as row input:
    input_cells['€m'] = True
    rows_to_exclude = [0, 1, 2, 3, 4, 6, 7, 9]  # Zero-based indices
    input_cells.loc[rows_to_exclude, [current_year, previous_year]] = True
    input_cells = input_cells.astype(bool)

    # Ensure scr_table_expected and scr_table_df have numeric data types:
    scr_table_expected = scr_table_expected.apply(pd.to_numeric, errors='coerce')
    scr_table_input =  scr_table_input.apply(pd.to_numeric, errors='coerce')

    # Calculate scr_table expected (totals, movements based on input data):

    # Totals check: 
    scr_table_expected.loc[5, [current_year, previous_year]] =  scr_table_input.iloc[:5][[current_year, previous_year]].sum()
    scr_table_expected.loc[8, [current_year, previous_year]] =  scr_table_input.iloc[5:8][[current_year, previous_year]].sum()
    scr_table_expected.loc[10, [current_year, previous_year]] =  scr_table_input.iloc[6:8][[current_year, previous_year]].sum()

    # Solvency ratio check:
    scr_table_expected.loc[10, current_year] = scr_table_input.loc[9, current_year] / scr_table_input.loc[8, current_year]
    scr_table_expected.loc[10, previous_year] = scr_table_input.loc[9, previous_year] / scr_table_input.loc[8, previous_year]

    scr_table_expected.loc[:, 'Movement'] = scr_table_input.loc[:, current_year] - scr_table_input.loc[:, previous_year]
    scr_table_expected.loc[:, 'Movement %'] = scr_table_input.loc[:, current_year] / scr_table_input.loc[:, previous_year] - 1

    # Compute absolute value of element-wise differences
    df_diff = scr_table_expected.subtract(scr_table_input).abs()

    # Apply the mask to set specified cells to NaN
    df_check = df_diff.mask(input_cells)


    # Replace NaN values with empty strings and round numeric values to 3 in the check:
    df_check = df_check.fillna('')

    # Put back categories into check dataframe:
    df_check["€m"] = scr_table_df["€m"]

    return df_check

