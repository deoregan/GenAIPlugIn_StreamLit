import streamlit as st
from main import generate_report

# Set page title and icon before anything else and set the page layout to wide for better visibility of the app elements
st.set_page_config(page_title="Report Automation", page_icon="🚀", layout="wide")

#

# Streamlit App
def run_app():

    """Main function to run the Streamlit app."""

    # Sidebar - Year selection
    st.sidebar.header("Select Year")
    current_year          = st.sidebar.number_input("Select Current Year", min_value=2020, max_value=2050, value=2024)
    target_solvency_ratio = st.sidebar.number_input("Specify Target Solvency Ratio (%)", min_value=100, max_value=200, value=125)/100

    # Move radio buttons to the sidebar
    llm_flag              = st.sidebar.radio("Use AI commentary (Background and Result trends)", ["Yes", "No"], index=1)
    llm_provider          = st.sidebar.radio("AI model provider:", ["Gemini", "OpenAi"], index=0)
    llm_nr_of_sentences   = st.sidebar.number_input("Nr of sentences in Background section", min_value=1, max_value=10, value=2)
    
    conclusion_wording    = st.sidebar.text_area("Conclusion (text inserted at the end)", value = '')

    # Create two tabs
    tab1, tab2 = st.tabs(["SCR Report", "Validation Report"])

    # Add a button to trigger report generation
    if st.button("Generate Report"):

        # Reset report_generated to False if LLM flag changes (or force generation)
        if "report_generated" in st.session_state:
            st.session_state.report_generated = False  # Allow report generation again

        if "report_generated" not in st.session_state:
            st.session_state.report_generated = False

        # Check if the report has been generated already
        if not st.session_state.report_generated:
            # When the button is pressed, generate the report
            report_paths, validation_report_html_path = generate_report(
                current_year, target_solvency_ratio, conclusion_wording,
                llm_flag, llm_provider, llm_nr_of_sentences
            )

            html_report = report_paths['html']
            validation_html_report = validation_report_html_path

            # Update session state to prevent multiple generations
            st.session_state.report_generated = True  # Prevent multiple calls after first generation
            #st.success("Report generated successfully!")


            with tab1:
                # Try embedding the HTML file using an iframe
                try:
                    with open(html_report, "r", encoding="utf-8") as file:
                        html_content = file.read()

                    # Use an iframe to display the full HTML document
                    st.write(f"### Generated Report for {current_year}")
                    st.components.v1.html(html_content, height=800, scrolling=True)

                except FileNotFoundError:
                    st.error(f"File not found: {html_report}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                
            with tab2:
                # Try embedding the HTML file using an iframe
                try:
                    with open(validation_html_report, "r", encoding="utf-8") as file:
                        validation_html_content = file.read()

                    # Use an iframe to display the full HTML document
                    st.write(f"### Generated Validation Report for {current_year}")
                    st.components.v1.html(validation_html_content, height=800, scrolling=True)

                except FileNotFoundError:
                    st.error(f"File not found: {validation_html_report}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

        else:
            
            st.warning("Report already generated. You can only generate the report once in this session.")


# Run the Streamlit app
if __name__ == "__main__":
    run_app()