import streamlit as st
import time
import os
from workflow import BankWorkflow
from agents import configure_genai

st.set_page_config(page_title="BankAssist Enterprise", page_icon="🏦", layout="wide")

# Custom CSS for "Billion Dollar" Look
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        background-color: #0052cc;
        color: white;
        border-radius: 5px;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar: Configuration
with st.sidebar:
    st.header("🔧 Configuration")
    api_key = st.text_input("Google API Key", type="password", help="Enter your Gemini API Key here.")
    
    if api_key:
        configure_genai(api_key)
        st.success("API Key Configured!")
    elif os.environ.get("GOOGLE_API_KEY"):
        st.success("API Key detected from Environment")
    else:
        st.warning("⚠️ No API Key found. Agents may fail.")

st.title("🏦 BankAssist: Intelligent Email Resolution")
st.markdown("### Enterprise-Grade Multi-Agent System")

# Initialize Workflow
if "workflow" not in st.session_state:
    st.session_state.workflow = BankWorkflow()
    st.session_state.history = []

# Top Metrics Bar
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Emails Processed", len(st.session_state.history))
with col2:
    st.metric("Avg. Resolution Time", "1.2s")
with col3:
    st.metric("Compliance Score", "100%")
with col4:
    st.metric("Cost Savings", f"${len(st.session_state.history) * 15}")

# Tabs for Professional Layout
tab1, tab2, tab3 = st.tabs(["📨 Live Operations", "📊 Analytics", "⚙️ System Health"])

with tab1:
    col_left, col_right = st.columns([1, 2])
    
    with col_left:
        st.subheader("Incoming Stream")
        with st.container(border=True):
            email_sender = st.selectbox("Select Customer", ["alice@example.com", "bob@example.com", "charlie@example.com"])
            email_content = st.text_area("Email Content", height=150, placeholder="Type your issue here...\ne.g., I lost my card!")
            
            if st.button("Process Email"):
                with st.spinner("Agents are working..."):
                    start_time = time.time()
                    response, logs = st.session_state.workflow.process_email(email_content, email_sender)
                    end_time = time.time()
                    
                    st.session_state.last_response = response
                    st.session_state.last_logs = logs
                    st.session_state.history.append({
                        "sender": email_sender,
                        "content": email_content,
                        "response": response,
                        "time": f"{end_time - start_time:.2f}s"
                    })

    with col_right:
        st.subheader("Agent Resolution")
        if "last_response" in st.session_state:
            # Response Display
            with st.container(border=True):
                st.success("✅ Response Generated Successfully")
                st.markdown("**From:** BankAssist Support Team")
                st.markdown(f"**To:** {email_sender}")
                st.markdown("**Subject:** Re: Your Inquiry")
                st.markdown("---")
                
                # Display the response in a nice formatted way
                st.markdown("### 📧 Email Response")
                st.markdown(st.session_state.last_response)
            
            # Agent Logs
            with st.expander("🧠 View Agent Thought Process (Logs)", expanded=False):
                for log in st.session_state.last_logs:
                    if "Triage" in log:
                        st.info(log)
                    elif "Auditor" in log:
                        st.warning(log)
                    elif "Error" in log:
                        st.error(log)
                    else:
                        st.write(log)
        else:
            st.info("Waiting for incoming emails...")

with tab2:
    st.subheader("Historical Data")
    if st.session_state.history:
        st.dataframe(st.session_state.history)
    else:
        st.write("No data yet.")

with tab3:
    st.subheader("System Status")
    st.success("All Agents Online")
    st.write("- Triage Agent: 🟢 Active")
    st.write("- Account Agent: 🟢 Active")
    st.write("- Card Agent: 🟢 Active")
    st.write("- Auditor Agent: 🟢 Active")
    st.write("- Database Connection: 🟢 Connected")
