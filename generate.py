import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import streamlit as st
import streamlit as st

groq_api_key = st.secrets["GROQ_API_KEY"]


# Load environment variables
load_dotenv()

# Initialize Groq LLM
# groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(temperature=0.7, groq_api_key=groq_api_key, model_name="llama-3.1-70b-versatile")

# Define the output parser
json_parser = JsonOutputParser()

# Define the prompt template
prompt_template = PromptTemplate(
    input_variables=["text"],
    template="""
     Based on the following text, generate 5 multiple-choice questions (MCQs) with 4 options each. 
    Ensure that one option is correct and the others are plausible but incorrect.
    Make sure the questions are not repeated and conform to the given text.
    Format the output as a JSON object with the following structure:
    [
        {{
            "question": "1. [Question text here]",
            "choices": [
                "a) [Option A text]",
                "b) [Option B text]",
                "c) [Option C text]",
                "d) [Option D text]"
            ],
            "answer": "[Correct option in full]"
        }},
        // ... 4 more questions ...
    ]
    
    Text: {text}
    """

)

def generate_mcqs(text):
    # Combine the prompt template and output parser
    chain = prompt_template | llm | json_parser
    
    try:
        # Generate MCQs
        result = chain.invoke({"text": text})
        return result
    except OutputParserException as e:
        st.error(f"Error parsing output: {e}")
        return None