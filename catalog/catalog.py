# Set user-specific inputs
# See ReadMe file for instructions on how to obtain API keys
root_folder     = 'C:/Users/User/Documents/Bence/Coding/report_automation/scr_report'
api_key_gemini  = 'your_gemini_api_key_here'
api_key_openai  = 'your_openai_api_key_here'


# Catalog of folders, filenames and API keys - do not change 
folders = {  'root':                               root_folder,
             'input_tables':                      'input/tables/',
             'layout':                            'layout/',
             'output_reports':                    'output/reports/',
             'output_images':                     'output/images/'}

filenames = {'bscr_current_chart':                'composition_basic_scr_current.png', 
             'bscr_previous_chart':               'composition_basic_scr_previous.png',
             'scr_report_layout':                 'layout_scr_report.html',
             'validation_report_layout_filename': 'layout_validation_report.html'}

api_keys =  {'gemini':                            api_key_gemini,
             'openai':                            api_key_openai}   