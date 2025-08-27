# utils/helpers.py

from ibm_watsonx_ai.foundation_models import ModelInference, TextChatParameters
from ibm_watsonx_ai import Credentials

def remove_non_ascii(text):
    """
    Remove non-ASCII characters from a string
    """
    return ''.join(i for i in text if ord(i) < 128)


def product_assistant(ascii_transcript, credentials: Credentials, project_id: str):
    """
    Process the transcript to adjust financial product terminology and produce a structured output.
    
    Parameters:
    - ascii_transcript: str, input transcript
    - credentials: IBM Watsonx Credentials object
    - project_id: str, IBM project ID

    Returns:
    - str: Adjusted transcript content from Llama 3.2
    """

    system_prompt = """You are an intelligent assistant specializing in financial products;
    your task is to process transcripts of earnings calls, ensuring that all references to
    financial products and common financial terms are in the correct format. For each
    financial product or common term that is typically abbreviated as an acronym, the full term 
    should be spelled out followed by the acronym in parentheses. For example, '401k' should be
    transformed to '401(k) retirement savings plan', 'HSA' should be transformed to 'Health Savings Account (HSA)' , 'ROA' should be transformed to 'Return on Assets (ROA)', 'VaR' should be transformed to 'Value at Risk (VaR)', and 'PB' should be transformed to 'Price to Book (PB) ratio'. Similarly, transform spoken numbers representing financial products into their numeric representations, followed by the full name of the product in parentheses. For instance, 'five two nine' to '529 (Education Savings Plan)' and 'four zero one k' to '401(k) (Retirement Savings Plan)'. However, be aware that some acronyms can have different meanings based on the context (e.g., 'LTV' can stand for 'Loan to Value' or 'Lifetime Value'). You will need to discern from the context which term is being referred to  and apply the appropriate transformation. In cases where numerical figures or metrics are spelled out but do not represent specific financial products (like 'twenty three percent'), these should be left as is. Your role is to analyze and adjust financial product terminology in the text. Once you've done that, produce the adjusted transcript and a list of the words you've changed"""
    
    # Concatenate the system prompt and the user transcript
    prompt_input = system_prompt + "\n" + ascii_transcript

    # Create messages object
    messages = [
        {
            "role": "user",
            "content": prompt_input
        }
    ]

    # Llama 3.2 model parameters
    model_id = "meta-llama/llama-3-2-11b-vision-instruct"
    params = TextChatParameters(
        temperature=0.2,  # Controls randomness; lower values make output more deterministic
        top_p=0.6         # Nucleus sampling to control output diversity
    )

    # Initialize Llama model inference
    llama32 = ModelInference(
        model_id=model_id,
        credentials=credentials,
        project_id=project_id,
        params=params
    )

    # Send input messages to model and get response
    response = llama32.chat(messages=messages)

    # Return the first choice content
    return response['choices'][0]['message']['content']
