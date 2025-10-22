

def set_llm_prompts(nr_of_sentences, previous_year, results_table):

    """Function to set dynamic LLM prompts based on user inputs.
    
    Args:
        nr_of_sentences (int): Number of sentences for background description.  
        previous_year (int): Previous year for analysis.
        results_table (pd.DataFrame): DataFrame containing the results table for analysis.
    Returns:
        dict: Dictionary containing LLM prompts.
    """

    prompts = {'background':        f"Describe the capital regime for an insurance undertaking in the EU and related \
                                      reporting requirements in {nr_of_sentences} sentences. Include reference to frequency \
                                      of reporting.",
           


               'results_analysis':  f"Analyse the movements in SCR and Own Funds separately based on the results table:\
                                    {results_table}. Identify trends in SCR and Own Funds and Solvency Ratio since \
                                    {previous_year} \
                                    in two sentences for each item of SCR, Own Funds and Solvency Ratio. \
                                    For SCR please explain which risks are driving the movements. Take into account that\
                                    the SCR is the sum of. Basic SCR, Operational risk and Deferred Tax Adjustment. \
                                    Basic SCR is the sum of Market Risk, Counterparty Default Risk, Life Risk, Health \
                                    Risk and Diversification Benefit. Diversification Benefit is not a risk, it is a negative \
                                    component of the Basic SCR and if the higher absolute value (i.e. more negative) Diversification \
                                    Benefit means that the portfolio is more diversified. Own Funds means available capital \
                                    or equity. The Solvency Ratio is the ratio of Own Funds and Total SCR.\
                                    Note that Operational Risk and Deferred Tax Adjustments are not part of the Basic SCR,\
                                    they are added to it to get the Total SCR. Do not attempt to recalculate the Solvency \
                                    Ratio by dividing Own Funds by the SCR and do not mention the movement \
                                    percentages, just comment on the direction of its change. When mentioning \
                                    movements in Solvency ratio plese do not mention \
                                    integers such as 1, 2 or 3 but rather percentages like 155.5% instead of 2."}
    


    return prompts


default_llm_response = {'background':   "The capital regime for an insurance undertaking in the EU is governed by the Solvency II Directive. This directive requires insurance undertakings to report their solvency to the supervisory authorities on a regular basis, typically quarterly or annually."}