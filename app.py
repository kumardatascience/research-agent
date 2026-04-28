from src.research_agent.report.generator import generate_pdf_report 
import streamlit as st
from src.research_agent.agent.graph import build_graph, ResearchState
result = None


st.set_page_config(
    page_title="Research Agent",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Multi-Source Research Agent")
st.caption("Powered by LangGraph + Gemini 2.5 Flash + Groq Llama 3.3")
st.divider()

col1, col2 = st.columns([3, 1])

with col1:
    topic = st.text_input(
        label="Enter your research topic:",
        placeholder="e.g. Impact of AI on healthcare in 2026",
        help="Be specific for better results"
    )

with col2:
    model_choice = st.selectbox(
        label="Select AI Model:",
        options=["gemini", "groq"],
        format_func=lambda x: "🤖 Gemini 2.5 Flash" if x == "gemini" else "🦙 llama-3.3-70b-versatile"
    )

st.write("")
start_button = st.button(
    label="🚀 Start Research",
    type="primary" 
)    

if start_button and not topic:
    st.warning("⚠️ Please enter a research topic first!")


if start_button and topic:
    with st.spinner("🔍 Agent is researching... This may take 30-60 seconds"):


        graph = build_graph()
        initial_state = {
            "topic": topic,
            "questions": [],
            "search_results": [],
            "scraped_content": [],
            "iterations": 0,
            "final_report": "",
            "model_choice": model_choice
        }
        result = graph.invoke(initial_state)
        st.success("✅ Research Complete!")   

st.divider()                                  

if result:                                    
    col1, col2, col3 = st.columns(3)          

    with col1:                               
        st.metric(                           
            label="Questions Generated",
            value=len(result["questions"])
        )

    with col2:                               
        st.metric(
            label="Sources Found",
            value=len(result["search_results"])
        )

    with col3:                              
        st.metric(
            label="Pages Scraped",
            value=len(result["scraped_content"])
        )
    st.subheader("📋 Research Report")
    st.markdown(result["final_report"])    

    st.divider()
    
    pdf_bytes = generate_pdf_report(
        topic=topic,
        content=result["final_report"]
    )
    
    st.download_button(
        label="📥 Download PDF Report",
        data=pdf_bytes,
        file_name=f"research_{topic[:30].replace(' ', '_')}.pdf",
        mime="application/pdf"
    )

