import streamlit as st
import os
from pathlib import Path
from ai_config.functions import get_prediction, do_websearch, summary, generate_email
from ai_config.config import client, model, instruction
import urllib.parse

# Page configuration
st.set_page_config(
    page_title="VC Pitch Deck Analyzer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling with animations and gradients
st.markdown("""
<style>
    /* Animated gradient background */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.05); opacity: 0.9; }
    }

    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.5), 0 0 40px rgba(102, 126, 234, 0.3); }
        50% { box-shadow: 0 0 30px rgba(102, 126, 234, 0.7), 0 0 60px rgba(102, 126, 234, 0.5); }
    }

    @keyframes glowIntense {
        0%, 100% {
            box-shadow: 0 0 30px rgba(102, 126, 234, 0.8),
                        0 0 60px rgba(102, 126, 234, 0.6),
                        0 0 90px rgba(118, 75, 162, 0.4);
        }
        50% {
            box-shadow: 0 0 50px rgba(102, 126, 234, 1),
                        0 0 100px rgba(102, 126, 234, 0.8),
                        0 0 150px rgba(118, 75, 162, 0.6);
        }
    }

    @keyframes rainbowGlow {
        0% { filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.8)); }
        25% { filter: drop-shadow(0 0 20px rgba(118, 75, 162, 0.8)); }
        50% { filter: drop-shadow(0 0 20px rgba(240, 147, 251, 0.8)); }
        75% { filter: drop-shadow(0 0 20px rgba(118, 75, 162, 0.8)); }
        100% { filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.8)); }
    }

    @keyframes shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    @keyframes borderGlow {
        0%, 100% {
            border-color: rgba(102, 126, 234, 0.5);
            box-shadow: inset 0 0 20px rgba(102, 126, 234, 0.2),
                        0 0 20px rgba(102, 126, 234, 0.4);
        }
        50% {
            border-color: rgba(102, 126, 234, 1);
            box-shadow: inset 0 0 30px rgba(102, 126, 234, 0.4),
                        0 0 40px rgba(102, 126, 234, 0.8);
        }
    }

    /* Main app background */
    .stApp {
        background: linear-gradient(-45deg, #0f0f23, #1a1a3e, #1e1e4f, #2a2a5a);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }

    /* Main header with gradient text */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: fadeIn 1s ease-out, shimmer 3s linear infinite;
        text-align: center;
        filter: drop-shadow(0 0 30px rgba(102, 126, 234, 0.6));
        cursor: default;
        transition: all 0.3s ease;
    }

    .main-header:hover {
        filter: drop-shadow(0 0 50px rgba(102, 126, 234, 1));
        transform: scale(1.05);
    }

    .sub-header {
        font-size: 1.8rem;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: slideInLeft 0.8s ease-out;
        filter: drop-shadow(0 0 15px rgba(102, 126, 234, 0.5));
        cursor: default;
        transition: all 0.3s ease;
    }

    .sub-header:hover {
        animation: shimmer 2s linear infinite;
        filter: drop-shadow(0 0 25px rgba(102, 126, 234, 0.8));
        transform: translateX(5px);
    }

    /* Animated traffic light with glow effect */
    .traffic-light {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        margin: 30px auto;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        animation: pulse 2s ease-in-out infinite, float 3s ease-in-out infinite;
        position: relative;
    }

    .green {
        background: radial-gradient(circle at 30% 30%, #48ff48, #28a745);
        box-shadow: 0 0 40px rgba(40, 167, 69, 0.8), 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    .yellow {
        background: radial-gradient(circle at 30% 30%, #ffeb3b, #ffc107);
        box-shadow: 0 0 40px rgba(255, 193, 7, 0.8), 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    .red {
        background: radial-gradient(circle at 30% 30%, #ff4444, #dc3545);
        box-shadow: 0 0 40px rgba(220, 53, 69, 0.8), 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    /* Glassmorphism result cards */
    .result-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        animation: fadeIn 0.6s ease-out;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .result-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        transition: left 0.5s;
    }

    .result-card:hover::before {
        left: 100%;
    }

    .result-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 0 40px rgba(102, 126, 234, 0.6),
                    0 0 80px rgba(102, 126, 234, 0.4),
                    0 20px 60px rgba(0, 0, 0, 0.4);
        border-color: rgba(102, 126, 234, 0.6);
        background: rgba(255, 255, 255, 0.08);
    }

    .config-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 35px;
        border-radius: 20px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        margin-bottom: 25px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        animation: fadeIn 0.8s ease-out, glowIntense 4s ease-in-out infinite;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }

    .config-card:hover {
        transform: scale(1.03);
        border-color: rgba(102, 126, 234, 0.8);
        box-shadow: 0 0 50px rgba(102, 126, 234, 0.8),
                    0 0 100px rgba(118, 75, 162, 0.6),
                    0 20px 60px rgba(0, 0, 0, 0.4);
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
    }

    /* Enhance Streamlit components */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4),
                    0 0 20px rgba(102, 126, 234, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeIn 0.5s ease-out;
        position: relative;
        overflow: hidden;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }

    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }

    .stButton > button:hover {
        transform: translateY(-4px) scale(1.05);
        box-shadow: 0 0 30px rgba(102, 126, 234, 0.8),
                    0 0 60px rgba(102, 126, 234, 0.6),
                    0 0 90px rgba(118, 75, 162, 0.4),
                    0 10px 40px rgba(0, 0, 0, 0.3);
        background: linear-gradient(135deg, #764ba2 0%, #f093fb 100%);
    }

    .stButton > button:active {
        transform: translateY(-2px) scale(1.03);
    }

    /* File uploader styling */
    .uploadedFile {
        background: rgba(102, 126, 234, 0.1);
        border-radius: 12px;
        padding: 10px;
        border: 1px solid rgba(102, 126, 234, 0.3);
        animation: slideInLeft 0.5s ease-out;
        transition: all 0.3s ease;
        box-shadow: 0 0 15px rgba(102, 126, 234, 0.2);
    }

    .uploadedFile:hover {
        background: rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.6);
        box-shadow: 0 0 30px rgba(102, 126, 234, 0.5),
                    0 0 60px rgba(102, 126, 234, 0.3);
        transform: scale(1.02);
    }

    .stFileUploader {
        transition: all 0.3s ease;
    }

    .stFileUploader:hover {
        filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.3));
    }

    /* Text input and text area */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        color: #e0e7ff;
        transition: all 0.4s ease;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.1);
    }

    .stTextInput > div > div > input:hover,
    .stTextArea > div > div > textarea:hover {
        border-color: rgba(102, 126, 234, 0.5);
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
        background: rgba(255, 255, 255, 0.08);
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: rgba(102, 126, 234, 0.8);
        box-shadow: 0 0 30px rgba(102, 126, 234, 0.6),
                    0 0 60px rgba(102, 126, 234, 0.3),
                    inset 0 0 20px rgba(102, 126, 234, 0.1);
        background: rgba(255, 255, 255, 0.1);
        animation: borderGlow 2s ease-in-out infinite;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(102, 126, 234, 0.1);
        border-radius: 12px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 0 15px rgba(102, 126, 234, 0.1);
    }

    .streamlit-expanderHeader:hover {
        background: rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.6);
        box-shadow: 0 0 30px rgba(102, 126, 234, 0.5),
                    0 0 60px rgba(102, 126, 234, 0.3);
        transform: translateX(5px);
    }

    /* Status container */
    .stStatus {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        animation: fadeIn 0.6s ease-out;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.2);
        transition: all 0.3s ease;
    }

    .stStatus:hover {
        box-shadow: 0 0 35px rgba(102, 126, 234, 0.4),
                    0 0 70px rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.4);
    }

    /* Chat messages */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 10px 0;
        animation: slideInLeft 0.5s ease-out;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }

    .stChatMessage:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: rgba(102, 126, 234, 0.5);
        box-shadow: 0 0 30px rgba(102, 126, 234, 0.4),
                    0 0 60px rgba(102, 126, 234, 0.2),
                    0 8px 30px rgba(0, 0, 0, 0.3);
        transform: translateX(5px);
    }

    /* Success/Error/Warning messages */
    .stSuccess {
        border-radius: 12px;
        backdrop-filter: blur(10px);
        animation: slideInLeft 0.5s ease-out;
        box-shadow: 0 0 20px rgba(40, 167, 69, 0.3);
        transition: all 0.3s ease;
    }

    .stSuccess:hover {
        box-shadow: 0 0 40px rgba(40, 167, 69, 0.6),
                    0 0 80px rgba(40, 167, 69, 0.3);
        transform: scale(1.02);
    }

    .stError {
        border-radius: 12px;
        backdrop-filter: blur(10px);
        animation: slideInLeft 0.5s ease-out;
        box-shadow: 0 0 20px rgba(220, 53, 69, 0.3);
        transition: all 0.3s ease;
    }

    .stError:hover {
        box-shadow: 0 0 40px rgba(220, 53, 69, 0.6),
                    0 0 80px rgba(220, 53, 69, 0.3);
        transform: scale(1.02);
    }

    .stWarning {
        border-radius: 12px;
        backdrop-filter: blur(10px);
        animation: slideInLeft 0.5s ease-out;
        box-shadow: 0 0 20px rgba(255, 193, 7, 0.3);
        transition: all 0.3s ease;
    }

    .stWarning:hover {
        box-shadow: 0 0 40px rgba(255, 193, 7, 0.6),
                    0 0 80px rgba(255, 193, 7, 0.3);
        transform: scale(1.02);
    }

    .stInfo {
        border-radius: 12px;
        backdrop-filter: blur(10px);
        animation: slideInLeft 0.5s ease-out;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }

    .stInfo:hover {
        box-shadow: 0 0 40px rgba(102, 126, 234, 0.6),
                    0 0 80px rgba(102, 126, 234, 0.3);
        transform: scale(1.02);
    }

    /* Divider with gradient */
    hr {
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.5), transparent);
        height: 2px;
        border: none;
        margin: 2rem 0;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }

    hr:hover {
        box-shadow: 0 0 40px rgba(102, 126, 234, 0.6),
                    0 0 80px rgba(102, 126, 234, 0.4);
        height: 3px;
    }

    /* Enhanced markdown headings */
    h3, .stMarkdown h3 {
        color: #e0e7ff;
        text-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }

    h3:hover, .stMarkdown h3:hover {
        text-shadow: 0 0 20px rgba(102, 126, 234, 0.6),
                     0 0 40px rgba(102, 126, 234, 0.3);
        transform: translateX(3px);
    }

    /* Column hover effects */
    [data-testid="column"] {
        transition: all 0.3s ease;
        border-radius: 16px;
    }

    [data-testid="column"]:hover {
        background: rgba(102, 126, 234, 0.03);
    }

    /* Enhanced links */
    a {
        color: #667eea;
        text-decoration: none;
        transition: all 0.3s ease;
        text-shadow: 0 0 5px rgba(102, 126, 234, 0.2);
    }

    a:hover {
        color: #f093fb;
        text-shadow: 0 0 15px rgba(240, 147, 251, 0.6),
                     0 0 30px rgba(240, 147, 251, 0.3);
        transform: translateX(2px);
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(15, 15, 35, 0.5);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #f093fb 100%);
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.8),
                    0 0 40px rgba(102, 126, 234, 0.5);
    }

    /* Smooth transitions for all elements */
    * {
        transition: background-color 0.3s ease, border-color 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'config'  # 'config' or 'results'
if 'results' not in st.session_state:
    st.session_state.results = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'workflow_completed' not in st.session_state:
    st.session_state.workflow_completed = False
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'allowed_sources' not in st.session_state:
    st.session_state.allowed_sources = ["crunchbase.com", "techcrunch.com", "pitchbook.com", "linkedin.com"]
if 'additional_criteria' not in st.session_state:
    st.session_state.additional_criteria = ""

# Main header
st.markdown('<div class="main-header">🚀 VC Pitch Deck Analyzer</div>', unsafe_allow_html=True)

# Configuration Page
if st.session_state.page == 'config':
    st.markdown("---")

    # Create a centered container
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # File upload section
        st.markdown("### 📄 Upload Pitch Deck")
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help="Upload a startup pitch deck in PDF format",
            key="file_uploader"
        )

        if uploaded_file:
            st.session_state.uploaded_file = uploaded_file
            st.success(f"✅ File uploaded: {uploaded_file.name}")

        st.markdown("---")

        # Web search sources configuration
        st.markdown("### 🔍 Web Search Sources")
        default_sources = ["crunchbase.com", "techcrunch.com", "pitchbook.com", "linkedin.com"]
        sources_text = st.text_area(
            "Allowed sources (one per line)",
            value="\n".join(st.session_state.allowed_sources),
            height=120,
            help="Specify websites to focus on during web research"
        )
        st.session_state.allowed_sources = [source.strip() for source in sources_text.split('\n') if source.strip()]

        st.markdown("---")

        # Additional evaluation criteria
        st.markdown("### 📋 Additional Criteria")
        additional_criteria = st.text_area(
            "Additional evaluation criteria",
            value=st.session_state.additional_criteria,
            height=150,
            help="Add custom criteria to enhance the evaluation prompt"
        )
        st.session_state.additional_criteria = additional_criteria

        st.markdown("---")

        # Run analysis button
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.session_state.uploaded_file:
                if st.button("🚀 Run Analysis", type="primary", use_container_width=True):
                    st.session_state.page = 'results'
                    st.session_state.workflow_completed = False
                    st.session_state.results = None
                    st.session_state.chat_history = []
                    st.session_state.generated_email = None
                    st.rerun()
            else:
                st.button("🚀 Run Analysis", type="primary", use_container_width=True, disabled=True)
                st.info("Please upload a PDF file to continue")

        st.markdown('</div>', unsafe_allow_html=True)

# Results Page
elif st.session_state.page == 'results':
    # Add a back button
    if st.button("← Back to Configuration"):
        st.session_state.page = 'config'
        st.rerun()

    st.markdown("---")

    # Run workflow if not completed
    if not st.session_state.workflow_completed:
        # Save uploaded file temporarily
        tmp_dir = Path("tmp")
        tmp_dir.mkdir(exist_ok=True)
        file_path = tmp_dir / st.session_state.uploaded_file.name

        with open(file_path, "wb") as f:
            f.write(st.session_state.uploaded_file.getbuffer())

        # Create progress container
        progress_container = st.container()

        with progress_container:
            st.markdown('<div class="sub-header">Analysis Progress</div>', unsafe_allow_html=True)

            # Step 1: Pitch Deck Analysis
            with st.status("📊 Analyzing pitch deck...", expanded=True) as status:
                st.write("Reading PDF and evaluating...")

                # Combine instruction with additional criteria
                combined_instruction = instruction
                if st.session_state.additional_criteria.strip():
                    combined_instruction += f"\n\nADDITIONAL CRITERIA:\n{st.session_state.additional_criteria}"

                success, prediction, reasoning, missing = get_prediction(
                    client=client,
                    model=model,
                    instruction=combined_instruction,
                    pdf_filename=st.session_state.uploaded_file.name
                )

                if success:
                    st.write("✅ Pitch deck analysis completed")
                    status.update(label="✅ Pitch deck analysis completed", state="complete")
                else:
                    st.error("❌ Error analyzing pitch deck")
                    status.update(label="❌ Error analyzing pitch deck", state="error")
                    st.stop()

            # Step 2: Web Research
            with st.status("🌐 Conducting web research...", expanded=True) as status:
                st.write(f"Searching for additional information...")

                web_success, web_prediction, web_reasoning, web_sources = do_websearch(
                    client=client,
                    model=model,
                    missing=missing,
                    allowed_sources=st.session_state.allowed_sources
                )

                if web_success:
                    st.write("✅ Web research completed")
                    status.update(label="✅ Web research completed", state="complete")
                else:
                    st.error("❌ Error during web research")
                    status.update(label="❌ Error during web research", state="error")
                    st.stop()

            # Step 3: Generate Summary
            with st.status("📝 Generating comprehensive summary...", expanded=True) as status:
                st.write("Synthesizing findings...")

                summary_success, summary_text, final_prediction = summary(
                    model=model,
                    text_1=reasoning,
                    text_2=web_reasoning,
                    score_1=prediction,
                    score_2=web_prediction
                )

                if summary_success:
                    st.write("✅ Summary generated")
                    status.update(label="✅ Summary generated", state="complete")
                else:
                    st.error("❌ Error generating summary")
                    status.update(label="❌ Error generating summary", state="error")
                    st.stop()

            # Store results in session state
            st.session_state.results = {
                'pitch_deck': {
                    'prediction': prediction,
                    'reasoning': reasoning
                },
                'web_research': {
                    'prediction': web_prediction,
                    'reasoning': web_reasoning,
                    'sources': web_sources
                },
                'summary': summary_text,
                'final_prediction': final_prediction,
                'filename': st.session_state.uploaded_file.name
            }
            st.session_state.workflow_completed = True

            st.success("🎉 Analysis complete!")
            st.rerun()

    # Display results if available
    if st.session_state.results:
        results = st.session_state.results

        st.markdown('<div class="sub-header">Analysis Results</div>', unsafe_allow_html=True)

        # Traffic light indicator
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            color_class = results['final_prediction']
            color_emoji = {
                'green': '🟢',
                'yellow': '🟡',
                'red': '🔴'
            }
            st.markdown(f"### {color_emoji[color_class]} Overall Assessment")
            st.markdown(f'<div class="traffic-light {color_class}"></div>', unsafe_allow_html=True)

            if color_class == 'green':
                st.success("Both analyses predict success")
            elif color_class == 'red':
                st.error("Both analyses predict failure")
            else:
                st.warning("Mixed predictions - further investigation recommended")

        st.markdown("---")

        # Summary
        st.markdown("### 📝 Executive Summary")
        st.markdown(f'<div class="result-card">{results["summary"]}</div>', unsafe_allow_html=True)

        # Detailed reasoning in accordions
        st.markdown("### 🔍 Detailed Analysis")

        with st.expander("📄 Pitch Deck Analysis", expanded=False):
            prediction_emoji = "✅" if results['pitch_deck']['prediction'] else "❌"
            st.markdown(f"**Prediction:** {prediction_emoji} {'Success' if results['pitch_deck']['prediction'] else 'Failure'}")
            st.markdown("**Reasoning:**")
            st.markdown(results['pitch_deck']['reasoning'])

        with st.expander("🌐 Web Research Analysis", expanded=False):
            prediction_emoji = "✅" if results['web_research']['prediction'] else "❌"
            st.markdown(f"**Prediction:** {prediction_emoji} {'Success' if results['web_research']['prediction'] else 'Failure'}")
            st.markdown("**Reasoning:**")
            st.markdown(results['web_research']['reasoning'])

            if results['web_research']['sources']:
                st.markdown("**Sources:**")
                for i, source in enumerate(results['web_research']['sources'], 1):
                    if isinstance(source, dict):
                        st.markdown(f"{i}. [{source['title']}]({source['url']})")
                    else:
                        st.markdown(f"{i}. {source}")

        # Email Generation Section
        st.markdown("---")
        st.markdown('<div class="sub-header">Generate Founder Response</div>', unsafe_allow_html=True)

        # Initialize email state if not exists
        if 'generated_email' not in st.session_state:
            st.session_state.generated_email = None

        col_email1, col_email2, col_email3 = st.columns([1, 2, 1])
        with col_email2:
            # Determine email type
            email_type = "invitation" if results['final_prediction'] == 'green' else "rejection"
            email_icon = "✅" if email_type == "invitation" else "📧"

            st.info(f"{email_icon} Email Type: **{email_type.title()}** - Based on {'positive' if email_type == 'invitation' else 'mixed or negative'} analysis results")

            if st.button("📝 Generate Email", type="primary", use_container_width=True):
                with st.spinner("Generating personalized email..."):
                    # Extract startup name from filename (remove .pdf extension)
                    startup_name = results['filename'].replace('.pdf', '').replace('_', ' ').replace('-', ' ').title()

                    success, subject, body = generate_email(
                        model=model,
                        final_prediction=results['final_prediction'],
                        pitch_deck_reasoning=results['pitch_deck']['reasoning'],
                        web_research_reasoning=results['web_research']['reasoning'],
                        summary_text=results['summary'],
                        startup_name=startup_name
                    )

                    if success:
                        st.session_state.generated_email = {
                            'subject': subject,
                            'body': body,
                            'type': email_type
                        }
                        st.success("✅ Email generated successfully!")
                        st.rerun()

        # Display generated email if available
        if st.session_state.generated_email:
            st.markdown("### 📧 Generated Email")
            email_data = st.session_state.generated_email

            with st.container():
                st.markdown(f"**Subject:** {email_data['subject']}")
                st.markdown("**Body:**")
                st.markdown(email_data['body'])
                st.markdown('</div>', unsafe_allow_html=True)

            # Create mailto link
            col_mail1, col_mail2, col_mail3 = st.columns([1, 2, 1])
            with col_mail2:
                # URL encode the subject and body
                encoded_subject = urllib.parse.quote(email_data['subject'])
                encoded_body = urllib.parse.quote(email_data['body'])
                mailto_link = f"mailto:?subject={encoded_subject}&body={encoded_body}"

                st.markdown(f"""
                    <a href="{mailto_link}" target="_blank">
                        <button style="
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            color: white;
                            border: none;
                            border-radius: 12px;
                            padding: 12px 24px;
                            font-weight: 600;
                            font-size: 1.1rem;
                            cursor: pointer;
                            width: 100%;
                            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
                            transition: all 0.3s ease;
                        ">
                            📬 Open in Email Client
                        </button>
                    </a>
                """, unsafe_allow_html=True)

                st.caption("Click to open this email in your default email program")

        # Chat interface
        st.markdown("---")
        st.markdown('<div class="sub-header">💬 Chat with Your Data</div>', unsafe_allow_html=True)
        st.markdown("Ask questions about the analysis results")

        # Create context from results
        context = f"""
        Pitch Deck Analysis Results for {results['filename']}:

        Overall Assessment: {results['final_prediction']}

        Pitch Deck Prediction: {'Success' if results['pitch_deck']['prediction'] else 'Failure'}
        Pitch Deck Reasoning: {results['pitch_deck']['reasoning']}

        Web Research Prediction: {'Success' if results['web_research']['prediction'] else 'Failure'}
        Web Research Reasoning: {results['web_research']['reasoning']}

        Executive Summary: {results['summary']}
        """

        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("Ask a question about the analysis..."):
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": prompt})

            # Display user message immediately
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # Load and encode the PDF
                    import base64
                    tmp_path = Path("tmp") / results['filename']
                    with open(tmp_path, 'rb') as f:
                        pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

                    # Build messages with PDF in the first message
                    chat_messages = []
                    for i, msg in enumerate(st.session_state.chat_history):
                        if i == 0:
                            # First message includes the PDF
                            chat_messages.append({
                                "role": msg["role"],
                                "content": [
                                    {
                                        "type": "document",
                                        "source": {
                                            "type": "base64",
                                            "media_type": "application/pdf",
                                            "data": pdf_data
                                        }
                                    },
                                    {
                                        "type": "text",
                                        "text": msg["content"]
                                    }
                                ]
                            })
                        else:
                            chat_messages.append({
                                "role": msg["role"],
                                "content": msg["content"]
                            })

                    response = client.messages.create(
                        model=model,
                        max_tokens=8192,
                        system=f"You are a helpful VC analyst assistant. You have access to the original pitch deck PDF and the analysis results. Answer questions based on both the PDF and the following analysis context:\n\n{context}\n\nYou also have access to web search to find additional information if needed.",
                        messages=chat_messages,
                        tools=[
                            {
                                "type": "web_search_20250305",
                                "name": "web_search"
                            }
                        ]
                    )

                    # Extract text from response and sources
                    assistant_message = ""
                    chat_sources = []

                    for content in response.content:
                        if content.type == "text":
                            assistant_message += content.text
                            # Extract citations if available
                            if hasattr(content, 'citations') and content.citations:
                                for citation in content.citations:
                                    if hasattr(citation, 'url'):
                                        chat_sources.append({
                                            'url': citation.url,
                                            'title': getattr(citation, 'title', citation.url)
                                        })

                    # Add sources to message if any
                    if chat_sources:
                        assistant_message += "\n\n**Sources:**\n"
                        for i, source in enumerate(chat_sources, 1):
                            assistant_message += f"{i}. [{source['title']}]({source['url']})\n"

                # Display assistant message
                st.markdown(assistant_message)

                # Add assistant message to chat history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": assistant_message
                })
