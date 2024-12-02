# Article Generator using RAG and Sentiment Analysis

An advanced article generation system that combines Retrieval-Augmented Generation (RAG) with sentiment analysis to create context-aware, style-specific content while providing emotional and tonal insights.

## Features

- **RAG Integration**: Utilizes user-provided documents as reference material
- **Multiple Writing Styles**:
  - Academic: Scholarly writing with citations and technical details
  - Technical: Professional content focused on technical accuracy
  - Conversational: Engaging content for general audiences
  - Journalistic: Balanced news-style articles
- **Sentiment Analysis**:
  - Emotional tone detection
  - Subjectivity analysis
  - Polarity measurement
- **Document Support**:
  - Text files (.txt)
  - PDF documents (.pdf)
- **History Tracking**:
  - Saves generated articles
  - Tracks sentiment metrics
  - Records reference sources
- **Customization**:
  - Adjustable word count (100-5000 words)
  - Style selection
  - Reference toggle

## Quick Start

1. **Clone and Setup**:

```bash
git clone https://github.com/yourusername/article-generator-rag.git
cd article-generator-rag
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Install Ollama**:
- Download from [Ollama's website](https://ollama.ai/download)
- Install and pull the model:

```bash
ollama pull llama3.2:latest
```

3. **Run the Application**:

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start Streamlit
streamlit run app.py
```

4. **Access**: Open `http://localhost:8501` in your browser

## Project Structure
```
article-generator-rag/
├── app.py                 # Main Streamlit application
├── utils/
│   └── rag_utils.py      # RAG and sentiment analysis utilities
├── requirements.txt      # Project dependencies
└── README.md            # Documentation
```

## Dependencies

```txt
streamlit
ollama
langchain
langchain-community
faiss-cpu
sentence-transformers
textblob
PyPDF2
python-dotenv
```

## Usage Guide

1. **Upload Documents**:
   - Use sidebar to upload reference materials (.txt or .pdf)
   - System processes documents for RAG

2. **Configure Generation**:
   - Enter your topic/prompt
   - Select word count (100-5000)
   - Choose writing style
   - Enable/disable RAG

3. **Generate and Analyze**:
   - Click "Generate Article"
   - View generated content
   - Check sentiment metrics:
     - Overall sentiment (Positive/Negative/Neutral)
     - Tone (Objective/Subjective/Balanced)
     - Polarity score (-1 to 1)
     - Subjectivity level (0 to 1)

4. **History Management**:
   - View past generations
   - Check previous configurations
   - Review sentiment analyses
   - Clear history as needed

## System Requirements

- Python 3.8+
- 8GB RAM (minimum)
- Storage for models
- Windows/Linux/MacOS

## Error Handling

The system handles:
- Ollama server connection issues
- Document processing errors
- Model availability
- File format validation
- Empty documents
- Generation failures

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## Future Enhancements

- Additional document formats
- More writing styles
- Enhanced sentiment analysis
- Multi-language support
- Custom model integration
- Export functionality
- Advanced RAG configurations

## License

MIT License. See `LICENSE` for details.

## Acknowledgments

- [Ollama](https://ollama.ai/) - LLM Integration
- [LangChain](https://www.langchain.com/) - RAG Framework
- [TextBlob](https://textblob.readthedocs.io/) - Sentiment Analysis
- [Streamlit](https://streamlit.io/) - Web Interface

## Contact

Your Name - [@yourgithub](https://github.com/yourgithub)
Project Link: [https://github.com/yourusername/article-generator-rag](https://github.com/yourusername/article-generator-rag)

## Support

For support:
1. Check existing issues
2. Create new issue with details
3. Contact maintainers
4. Join community discussions

---
Made with ❤️ by [Your Name]