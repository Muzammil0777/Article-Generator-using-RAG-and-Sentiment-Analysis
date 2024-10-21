import streamlit as st
import ollama

def getLLamaresponse(input_text, no_words, blog_style):
    try:
        # Generate text based on the input prompt
        prompt = f"Write a blog in the style of {blog_style} on the topic {input_text} within {no_words} words."

        # Generate the response from the Ollama model
        response = ollama.generate(model="llama3.2", prompt=prompt)
        
        return response['response']
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Streamlit App Configuration
st.set_page_config(
    page_title="Ollama LLaMA Model",
    page_icon=":robot:",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.header("Generate Blogs")

input_text = st.text_input("Enter the blog topic")

# Creating two more columns for additional fields
col1, col2 = st.columns([5, 5])

with col1:
    no_words = st.text_input("Number of words")

with col2:
    blog_style = st.selectbox('Writing the blog for ',
                              ('Researchers', 'Data Scientist', 'Common People'), index=0)

submit = st.button("Generate")

# Final Response
if submit:
    response = getLLamaresponse(input_text, no_words, blog_style)
    if response:
        st.write(response)
    else:
        st.warning("Failed to generate response. Please check your Ollama setup.")


