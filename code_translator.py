import streamlit as st

# Set the app to wide mode
st.set_page_config(layout="wide")

# Function to simulate translation (replace with actual translation logic)
def translate_java_to_python(java_code):
    # Mock translation logic for demonstration purposes
    python_code = java_code.replace("System.out.println", "print")  # Simple example
    return python_code

# Header Section
st.title("Java to Python Code Translator")
st.markdown("### Leveraging AI for Code Translation")

# Instructions Section
st.markdown("""
    This web app uses AI to translate Java code into Python code in real-time. 
    Simply enter your Java code in the input box below and click 'Translate' to see the Python translation.
""")

# Create two columns
col1, col2 = st.columns(2)

# Java Code Input Section
with col1:
    st.header("Java Code Input")
    java_code = st.text_area("Enter Java Code Here:", height=300, placeholder="Type or paste your Java code here...")

# Translation Button and Python Code Output Section
translated_code = ""
if st.button("Translate"):
    if java_code:
        # Translate Java to Python
        translated_code = translate_java_to_python(java_code)
    else:
        st.warning("Please enter Java code to translate.")

# Python Code Output Section
with col2:
    st.header("Translated Python Code")
    st.text_area("Python Code:", value=translated_code, height=300)

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
