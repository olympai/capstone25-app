# VC Pitch Deck Analyzer

## Overview

An AI-powered Streamlit application that analyzes startup pitch decks using Claude AI. The system evaluates pitch decks across seven key investment dimensions (Company, Competition, Financials, Market, Product, Team, Technology), conducts automated web research to validate claims and fill information gaps, then synthesizes findings into a traffic light assessment and executive summary.

**Disclaimer:** This tool generates analytical signals to support due diligence processes. Outputs represent AI-based interpretations and should not be used as the sole basis for investment decisions. Professional judgment and comprehensive due diligence remain essential.

## Quickstart

```bash
# Clone repository
git clone https://github.com/olympai/capstone25-app.git
cd capstone25-app

# Configure credentials
cat > .env << EOF
API_KEY=your_anthropic_api_key
API_ENDPOINT=your_api_endpoint_url
EOF

# Launch application (creates virtual environment and installs all dependencies)
./run.sh
```

Access the application at `http://localhost:8501`

## Tech Stack

**Frontend**
- Streamlit (>=1.28.0)

**AI & Processing**
- Anthropic Claude API (v0.75.0)
- Model: `claude-haiku-4-5`
- Native PDF parsing via Claude API
- Web search via Claude's `web_search_20250305` tool

**Data Storage**
- Session-based (in-memory)
- Temporary PDF storage in `tmp/` directory

## Architecture & Data Flow

The application executes a three-stage analysis pipeline:

**Stage 1: Pitch Deck Analysis**
- User uploads PDF via web interface
- PDF encoded and sent to Claude AI
- Evaluation against structured framework covering Company, Competition, Financials, Market, Product, Team, and Technology dimensions
- Output: Success/failure prediction, reasoning, and identified information gaps

**Stage 2: Web Research**
- Claude conducts automated web search to address information gaps
- Focuses on configured sources (default: Crunchbase, TechCrunch, PitchBook, LinkedIn)
- Output: Second prediction, reasoning, and source citations

**Stage 3: Summary Generation**
- Synthesizes findings from both analyses
- Generates traffic light indicator:
  - **Green**: Both analyses predict success
  - **Red**: Both analyses predict failure
  - **Yellow**: Mixed predictions
- Produces executive summary

**Interactive Chat**
- Context-aware Q&A about analysis results
- Access to original PDF content and web search capability

## Configuration

**Required Environment Variables** (`.env` file):

```bash
API_KEY=<your-anthropic-api-key>
API_ENDPOINT=<your-api-endpoint>
```

**Application Settings** (configurable via UI):
- Web search sources (domain list)
- Additional evaluation criteria (custom prompts)

**System Configuration:**
- Model: `claude-haiku-4-5` (`ai_config/config.py:19`)
- Server port: 8501 (`.streamlit/config.toml`)

## Usage

**1. Configuration**
- Upload PDF pitch deck
- Optionally customize web search sources
- Add any additional evaluation criteria

**2. Analysis**
- Click "Run Analysis"
- Monitor progress through three stages (pitch deck → web research → summary)
- Wait for completion (typically 35-105 seconds)

**3. Review Results**
- View traffic light assessment
- Read executive summary
- Expand detailed reasoning sections
- Review cited sources

**4. Ask Questions**
- Use chat interface for follow-up queries
- System has access to original PDF and analysis context
- Can perform additional web searches as needed

## Scoring & Interpretation

**Traffic Light System:**
- **Green (🟢)**: Both pitch deck and web research analyses predict success
- **Yellow (🟡)**: Conflicting predictions; further investigation recommended
- **Red (🔴)**: Both analyses predict failure

**Recommended Use:**
This tool is designed as a preliminary screening and due diligence support system. Combine outputs with traditional analysis methods, domain expertise, and comprehensive research before making investment decisions.

## Troubleshooting

**Analysis Errors**

*"Error analyzing pitch deck"*
- Verify API credentials in `.env` file
- Ensure PDF is readable and not corrupted
- Check PDF contains extractable text (not just scanned images)

*"Error during web research"*
- Confirm internet connectivity
- Verify Anthropic API service status
- Retry after brief wait (may be transient network issue)

**Application Errors**

*ModuleNotFoundError on startup*
```bash
source venv/bin/activate
pip install -r requirements.txt
```

*Port 8501 already in use*
```bash
streamlit run app.py --server.port 8502
```

*Chat not responding*
- Check browser console for JavaScript errors (F12)
- Verify PDF file still exists in `tmp/` directory
- Confirm API credentials remain valid

## Development

**Project Structure:**
```
app.py                      # Main application and UI
ai_config/
  config.py                 # API configuration and evaluation framework
  functions.py              # Core analysis functions
  pdf_export.py             # PDF Export
  workflow.py               # Orchestration
tmp/                        # Temporary PDF storage
.streamlit/config.toml      # Application settings
requirements.txt            # Python dependencies
run.sh                      # Start Script
```

## License

License not specified. Contact repository maintainer for licensing information and usage rights.

## Use of AI
Claude by Anthropic was used to support bug fixing and testing throughout the development process.