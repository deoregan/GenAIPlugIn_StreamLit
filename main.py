# Import python libraries:
import os
import pandas as pd
import warnings
import time

# Import catalog and helper functions:
from catalog.catalog import folders, filenames
from helpers.formatting import format_scr_table
from helpers.utils import create_pie_charts, perform_validation
from helpers.create_reports import create_html_report, create_pdf_report, create_word_report, create_validation_report

# Turn off all FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Function to generate SCR report in HTML and PDF formats:
def generate_report(current_year, target_solvency_ratio = 1.25, conclusion_wording = '', 
                    llm_flag = 'No', llm_provider = 'Gemini', llm_nr_of_sentences = 2,
                    output_formats = ['html', 'pdf', 'docx'],  validation_threshold = 0.001):

    """Function to generate the SCR and validation reports.
    
    Args:
        current_year (int): The current year for the report.
        target_solvency_ratio (float): The target solvency ratio.
        conclusion_wording (str): Text to be inserted at the end of the report. 
        llm_flag (str): Flag to indicate if LLM should be used.
        llm_provider (str): The provider of the LLM.
        llm_nr_of_sentences (int): The number of sentences to generate with the LLM.
        output_formats (list): The desired output formats for the report.
        validation_threshold (float): The threshold for validation checks.
    Returns:
        report_paths (dict): Paths to the generated reports.
    """

    # Start runtime measurement:
    start_time = time.time()

    # Calculate previous year from current:
    previous_year = current_year - 1

    # Import data:
    input_tables_folder    = folders['input_tables']
    scr_table_df           = pd.read_excel(f"{input_tables_folder}scr_table_{current_year}YE.xlsx", usecols = "A:E")
    scr_table_df_formatted = format_scr_table(scr_table_df, previous_year, current_year)

    # Set output images folder:
    output_images_folder                    = folders['output_images'] + str(current_year) + '/'

    # Create pie charts for the composition of the Basic SCR and save in the images folder - current year:
    bscr_current_chart_filename             = str(current_year) + '_' + filenames['bscr_current_chart'] 
    bscr_current_chart_path                 = os.path.join(output_images_folder, bscr_current_chart_filename)
    create_pie_charts(scr_table_df, current_year, bscr_current_chart_path)

    # Create pie charts for the composition of the Basic SCR and save in the images folder - previous year:
    bscr_previous_chart_filename            = str(previous_year) + '_' + filenames['bscr_previous_chart'] 
    bscr_previous_chart_path                = os.path.join(output_images_folder, bscr_previous_chart_filename)
    create_pie_charts(scr_table_df, previous_year, bscr_previous_chart_path)

    # Create html report:
    report_paths, report_html  = create_html_report(folders, filenames, current_year, previous_year, scr_table_df_formatted, 
                                                    llm_flag, llm_provider, llm_nr_of_sentences,
                                                    target_solvency_ratio, conclusion_wording)

    # Convert HTML Report to pdf if pdf output format selected by the user and updater output paths:
    if 'pdf' in output_formats:
        report_paths = create_pdf_report(folders, report_paths, current_year)

    # Convert HTML Report to pdf if pdf output format selected by the user and update output paths:
    if 'docx' in output_formats:
        report_paths = create_word_report(folders, report_paths, report_html, current_year)

    # Perform validation:
    df_check = perform_validation(scr_table_df, current_year, previous_year)

    # Create validation report:
    validation_report_html_path, _  = create_validation_report(df_check, folders, current_year, previous_year, validation_threshold)

    # Stop runtime measurement:
    end_time = time.time()    
    runtime  = end_time - start_time

    # Print runtime:
    print('Runtime of generating reports: ', round(runtime, 2), 'seconds')    

    # Return the HTML and PDF reports:
    return report_paths, validation_report_html_path
