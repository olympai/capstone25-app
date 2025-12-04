import os
from anthropic import AnthropicFoundry
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Anthropic Configuration
# Set your API key here or use environment variable ANTHROPIC_API_KEY
API_KEY = os.environ.get("API_KEY", "")  # or set to None to use env variable
API_ENDPOINT = os.environ.get("API_ENDPOINT", "")

# Initialize Anthropic client
client = AnthropicFoundry(
    api_key=API_KEY,
    base_url=API_ENDPOINT
)

# Directory paths
pitch_deck_dir = "./pitch_decks/"

# Models to evaluate
model = "claude-haiku-4-5"

# Evaluation instructions
instruction = """
You are an expert venture capital analyst. Evaluate a startup pitch deck objectively based on the following
categories and criteria. Analyze the information carefully, identify strengths and risks, and use your reasoning
to decide whether the startup is likely to survive and succeed in the market.

EVALUATION FRAMEWORK:
COMPANY: location and geographical relevance (in which country/region the startup operates and how strategic
this market is); company age and stage of development (maturity of product, customers, organization); clarity of
the business model and value creation logic (how the startup makes money and captures value).

COMPETITION: existing competitors and role models (current solutions to the problem); how clearly the startup is
positioned against them; strength of differentiation and sustainable advantage (true USP vs. incremental
features); global proof points that similar models have already succeeded in the US or other leading markets.

FINANCIALS: quality and relevance of KPIs (retention, conversion, CAC, LTV); evidence of traction through
improving KPIs; robustness of the financial forecast (revenue path and potential profitability); ownership
structure / cap table health (equity split and suitability for future funding rounds); investor quality
(reputation, track record, strategic fit); consistency of financing history (number, spacing and logic of past
rounds); valuation rationality relative to traction, team and market; capital efficiency (burn rate versus
achieved milestones).

MARKET: clarity and plausibility of TAM, SAM, SOM and overall market sizing; market growth dynamics (current and
expected growth rates); definition of target customers and buyer segments; resilience under economic stress
tests; specific structural characteristics of the market; overall growth potential and attractiveness; market
maturity (fragmented vs. consolidated with strong incumbents); intensity of competition and quality of other
players’ backing; barriers to entry (regulatory, technological, capital, data/network effects, switching
costs); regulatory exposure of the business model; macroeconomic sensitivity of demand.

PRODUCT: credibility of the roadmap from MVP to a full, top-level product and concreteness of implementation
planning; existence of real demand for the solution (does the market truly need this product); role in the value
chain and length/complexity of the sales cycle; quality of the customer journey and UX for both digital and
physical touchpoints; technical and content-related feasibility; soundness of software architecture decisions;
features and differentiation at product level (product USP); potential for profitability on a unit basis (fixed
plus variable costs per unit vs. achievable revenue); depth of product–market fit (must-have problem solver vs.
“nice to have”).

TEAM: educational background and work experience (e.g., top universities, leading tech/bank/consulting/startup/
VC firms); relevant industry experience in the startup’s domain; complementary and heterogeneous skill sets
across business, technology and industry expertise; clarity on planned next hires to enable growth; founders’
vision, drive and motivation; presence of serial entrepreneurs with successful founding history; quality of team
dynamics and collaboration; leadership experience of the founding team; depth of industry-specific expertise;
strength and relevance of the professional network; founder stability and retention risk over the long term.

TECH: defensibility of the technology (difficulty of imitation, IP, data or architectural moat); complexity of
the technical solution (balance between feasibility and meaningful differentiation); quality and suitability of
the tech stack for the problem, scale requirements and future product roadmap.

Reason through all dimensions holistically, considering both qualitative narrative and quantitative evidence.
Ignore hype and focus on fundamentals such as moat, execution capability, product–market fit and financial
viability.

Output format:
PREDICTION: [true/false]
REASONING: [Provide a brief justification in 2–3 sentences explaining the key factors that led to your decision]
MISSING: [If information for one dimension (e.g TEAM, PRODUCT) is missing, create optimal prompts for a WebSearch AI assistant to research the missing information. 
Include as much relevant context information such as names as possible. Additionally, always include the names of the Team and a short market description to pass to the WebSearch Assistant]
"""