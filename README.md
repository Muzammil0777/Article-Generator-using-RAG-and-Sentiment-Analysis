# Blog-Generation-AI-tool

# Ollama Streamlit Blog Generator

This project is a Streamlit-based web application that uses the Ollama LLaMA model to generate blog posts on various topics. Users can specify the topic, word count, and target audience for the blog post.

## Features

- Generate blog posts using Ollama's LLaMA model
- Customize blog topic, word count, and style
- User-friendly interface built with Streamlit

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7+
- [Ollama](https://github.com/jmorganca/ollama) installed and set up on your system
- The "llama3.2" model available in your Ollama installation

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/your-username/ollama-streamlit-blog-generator.git
   cd ollama-streamlit-blog-generator
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Ensure the Ollama server is running:
   ```
   ollama serve
   ```

2. In a new terminal window, navigate to the project directory and activate the virtual environment.

3. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

4. Open your web browser and go to `http://localhost:8501` to use the application.

## How to Use

1. Enter the blog topic in the text input field.
2. Specify the desired word count.
3. Select the target audience from the dropdown menu.
4. Click the "Generate" button to create your blog post.

## Troubleshooting

If you encounter any issues:

1. Check that Ollama is properly installed and the server is running.
2. Ensure the "llama3.2" model is available (`ollama list`).
3. Verify that all dependencies are installed correctly.
4. Check the debug information in the sidebar of the Streamlit app.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## Acknowledgments

- [Ollama](https://github.com/jmorganca/ollama) for providing the LLaMA model integration
- [Streamlit](https://streamlit.io/) for the web application framework
