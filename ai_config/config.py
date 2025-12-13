"""
Konfigurationsdatei für die VC Pitch Deck Analyzer Anwendung.

Diese Datei enthält alle wichtigen Konfigurationseinstellungen wie:
- API-Konfiguration für Anthropic Claude
- Verzeichnispfade
- Modellkonfiguration
- Bewertungsanweisungen für die KI
"""

import os
from anthropic import AnthropicFoundry
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus der .env Datei
load_dotenv()

# Anthropic API Konfiguration
# API-Schlüssel und Endpunkt werden aus den Umgebungsvariablen geladen
API_KEY = os.environ.get("API_KEY", "")
API_ENDPOINT = os.environ.get("API_ENDPOINT", "")

# Initialisiere den Anthropic Client mit API-Schlüssel und Endpunkt
client = AnthropicFoundry(
    api_key=API_KEY,
    base_url=API_ENDPOINT
)

# Verzeichnispfade für Pitch Decks
pitch_deck_dir = "./pitch_decks/"

# Claude Modell für die Bewertung
# claude-haiku-4-5 ist ein schnelles und kostengünstiges Modell
model = "claude-haiku-4-5"

# Bewertungskriterien als strukturierte Daten
# Diese Kategorien können vom Nutzer gewichtet werden
EVALUATION_CRITERIA = {
    "COMPANY": """location and geographical relevance (in which country/region the startup operates and how strategic
this market is); company age and stage of development (maturity of product, customers, organization); clarity of
the business model and value creation logic (how the startup makes money and captures value).""",

    "COMPETITION": """existing competitors and role models (current solutions to the problem); how clearly the startup is
positioned against them; strength of differentiation and sustainable advantage (true USP vs. incremental
features); global proof points that similar models have already succeeded in the US or other leading markets.""",

    "FINANCIALS": """quality and relevance of KPIs (retention, conversion, CAC, LTV); evidence of traction through
improving KPIs; robustness of the financial forecast (revenue path and potential profitability); ownership
structure / cap table health (equity split and suitability for future funding rounds); investor quality
(reputation, track record, strategic fit); consistency of financing history (number, spacing and logic of past
rounds); valuation rationality relative to traction, team and market; capital efficiency (burn rate versus
achieved milestones).""",

    "MARKET": """clarity and plausibility of TAM, SAM, SOM and overall market sizing; market growth dynamics (current and
expected growth rates); definition of target customers and buyer segments; resilience under economic stress
tests; specific structural characteristics of the market; overall growth potential and attractiveness; market
maturity (fragmented vs. consolidated with strong incumbents); intensity of competition and quality of other
players' backing; barriers to entry (regulatory, technological, capital, data/network effects, switching
costs); regulatory exposure of the business model; macroeconomic sensitivity of demand.""",

    "PRODUCT": """credibility of the roadmap from MVP to a full, top-level product and concreteness of implementation
planning; existence of real demand for the solution (does the market truly need this product); role in the value
chain and length/complexity of the sales cycle; quality of the customer journey and UX for both digital and
physical touchpoints; technical and content-related feasibility; soundness of software architecture decisions;
features and differentiation at product level (product USP); potential for profitability on a unit basis (fixed
plus variable costs per unit vs. achievable revenue); depth of product–market fit (must-have problem solver vs.
"nice to have").""",

    "TEAM": """educational background and work experience (e.g., top universities, leading tech/bank/consulting/startup/
VC firms); relevant industry experience in the startup's domain; complementary and heterogeneous skill sets
across business, technology and industry expertise; clarity on planned next hires to enable growth; founders'
vision, drive and motivation; presence of serial entrepreneurs with successful founding history; quality of team
dynamics and collaboration; leadership experience of the founding team; depth of industry-specific expertise;
strength and relevance of the professional network; founder stability and retention risk over the long term."""
}

def build_instruction_with_weights(criteria_weights: dict = None, additional_criteria: list = None):
    """
    Erstellt die Bewertungsanweisung mit gewichteten Kriterien.

    Args:
        criteria_weights (dict): Dictionary mit Kategorie -> Gewichtung ("niedrig", "mittel", "hoch")
        additional_criteria (list): Liste von Dicts mit {"weight": str, "description": str}

    Returns:
        str: Vollständige Bewertungsanweisung mit Gewichtungen
    """
    # Standard-Gewichtung falls keine angegeben
    if criteria_weights is None:
        criteria_weights = {key: "mittel" for key in EVALUATION_CRITERIA.keys()}

    # Gewichtungs-Mapping
    weight_instructions = {
        "niedrig": "Gewichte diese Kategorie GERINGER in deiner Gesamtbewertung",
        "mittel": "Gewichte diese Kategorie STANDARD in deiner Gesamtbewertung",
        "hoch": "Gewichte diese Kategorie HÖHER in deiner Gesamtbewertung - dies ist KRITISCH für die Investitionsentscheidung"
    }

    instruction_parts = ["""Du bist ein erfahrener Venture Capital Analyst. Bewerte ein Startup Pitch Deck objektiv basierend auf den folgenden
Kategorien und Kriterien. Analysiere die Informationen sorgfältig, identifiziere Stärken und Risiken und nutze dein Urteilsvermögen,
um zu entscheiden, ob das Startup voraussichtlich überleben und erfolgreich sein wird.

BEWERTUNGSRAHMEN:
"""]

    # Füge jede Kategorie mit Gewichtung hinzu
    for category, description in EVALUATION_CRITERIA.items():
        weight = criteria_weights.get(category, "mittel")
        weight_instruction = weight_instructions.get(weight, weight_instructions["mittel"])

        instruction_parts.append(f"{category} [{weight_instruction}]: {description}\n")

    # Füge zusätzliche Kriterien hinzu
    if additional_criteria:
        instruction_parts.append("\nZUSÄTZLICHE BENUTZERDEFINIERTE KRITERIEN:\n")
        for criterion in additional_criteria:
            if criterion.get("description", "").strip():
                weight = criterion.get("weight", "mittel")
                weight_instruction = weight_instructions.get(weight, weight_instructions["mittel"])
                instruction_parts.append(f"[{weight_instruction}]: {criterion['description']}\n")

    instruction_parts.append("""
Denke alle Dimensionen ganzheitlich durch und berücksichtige sowohl qualitative Narrative als auch quantitative Beweise.
Ignoriere Hype und konzentriere dich auf Fundamentaldaten wie Wettbewerbsvorteile, Ausführungsfähigkeit, Product-Market Fit und finanzielle
Tragfähigkeit.

WICHTIG: Antworte in deutscher Sprache!

Ausgabeformat:
PREDICTION: [true/false]
REASONING: [Gib eine kurze Begründung in 2-3 Sätzen auf Deutsch, die die Schlüsselfaktoren erklärt, die zu deiner Entscheidung geführt haben]
MISSING: [Falls Informationen für eine Dimension (z.B. TEAM, PRODUCT) fehlen, erstelle optimale Prompts für einen WebSearch-KI-Assistenten, um die fehlenden Informationen zu recherchieren.
Füge so viele relevante Kontextinformationen wie Namen hinzu. Füge zusätzlich immer die Namen des Teams und eine kurze Marktbeschreibung hinzu, um sie an den WebSearch-Assistenten weiterzugeben]
""")

    return "".join(instruction_parts)

# Standard-Instruktion mit mittlerer Gewichtung für alle Kriterien
instruction = build_instruction_with_weights()