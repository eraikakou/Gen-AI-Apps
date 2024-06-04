import streamlit as st
import openai
import yaml
from azure.identity import DefaultAzureCredential
from azure.ai.openai import OpenAIClient


def create_azure_openai_client(config_path):
    """
    Create and return an Azure OpenAI client using the settings from a configuration file.

    Args:
        config_path (str): Path to the YAML configuration file with Azure OpenAI settings.

    Returns:
        OpenAIClient: An authenticated Azure OpenAI client.
    """
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    credential = DefaultAzureCredential()
    client = OpenAIClient(endpoint=config['endpoint'], credential=credential)
    return client


def get_completion(client, prompt, model):
    """
    Get the completion from the OpenAI model using the given prompt.

    Args:
        client (OpenAIClient): The Azure OpenAI client.
        prompt (str): The prompt to send to the OpenAI model.
        model (str): The name of the OpenAI model to use for completion.

    Returns:
        dict: The completion response from the OpenAI model.
        dict: Token usage details.
    """
    response = client.completions.create(
        engine=model,
        prompt=prompt,
        max_tokens=1000
    )
    return response, response.usage


def translate_java_to_python(client, java_code, prompt, model="text-davinci-003"):
    """
    Translate Java code to Python using the OpenAI model.

    Args:
        client (OpenAIClient): The Azure OpenAI client.
        java_code (str): The Java code to be translated.
        prompt (str): The prompt for the translation.
        model (str, optional): The name of the OpenAI model to use. Defaults to "text-davinci-003".

    Returns:
        str: The translated Python code.
    """
    full_prompt = f"{prompt}\n\nJava Code:\n{java_code}\n\nPython Code:"
    response, _ = get_completion(client, full_prompt, model)
    python_code = response.choices[0].text.strip()
    return python_code



# Set the app to wide mode
st.set_page_config(layout="wide")

# Function to simulate translation (replace with actual translation logic)
def translate_java_to_python(java_code, prompt):
    # Mock translation logic for demonstration purposes
    # Normally, you would send the prompt and Java code to the ChatGPT API for translation
    python_code = java_code.replace("System.out.println", "print")  # Simple example
    return python_code

# Header Section
st.title("Java to Python Code Translator")
st.markdown("### Leveraging AI for Code Translation")

# Instructions Section
st.markdown("""
    This web app uses AI to translate Java code into Python code in real-time. 
    Simply enter your Java code and a prompt for ChatGPT in the input boxes below and click 'Translate' to see the Python translation.
""")

# Create two columns for input
col1, col2 = st.columns(2)

# Java Code Input Section
with col1:
    st.header("Java Code Input")
    java_code = st.text_area("Enter Java Code Here:", height=300, placeholder="Type or paste your Java code here...")

# Prompt Input Section
with col2:
    st.header("Prompt for ChatGPT")
    prompt = st.text_area("Enter your prompt for ChatGPT here:", height=300, placeholder="Describe what you want ChatGPT to do...")

# Placeholder for translated code
translated_code = ""

# Translation Button
if st.button("Translate"):
    if java_code and prompt:
        # Translate Java to Python
        translated_code = translate_java_to_python(java_code, prompt)
    else:
        st.warning("Please enter both Java code and a prompt to translate.")

# Create two columns for output
col3, col4 = st.columns(2)

# Display the code with syntax highlighting
with col3:
    if java_code:
        st.header("Java Code")
        st.markdown(f"```java\n{java_code}\n```", unsafe_allow_html=True)

with col4:
    if translated_code:
        st.header("Translated Python Code")
        st.markdown(f"```python\n{translated_code}\n```", unsafe_allow_html=True)

# Footer Section (Optional)
st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        text-align: center;
        padding: 10px;
    }
    </style>
    <div class="footer">
        <p>Developed by [Your Name]</p>
    </div>
""", unsafe_allow_html=True)
