import streamlit as st
import requests

# Page Configuration
st.set_page_config(
    page_title="ResearchMind - AI Research",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Styling (Fixed Layout, Custom Pills & Apple Dark Minimalist UI)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #0c0d10;
        color: #e2e8f0;
    }

    #MainMenu, footer, header {visibility: hidden;}

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    .section-label {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        color: #ff6b00;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    /* Input Field */
    .stTextInput > div > div > input {
        background-color: #18191e;
        color: #f1f5f9;
        border: 1px solid #27272a;
        border-radius: 10px;
        padding: 14px 16px;
        font-size: 15px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #ff6b00;
        box-shadow: 0 0 0 1px #ff6b00;
    }

    /* CTA Button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #ff6b00 0%, #ff8800 100%);
        color: #ffffff;
        border: none;
        border-radius: 10px;
        padding: 14px 20px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.2s ease;
        box-shadow: 0 4px 20px rgba(255, 107, 0, 0.3);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #ff7711 0%, #ff9911 100%);
        box-shadow: 0 6px 24px rgba(255, 107, 0, 0.45);
    }

    /* Pipeline Cards */
    .pipe-card {
        background-color: #121318;
        border: 1px solid #22232a;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .pipe-card.waiting { border-left: 3px solid #3f3f46; }
    .pipe-card.running { 
        border-left: 3px solid #ff6b00; 
        background-color: #1a1714;
        box-shadow: 0 0 15px rgba(255, 107, 0, 0.15);
    }
    .pipe-card.complete { 
        border-left: 3px solid #10b981; 
        background-color: #0f1a15;
    }

    .pipe-title { font-size: 15px; font-weight: 600; color: #f8fafc; }
    .pipe-desc { font-size: 12px; color: #94a3b8; margin-top: 2px; }
    .pipe-status { font-size: 12px; font-weight: 600; letter-spacing: 0.05em; }
    
    .status-waiting { color: #52525b; }
    .status-running { color: #ff6b00; }
    .status-complete { color: #10b981; }

    .footer-text {
        text-align: center;
        color: #475569;
        font-size: 12px;
        margin-top: 40px;
    }
    </style>
""", unsafe_allow_html=True)

# Session State
if "query_text" not in st.session_state:
    st.session_state.query_text = ""
if "research_data" not in st.session_state:
    st.session_state.research_data = None

# App Title
st.title("ResearchMind")
st.caption("AI-Powered Multi-Agent Research System")
st.markdown("<br>", unsafe_allow_html=True)

# Grid Layout
left_col, right_col = st.columns([1.1, 1], gap="large")

with left_col:
    st.markdown('<div class="section-label">RESEARCH TOPIC</div>', unsafe_allow_html=True)
    
    query_input = st.text_input(
        label="Research Topic Input",
        value=st.session_state.query_text,
        placeholder="e.g. Quantum computing breakthroughs in 2026",
        label_visibility="collapsed"
    )
    
    run_pipeline = st.button("⚡ Run Research Pipeline")

    # Updated Sample Topics
    st.markdown('<div style="margin-top: 18px; font-size: 12px; color: #64748b; font-weight: 600;">TRY SAMPLE TOPICS →</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    if c1.button("Autonomous AI Agents Architecture", key="chip1"):
        st.session_state.query_text = "Autonomous AI Agents Architecture"
        st.rerun()
    if c2.button("Solid State Battery Advances", key="chip2"):
        st.session_state.query_text = "Solid State Battery Advances"
        st.rerun()

# Pipeline Renderer Function (Targeted Container Rendering)
def render_pipeline_ui(container, search_st="WAITING", reader_st="WAITING", writer_st="WAITING", critic_st="WAITING",
                       search_sub="", reader_sub="", writer_sub="", critic_sub=""):
    with container.container():
        st.markdown('### Pipeline')
        
        st.markdown(f'''
            <div class="pipe-card {search_st.lower()}">
                <div>
                    <div class="pipe-title">01 &nbsp; Search Agent</div>
                    <div class="pipe-desc">Gathers recent web information {f"({search_sub})" if search_sub else ""}</div>
                </div>
                <div class="pipe-status status-{search_st.lower()}">{search_st}</div>
            </div>
        ''', unsafe_allow_html=True)

        st.markdown(f'''
            <div class="pipe-card {reader_st.lower()}">
                <div>
                    <div class="pipe-title">02 &nbsp; Reader Agent</div>
                    <div class="pipe-desc">Scrapes & extracts deep content {f"({reader_sub})" if reader_sub else ""}</div>
                </div>
                <div class="pipe-status status-{reader_st.lower()}">{reader_st}</div>
            </div>
        ''', unsafe_allow_html=True)

        st.markdown(f'''
            <div class="pipe-card {writer_st.lower()}">
                <div>
                    <div class="pipe-title">03 &nbsp; Writer Chain</div>
                    <div class="pipe-desc">Drafts the full research report {f"({writer_sub})" if writer_sub else ""}</div>
                </div>
                <div class="pipe-status status-{writer_st.lower()}">{writer_st}</div>
            </div>
        ''', unsafe_allow_html=True)

        st.markdown(f'''
            <div class="pipe-card {critic_st.lower()}">
                <div>
                    <div class="pipe-title">04 &nbsp; Critic Chain</div>
                    <div class="pipe-desc">Reviews & scores the report {f"({critic_sub})" if critic_sub else ""}</div>
                </div>
                <div class="pipe-status status-{critic_st.lower()}">{critic_sub if critic_sub else critic_st}</div>
            </div>
        ''', unsafe_allow_html=True)

# Right Column Container Placeholder
pipeline_placeholder = right_col.empty()

# Initial Render
render_pipeline_ui(pipeline_placeholder)

BACKEND_URL = "http://127.0.0.1:8000/multi_agent"

# Execution Handling
if run_pipeline:
    target_query = query_input.strip() or st.session_state.query_text.strip()
    if not target_query:
        st.warning("Please enter a research topic first.")
    else:
        # Step 1: Running
        render_pipeline_ui(pipeline_placeholder, search_st="RUNNING")
        
        try:
            response = requests.post(BACKEND_URL, json={"query": target_query}, timeout=120)
            
            if response.status_code == 200:
                data = response.json()
                st.session_state.research_data = data

                # All Completed UI Update
                render_pipeline_ui(
                    pipeline_placeholder, 
                    search_st="COMPLETE", reader_st="COMPLETE", writer_st="COMPLETE", critic_st="COMPLETE",
                    search_sub="Discovered references", reader_sub="Extracted deep content",
                    writer_sub="Report generated", critic_sub="Evaluated report"
                )
            else:
                st.error(f"Backend Returned Error Code: {response.status_code}")
                render_pipeline_ui(pipeline_placeholder)

        except Exception as e:
            st.error(f"Failed to connect to FastAPI backend: {e}")
            render_pipeline_ui(pipeline_placeholder)

# Output Results
if st.session_state.research_data:
    st.markdown("---")
    st.markdown("### Research Outputs")
    
    res = st.session_state.research_data
    tab1, tab2, tab3, tab4 = st.tabs(["Final Report", "Critic Evaluation", "Scraped Content", "Sources & Links"])

    with tab1:
        st.markdown(res.get("writer_results", "No report available."))

    with tab2:
        st.markdown(res.get("critic_results", "No review available."))

    with tab3:
        st.write(res.get("reader_results", "No scraped text available."))

    with tab4:
        st.markdown(res.get("search_results", "No links found."))

st.markdown('<div class="footer-text">ResearchMind • Powered by LangChain multi-agent pipeline • Built with Streamlit</div>', unsafe_allow_html=True)