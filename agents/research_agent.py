# research_agent.py - Enhanced version
from dotenv import load_dotenv
import os
from langchain.tools.tavily_search import TavilySearchResults
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain.retrievers import TavilySearchAPIRetriever
from langchain.schema import Document

load_dotenv()

def research_agent_fn(state):
    query = state["input"]
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    
    if not tavily_api_key:
        raise ValueError("TAVILY_API_KEY is missing from the environment variables.")
    
    # Use LangChain's retriever for more structured data collection
    retriever = TavilySearchAPIRetriever(
        api_key=tavily_api_key,
        k=8,  # Number of results to retrieve
        include_domains=None,  # Optional: specific domains to include
        exclude_domains=None   # Optional: domains to exclude
    )
    
    # Get search results as documents
    docs = retriever.get_relevant_documents(query)
    
    # Extract sources for later reference
    sources = []
    for doc in docs:
        source = {
            "title": doc.metadata.get("title", "Untitled"),
            "url": doc.metadata.get("source", ""),
            "content": doc.page_content[:500]  # Truncate long content
        }
        sources.append(source)
    
    # Use LangChain to synthesize search results
    llm = Ollama(model="phi", temperature=0.3)
    
    synthesis_prompt = ChatPromptTemplate.from_template("""
    You are a research assistant. Organize and synthesize the following search results into a coherent summary.
    Focus on key information relevant to this query: {query}
    
    SEARCH RESULTS:
    {docs}
    
    Provide a well-structured summary that captures the essential information from these sources.
    Include factual information, statistics, and expert opinions when available.
    Organize by subtopic where appropriate.
    """)
    
    # Create a chain to process the documents
    synthesis_chain = (
        synthesis_prompt 
        | llm 
        | StrOutputParser()
    )
    
    # Format document content for the prompt
    formatted_docs = "\n\n".join([f"SOURCE {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])
    
    # Run the synthesis chain
    research_data = synthesis_chain.invoke({
        "query": query,
        "docs": formatted_docs
    })
    
    return {"research_data": research_data, "sources": sources}