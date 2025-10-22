# Prerequisites

Make sure that the following are installed:    
> 1. Python IDE (VSCode, Pycharm or Spyder) with Git extension
> 2. A software called *wkhtmltopdf* that convert html files to pdf documents (download from [here](https://wkhtmltopdf.com/downloads/))

Then follow these steps:    
> 3. Pull this repo with this command on terminal:      
> *git pull https://github.com/saidataanalytics/report_automation.git*    
> 4. Install all required Python libraries in one go with:      
> *pip install -r requirements.txt*    
      *Note*: This may reinstall a different version of already installed libraries and hence cause issues with dependencies. If you wish to avoid this then you can also install the libraries one by one with *pip install library_name*
> 5. Get API keys for Google Gemini and OpenAI (see details in the next section)
> 6. Set the values of these string variables at the top of *catalog.py* in the catalog folder:    
> *root_folder* : The path to your local repo (use C:/ for drives and / as subfolder separator, this should work on all operating systems including Windows).    
> *api_key_gemini* : Your Google Gemini API key.    
> *api_key_openai* : Your OpenAI API key.    

# Getting API keys (step 5 of Prerequisites)

## Google Gemini

Google provides free API keys for its AI models called Gemini. 

You need a Google account (sign up if you do not have one) and get your API key via the link below:    
[Google Account Sign Up](https:/accounts.google.com/signup)    
[Google AI Studio — API key page](https://aistudio.google.com/app/api-keys)    

More details on how to use Google Gemini API keys is provided in the documentation:
[Gemini API docs — how to get an API key](https://ai.google.dev/gemini-api/docs/api-key)

## OpenAI

The OpenAI API keys are not free but you only need to a small credit (a few euros) to use it up to millions of tokens on a pay as you go basis. 

You can sign up for an OpenAI account, add credit and get your API key via the links below:    
[OpenAI Account Sign Up](https://platform.openai.com/signup)    
[OpenaAI Billing Page](https://platform.openai.com/account/api-keys)    
[OpenAI API Page](https://openai.com/api/pricing/ )

# Running the application

Once all set, you can run the application with these command from terminal:

> *streamlit run app.py*

# Description of app functionality

This interactive application generates a report on SCR (Solvency Capital Requirement) results real-time based on:
 - Excel input table (saved in the input folder)
 - User inputs (shown in the sidebar of the app on the left hand side)
 - AI generated commentary (if selected by the user)

The report is generated real-time in three formats:
 - HTML (shown in the browswer on the SCR Report tab)
 - Pdf (saved in the output folder)
 - Word (saved in the output folder)

Furthermore, a validation report is also generated real-time to perform checks on internal consistency in two formats:
 - HTML (shown in the browser on the Validation Report tab)
 - Pdf (saved in the output folder)

The user has the following options shown in the sidebar on the left hand side:
 - Select Current Year (Excel inputs are available for 2024-2026)
 - Specity Target Solvency Ratio (%) 
 - Use AI commentary (Yes or No)
   - AI model provider (Gemini or OpenAI)
   - Nr of sentences in Background section (number)
 - Conclusion (text)

The current year selected will determine the source of results (e.g. if 2024 selected then the input file is input/tables/SCR_table_2024YE.xlxs) and will be used through-out the report and in the title.

The selected target solvency ratio is mentioned at the end of the report and will be updated in case the user changes the input in the sidebar. There is an option to add text to the conclusion at the end of the report, this should be useful e.g. if the solvency target is breached.

If AI commentary is selected (with Yes) then it will affect:
 - The Background section will be rewritten and will have the specified length
 - The results commentary below table providing explanations on movements in SCR, Own Funds and the Solvency Ratio

 The AI commentary is provided by sending the results to an LLM (Gemini or OpenAI) via an API using prompts. The response is built in the report real-time. (You can inpect the prompts in *catalog/llm_prompts.py*)

# Folder structure

The folders (bold), subfolders (italic) and files (highlight) used by app are listed below with explanation.

**(root folder)**  
| File | Description |
|------|-------------|
| `app.py` | Application — see *Running the application* section on how to launch it. |
| `main.py` | Main report generation function used by the application. Uses a number of helper functions. |
| `README.md` | This document. |
| `requirements.txt` | List of required Python libraries and their versions. Please refer to the *Prerequisites* section for installation guidance. |

**input**
| Subfolder | Description |
|-----------|-------------|
| *sample_report* | Sample SCR report before automation, i.e. prepared manually. |
|*tables* | Includes the result tables in Excel format (scr_table_YYYYYE.xlsx where YYYY varies between 2024-2026) |

**layout**              
| File | Description |
|------|-------------|
| `layout_scr_report.html` | HTML layout of the SCR report. |
| `layout_validation_report.html` | HTML layout of the validation report. |

**output**
| Subfolder | Description |
|-----------|-------------|
| *reports/YYYY* | SCR reports (in HTML, pdf and Word formats) and validation reports (in HTML and pdf formats) generated for year YYYY. |    
| *images/YYYY* | Images generated for year YYYY |

**catalog**           
| File | Description |
|------|-------------|
| `catalog.py` |  Catalog of files, folders and api keys. |
| `llm_prompts.py` | LLM prompts for Background section and explanation. |

**helpers**           
| File | Description |
|------|-------------|
| `api_calls.py` | API call - sends prompt to LLM (Google Gemini or OpenAI), takes response and incorporates in the report. |
| `create_reports.py` | Functions to create HTML reports from inputs and convert them to pdf and Word reports. |
| `formatting.py` | Formatting for tables and text in reports. |
| `generate_text.py` | Generate report commentary including movement analysis. |
| `utils.py` | Other utilities - conversion of images and perform validation. |

A more detailed description of helper functions is included in each Python script either at the top or as in-line comments.