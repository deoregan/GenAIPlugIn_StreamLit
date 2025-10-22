import os
from catalog.llm_prompts import default_llm_response
import openai
import google.generativeai as genai

# Import catalog:
from catalog.catalog import api_keys

# Generate LLM response (ChatGPT or Gemini) if llm_flag = True, otherwise return default prompt.
def llm_response(prompt, llm_flag, provider='Gemini'):

    """Function to get LLM response based on the selected provider and flag.

    Args:
        prompt (str): The prompt to send to the LLM.
        llm_flag (str): Flag indicating whether to use the LLM or not.
        provider (str): The LLM provider to use (e.g., 'OpenAI' or 'Gemini').
    Returns:
        str: The response from the LLM or the default response.
    """


    if llm_flag != 'Yes':
        return default_llm_response['background']

    prov = (provider or '').strip().lower()

    if prov == 'openai':
        api_key = api_keys.get('openai')
    elif prov == 'gemini':
        api_key = api_keys.get('gemini')
    else:
        raise ValueError(f"Unknown provider: {provider}")

    if not api_key:
        raise RuntimeError(f"API key for {provider} not found or empty.")

    # Use the OpenAI or Gemini API to get the response
    # OpenAI
    if prov == 'openai':                 
        # REQUIRED for openai==0.28
        openai.api_key = api_key

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Your system message here."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
        )
        response_text = response['choices'][0]['message']['content']

    # Google Gemini
    else:  
        genai.configure(api_key=api_key)

        # Use the latest high-quality Gemini model
        model = genai.GenerativeModel("models/gemini-2.5-pro")

        response = model.generate_content(prompt)
        response_text = response.text

    return response_text