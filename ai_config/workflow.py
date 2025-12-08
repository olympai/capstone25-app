"""
Workflow-Modul für die orchestrierte Pitch Deck Analyse.

Dieses Modul koordiniert den gesamten Analyse-Workflow:
1. Pitch Deck PDF Analyse
2. Web-Recherche für fehlende Informationen
3. Zusammenfassung und finale Bewertung
"""

from ai_config.functions import get_prediction, do_websearch, summary

def start_workflow(file_name: str = "", allowed_sources: list = []):
    """
    Startet den vollständigen Analyse-Workflow für ein Pitch Deck.

    Diese Funktion orchestriert den gesamten Bewertungsprozess in drei Schritten:
    1. Analysiert das Pitch Deck PDF und identifiziert fehlende Informationen
    2. Führt Web-Recherche durch, um fehlende Informationen zu ergänzen
    3. Erstellt eine finale Zusammenfassung und Gesamtbewertung

    Args:
        file_name (str): Dateiname des Pitch Deck PDFs (im tmp/ Ordner)
        allowed_sources (list): Liste erlaubter Webseiten für die Recherche

    Returns:
        tuple oder dict: Bei Erfolg: (Finale_Bewertung, Zusammenfassung, PDA_Ergebnisse, WS_Ergebnisse)
                        Bei Fehler: {"error": Fehlermeldung}
            - Finale_Bewertung: "green", "yellow" oder "red"
            - Zusammenfassung: Zusammenfassende Textanalyse
            - PDA_Ergebnisse: (Prognose, Begründung) aus Pitch Deck Analyse
            - WS_Ergebnisse: (Prognose, Begründung, Quellen) aus Web-Recherche
    """
    alert = {}

    # Schritt 1: Pitch Deck Analyse (PDA)
    success_1, prediction_1, reasoning_1, missing = get_prediction(pdf_filename=file_name)
    if not success_1:
        alert = {"error": reasoning_1}
        return alert

    # Schritt 2: Web-Recherche für fehlende Informationen
    success_2, prediction_2, reasoning_2, sources = do_websearch(missing=missing, allowed_sources=allowed_sources)
    if not success_2:
        alert = {"error": reasoning_2}
        return alert

    # Schritt 3: Erstelle finale Zusammenfassung und Bewertung
    final_success, final_result, final_prediction = summary(text_1=reasoning_1,
                                                            text_2=reasoning_2,
                                                            score_1=prediction_1,
                                                            score_2=prediction_2
                                                            )
    if not final_success:
        alert = {"error": final_result}
        return alert

    return final_prediction, final_result, (prediction_1, reasoning_1), (prediction_2, reasoning_2, sources)

# Beispiel-Aufruf für Tests
if __name__ == "__main__":
    start_workflow("yoolox.pdf")