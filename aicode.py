import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 🎨 Custom CSS for Styling
st.markdown("""
    <style>
        body {
            background-color: #1e1e2e;
            color: white;
            font-family: 'Arial', sans-serif;
        }
        .stTextArea textarea {
            background-color: #282c34;
            color: #61dafb;
            font-size: 16px;
            border-radius: 8px;
        }
        .stButton>button {
            background-color: #ff7b00;
            color: white;
            border-radius: 8px;
            transition: all 0.3s ease-in-out;
        }
        .stButton>button:hover {
            background-color: #ff4b00;
            transform: scale(1.05);
        }
        .stSpinner {
            color: #ff7b00;
        }
        .review-box {
            background-color: #262626;
            padding: 15px;
            border-radius: 10px;
            font-size: 16px;
            color: #ffffff;
        }
    </style>
""", unsafe_allow_html=True)

# 🎯 Configure Gemini API
load_dotenv()

# Get API Key from .env
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API securely
genai.configure(api_key=API_KEY)

# 📌 AI Model Configuration
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

# 🔍 Function to Generate Code Review
def generate_code_review(code_snippet):
    prompt = f"""
    You are an expert Python code reviewer. Analyze the following code and provide a structured review:
    - **Identify any syntax errors or potential bugs.**
    - **Suggest improvements for readability and maintainability.**
    - **Highlight security concerns, if any.**
    - **Recommend best coding practices.**

    Code Snippet:
    ```python
    {code_snippet}
    ```

    Review:
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {e}"

# 🚀 Main App UI
def main():
    st.title("🧑‍💻 AI Code Reviewer 💡")
    
    st.write("""
    **🔎 Get instant feedback on your Python code!**  
    - Paste your code below or upload a `.py` file.  
    - Click **Review Code** to analyze and improve your code.
    """)
    
    # 📂 File Upload Option
    uploaded_file = st.file_uploader("📄 Upload a Python file", type=["py"])
    
    if uploaded_file:
        code_snippet = uploaded_file.read().decode("utf-8")
    else:
        code_snippet = st.text_area("✍️ Paste your code here:", height=250)

    # 🎬 Animated Button & Review Generation
    if st.button("🔍 Review Code"):
        if not code_snippet.strip():
            st.warning("⚠️ Please provide a code snippet.")
        else:
            with st.spinner("🚀 Analyzing your code..."):
                review = generate_code_review(code_snippet)
                st.success("✅ Review Completed!")

                # 📝 Display Review with a Styled Box
                st.markdown(f"""
                <div class='review-box'>
                {review.replace('\n', '<br>')}
                </div>
                """, unsafe_allow_html=True)

                # 📌 Display the Original Code with Syntax Highlighting
                st.subheader("📌 Your Code:")
                st.code(code_snippet, language="python")

if __name__ == "__main__":
    main()
