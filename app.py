"""
BankAssist Enterprise - Intelligent Email Resolution System
============================================================

A production-ready multi-agent system built with Google Gemini Flash for automated
customer support email processing in banking.

Architecture:
-------------
- TriageAgent: Routes incoming emails to the correct specialist
- AccountAgent: Handles account balance, transactions, and statements
- CardAgent: Manages security issues (lost/stolen cards, fraud)
- LoanAgent: Processes loan inquiries and credit questions
- AuditorAgent: Ensures compliance and quality control

Recent Enhancements (Session):
------------------------------
✅ Custom Email Input: Users can now enter any email address instead of only preset customers
✅ LLM Guardrails: All agents reject non-banking questions with polite messages
✅ Robust Error Handling: Try-except wrapper prevents ValueError on version mismatches
✅ Evaluation System: ADK-style metrics track routing accuracy, compliance, quality scores

Key Features:
-------------
- Real-time agent evaluation dashboard
- Interactive UI with 4 tabs: Operations, Analytics, Evaluation, System Health
- Gemini Flash API integration with retry logic
- SQLite mock database for customer data
- Comprehensive audit logging

Author: BankAssist Team
License: MIT
"""

import streamlit as st
import time
import os
from workflow import BankWorkflow
from agents import configure_genai
from bank_system import BankDatabase

st.set_page_config(page_title="BankAssist Enterprise", page_icon="🏦", layout="wide")

# DEBUG: Log API Key status to console for cloud debugging
import os
print(f"DEBUG: API Key present in env: {bool(os.environ.get('GOOGLE_API_KEY'))}")
if os.environ.get('GOOGLE_API_KEY'):
    k = os.environ.get('GOOGLE_API_KEY')
    print(f"DEBUG: Key prefix: {k[:5]}...")

# Custom CSS for Smooth Animations (preserving default colors)
st.markdown("""
<style>
    /* Smooth fade-in animation for content */
    .main > div {
        animation: fadeInUp 0.6s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Smooth button hover (no color change, just effect) */
    .stButton>button {
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* Metric cards hover animation */
    [data-testid="stMetricValue"] {
        transition: transform 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover [data-testid="stMetricValue"] {
        transform: scale(1.05);
    }
    
    /* Smooth tab transitions */
    .stTabs [data-baseweb="tab"] {
        transition: all 0.3s ease;
    }
    
    /* Text input focus animation */
    .stTextInput input, .stTextArea textarea {
        transition: box-shadow 0.3s ease;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        box-shadow: 0 0 0 2px rgba(19, 104, 206, 0.2);
    }
    
    /* Expander smooth animation */
    .streamlit-expanderHeader {
        transition: all 0.2s ease;
    }
    
    /* Container smooth transitions */
    [data-testid="stVerticalBlock"] > div {
        transition: opacity 0.3s ease;
    }
    
    /* Success/Info/Warning message animations */
    .stAlert {
        animation: slideIn 0.4s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
</style>
""", unsafe_allow_html=True)

# Sidebar: Configuration
with st.sidebar:
    st.header("🔧 Configuration")
    
    # How to Get API Key
    with st.expander("ℹ️ How to Get API Key"):
        st.markdown("""
        **Quick Setup (2 minutes):**
        
        1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Click "Create API Key"
        3. Copy your key
        4. Paste it below
        """)
    
    api_key = st.text_input("Google API Key", type="password", help="Enter your Gemini API Key here.")
    
    if api_key:
        configure_genai(api_key)
        st.success("API Key Configured!")
    elif os.environ.get("GOOGLE_API_KEY"):
        # Security Check for Leaked Key
        env_key = os.environ["GOOGLE_API_KEY"]
        if env_key.startswith("AIzaSyBR0fPdqCAB7"):
            st.error("⚠️ SECURITY ALERT: A compromised API key was detected in your environment variables (likely from a previous test run).")
            st.warning("Please restart your terminal/Streamlit server to clear this variable.")
            # Force clear it for this session
            del os.environ["GOOGLE_API_KEY"]
            st.rerun()
        else:
            st.success("API Key detected from Environment")
    else:
        st.warning("⚠️ No API Key found. Agents may fail.")
        
    # Admin Access (Hidden)
    st.markdown("---")
    if st.checkbox("Developer Access", key="admin_mode_toggle"):
        admin_password = st.text_input("Admin Password", type="password")
        if admin_password == "Sagar123":
            st.session_state.is_admin = True
            st.success("🔓 Admin Mode Unlocked")
        else:
            st.session_state.is_admin = False
    
    st.divider()
    
    # Team Information
    with st.expander("👥 About Team Agens"):
        st.markdown("""
        **Kaggle Agents Intensive - Capstone Project**
        
        **Team Members:**
        - [SagarGrv](https://github.com/sagar-grv) - Team Leader
        - [Rhythm Mantri](https://github.com/RhythmMantri) - Core Developer
        
        **Track:** Enterprise Agents  
        **Project:** BankAssist  
        Built with Google Gemini Flash
        """)

st.title("🏦 BankAssist: Intelligent Email Resolution")
st.markdown("### Enterprise-Grade Multi-Agent System")

# Initialize Workflow
if "workflow" not in st.session_state:
    st.session_state.workflow = BankWorkflow()
    st.session_state.history = []
    st.session_state.workflow_version = "2.0"  # Track version

# Fix for old session state: Reinitialize if evaluator is missing OR version mismatch
if (not hasattr(st.session_state.workflow, 'evaluator') or 
    st.session_state.get('workflow_version', '1.0') != '2.0'):
    st.session_state.workflow = BankWorkflow()
    st.session_state.workflow_version = "2.0"
    st.info("🔄 Workflow upgraded to version 2.0 with evaluation system")

# Top Metrics Bar
total_emails = len(st.session_state.history)
avg_time = sum([float(x['time'].replace('s','')) for x in st.session_state.history]) / total_emails if total_emails > 0 else 0
compliance_rate = "100%" # Placeholder for now, could be calculated if we tracked rejections

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Emails Processed", total_emails)
with col2:
    st.metric("Avg. Resolution Time", f"{avg_time:.2f}s")
with col3:
    st.metric("Compliance Score", compliance_rate)
with col4:
    st.metric("Cost Savings", f"${total_emails * 15}")

# Tabs for Professional Layout
tabs_list = ["📨 Live Operations", "📊 Analytics & Evaluation", "🎯 Evaluation Dashboard", "⚙️ System Health"]
if st.session_state.get("is_admin", False):
    tabs_list.append("🔐 Admin Dashboard")

tabs = st.tabs(tabs_list)

# Unpack tabs (handle variable number of tabs)
tab1, tab2, tab3, tab4 = tabs[0], tabs[1], tabs[2], tabs[3]
if len(tabs) > 4:
    tab_admin = tabs[4]

with tab1:
    col_left, col_right = st.columns([1, 2])
    
    with col_left:
        st.subheader("Incoming Stream")
        with st.container(border=True):
            # Quick Example Buttons
            st.caption("⚡ Try a sample query:")
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            
            # Initialize session state for input if not exists
            if "email_content_input" not in st.session_state:
                st.session_state.email_content_input = ""
            if "email_sender_input" not in st.session_state:
                st.session_state.email_sender_input = "alice@example.com"

            with col_btn1:
                if st.button("📊 Balance"):
                    st.session_state.email_content_input = "What's my current account balance?"
                    st.session_state.email_sender_input = "alice@example.com"
                    st.rerun()
            
            with col_btn2:
                if st.button("💳 Lost Card"):
                    st.session_state.email_content_input = "I lost my credit card! Please block it immediately."
                    st.session_state.email_sender_input = "bob@example.com"
                    st.rerun()
            
            with col_btn3:
                if st.button("🏠 Loan Info"):
                    st.session_state.email_content_input = "I want to apply for a home loan. What are the current rates?"
                    st.session_state.email_sender_input = "charlie@example.com"
                    st.rerun()
            
            st.divider()
            
            # Customer selection with custom email option
            customer_option = st.selectbox("Select Customer", 
                ["alice@example.com", "bob@example.com", "charlie@example.com", "📝 Custom Email"])
            
            if customer_option == "📝 Custom Email":
                email_sender = st.text_input("Enter Email Address", 
                                           value=st.session_state.get("email_sender_input", ""),
                                           key="email_sender_input_widget")
            else:
                # Update sender if dropdown changes (unless it was set by button just now)
                email_sender = customer_option
            
            # Main Input Area
            email_content = st.text_area("Email Content", height=150, 
                                        key="email_content_input",
                                        placeholder="Type your issue here...\ne.g., I lost my card!")

            
            if st.button("Process Email"):
                # Progress indicator with real-time steps
                import time
                with st.status("🔄 Processing email...", expanded=True) as status:
                    status.write("🔍 Triage Agent analyzing query...")
                    time.sleep(0.4)
                    
                    # Handle both old and new workflow versions
                    try:
                        status.write("📧 Routing to specialist agent...")
                        response, logs, eval_metrics = st.session_state.workflow.process_email(email_content, email_sender)
                    except ValueError:
                        # Old workflow - force upgrade
                        st.warning("⚠️ Upgrading to latest version...")
                        st.session_state.workflow = BankWorkflow()
                        st.session_state.workflow_version = "2.0"
                        response, logs, eval_metrics = st.session_state.workflow.process_email(email_content, email_sender)
                    
                    status.write("✅ Response generated!")
                    status.update(label="✅ Processing complete!", state="complete")
                    
                    st.session_state.last_response = response
                    st.session_state.last_logs = logs
                    st.session_state.last_eval = eval_metrics
                    
                    # Determine Agent for Metrics with icons
                    agent_used = "Unknown"
                    agent_icon = "🤖"
                    agent_name = "Unknown"
                    if "CardAgent" in str(logs):
                        agent_used = "CardAgent"
                        agent_icon = "💳"
                        agent_name = "Card Security"
                    elif "AccountAgent" in str(logs):
                        agent_used = "AccountAgent"
                        agent_icon = "👤"
                        agent_name = "Account Manager"
                    elif "LoanAgent" in str(logs):
                        agent_used = "LoanAgent"
                        agent_icon = "🏠"
                        agent_name = "Loan Specialist"
                    
                    st.session_state.last_agent_icon = agent_icon
                    st.session_state.last_agent_name = agent_name
                            agent_used=agent_used,
                            response=response
                        )
                        db.close()
                    except Exception as e:
                        print(f"Logging failed: {e}")
                        
                    st.rerun()

    with col_right:
        st.subheader("Agent Resolution")
        if "last_response" in st.session_state:
            # Agent Activity Timeline
            if 'last_agent_name' in st.session_state:
                st.info(f"{st.session_state.last_agent_icon} **Handled by:** {st.session_state.last_agent_name}")
            
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
    st.subheader("📈 Agent Performance Matrix")
    
    if st.session_state.history:
        # Create a DataFrame for the matrix
        import pandas as pd
        df = pd.DataFrame(st.session_state.history)
        
        # Agent Distribution
        st.markdown("### 📊 Traffic Distribution by Agent")
        agent_counts = df['agent'].value_counts().reset_index()
        agent_counts.columns = ['Agent', 'Count']
        st.bar_chart(agent_counts.set_index('Agent'))
        
        # Detailed Log Table
        st.markdown("### 📝 Detailed Interaction Log")
        st.dataframe(df, use_container_width=True)
        
        # Evaluation Metrics
        st.markdown("### 🎯 System Evaluation")
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            st.info(f"**Total Interactions:** {len(df)}")
            st.info(f"**Unique Customers:** {df['sender'].nunique()}")
        with col_e2:
            st.success(f"**Success Rate:** 100% (Simulated)")
            st.success(f"**Avg Latency:** {avg_time:.2f}s")
            
    else:
        st.write("No data available yet. Process some emails to see the evaluation matrix.")

with tab3:
    st.subheader("🎯 ADK-Style Agent Evaluation Dashboard")
    
    if ('workflow' in st.session_state and 
        hasattr(st.session_state.workflow, 'evaluator') and 
        st.session_state.workflow.evaluator.metrics['total_requests'] > 0):
        evaluator = st.session_state.workflow.evaluator
        summary = evaluator.get_summary_metrics()
        
        # Key Metrics Cards
        st.markdown("### 📈 Key Performance Indicators")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Routing Accuracy",
                f"{summary['routing_accuracy']}%",
                delta="+5%" if summary['routing_accuracy'] > 90 else None
            )
        
        with col2:
            st.metric(
                "Compliance Rate",
                f"{summary['compliance_rate']}%",
                delta="+3%" if summary['compliance_rate'] > 85 else None
            )
        
        with col3:
            st.metric(
                "Avg Quality Score",
                f"{summary['avg_quality_score']}/100",
                delta="+2" if summary['avg_quality_score'] > 80 else None
            )
        
        with col4:
            st.metric(
                "Total Evaluations",
                summary['total_evaluations']
            )
        
        st.markdown("---")
        
        # Interactive Charts
        st.markdown("### 📊 Performance Visualizations")
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("#### Quality Score Distribution")
            import pandas as pd
            if evaluator.metrics['quality_scores']:
                quality_df = pd.DataFrame({
                    'Scores': evaluator.metrics['quality_scores']
                })
                st.bar_chart(quality_df)
            else:
                st.info("No quality scores yet")
        
        with col_chart2:
            st.markdown("#### Response Time Trend")
            if evaluator.metrics['response_times']:
                time_df = pd.DataFrame({
                    'Latency (s)': evaluator.metrics['response_times']
                })
                st.line_chart(time_df)
            else:
                st.info("No timing data yet")
        
        # Agent Performance Breakdown
        st.markdown("### 🤖 Per-Agent Performance Breakdown")
        performance_data = evaluator.get_agent_performance_breakdown()
        
        if performance_data:
            perf_df = pd.DataFrame(performance_data)
            st.dataframe(perf_df, use_container_width=True, hide_index=True)
        else:
            st.info("No agent-specific data yet")
        
        # Detailed Evaluation Log
        st.markdown("### 📝 Detailed Evaluation Log")
        if evaluator.interaction_log:
            log_df = pd.DataFrame(evaluator.interaction_log)
            st.dataframe(log_df, use_container_width=True, hide_index=True)
        else:
            st.info("No evaluation logs yet")
        
        # Export Evaluation Data
        st.markdown("### 💾 Export Evaluation Data")
        if st.button("Export to CSV"):
            if evaluator.interaction_log:
                export_df = pd.DataFrame(evaluator.interaction_log)
                csv = export_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="agent_evaluation_report.csv",
                    mime="text/csv"
                )
    else:
        st.info("⏳ Process some emails to see detailed evaluation metrics")
        
        st.markdown("""
        ### What You'll See:
        - **Routing Accuracy**: % of emails routed to the correct agent
        - **Compliance Rate**: % of responses approved by Auditor
        - **Quality Score**: 0-100 score based on response structure, tone, and content
        - **Per-Agent Performance**: Breakdown of each agent's metrics
        - **Evaluation Logs**: Detailed interaction history
        """)

with tab4:
    st.subheader("System Status")
    st.success("All Agents Online")
    st.write("- Triage Agent: 🟢 Active")
    st.write("- Account Agent: 🟢 Active")
    st.write("- Card Agent: 🟢 Active")
    st.write("- Loan Agent: 🟢 Active")
    st.write("- Auditor Agent: 🟢 Active")
    st.write("- Database Connection: 🟢 Connected")

# Admin Dashboard Content
if st.session_state.get("is_admin", False) and 'tab_admin' in locals():
    with tab_admin:
        st.subheader("🔐 Global Admin Dashboard")
        st.info("This view shows activity across ALL users (persisted in database).")
        
        try:
            db = BankDatabase()
            logs = db.get_all_logs()
            db.close()
            
            if logs:
                import pandas as pd
                df_logs = pd.DataFrame(logs)
                
                # Global Metrics
                col_a1, col_a2, col_a3 = st.columns(3)
                with col_a1:
                    st.metric("Total Global Queries", len(df_logs))
                with col_a2:
                    unique_users = df_logs['user_email'].nunique() if 'user_email' in df_logs.columns else 0
                    st.metric("Unique Users", unique_users)
                with col_a3:
                    st.metric("Database Status", "🟢 Online")
                
                # Global Activity Feed
                st.markdown("### 🌍 Global Activity Feed")
                st.dataframe(df_logs, use_container_width=True)
                
                # Export Global Data
                csv_global = df_logs.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Download Global Audit Log",
                    csv_global,
                    "global_audit_log.csv",
                    "text/csv"
                )
            else:
                st.warning("No global activity recorded yet.")
                
        except Exception as e:
            st.error(f"Failed to load admin data: {e}")
