"""
Funktionsmodul für die KI-gestützte Pitch Deck Analyse.

Dieses Modul enthält alle wichtigen Funktionen für:
- Pitch Deck Analyse mit Claude
- Web-Recherche für fehlende Informationen
- Zusammenfassung der Ergebnisse
- E-Mail-Generierung für Gründer
"""

import anthropic
import base64
from typing import Tuple

from ai_config.config import client, model

def get_prediction(client: anthropic.Anthropic = client, model: str = model, instruction: str = "", pdf_filename: str = "") -> Tuple[bool, str]:
    """
    Analysiert ein Pitch Deck PDF und erstellt eine Erfolgs-Prognose mit Claude AI.

    Die Funktion lädt ein PDF, kodiert es als Base64 und sendet es an Claude zur Analyse.
    Claude bewertet das Pitch Deck anhand definierter Kriterien und gibt eine strukturierte
    Bewertung zurück mit Prognose, Begründung und fehlenden Informationen.

    Args:
        client (anthropic.Anthropic): Anthropic API Client
        model (str): Name des zu verwendenden Modells (z.B. "claude-haiku-4-5")
        instruction (str): System-Anweisung mit Bewertungskriterien
        pdf_filename (str): Dateiname des PDF (liegt im tmp/ Ordner)

    Returns:
        Tuple[bool, bool, str, str]: (Erfolg, Prognose, Begründung, fehlende_Informationen)
            - Erfolg: True wenn Analyse erfolgreich, False bei Fehler
            - Prognose: True wenn Startup voraussichtlich erfolgreich, False sonst
            - Begründung: Textuelle Erklärung der Entscheidung
            - fehlende_Informationen: Informationen für Web-Recherche
    """
    try:
        # Lade und kodiere das PDF als Base64
        with open("tmp/" + pdf_filename, 'rb') as f:
            pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

        # Definiere das Tool für strukturierte Ausgabe
        # Claude nutzt dieses Schema, um die Bewertung zu formatieren
        evaluation_tool = {
            "name": "pitch_deck_evaluation",
            "description": "Provides a structured evaluation of a startup pitch deck with prediction, reasoning, and missing information",
            "input_schema": {
                "type": "object",
                "properties": {
                    "pitch": {
                        "type": "string",
                        "description": "Short description of the startups idea, market and founders (if available)."
                    },
                    "prediction": {
                        "type": "boolean",
                        "description": "True if the startup is likely to survive and succeed, False otherwise"
                    },
                    "reasoning": {
                        "type": "string",
                        "description": "Brief justification in 2-3 sentences explaining the key factors that led to the decision"
                    },
                    "missing": {
                        "type": "string",
                        "description": "Information that is missing from the pitch deck that would be helpful for a more accurate evaluation"
                    }
                },
                "required": ["pitch", "prediction", "reasoning", "missing"]
            }
        }

        # Erstelle API-Anfrage mit Base64-kodiertem PDF und Tool
        message = client.messages.create(
            model=model,
            max_tokens=8192,
            system=instruction,
            messages=[
                {
                    "role": "user",
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
                            "text": "Bitte bewerte dieses Pitch Deck und gib deine Einschätzung und Begründung auf Deutsch mit dem pitch_deck_evaluation Tool an."
                        }
                    ]
                }
            ],
            tools=[evaluation_tool],
            tool_choice={"type": "tool", "name": "pitch_deck_evaluation"}
        )

        # Extrahiere strukturierte Ausgabe vom Tool
        for content in message.content:
            if content.type == "tool_use" and content.name == "pitch_deck_evaluation":
                result = content.input
                prediction = result.get("prediction", False)
                reasoning = result.get("reasoning", "No reasoning provided")
                pitch = result.get("pitch", "")
                missing = pitch + result.get("missing", "")
                missing += " Recherchiere Informationen über den Markt und die Gründer"

                print(f"Prediction: {prediction}")
                print(f"Reasoning: {reasoning}")
                print(f"Missing: {missing}")

                return True, prediction, reasoning, missing

        # Fallback falls keine strukturierte Ausgabe gefunden wurde
        return False, False, "No structured output received", ""

    except Exception as e:
        print(f"Error in prediction for {pdf_filename}: {e}")
        return False, False, f"Error: {str(e)}", ""
    
def do_websearch(client: anthropic.Anthropic = client, model: str = model, missing: str = "", allowed_sources: list = []):
    """
    Führt eine umfassende Web-Recherche durch, um fehlende Informationen über das Startup
    und aktuelle Markt-Trends zu finden.

    Diese Funktion nutzt Claudes Web-Search Tool, um zusätzliche Informationen über
    das Startup zu recherchieren, die im Pitch Deck fehlen. Zusätzlich werden automatisch
    aktuelle Markt-Trends des Zielmarktes analysiert (letzte 6-12 Monate), einschließlich:
    - Marktentwicklungen und emerging Trends
    - Wachstumsprognosen und Marktdynamik
    - Regulatorische Änderungen
    - Technologie-Trends und Investitionsaktivität

    Die Recherche fokussiert sich auf definierte Quellen und erstellt eine eigenständige
    Bewertung unter Berücksichtigung der Markt-Trends.

    Args:
        client (anthropic.Anthropic): Anthropic API Client
        model (str): Name des zu verwendenden Modells
        missing (str): Beschreibung der fehlenden Informationen und Recherche-Anweisungen
        allowed_sources (list): Liste erlaubter Webseiten für die Recherche

    Returns:
        Tuple[bool, bool, str, list]: (Erfolg, Prognose, Begründung, Quellen)
            - Erfolg: True wenn Recherche erfolgreich, False bei Fehler
            - Prognose: True wenn Startup voraussichtlich erfolgreich, False sonst
            - Begründung: Textuelle Erklärung basierend auf Web-Recherche inkl. Markt-Trends
            - Quellen: Liste der genutzten Webseiten mit URLs und Titeln
    """
    try:
        # Definiere einfaches Bewertungs-Tool
        evaluation_tool = {
            "name": "evaluation",
            "description": "Provides prediction and reasoning based on web research",
            "input_schema": {
                "type": "object",
                "properties": {
                    "prediction": {
                        "type": "boolean",
                        "description": "True if the startup is likely to survive and succeed, False otherwise"
                    },
                    "reasoning": {
                        "type": "string",
                        "description": "Brief justification in 2-3 sentences explaining the key factors"
                    }
                },
                "required": ["prediction", "reasoning"]
            }
        }

        response = client.messages.create(
            model=model,
            max_tokens=8192,
            messages=[
                {
                    "role": "user",
                    "content": f"""Du bist ein VC-Research-Experte. Führe eine umfassende Recherche zu Folgendem durch:

1. FEHLENDE INFORMATIONEN: {missing}

2. MARKT-TRENDS (PFLICHT):
   Recherchiere und analysiere AKTUELLE Markt-Trends für den Zielmarkt des Startups:
   - Aktuelle Marktentwicklungen und aufkommende Trends (letzte 6-12 Monate)
   - Marktwachstumsentwicklung und Prognosen
   - Wichtige Markttreiber und Disruptoren
   - Regulatorische Änderungen oder politische Verschiebungen, die den Markt betreffen
   - Technologie-Trends, die die Branche beeinflussen
   - Veränderungen im Konsumentenverhalten und Nachfragemuster
   - Bemerkenswerte Investitionen oder M&A-Aktivitäten im Sektor
   - Expertenmeinungen und Analystenperspektiven zum Marktausblick

Fokussiere dich auf diese Quellen: {allowed_sources}

WICHTIG: Deine Bewertung muss Einblicke in aktuelle Markt-Trends enthalten und wie diese die Positionierung und das Wachstumspotenzial des Startups beeinflussen.

Nach deiner umfassenden Recherche nutze das evaluation Tool, um deine Vorhersage und Begründung auf Deutsch bereitzustellen, die sowohl die fehlenden Informationen ALS AUCH die Markt-Trends-Analyse einbezieht.
                    """
                }
            ],
            tools=[
                {
                    "type": "web_search_20250305",
                    "name": "web_search"
                },
                evaluation_tool
            ]
        )

        # Extrahiere Prognose, Begründung und Quellen aus der Antwort
        prediction = False
        reasoning = "No reasoning provided"
        sources = []

        for content in response.content:
            if content.type == "tool_use" and content.name == "evaluation":
                result = content.input
                prediction = result.get("prediction", False)
                reasoning = result.get("reasoning", "No reasoning provided")
            elif content.type == "text":
                # Extrahiere Quellen aus Citations falls vorhanden
                if hasattr(content, 'citations') and content.citations:
                    for citation in content.citations:
                        if hasattr(citation, 'url') and citation.url:
                            source_info = {
                                'url': citation.url,
                                'title': getattr(citation, 'title', citation.url)
                            }
                            sources.append(source_info)
            elif hasattr(content, 'type') and 'web_search' in str(content.type):
                # Extrahiere aus web_search_tool_result
                if hasattr(content, 'content') and isinstance(content.content, list):
                    for item in content.content:
                        if hasattr(item, 'url'):
                            source_info = {
                                'url': item.url,
                                'title': getattr(item, 'title', item.url)
                            }
                            sources.append(source_info)

        # Entferne doppelte URLs
        seen_urls = set()
        unique_sources = []
        for source in sources:
            if source['url'] not in seen_urls:
                seen_urls.add(source['url'])
                unique_sources.append(source)

        print(f"Prediction WS: {prediction}")
        print(f"Reasoning WS: {reasoning}")
        print(f"Sources: {unique_sources}")

        return True, prediction, reasoning, unique_sources

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False, False, f"Error: {str(e)}", []
    
def summary(model: str = model, text_1: str = "", text_2: str = "", score_1: bool = False, score_2: bool = False):
    """
    Fasst die Ergebnisse aus Pitch Deck Analyse und Web-Recherche zusammen.

    Diese Funktion kombiniert die Bewertungen aus beiden Analysen zu einer finalen
    Gesamtbewertung (Ampelsystem: grün/gelb/rot) und generiert eine zusammenfassende
    Textanalyse durch Claude.

    Args:
        model (str): Name des zu verwendenden Modells
        text_1 (str): Begründung aus der Pitch Deck Analyse
        text_2 (str): Begründung aus der Web-Recherche
        score_1 (bool): Prognose aus der Pitch Deck Analyse (True = Erfolg)
        score_2 (bool): Prognose aus der Web-Recherche (True = Erfolg)

    Returns:
        Tuple[bool, str, str]: (Erfolg, Zusammenfassung, Finale_Bewertung)
            - Erfolg: True wenn Zusammenfassung erfolgreich erstellt
            - Zusammenfassung: Zusammenfassende Textanalyse
            - Finale_Bewertung: "green" (beide positiv), "red" (beide negativ), "yellow" (gemischt)
    """
    try:
        # Bestimme finale Bewertung basierend auf beiden Prognosen
        final_prediction = "red"
        if score_1 == score_2:
            if score_1:
                final_prediction = "green"  # Beide Analysen positiv
            else:
                final_prediction = "red"    # Beide Analysen negativ
        else:
            final_prediction = "yellow"     # Gemischte Ergebnisse

        # Generiere zusammenfassende Analyse mit Claude
        message = client.messages.create(
            model=model,
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": f"""Du bist ein VC-Analyst. Schreibe eine umfassende Zusammenfassung auf Deutsch basierend auf den folgenden zwei Texten:
                    1. Text (vom Pitch Deck Analyzer): {text_1}
                    2. Text (vom Web-Search-Assistenten): {text_2}

                    Erstelle eine gut strukturierte Analyse auf Deutsch, die Erkenntnisse aus beiden Quellen zusammenführt.
                    """
                }
            ]
        )

        # Extrahiere Text aus der Antwort
        result = message.content[0].text.strip()
        print(f"Summary: {result}")
        return True, result, final_prediction

    except Exception as e:
        print(f"Error: {e}")
        return False, f"Error: {e}", "red"

def generate_email(model: str = model, final_prediction: str = "red", pitch_deck_reasoning: str = "", web_research_reasoning: str = "", summary_text: str = "", startup_name: str = ""):
    """
    Generiert eine personalisierte E-Mail-Antwort an die Gründer basierend auf den Analyse-Ergebnissen.

    Diese Funktion erstellt automatisch eine professionelle E-Mail an die Startup-Gründer.
    Je nach Bewertung wird entweder eine Einladung zu einem Folgegespräch oder eine
    höfliche Absage generiert.

    Args:
        model (str): Name des zu verwendenden Modells
        final_prediction (str): Finale Bewertung - "green", "yellow" oder "red"
        pitch_deck_reasoning (str): Begründung aus der Pitch Deck Analyse
        web_research_reasoning (str): Begründung aus der Web-Recherche
        summary_text (str): Zusammenfassende Gesamtanalyse
        startup_name (str): Name des Startups

    Returns:
        Tuple[bool, str, str]: (Erfolg, Betreff, Text)
            - Erfolg: True wenn E-Mail erfolgreich generiert
            - Betreff: E-Mail-Betreffzeile
            - Text: E-Mail-Haupttext
    """
    try:
        # Bestimme E-Mail-Typ basierend auf finaler Bewertung
        email_type = "invitation" if final_prediction == "green" else "rejection"

        prompt = f"""Du bist ein professioneller VC-Partner, der eine E-Mail auf Deutsch an Startup-Gründer schreibt.

Basierend auf der folgenden Analyse von {startup_name if startup_name else "dem Startup"}:

Executive Summary: {summary_text}

Pitch Deck Analyse: {pitch_deck_reasoning}

Web-Recherche Ergebnisse: {web_research_reasoning}

Schreibe eine {"herzliche Einladungs-E-Mail für ein nächstes Treffen, um Investitionsmöglichkeiten zu besprechen" if email_type == "invitation" else "höfliche Absage-E-Mail"}.

Die E-Mail sollte:
- Professionell aber persönlich sein
- {"Die spezifischen Stärken hervorheben, die uns beeindruckt haben, und nächste Schritte für ein Treffen vorschlagen" if email_type == "invitation" else "Respektvoll und konstruktiv sein und kurz erwähnen, dass wir zu diesem Zeitpunkt nicht fortfahren können"}
- Prägnant sein (maximal 3-4 Absätze)
- {"Mit vorgeschlagenen Treffzeiten oder einer Bitte um Terminvereinbarung enden" if email_type == "invitation" else "Ihnen alles Gute für ihre zukünftigen Unternehmungen wünschen"}
- Mit "Das Investment Team" unterschreiben

Formatiere die Antwort auf Deutsch als:
SUBJECT: [E-Mail-Betreffzeile]
BODY: [E-Mail-Text]
"""

        # Generiere E-Mail mit Claude
        message = client.messages.create(
            model=model,
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Extrahiere Text aus der Antwort
        result = message.content[0].text.strip()

        # Parse Betreff und Haupttext aus der Antwort
        subject = ""
        body = ""

        if "SUBJECT:" in result and "BODY:" in result:
            parts = result.split("BODY:", 1)
            subject = parts[0].replace("SUBJECT:", "").strip()
            body = parts[1].strip()
        else:
            # Fallback falls das Format nicht befolgt wurde
            lines = result.split("\n", 1)
            subject = lines[0].strip()
            body = lines[1].strip() if len(lines) > 1 else result

        print(f"Email Subject: {subject}")
        print(f"Email Body: {body}")

        return True, subject, body

    except Exception as e:
        print(f"Error generating email: {e}")
        return False, "Follow-up", f"Error generating email: {str(e)}"

def do_competitor_analysis(client: anthropic.Anthropic = client, model: str = model, startup_info: str = "", allowed_sources: list = []):
    """
    Führt eine detaillierte Wettbewerber-Analyse für das Startup durch.

    Diese Funktion nutzt Claudes Web-Search Tool, um eine umfassende Wettbewerbslandschaft
    zu erstellen. Sie identifiziert direkte und indirekte Konkurrenten, analysiert deren
    Stärken/Schwächen und bewertet die Positionierung des Startups im Markt.

    Args:
        client (anthropic.Anthropic): Anthropic API Client
        model (str): Name des zu verwendenden Modells
        startup_info (str): Informationen über das Startup (Idee, Markt, Produkt)
        allowed_sources (list): Liste erlaubter Webseiten für die Recherche

    Returns:
        Tuple[bool, str, list]: (Erfolg, Analyse, Quellen)
            - Erfolg: True wenn Analyse erfolgreich, False bei Fehler
            - Analyse: Detaillierte Wettbewerber-Analyse als Text
            - Quellen: Liste der genutzten Webseiten mit URLs und Titeln
    """
    try:
        # Definiere strukturiertes Tool für Wettbewerber-Analyse
        competitor_tool = {
            "name": "competitor_analysis",
            "description": "Provides a structured competitor analysis with identified competitors and strategic assessment",
            "input_schema": {
                "type": "object",
                "properties": {
                    "direct_competitors": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of direct competitors (same product/service, same target market)"
                    },
                    "indirect_competitors": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of indirect competitors (alternative solutions to the same problem)"
                    },
                    "competitive_advantages": {
                        "type": "string",
                        "description": "Key competitive advantages and differentiation factors of the startup"
                    },
                    "competitive_risks": {
                        "type": "string",
                        "description": "Main competitive risks and threats from the market"
                    },
                    "market_positioning": {
                        "type": "string",
                        "description": "Assessment of market positioning and competitive intensity"
                    }
                },
                "required": ["direct_competitors", "indirect_competitors", "competitive_advantages", "competitive_risks", "market_positioning"]
            }
        }

        # Erstelle Prompt für Wettbewerber-Analyse
        prompt = f"""Du bist ein Competitive Intelligence Analyst für Venture Capital.

Basierend auf den folgenden Startup-Informationen führe eine umfassende Wettbewerber-Analyse durch:

{startup_info}

Fokussiere dich auf diese Quellen, falls verfügbar: {allowed_sources}

Deine Analyse sollte:
1. 3-5 direkte Wettbewerber identifizieren (Unternehmen, die ähnliche Produkte/Dienstleistungen für denselben Zielmarkt anbieten)
2. 2-3 indirekte Wettbewerber identifizieren (alternative Lösungen, die Kunden stattdessen nutzen könnten)
3. Die Wettbewerbsvorteile und das einzigartige Wertversprechen des Startups analysieren
4. Wettbewerbsrisiken und Bedrohungen bewerten
5. Marktpositionierung und Wettbewerbsintensität evaluieren

Nutze die Web-Suche, um genaue, aktuelle Informationen über Wettbewerber, deren Finanzierung, Produkte und Marktposition zu finden.
Nach deiner Recherche nutze das competitor_analysis Tool auf Deutsch, um strukturierte Ergebnisse bereitzustellen.
"""

        # API-Anfrage mit Web-Search und Competitor-Tool
        response = client.messages.create(
            model=model,
            max_tokens=8192,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            tools=[
                {
                    "type": "web_search_20250305",
                    "name": "web_search"
                },
                competitor_tool
            ]
        )

        # Extrahiere Analyse und Quellen aus der Antwort
        analysis_text = ""
        sources = []

        for content in response.content:
            if content.type == "tool_use" and content.name == "competitor_analysis":
                result = content.input

                # Formatiere die Analyse als strukturierten Text
                analysis_parts = []

                # Direkte Wettbewerber
                if result.get("direct_competitors"):
                    analysis_parts.append("**Direkte Wettbewerber:**")
                    for comp in result["direct_competitors"]:
                        analysis_parts.append(f"- {comp}")
                    analysis_parts.append("")

                # Indirekte Wettbewerber
                if result.get("indirect_competitors"):
                    analysis_parts.append("**Indirekte Wettbewerber:**")
                    for comp in result["indirect_competitors"]:
                        analysis_parts.append(f"- {comp}")
                    analysis_parts.append("")

                # Wettbewerbsvorteile
                if result.get("competitive_advantages"):
                    analysis_parts.append("**Wettbewerbsvorteile:**")
                    analysis_parts.append(result["competitive_advantages"])
                    analysis_parts.append("")

                # Wettbewerbsrisiken
                if result.get("competitive_risks"):
                    analysis_parts.append("**Wettbewerbsrisiken:**")
                    analysis_parts.append(result["competitive_risks"])
                    analysis_parts.append("")

                # Marktpositionierung
                if result.get("market_positioning"):
                    analysis_parts.append("**Marktpositionierung:**")
                    analysis_parts.append(result["market_positioning"])

                analysis_text = "\n".join(analysis_parts)

            elif content.type == "text":
                # Extrahiere Quellen aus Citations falls vorhanden
                if hasattr(content, 'citations') and content.citations:
                    for citation in content.citations:
                        if hasattr(citation, 'url') and citation.url:
                            source_info = {
                                'url': citation.url,
                                'title': getattr(citation, 'title', citation.url)
                            }
                            sources.append(source_info)

        # Entferne doppelte URLs
        seen_urls = set()
        unique_sources = []
        for source in sources:
            if source['url'] not in seen_urls:
                seen_urls.add(source['url'])
                unique_sources.append(source)

        print(f"Competitor Analysis completed")
        print(f"Analysis: {analysis_text[:200]}...")
        print(f"Sources: {unique_sources}")

        return True, analysis_text, unique_sources

    except Exception as e:
        print(f"Error in competitor analysis: {e}")
        import traceback
        traceback.print_exc()
        return False, f"Error: {str(e)}", []

def check_red_flags(client: anthropic.Anthropic = client, model: str = model, pitch_deck_analysis: str = "", web_research_analysis: str = "", competitor_analysis: str = "", red_flags_list: list = []):
    """
    Überprüft, ob definierte Red Flags im Startup vorliegen.

    Diese Funktion analysiert alle gesammelten Informationen (Pitch Deck, Web-Recherche,
    Wettbewerber-Analyse) und prüft systematisch, ob eine der definierten Red Flags zutrifft.
    Red Flags sind K.O.-Kriterien, die automatisch zu einer negativen Bewertung führen.

    Args:
        client (anthropic.Anthropic): Anthropic API Client
        model (str): Name des zu verwendenden Modells
        pitch_deck_analysis (str): Begründung aus der Pitch Deck Analyse
        web_research_analysis (str): Begründung aus der Web-Recherche
        competitor_analysis (str): Wettbewerber-Analyse
        red_flags_list (list): Liste der zu prüfenden Red Flags

    Returns:
        Tuple[bool, list, str]: (Erfolg, Getroffene_Red_Flags, Begründung)
            - Erfolg: True wenn Prüfung erfolgreich, False bei Fehler
            - Getroffene_Red_Flags: Liste der Red Flags, die zutreffen
            - Begründung: Detaillierte Erklärung für jede getroffene Red Flag
    """
    try:
        # Wenn keine Red Flags definiert sind, überspringe die Prüfung
        if not red_flags_list:
            return True, [], ""

        # Definiere strukturiertes Tool für Red Flag Check
        red_flag_tool = {
            "name": "red_flag_check",
            "description": "Checks if any of the defined red flags apply to the startup based on all available information",
            "input_schema": {
                "type": "object",
                "properties": {
                    "triggered_flags": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "flag": {
                                    "type": "string",
                                    "description": "The red flag that was triggered"
                                },
                                "reasoning": {
                                    "type": "string",
                                    "description": "Detailed explanation why this red flag applies, with specific evidence from the analysis"
                                }
                            },
                            "required": ["flag", "reasoning"]
                        },
                        "description": "List of red flags that apply to this startup"
                    }
                },
                "required": ["triggered_flags"]
            }
        }

        # Erstelle Prompt für Red Flag Check
        red_flags_formatted = "\n".join([f"- {flag}" for flag in red_flags_list])

        prompt = f"""Du bist ein kritischer Due-Diligence-Analyst für Venture Capital.

Basierend auf ALLEN verfügbaren Informationen über das Startup, prüfe, ob EINES der folgenden RED FLAGS zutrifft:

{red_flags_formatted}

Verfügbare Informationen:

PITCH DECK ANALYSE:
{pitch_deck_analysis}

WEB-RECHERCHE:
{web_research_analysis}

WETTBEWERBER-ANALYSE:
{competitor_analysis}

WICHTIGE ANWEISUNGEN:
1. Sei gründlich und kritisch in deiner Analyse
2. Markiere eine Red Flag nur, wenn du konkrete Beweise aus den bereitgestellten Informationen hast
3. Gib für jede zutreffende Red Flag spezifische Beweise aus der Analyse an (auf Deutsch)
4. Wenn eine Red Flag NICHT zutrifft oder es unzureichende Informationen gibt, schließe sie NICHT ein
5. Sei konservativ - markiere nur eindeutige Verstöße, keine Grenzfälle

Nutze das red_flag_check Tool, um deine Ergebnisse auf Deutsch zu melden.
"""

        # API-Anfrage
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            tools=[red_flag_tool],
            tool_choice={"type": "tool", "name": "red_flag_check"}
        )

        # Extrahiere getroffene Red Flags
        triggered_flags = []
        reasoning_text = ""

        for content in response.content:
            if content.type == "tool_use" and content.name == "red_flag_check":
                result = content.input
                triggered_list = result.get("triggered_flags", [])

                if triggered_list:
                    reasoning_parts = ["**Getroffene Red Flags:**\n"]
                    for item in triggered_list:
                        flag = item.get("flag", "")
                        reasoning = item.get("reasoning", "")
                        triggered_flags.append(flag)
                        reasoning_parts.append(f"🚨 **{flag}**")
                        reasoning_parts.append(f"   {reasoning}\n")

                    reasoning_text = "\n".join(reasoning_parts)

        print(f"Red Flag Check completed")
        print(f"Triggered Flags: {triggered_flags}")
        print(f"Reasoning: {reasoning_text[:200]}...")

        return True, triggered_flags, reasoning_text

    except Exception as e:
        print(f"Error in red flag check: {e}")
        import traceback
        traceback.print_exc()
        return False, [], f"Error: {str(e)}"