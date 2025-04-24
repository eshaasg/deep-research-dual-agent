<p align="center">
    <img src="https://github.com/user-attachments/assets/34895ddf-4a79-4ef6-adaf-45512d0ec1b8" alt="banner" height="250" width = "450">
</p>

# Deep Research Dual Agent 👾

A powerful AI research assistant that combines web search capabilities with local language models to deliver comprehensive answers to complex questions.

# Overview 🛰️

Deep Research Dual Agent employs a sophisticated two-agent system that:
1. **Research Agent**: Collects and synthesizes information from the web using Tavily Search API
2. **Answer Agent**: Transforms research data into well-structured, comprehensive answers using local LLMs

The result is a powerful research tool that provides accurate, up-to-date responses with full transparency about sources.

# How it works 🚀
### Initial Build
Started with a dual-agent architecture using LangChain and LangGraph to create a research system that combines web search capabilities with local language model processing.

### Data Collection
Leveraged Tavily Search API to retrieve relevant information from across the web, organizing results into structured documents with source tracking.

### LLM Integration 
Chose Phi model via Ollama for its efficiency and local processing capabilities. It synthesizes web content and generates comprehensive answers based on user research questions.

### Streamlit Interface
Built a clean, intuitive Streamlit UI where users can enter research questions and receive detailed answers with supporting information.

### Source Management
Implemented transparent source tracking that displays original URLs, titles, and content snippets for verification and further exploration.

### Performance

Speed: 5-8s for scraping, 7–10s for responses

Impact: Cuts outreach drafting time by ~70%

# How to run it 🛠️
### 1. Install dependencies
   ```bash
   pip install -r requirements.txt
```

### 2. Create a .env file in the project root directory
 Get your API key [here](https://app.tavily.com/home)
   ```bash
    TAVILY_API_KEY=your_tavily_api_key_here
```

### 3. Make sure Ollama is installed and the phi model is available
 If you havent already you can download it [here](https://ollama.com/download)
   ```bash
    ollama pull phi
```

### 4. Usage
 Start the Streamlit application 
```bash
streamlit run main.py
```

# Demo  


    

   
