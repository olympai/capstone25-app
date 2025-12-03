# VC Pitch Deck Analyzer

## TO START RUN: ./run.sh

An AI-powered Streamlit application for analyzing startup pitch decks using Claude AI. The application performs comprehensive evaluations combining pitch deck analysis with web research to provide investment insights.

## Features

- **PDF Upload**: Upload startup pitch decks in PDF format
- **AI-Powered Analysis**: Leverages Claude AI to evaluate pitch decks across multiple dimensions:
  - Company & Business Model
  - Competition & Market Position
  - Financials & Metrics
  - Market Size & Dynamics
  - Product & Technology
  - Team & Expertise
- **Web Research**: Automatically researches missing information using web search
- **Traffic Light Scoring**: Visual red/yellow/green indicator for quick assessment
- **Detailed Reports**: Comprehensive reasoning for both pitch deck and web research analyses
- **Interactive Chat**: Chat interface to ask questions about the analysis results
- **Customizable Criteria**: Add additional evaluation criteria to the analysis
- **Source Configuration**: Specify preferred web sources for research

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd capstone25-app
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root with:
```
API_KEY=your_anthropic_api_key
API_ENDPOINT=your_api_endpoint
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Configure the analysis:
   - Upload a pitch deck PDF
   - Customize web search sources (optional)
   - Add additional evaluation criteria (optional)

4. Run the analysis:
   - Click "Run Analysis"
   - Wait for the workflow to complete (pitch deck analysis → web research → summary)

5. Review results:
   - Check the traffic light indicator for overall assessment
   - Read the executive summary
   - Expand accordions for detailed reasoning
   - Use the chat interface to ask questions

## Project Structure

```
capstone25-app/
├── app.py                 # Main Streamlit application
├── ai_config/
│   ├── config.py          # API configuration and evaluation instructions
│   └── functions.py       # Core AI functions (prediction, web search, summary)
├── tmp/                   # Temporary directory for uploaded files
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in version control)
└── README.md             # This file
```

## How It Works

### 1. Pitch Deck Analysis
The application uses Claude AI with a structured evaluation framework to analyze:
- Company location, stage, and business model
- Competitive positioning and differentiation
- Financial metrics and traction
- Market size and growth potential
- Product roadmap and technical feasibility
- Team experience and capabilities

### 2. Web Research
Based on missing information identified in the pitch deck, the system:
- Conducts targeted web searches
- Focuses on specified sources (Crunchbase, TechCrunch, etc.)
- Gathers additional context about the market and team

### 3. Summary Generation
Combines insights from both analyses to provide:
- Comprehensive executive summary
- Overall assessment (green/yellow/red)
- Detailed reasoning from both sources

### 4. Interactive Q&A
Chat interface allows you to:
- Ask questions about specific aspects of the analysis
- Explore implications of the findings
- Get clarification on recommendations

## Configuration

### Evaluation Criteria
The default evaluation framework covers:
- **Company**: Location, stage, business model
- **Competition**: Market positioning, differentiation
- **Financials**: KPIs, traction, valuation, cap table
- **Market**: TAM/SAM/SOM, growth dynamics, barriers to entry
- **Product**: Roadmap, product-market fit, UX
- **Team**: Experience, skills, network
- **Technology**: Defensibility, complexity, tech stack

### Web Search Sources
Default sources include:
- crunchbase.com
- techcrunch.com
- pitchbook.com
- linkedin.com

You can customize these in the sidebar.

## Traffic Light Scoring

- **🟢 Green**: Both pitch deck and web research predict success
- **🟡 Yellow**: Mixed predictions (further investigation recommended)
- **🔴 Red**: Both analyses predict failure

## Requirements

- Python 3.9+
- Anthropic API key with Claude access
- Internet connection for web search functionality

## Troubleshooting

**Issue**: "Error analyzing pitch deck"
- Check that your API key is valid
- Ensure the PDF is readable and not corrupted
- Verify your API endpoint is correct

**Issue**: "Error during web research"
- Check internet connectivity
- Verify web search is enabled for your API key
- Try with default sources first

**Issue**: Streamlit won't start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.9+)
- Try clearing Streamlit cache: `streamlit cache clear`

## Support

For issues and questions, please open an issue on GitHub.
