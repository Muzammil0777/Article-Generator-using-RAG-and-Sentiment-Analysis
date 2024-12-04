from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain.docstore.document import Document
from textblob import TextBlob
import tempfile
import os
import PyPDF2

def analyze_sentiment(text):
    """Analyze sentiment of the text"""
    analysis = TextBlob(text)
    
    # Get polarity score (-1 to 1)
    polarity = analysis.sentiment.polarity
    
    # Get subjectivity score (0 to 1)
    subjectivity = analysis.sentiment.subjectivity
    
    # Determine sentiment category
    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    # Determine tone based on subjectivity
    if subjectivity < 0.3:
        tone = "Objective"
    elif subjectivity > 0.7:
        tone = "Subjective"
    else:
        tone = "Balanced"
    
    return {
        'sentiment': sentiment,
        'tone': tone,
        'polarity': round(polarity, 2),
        'subjectivity': round(subjectivity, 2)
    }

def process_pdf(file_path):
    """Extract text from PDF file"""
    text = ""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        raise Exception(f"Error processing PDF {os.path.basename(file_path)}: {str(e)}")
    return text

def create_vector_store(uploaded_files):
    """Create a FAISS vector store from uploaded files"""
    documents = []
    
    with tempfile.TemporaryDirectory() as temp_dir:
        for uploaded_file in uploaded_files:
            temp_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_path, 'wb') as f:
                f.write(uploaded_file.getvalue())
            
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            try:
                if file_extension == '.pdf':
                    text = process_pdf(temp_path)
                else:  # .txt files
                    with open(temp_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                
                if text.strip():
                    doc = Document(
                        page_content=text,
                        metadata={
                            "source": uploaded_file.name,
                            "type": file_extension
                        }
                    )
                    documents.append(doc)
            except Exception as e:
                raise Exception(f"Error processing {uploaded_file.name}: {str(e)}")
    
    if not documents:
        raise Exception("No valid documents were processed")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    texts = text_splitter.split_documents(documents)
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    vector_store = FAISS.from_documents(texts, embeddings)
    return vector_store

def get_rag_response(vector_store, query, style="detailed"):
    """Get response using RAG"""
    llm = Ollama(model="llama3.2:latest")
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={'k': 3}),
        return_source_documents=True
    )
    
    return qa_chain(query) 