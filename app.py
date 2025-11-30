import streamlit as st
import os
from pathlib import Path
from ai_config.functions import get_prediction, do_websearch, summary
from ai_config.config import client, model, instruction

# Page configuration
st.set_page_config(
    page_title="VC Pitch Deck Analyzer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #1f77b4;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .traffic-light {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        margin: 20px auto;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .green {
        background-color: #28a745;
    }
    .yellow {
        background-color: #ffc107;
    }
    .red {
        background-color: #dc3545;
    }
    .result-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin-bottom: 20px;
    }
    .config-card {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 10px;
        border: 2px solid #1f77b4;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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
    st.markdown("Configure your pitch deck analysis")
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

    st.markdown("Analyze startup pitch decks with AI-powered evaluation and web research")
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
                st.write(f"Focusing on: {', '.join(st.session_state.allowed_sources)}")

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

        st.markdown("---")
        st.markdown('<div class="sub-header">📊 Analysis Results</div>', unsafe_allow_html=True)

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

            # Display user message
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
                        max_tokens=2048,
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

                    st.markdown(assistant_message)

                    # Display sources if any
                    if chat_sources:
                        st.markdown("**Sources:**")
                        for i, source in enumerate(chat_sources, 1):
                            st.markdown(f"{i}. [{source['title']}]({source['url']})")

                    # Add assistant message to chat history
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": assistant_message
                    })
