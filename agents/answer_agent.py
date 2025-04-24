from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def answer_drafter_fn(state):
    research_data = state.get("research_data", "")
    question = state["input"]
    sources = state.get("sources", [])

    answer_template = ChatPromptTemplate.from_template("""
    You are an expert research assistant tasked with creating a comprehensive answer based on collected research.
    
    RESEARCH QUESTION: {question}
    
    RESEARCH DATA: 
    {research_data}
    
    Based on this research, provide a detailed, well-structured answer to the question.
    Your answer should:
    1. Begin with a clear summary of the key findings
    2. Present information in a logical, organized manner
    3. Include concrete examples, data, or evidence when available
    4. Address different perspectives or approaches where relevant
    5. End with a concise conclusion
    
    Write in a professional, informative tone suitable for academic or professional audiences.
    """)

    # Create and run the answer chain
    llm = Ollama(model="phi", temperature=0.3)
    answer_chain = (
        answer_template 
        | llm 
        | StrOutputParser()
    )
    
    result = answer_chain.invoke({
        "research_data": research_data,
        "question": question
    })

    return {"answer": result, "sources": sources}