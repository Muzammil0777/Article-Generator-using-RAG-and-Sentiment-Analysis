import streamlit as st
import ollama
from langchain_community.document_loaders import DirectoryLoader
from utils.rag_utils import create_vector_store, get_rag_response, analyze_sentiment
from datetime import datetime

# Initialize session states
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def generate_prompt(context, input_text, no_words, writing_style):
    """Generate an improved prompt based on the style and context"""
    style_prompts = {
        'Academic': """You are a scholarly writer with expertise in academic writing. 
            Using the following context: {context}
            Write a well-researched article about: {input_text}
            Include relevant technical details and cite theoretical frameworks where applicable.
            The response should be approximately {no_words} words.
            Focus on methodology, findings, and academic implications.""",
        
        'Technical': """You are a technical expert writing for professionals.
            Using the following context: {context}
            Create a technical article about: {input_text}
            Include relevant technical concepts, methodologies, and practical implementations.
            The response should be approximately {no_words} words.
            Focus on technical accuracy and actionable insights.""",
        
        'Conversational': """You are a skilled writer creating content for a general audience.
            Using the following context: {context}
            Write an engaging and accessible article about: {input_text}
            Explain complex concepts in simple terms and use relatable examples.
            The response should be approximately {no_words} words.
            Focus on clarity and practical applications.""",
        
        'Journalistic': """You are a professional journalist.
            Using the following context: {context}
            Write a well-balanced news article about: {input_text}
            Present facts objectively and include relevant quotes or references.
            The response should be approximately {no_words} words.
            Focus on clarity, accuracy, and newsworthiness."""
    }
    
    return style_prompts[writing_style].format(
        context=context,
        input_text=input_text,
        no_words=no_words
    )

def getLLamaresponse(input_text, no_words, writing_style, use_rag=False):
    try:
        try:
            ollama.list()
        except ConnectionRefusedError:
            st.error("""Ollama server connection error. Please:
            1. Open Command Prompt as Administrator
            2. Run: netstat -ano | findstr :11434
            3. If you see a process, run: taskkill /PID XXXX /F (replace XXXX with the process ID)
            4. Run: ollama serve
            5. Refresh this page""")
            return None, None, None
        except Exception as e:
            st.error(f"""Ollama server error: {str(e)}
            Please make sure Ollama is properly installed and running.""")
            return None, None, None

        available_models = ollama.list()
        if not any(model.get('name') == 'llama3.2:latest' for model in available_models['models']):
            st.error("""llama3.2:latest model not found. Please:
            1. Run: ollama pull llama3.2:latest
            2. Wait for the download to complete
            3. Refresh this page""")
            return None, None, None

        if use_rag and st.session_state.vector_store:
            rag_response = get_rag_response(
                st.session_state.vector_store,
                input_text
            )
            context = rag_response['result']
            sources = [doc.metadata['source'] for doc in rag_response['source_documents']]
        else:
            context = ""
            sources = []
        
        prompt = generate_prompt(context, input_text, no_words, writing_style)
        
        response = ollama.generate(
            model="llama3.2:latest",
            prompt=prompt,
            options={
                "temperature": 0.7,
                "top_p": 0.9,
                "num_tokens": int(no_words) * 4
            }
        )
        
        # Analyze sentiment
        sentiment_analysis = analyze_sentiment(response['response'])
        
        # Store in chat history
        st.session_state.chat_history.append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'input': input_text,
            'style': writing_style,
            'words': no_words,
            'output': response['response'],
            'sentiment': sentiment_analysis,
            'sources': sources if sources else None
        })
        
        return response['response'], sources, sentiment_analysis
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None, None, None

# Streamlit App Configuration
st.set_page_config(
    page_title="Article Generator using RAG and Sentiment Analysis",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.header("Article Generator using RAG and Sentiment Analysis")

# Sidebar for RAG configuration and history
with st.sidebar:
    st.header("Configuration")
    
    # Document upload section
    st.subheader("Reference Documents")
    uploaded_files = st.file_uploader(
        "Upload reference documents",
        accept_multiple_files=True,
        type=['txt', 'pdf']
    )
    
    if uploaded_files:
        try:
            with st.spinner("Processing documents..."):
                st.session_state.vector_store = create_vector_store(uploaded_files)
            st.success("Documents processed successfully!")
        except Exception as e:
            st.error(f"Error processing documents: {str(e)}")
            st.session_state.vector_store = None
    
    # Chat history section
    st.subheader("Generation History")
    if st.session_state.chat_history:
        for idx, item in enumerate(reversed(st.session_state.chat_history)):
            with st.expander(f"#{len(st.session_state.chat_history)-idx}: {item['input'][:50]}..."):
                st.text(f"Timestamp: {item['timestamp']}")
                st.text(f"Style: {item['style']}")
                st.text(f"Target Words: {item['words']}")
                st.text("Input:")
                st.text(item['input'])
                st.text("Sentiment Analysis:")
                st.text(f"• Sentiment: {item['sentiment']['sentiment']}")
                st.text(f"• Tone: {item['sentiment']['tone']}")
                st.text(f"• Polarity: {item['sentiment']['polarity']}")
                st.text(f"• Subjectivity: {item['sentiment']['subjectivity']}")
                st.text("Output:")
                st.text(item['output'])
                if item['sources']:
                    st.text("Sources used:")
                    for source in item['sources']:
                        st.text(f"- {source}")
    
    if st.button("Clear History"):
        st.session_state.chat_history = []
        st.experimental_rerun()

# Main interface
col1, col2 = st.columns([7, 3])

with col1:
    input_text = st.text_area("Enter your topic or prompt", height=100)
    
    col_a, col_b = st.columns(2)
    with col_a:
        no_words = st.number_input("Target word count", min_value=100, max_value=5000, value=500, step=100)
    with col_b:
        writing_style = st.selectbox(
            'Writing style',
            ['Academic', 'Technical', 'Conversational', 'Journalistic'],
            index=2
        )
    
    use_rag = st.checkbox("Use uploaded documents as reference", value=True if st.session_state.vector_store else False)
    
    submit = st.button("Generate Article")

# Final Response
if submit:
    if not input_text.strip():
        st.warning("Please enter a topic or prompt.")
    else:
        with st.spinner("Generating article..."):
            response, sources, sentiment = getLLamaresponse(input_text, no_words, writing_style, use_rag)
            if response:
                st.markdown("### Generated Article:")
                st.write(response)
                
                st.markdown("### Sentiment Analysis:")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Sentiment", sentiment['sentiment'])
                with col2:
                    st.metric("Tone", sentiment['tone'])
                with col3:
                    st.metric("Polarity", sentiment['polarity'])
                with col4:
                    st.metric("Subjectivity", sentiment['subjectivity'])
                
                if sources:
                    st.markdown("### References Used:")
                    for source in sources:
                        st.write(f"- {source}")
            else:
                st.warning("Failed to generate response. Please check your Ollama setup.")

