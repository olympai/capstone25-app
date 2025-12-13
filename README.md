# VC Pitch Deck Analyzer

## Overview

An AI-powered Streamlit application that analyzes startup pitch decks using Claude AI. The system evaluates pitch decks across seven key investment dimensions (Company, Competition, Financials, Market, Product, Team, Technology), conducts automated web research to validate claims and fill information gaps, then synthesizes findings into a traffic light assessment and executive summary.

**Disclaimer:** This tool generates analytical signals to support due diligence processes. Outputs represent AI-based interpretations and should not be used as the sole basis for investment decisions. Professional judgment and comprehensive due diligence remain essential.

## Quickstart

```bash
# Clone repository
git clone <repository-url>
cd capstone25-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure credentials
cat > .env << EOF
API_KEY=your_anthropic_api_key
API_ENDPOINT=your_api_endpoint_url
EOF

# Launch application
streamlit run app.py
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
- Token limits: 2048 (analysis), 4096 (research), 1024 (summary)
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

**Important Limitations:**
- Predictions are binary (success/failure) without probability estimates
- System has not been validated against actual startup outcomes
- Results sensitive to prompt formulation and input quality
- Web search quality varies based on available public information
- No calibration to real-world success base rates

**Recommended Use:**
This tool is designed as a preliminary screening and due diligence support system. Combine outputs with traditional analysis methods, domain expertise, and comprehensive research before making investment decisions.

## Data Privacy & Security

**Data Handling:**
- Uploaded PDFs temporarily stored in `tmp/` directory
- PDFs transmitted to Anthropic API for processing
- Analysis results stored in browser session only (not persisted to disk)
- Files not automatically deleted after analysis

**Third-Party Data Transmission:**
- Anthropic API: Full PDF content, company descriptions, analysis text
- Web search queries issued based on identified information gaps
- Subject to Anthropic's data retention and privacy policies

**Security Considerations:**
- No user authentication (suitable for trusted environments only)
- API credentials stored in plaintext `.env` file
- No encryption of uploaded files
- No rate limiting on API calls
- XSRF protection enabled

**Data Protection Recommendations:**
- Deploy behind authentication layer for multi-user environments
- Delete uploaded files manually from `tmp/` directory
- Store API credentials in secure secret management system
- Review Anthropic data processing agreement for regulatory compliance

## Limitations

**Technical Constraints:**
- PDF parsing relies on Claude's native capabilities (no OCR)
- Scanned images or complex layouts may not parse correctly
- No retry logic for API failures
- Web search source filtering passed as context only (not enforced)
- Session data lost on browser refresh
- No export functionality for analysis results

**Analytical Limitations:**
- AI may generate plausible but inaccurate reasoning
- No automated fact-checking or verification
- English-language evaluation framework only
- Web research limited to publicly available information
- Results dependent on current web content (may become stale)

**Operational Constraints:**
- Typical analysis time: 35-105 seconds
- No cost tracking or budget controls
- Concurrent file uploads may cause overwrites
- Requires stable internet connection

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
tmp/                        # Temporary PDF storage
.streamlit/config.toml      # Application settings
requirements.txt            # Python dependencies
```

**Customization Options:**

*Evaluation Framework*
- Modify prompt in `ai_config/config.py:22-78`
- Or add criteria via UI without code changes

*Model Selection*
- Edit `ai_config/config.py:19` to change Claude model

*Scoring Logic*
- Traffic light calculation in `ai_config/functions.py:204-211`

*Web Search Sources*
- Default sources in `app.py:76`

## Deployment Notes

**Streamlit Cloud Deployment:**
1. Connect repository to Streamlit Cloud
2. Add API credentials in Settings → Secrets:
```toml
[env]
API_KEY = "your-key"
API_ENDPOINT = "your-endpoint"
```
3. Update `ai_config/config.py` to read from `st.secrets` if deploying to cloud
4. Set app to private mode for access control

**Self-Hosted Deployment:**
- Use provided `run.sh` script or run `streamlit run app.py` directly
- Configure reverse proxy (nginx, Apache) for production environments
- Implement authentication layer for multi-user access
- Set up file cleanup process (manual or scheduled)
- Monitor API usage and costs

**Docker Deployment:**
```bash
docker build -t vc-analyzer .
docker run -p 8501:8501 --env-file .env vc-analyzer
```

## License

License not specified. Contact repository maintainer for licensing information and usage rights.
