import streamlit as st
import requests
import re

URL = "http://localhost:8000/summarize"

st.set_page_config(
    page_title="Policy Simplifier AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:

    st.title("📄 Policy Simplifier AI")

    st.markdown("---")

    st.write("### Model")

    st.success("Fine-tuned BART")

    st.write("### Backend")

    st.info("FastAPI")

    st.write("### Version")

    st.write("v1.0")

st.title("📄 Policy Simplifier AI")

st.caption(
    "Summarize Privacy Policies and Terms & Conditions using a fine-tuned BART model."
)

policy = st.text_area(
    "Paste Policy",
    height=200,
    placeholder="Paste your policy here..."
)

generate=st.button("Generate Summary",use_container_width=True)

if generate:
    if(policy.strip()==""):
        st.warning("Please Paste A Policy First")
        st.stop()
        
    else:
        with st.spinner("Generating Summary....."):
            try:
                response=requests.post(
                    URL,
                    json={
                        'text':policy
                    }
                )    
                
                summary=response.json()['summary']
            
            except Exception as e:
                st.error(str(e))
            
        st.success("Summary Generated Successfully")
        
        st.subheader("Summary")
        
        sentences = re.split(r'(?<=[.!?])\s+', summary)
        
        
        for sentence in sentences:
            if sentence.strip():
                st.write(f"• {sentence}")
        

    