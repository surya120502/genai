import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import streamlit as st

load_dotenv()

azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
azure_openai_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

client = AzureOpenAI(
    api_key=azure_openai_api_key,
    api_version=azure_openai_api_version,
    azure_endpoint=azure_openai_endpoint
)

def generate_code(prompt):
    try:
        with st.spinner("Generating code..."):
            response = client.chat.completions.create(
                model=azure_openai_deployment,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates code."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000  
            )
        generated_code = response.choices[0].message.content.strip()
        return generated_code
    except Exception as e:
        return str(e)

st.set_page_config(page_title="Surya Prakash", page_icon="💻", layout="centered")
# st.title("💻 Prompt and Code Generator")

# Navigation
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    st.markdown("""
        <style>
            .main {
                background: url('https://static.vecteezy.com/system/resources/thumbnails/022/965/844/original/animated-bw-robot-with-glowing-eyes-black-and-white-thin-line-icon-4k-footage-for-web-design-robotics-isolated-monochromatic-flat-element-animation-with-alpha-channel-transparency-video.jpg') no-repeat center center fixed; 
                background-size: cover;
                color: #333333;  /* Darker text color for better readability */
            }
            .welcome-container {
                position: absolute;
                bottom: 10px;
                left: 50%;
                transform: translateX(-50%);
                text-align: center;
            }
            .welcome-text {
                font-weight: bold;
                font-size: 19px; /* Smaller font size */
                margin-bottom: 5px;
            }
            .stButton button {
                background-color: #4CAF50;  /* Green button */
                color: white;
                font-size: 14px;  /* Smaller font size */
                font-weight: bold;
                padding: 10px 20px;
                border: none;
                cursor: pointer;
            }
            .stButton button:hover {
                background-color: #45a049;  /* Darker green on hover */
            }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="welcome-container"><div class="welcome-text">Welcome to the code generator app.</div></div>', unsafe_allow_html=True)
    if st.button("Let's Code", key="lets_code_button"):
        st.session_state.page = 'code_generation'
        st.rerun()

if st.session_state.page == 'code_generation':
    st.markdown("""
        <style>
            .main {
                background-color: #000000;  /* Black background color */
                color: #ffffff;  /* White text color */
                padding: 20px;
            }
            .welcome-container {
                text-align: center;
                margin-bottom: 20px;
            }
            .welcome-text {
                font-weight: bold;
                font-size: 18px;
            }
            .stButton button {
                background-color: #4CAF50;  /* Green button */
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 10px 20px;
                border: none;
                cursor: pointer;
            }
            .stButton button:hover {
                background-color: #45a049;  /* Darker green on hover */
            }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="welcome-container"><div class="welcome-text">Welcome to the code generator app.</div></div>', unsafe_allow_html=True)
    st.write("### Enter your prompt below:")
    user_input = st.text_area("Prompt:", height=150, help="Describe the code you need, e.g., 'Generate a Python function to add two numbers'.")

    if st.button("Generate Code"):
        if user_input:
            generated_code = generate_code(user_input)
            st.markdown("### Generated Code")
            st.code(generated_code, language='python')
        else:
            st.error("Please enter a prompt.")
