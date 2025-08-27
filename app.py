# app.py

import os
import gradio as gr
from transformers import pipeline
from helpers import remove_non_ascii, product_assistant
from langchain_ibm import WatsonxLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models.utils.enums import GenTextParamsMetaNames as GenParams

# ---------------- IBM Watsonx LLM Initialization ----------------

project_id = "skills-network"
credentials = Credentials(
    url="https://us-south.ml.cloud.ibm.com",
    # api_key="<YOUR_API_KEY>"  #  Put your API key here
)

model_id = "ibm/granite-3-3-8b-instruct"
parameters = {
    GenParams.DECODING_METHOD: "sample",
    GenParams.MAX_NEW_TOKENS: 512,
    GenParams.MIN_NEW_TOKENS: 1,
    GenParams.TEMPERATURE: 0.5,
    GenParams.TOP_K: 50,
    GenParams.TOP_P: 1,
}

llm = WatsonxLLM(
    model_id=model_id,
    url="https://us-south.ml.cloud.ibm.com",
    project_id=project_id,
    params=parameters,
)

# ---------------- Prompt Template ----------------

prompt_file = os.path.join("prompts", "meeting_prompt.txt")
prompt = ChatPromptTemplate.from_file(prompt_file)

# ---------------- Chain ----------------

chain = (
    {"context": RunnablePassthrough()}  # Pass the transcript as context
    | prompt
    | llm
    | StrOutputParser()
)

# ---------------- Speech-to-Text & Processing ----------------

def transcript_audio(audio_file):
    # Pipeline Whisper
    pipe = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-tiny.en",
        chunk_length_s=30,
    )
    raw_transcript = pipe(audio_file, batch_size=8)["text"]
    
    # Clean transcript
    ascii_transcript = remove_non_ascii(raw_transcript)
    adjusted_transcript = product_assistant(ascii_transcript, credentials, project_id)
    
    # Generate meeting minutes & tasks
    result = chain.invoke({"context": adjusted_transcript})
    result = result.lstrip("} \n")  # remove any extra leading characters

    # Save to outputs folder
    os.makedirs("outputs", exist_ok=True)
    output_file = os.path.join("outputs", "meeting_minutes_and_tasks.txt")
    with open(output_file, "w") as file:
        file.write(result)

    return result, output_file

# ---------------- Gradio Interface ----------------

audio_input = gr.Audio(sources="upload", type="filepath", label="Upload your audio file")
output_text = gr.Textbox(label="Meeting Minutes and Tasks")
download_file = gr.File(label="Download the Generated Meeting Minutes and Tasks")

iface = gr.Interface(
    fn=transcript_audio,
    inputs=audio_input,
    outputs=[output_text, download_file],
    title="AI Meeting Assistant",
    description="Upload an audio file of a meeting. This tool will transcribe the audio, fix product-related terminology, and generate meeting minutes along with a list of tasks."
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=5000,share=True)
