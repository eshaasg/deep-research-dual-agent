import streamlit as st
import streamlit.components.v1 as components
import base64
from datetime import datetime

st.set_page_config(
    page_title="Deep Research AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def local_css():
    st.markdown("""
    <style>
        /* Overall page styling */
        .stApp {
            background-color: #111827;
            font-family: 'SF Pro Text', 'Helvetica Neue', sans-serif;
            color: #E5E7EB;
        }
        
        /* Header styling */
        .main-header {
            padding: 1rem 0 0.5rem 0;  /* Reduced padding */
            border-bottom: 1px solid #374151;
            margin-bottom: 0.5rem;  /* Reduced margin */
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .app-title {
            color:#ff1f3e;
            font-size: 60px;
            font-weight: 550;
            margin: 0;
        }
        
        /* Input area styling */
        .stTextInput>div>div>input {
            background-color: #1F2937;
            color: #F9FAFB;
            border: 1px solid #374151;
        }
        
        .stTextInput div {
            padding: 0.5rem;
        }
        
        /* Message styling */
        .message-container {
            max-width: 900px;
            margin: 0 auto;
            padding: 0 1rem;
        }
        
        .user-message {
            background-color: #1F2937;
            border-radius: 0.75rem;
            padding: 1rem;
            margin: 1rem 0;
            border-left: 4px solid #6366F1;
            color: #F3F4F6;
        }
        
        .assistant-message {
            background-color: #111827;
            border-radius: 0.75rem;
            padding: 1rem;
            margin: 1rem 0;
            border-left: 4px solid #10B981;
            box-shadow: 0 1px 3px rgba(0,0,0,0.3);
            color: #F3F4F6;
            border: 1px solid #374151;
        }
        
        /* Date display - reduced margin */
        .date-display {
            color: #9CA3AF;
            font-size: 0.975rem;
            margin: 0.2rem 0 0.5rem 0;  /* Top margin reduced from 0.8rem to 0.2rem */
        }
        
        /* Response styling */
        .stMarkdown {
            line-height: 1.6;
            color: #F3F4F6;
        }
        
        .source-item {
            padding: 0.75rem;
            border-bottom: 1px solid #374151;
        }
        
        /* Button styling */
        .stButton button {
            background-color: #FFFFFF;
            color: #000f48;
            border-radius: 0.5rem;
            border: none;
            padding: 0.3rem 3rem;
            font-weight: 900;
        }
        
        .stButton button:hover {
            background-color: #000f48;
            color: #FFFFFF;
        }
        
        /* Remove default Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        
        /* Spinner */
        .stSpinner > div > div {
            border-top-color: #4F46E5 !important;
        }
        
        /* Remove padding/margin from main container */
        .block-container {
            padding-top: 0.5rem;  /* Reduced from 1rem */
            padding-bottom: 1rem;
            max-width: 1000px;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            font-size: 0.875rem;
            color: #D1D5DB;
            background-color: #1F2937;
            border: 1px solid #374151;
            border-radius: 0.5rem;
        }
        
        .streamlit-expanderContent {
            border: none;
            background-color: #1F2937;
        }
        
        /* Header styling */
        h1, h2, h3, h4, h5, h6 {
            color: #F9FAFB !important;
        }
        
        /* Link styling */
        a {
            color: #93C5FD !important;
        }
        
        a:hover {
            color: #BFDBFE !important;
        }
        
        /* Code blocks */
        code {
            background-color: #374151 !important;
            color: #F3F4F6 !important;
        }
        
        /* Input placeholder */
        ::placeholder {
            color: #9CA3AF !important;
        }
    </style>
    """, unsafe_allow_html=True)

def render_logo():
    st.markdown(
        """
        <div class="main-header">
            <h1 class="app-title">Deep Research AI 👾</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

def display_date():
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    st.markdown(f'<p class="date-display">Today is {current_date}</p>', unsafe_allow_html=True)

# Main app
def main():
    local_css()
    render_logo()
    display_date()
    
    st.markdown('<div class="message-container">', unsafe_allow_html=True)
    
    # Input area
    query = st.text_input("", placeholder="Enter your research question (e.g. What are the latest trends in Quantum Machine Learning?)", key="research_query")
    col1, col2 = st.columns([8, 2])
    with col2:
        search_button = st.button("Research", key="search_button")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process query when button is clicked
    if search_button and query:
        # Display user query
        st.markdown(f'<div class="user-message">{query}</div>', unsafe_allow_html=True)
        
        # Run the research process
        with st.spinner("Collecting and analyzing research data..."):
            try:
                # Import app module and process the query
                from graph.research_graph import app
                result = app.invoke({"input": query})
                
                # Get answer and research data
                answer = result.get("answer", "")
                research_data = result.get("research_data", "")
                sources = result.get("sources", [])
                
                # Create a combined response
                if research_data:
                    combined_response = f"{answer}\n\n---\n\n**Supporting Research Data:**\n\n{research_data}"
                else:
                    combined_response = answer
                
                # Display assistant response
                st.markdown(f'<div class="assistant-message">{combined_response}</div>', unsafe_allow_html=True)
                
                # Display sources
                if sources:
                    with st.expander("View Research Sources"):
                        st.markdown('<div class="sources-container">', unsafe_allow_html=True)
                        for i, source in enumerate(sources, 1):
                            st.markdown(f'<div class="source-item">', unsafe_allow_html=True)
                            st.markdown(f"**{i}. {source.get('title', 'No title')}**")
                            if 'url' in source:
                                st.markdown(f"[Read more]({source['url']})")
                            if 'content' in source:
                                st.markdown(f"*{source['content'][:200]}...*")
                            st.markdown('</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Related URLs section
                    st.markdown('<div class="sources-container">', unsafe_allow_html=True)
                    st.subheader("Related URLs")
                    url_list = []
                    for source in sources:
                        if 'url' in source:
                            title = source.get('title', 'Untitled')
                            url_list.append(f"- [{title}]({source['url']})")
                    
                    if url_list:
                        st.markdown("\n".join(url_list))
                    else:
                        st.markdown("No related URLs found.")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
            except Exception as e:
                st.markdown(f'<div class="assistant-message">I encountered an error while processing your request: {str(e)}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()