# alle wichtigen Funktionsbestandteile unserer App

import os
from typing import List, Dict, Optional
from anthropic import Anthropic


def chat_with_data(
    user_message: str,
    data_context: str = "",
    conversation_history: Optional[List[Dict[str, str]]] = None,
    model: str = "claude-haiku-4-5-20250929",
    max_tokens: int = 4096,
    temperature: float = 1.0
) -> Dict[str, any]:
    """
    Chat mit Anthropic Haiku 4.5 unter Einbeziehung von Datenkontext.

    Args:
        user_message: Die Nachricht/Frage des Benutzers
        data_context: Zusätzlicher Datenkontext (z.B. CSV-Daten, JSON, Text)
        conversation_history: Optional - Liste von vorherigen Nachrichten im Format
                            [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
        model: Das zu verwendende Anthropic-Modell (Standard: claude-haiku-4-5-20250929)
        max_tokens: Maximale Anzahl der Tokens in der Antwort
        temperature: Kreativität der Antwort (0.0 - 1.0)

    Returns:
        Dict mit 'response' (Text der Antwort) und 'usage' (Token-Verwendung)
    """
    # API-Key aus Umgebungsvariable laden
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY Umgebungsvariable nicht gesetzt")

    # Anthropic Client initialisieren
    client = Anthropic(api_key=api_key)

    # Nachrichten-Array erstellen
    messages = []

    # Conversation History hinzufügen falls vorhanden
    if conversation_history:
        messages.extend(conversation_history)

    # Aktuelle Nachricht mit Datenkontext erstellen
    if data_context:
        full_message = f"""Hier sind relevante Daten für deine Antwort:

<data>
{data_context}
</data>

Benutzerfrage: {user_message}

Bitte beantworte die Frage basierend auf den bereitgestellten Daten."""
    else:
        full_message = user_message

    messages.append({
        "role": "user",
        "content": full_message
    })

    # API-Call an Anthropic
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=messages
    )

    # Antwort extrahieren
    response_text = response.content[0].text

    return {
        "response": response_text,
        "usage": {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "total_tokens": response.usage.input_tokens + response.usage.output_tokens
        },
        "model": response.model,
        "stop_reason": response.stop_reason
    }


def chat_with_csv_data(
    user_message: str,
    csv_file_path: str,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    sample_rows: int = 100
) -> Dict[str, any]:
    """
    Chat mit CSV-Daten - liest eine CSV-Datei und nutzt sie als Kontext.

    Args:
        user_message: Die Nachricht/Frage des Benutzers
        csv_file_path: Pfad zur CSV-Datei
        conversation_history: Optional - Liste von vorherigen Nachrichten
        sample_rows: Anzahl der Zeilen, die als Kontext verwendet werden sollen

    Returns:
        Dict mit 'response' (Text der Antwort) und 'usage' (Token-Verwendung)
    """
    import pandas as pd

    # CSV-Datei laden
    df = pd.read_csv(csv_file_path)

    # Datenkontext erstellen (mit Sample um Token-Limit nicht zu überschreiten)
    data_summary = f"""CSV-Datei: {csv_file_path}
Anzahl Zeilen: {len(df)}
Anzahl Spalten: {len(df.columns)}
Spalten: {', '.join(df.columns)}

Erste {min(sample_rows, len(df))} Zeilen:
{df.head(sample_rows).to_string()}

Datentypen:
{df.dtypes.to_string()}

Statistische Zusammenfassung:
{df.describe().to_string()}
"""

    # Chat-Funktion mit Datenkontext aufrufen
    return chat_with_data(
        user_message=user_message,
        data_context=data_summary,
        conversation_history=conversation_history
    )


def chat_with_json_data(
    user_message: str,
    json_data: Dict,
    conversation_history: Optional[List[Dict[str, str]]] = None
) -> Dict[str, any]:
    """
    Chat mit JSON-Daten - nutzt JSON-Objekte als Kontext.

    Args:
        user_message: Die Nachricht/Frage des Benutzers
        json_data: JSON-Daten als Dictionary
        conversation_history: Optional - Liste von vorherigen Nachrichten

    Returns:
        Dict mit 'response' (Text der Antwort) und 'usage' (Token-Verwendung)
    """
    import json

    # JSON zu formatiertem String konvertieren
    data_context = json.dumps(json_data, indent=2, ensure_ascii=False)

    # Chat-Funktion mit Datenkontext aufrufen
    return chat_with_data(
        user_message=user_message,
        data_context=data_context,
        conversation_history=conversation_history
    )


# Beispiel-Verwendung:
"""
# Einfacher Chat mit Datenkontext
result = chat_with_data(
    user_message="Was sind die wichtigsten Trends in diesen Daten?",
    data_context="Verkaufszahlen Q1 2024: Produkt A: 1500, Produkt B: 2300, Produkt C: 890"
)
print(result['response'])

# Chat mit CSV-Datei
result = chat_with_csv_data(
    user_message="Analysiere diese Verkaufsdaten und gib mir die Top 3 Insights",
    csv_file_path="sales_data.csv"
)
print(result['response'])

# Chat mit JSON-Daten
result = chat_with_json_data(
    user_message="Fasse diese Kundendaten zusammen",
    json_data={"customers": [{"name": "Max", "orders": 5}, {"name": "Anna", "orders": 3}]}
)
print(result['response'])

# Multi-Turn Conversation
history = []
result1 = chat_with_data("Hallo, kannst du mir helfen?", data_context="Produktdaten: ...")
history.append({"role": "user", "content": "Hallo, kannst du mir helfen?"})
history.append({"role": "assistant", "content": result1['response']})

result2 = chat_with_data("Was war meine erste Frage?", conversation_history=history)
"""
