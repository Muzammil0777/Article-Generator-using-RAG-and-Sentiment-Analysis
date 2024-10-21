# import streamlit as st
# from langchain.prompts import PromptTemplate
# from langchain.llms import ctransformers
# from ctransformers import AutoModelForCausalLM
# import ollama

# ## Function to get response from my Ollama llama 3.2 model

# # def getLLamarespose(input_text,no_words,blog_style):
    
# #     ###llama3 model
# #     llm = ctransformers(model='muzam\AppData\Local\Ollama',
# #                         model_type='llama3.2',
# #                         config= {'max_new_tokens':256,
# #                                  'temperature':0.01})
    
# #     ## Prompt Template
    
# #     template= """
# #         Write a blog for {blog_style} job profile for a topic {input_text}
# #         within {no_words} words.
# #         """
# #     prompt = PromptTemplate(input_variables=["blog_style", "input_text", "no_words"],
# #                             template1=template) 
    
# #     ##Generate the response from the llama3 model
# #     response= llm(prompt.format(style= blog_style,text= input_text,n_words= no_words))   
# #     print(response)
# #     return response
        
# def getLLamarespose(input_text, no_words, blog_style):
#     # Correct way to load the model
#     llm = AutoModelForCausalLM.from_pretrained(r'C:\Users\muzam\AppData\Local\Ollama', model_type='llama3.2')

#     # Generate text based on the input prompt
#     prompt = f"Write {no_words} words in {blog_style} style on {input_text}."
#     response = llm(prompt)
    
#     return response
        
        
# st.set_page_config(
#     page_title="Ollama 3.2 Model",
#     page_icon=":robot:",
#     layout="centered",
#     initial_sidebar_state="collapsed"
# )

# st.header("Generate Blogs")

# input_text= st.text_input("Enter the blog topic")

# ##Creating two more columns for additional 2 fields

# col1,col2 = st.columns([5,5])

# with col1:
#     no_words = st.text_input("Number of words")
    
# with col2:
#     blog_style = st.selectbox('Writing the blog for ',
#                               ('Researchers','Data Scientist', 'Common People'),index=0)
    

# submit = st.button("Generate")

# ## Final Response
# if submit:
#     st.write(getLLamarespose(input_text,no_words,blog_style))






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


