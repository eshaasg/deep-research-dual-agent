import streamlit as st
from graph.research_graph import app

st.set_page_config(page_title="Deep Research AI", layout="wide")
st.title("Deep Research AI")
st.markdown("Enter a research question. The AI will collect online data and generate a detailed answer locally using LLaMA 3.")

query = st.text_input("Enter your research question:", placeholder="e.g. What are the latest trends in Quantum Machine Learning?")

if query:
    with st.spinner("Running agents..."):
        result = app.invoke({"input": query})
    
    # Combine answer and research data into a single response
    combined_response = result.get("answer", "")
    
    if "research_data" in result and result["research_data"]:
        # Append research data to the answer with a separator
        combined_response += "\n\n---\n\n**Supporting Research Data:**\n\n" + result["research_data"]
    
    st.subheader("Comprehensive Answer")
    st.markdown(combined_response)

    # Optional: Show sources if available
    if "sources" in result and result["sources"]:
        with st.expander("View Sources"):
            for i, source in enumerate(result["sources"], 1):
                st.markdown(f"{i}. **{source.get('title', 'No title')}**")
                if 'url' in source:
                    st.markdown(f"   [Read more]({source['url']})")
                if 'content' in source:
                    st.markdown(f"   *{source['content'][:200]}...*")
                st.write("---")
    
    # Add Related URLs section at the end
    if "sources" in result and result["sources"]:
        st.subheader("Related URLs")
        st.markdown("Here are some relevant links for further reading:")
        url_list = []
        for source in result["sources"]:
            if 'url' in source:
                title = source.get('title', 'Untitled')
                url_list.append(f"- [{title}]({source['url']})")
        
        if url_list:
            st.markdown("\n".join(url_list))
        else:
            st.markdown("No related URLs found.")