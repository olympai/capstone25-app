"""
VC Pitch Deck Analysator - Streamlit Hauptanwendung

Diese Anwendung analysiert Startup Pitch Decks mit KI-Unterstützung:
- PDF-Upload und Analyse mit Claude AI
- Web-Recherche für zusätzliche Informationen
- Ampel-Bewertungssystem (grün/gelb/rot)
- Automatische E-Mail-Generierung für Gründer
- Interaktiver Chat mit den Analyse-Ergebnissen

Technologien:
- Streamlit für die Web-Oberfläche
- Anthropic Claude für KI-Analyse
- PDF-Verarbeitung mit Base64-Encoding
"""

import streamlit as st
import os
from pathlib import Path
from ai_config.functions import get_prediction, do_websearch, summary, generate_email, do_competitor_analysis, check_red_flags
from ai_config.config import client, model, instruction, EVALUATION_CRITERIA, build_instruction_with_weights
from ai_config.pdf_export import generate_executive_summary_pdf
import urllib.parse
from datetime import datetime

# Seiten-Konfiguration
st.set_page_config(
    page_title="VC Pitch Deck Analysator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS für modernes Design mit Animationen und Farbverläufen
# Umfasst: Hintergrundanimation, Glassmorphismus-Effekte, interaktive Hover-States
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

    /* Source Cards Styling */
    .source-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        display: flex;
        align-items: center;
        gap: 15px;
        transition: all 0.3s ease;
        text-decoration: none;
        color: inherit;
    }

    .source-card:hover {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
        border-color: rgba(102, 126, 234, 0.6);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        transform: translateY(-2px);
    }

    .source-icon {
        width: 40px;
        height: 40px;
        border-radius: 8px;
        background: white;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        font-size: 24px;
    }

    .source-content {
        flex: 1;
        min-width: 0;
    }

    .source-title {
        font-weight: 600;
        color: #667eea;
        margin-bottom: 4px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .source-url {
        font-size: 0.85em;
        color: #888;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .linkedin-card {
        background: linear-gradient(135deg, rgba(10, 102, 194, 0.1) 0%, rgba(0, 119, 181, 0.1) 100%);
        border-color: rgba(10, 102, 194, 0.3);
    }

    .linkedin-card:hover {
        background: linear-gradient(135deg, rgba(10, 102, 194, 0.2) 0%, rgba(0, 119, 181, 0.2) 100%);
        border-color: rgba(10, 102, 194, 0.6);
        box-shadow: 0 4px 15px rgba(10, 102, 194, 0.3);
    }

    .linkedin-card .source-title {
        color: #0a66c2;
    }

    .sources-section {
        margin-top: 20px;
        padding-top: 20px;
        border-top: 1px solid rgba(102, 126, 234, 0.2);
    }

    .sources-subtitle {
        font-size: 0.95em;
        font-weight: 600;
        color: #667eea;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialisiere Session State Variablen
# Session State ermöglicht das Speichern von Daten zwischen Seitenaufrufen
if 'page' not in st.session_state:
    st.session_state.page = 'config'  # Aktuelle Seite: 'config' (Konfiguration) oder 'results' (Ergebnisse)
if 'results' not in st.session_state:
    st.session_state.results = None  # Speichert alle Analyse-Ergebnisse
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []  # Speichert Chat-Verlauf
if 'workflow_completed' not in st.session_state:
    st.session_state.workflow_completed = False  # Flag ob Analyse abgeschlossen
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None  # Hochgeladenes PDF
if 'allowed_sources' not in st.session_state:
    st.session_state.allowed_sources = []  # Erlaubte Quellen für Web-Recherche
if 'criteria_weights' not in st.session_state:
    st.session_state.criteria_weights = {key: "mittel" for key in EVALUATION_CRITERIA.keys()}  # Gewichtungen für Standard-Kriterien
if 'additional_criteria' not in st.session_state:
    st.session_state.additional_criteria = []  # Zusätzliche Kriterien mit Gewichtung [{"weight": str, "description": str}]
if 'red_flags' not in st.session_state:
    st.session_state.red_flags = ""  # Red Flags die automatisch zur roten Ampel führen

# Hilfsfunktion zum Rendern von Quellen als Cards
def render_sources(sources: list):
    """
    Rendert Quellen als schöne Cards mit separater Darstellung von LinkedIn-Links.

    Args:
        sources (list): Liste von Quellen (dict mit 'url' und 'title' oder string)
    """
    if not sources:
        return

    # Kategorisiere Quellen
    linkedin_sources = []
    other_sources = []

    for source in sources:
        if isinstance(source, dict):
            url = source.get('url', '')
            title = source.get('title', url)

            if 'linkedin.com' in url.lower():
                linkedin_sources.append({'url': url, 'title': title})
            else:
                other_sources.append({'url': url, 'title': title})
        elif isinstance(source, str):
            if 'linkedin.com' in source.lower():
                linkedin_sources.append({'url': source, 'title': source})
            else:
                other_sources.append({'url': source, 'title': source})

    # Rendere LinkedIn-Quellen (Founders/Team)
    if linkedin_sources:
        st.markdown('<div class="sources-section">', unsafe_allow_html=True)
        st.markdown('<div class="sources-subtitle">👥 Team & Founder Profile</div>', unsafe_allow_html=True)

        for source in linkedin_sources:
            url = source['url']
            title = source['title']

            # Extrahiere Domain für Favicon
            domain = url.split('/')[2] if len(url.split('/')) > 2 else url

            card_html = f"""
            <a href="{url}" target="_blank" class="source-card linkedin-card">
                <div class="source-icon">
                    <img src="https://www.google.com/s2/favicons?domain={domain}&sz=32"
                         onerror="this.style.display='none'; this.nextElementSibling.style.display='block';"
                         style="width: 32px; height: 32px;"/>
                    <span style="display: none;">💼</span>
                </div>
                <div class="source-content">
                    <div class="source-title">{title}</div>
                    <div class="source-url">{domain}</div>
                </div>
            </a>
            """
            st.markdown(card_html, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Rendere andere Quellen
    if other_sources:
        st.markdown('<div class="sources-section">', unsafe_allow_html=True)
        st.markdown('<div class="sources-subtitle">🔗 Weitere Quellen</div>', unsafe_allow_html=True)

        for source in other_sources:
            url = source['url']
            title = source['title']

            # Extrahiere Domain für Favicon
            domain = url.split('/')[2] if len(url.split('/')) > 2 else url

            # Icon basierend auf Domain
            icon = "📰"
            if 'crunchbase' in domain.lower():
                icon = "💼"
            elif 'techcrunch' in domain.lower():
                icon = "📱"
            elif 'pitchbook' in domain.lower():
                icon = "📊"
            elif 'github' in domain.lower():
                icon = "💻"

            card_html = f"""
            <a href="{url}" target="_blank" class="source-card">
                <div class="source-icon">
                    <img src="https://www.google.com/s2/favicons?domain={domain}&sz=32"
                         onerror="this.style.display='none'; this.nextElementSibling.style.display='block';"
                         style="width: 32px; height: 32px;"/>
                    <span style="display: none;">{icon}</span>
                </div>
                <div class="source-content">
                    <div class="source-title">{title}</div>
                    <div class="source-url">{domain}</div>
                </div>
            </a>
            """
            st.markdown(card_html, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# Haupt-Header der Anwendung
st.markdown('<div class="main-header">🚀 F Technologies Pitch Deck Analysator</div>', unsafe_allow_html=True)

# ===== KONFIGURATIONSSEITE =====
# Hier kann der Nutzer ein PDF hochladen und Einstellungen vornehmen
if st.session_state.page == 'config':
    st.markdown("---")

    # Erstelle ein zentriertes Layout mit 3 Spalten
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Datei-Upload Bereich
        st.markdown("### 📄 Pitch Deck hochladen")
        uploaded_file = st.file_uploader(
            "Wähle eine PDF-Datei",
            type=['pdf'],
            help="Lade ein Startup Pitch Deck im PDF-Format hoch",
            key="file_uploader"
        )

        if uploaded_file:
            st.session_state.uploaded_file = uploaded_file
            st.success(f"✅ Datei hochgeladen: {uploaded_file.name}")

        st.markdown("---")

        # Web search sources configuration
        st.markdown("### 🔍 Web-Suchquellen")
        default_sources = []
        sources_text = st.text_area(
            "Erlaubte Quellen (eine pro Zeile)",
            value="\n".join(st.session_state.allowed_sources),
            height=120,
            help="Gib Webseiten an, auf die sich die Web-Recherche konzentrieren soll"
        )
        st.session_state.allowed_sources = [source.strip() for source in sources_text.split('\n') if source.strip()]

        st.markdown("---")

        # Kriterien-Gewichtung
        st.markdown("### ⚖️ Kriterien-Gewichtung")
        st.markdown("Passe die Wichtigkeit der einzelnen Bewertungskriterien an:")
        st.info("💡 **Niedrig** = Geringere Gewichtung | **Mittel** = Standard-Gewichtung | **Hoch** = Höchste Priorität (kritisch für Investment-Entscheidung)")

        # Standard-Kriterien mit Gewichtung
        weight_options = ["niedrig", "mittel", "hoch"]
        german_labels = {
            "COMPANY": "Unternehmen",
            "COMPETITION": "Wettbewerb",
            "FINANCIALS": "Finanzen",
            "MARKET": "Markt",
            "PRODUCT": "Produkt",
            "TEAM": "Team"
        }

        for criterion_key in EVALUATION_CRITERIA.keys():
            col_label, col_weight = st.columns([3, 1])
            with col_label:
                st.markdown(f"**{german_labels.get(criterion_key, criterion_key)}**")
            with col_weight:
                current_weight = st.session_state.criteria_weights.get(criterion_key, "mittel")
                weight_index = weight_options.index(current_weight) if current_weight in weight_options else 1
                new_weight = st.selectbox(
                    f"Gewichtung {criterion_key}",
                    weight_options,
                    index=weight_index,
                    key=f"weight_{criterion_key}",
                    label_visibility="collapsed"
                )
                st.session_state.criteria_weights[criterion_key] = new_weight

        st.markdown("---")

        # Zusätzliche eigene Kriterien
        st.markdown("### 📋 Eigene Kriterien hinzufügen")
        st.markdown("Füge spezifische Bewertungskriterien für deine Investment-These hinzu:")

        # Button zum Hinzufügen eines neuen Kriteriums
        if st.button("➕ Neues Kriterium hinzufügen", key="add_criterion"):
            st.session_state.additional_criteria.append({"weight": "mittel", "description": ""})
            st.rerun()

        # Zeige alle zusätzlichen Kriterien
        criteria_to_remove = []
        for idx, criterion in enumerate(st.session_state.additional_criteria):
            col_weight, col_desc, col_remove = st.columns([1, 4, 1])

            with col_weight:
                weight = st.selectbox(
                    f"Gewichtung {idx}",
                    weight_options,
                    index=weight_options.index(criterion.get("weight", "mittel")),
                    key=f"additional_weight_{idx}",
                    label_visibility="collapsed"
                )
                criterion["weight"] = weight

            with col_desc:
                description = st.text_input(
                    f"Beschreibung {idx}",
                    value=criterion.get("description", ""),
                    key=f"additional_desc_{idx}",
                    placeholder="z.B. 'Nachhaltigkeit der Lösung', 'Social Impact'",
                    label_visibility="collapsed"
                )
                criterion["description"] = description

            with col_remove:
                if st.button("🗑️", key=f"remove_{idx}"):
                    criteria_to_remove.append(idx)

        # Entferne markierte Kriterien
        for idx in reversed(criteria_to_remove):
            st.session_state.additional_criteria.pop(idx)
            st.rerun()

        st.markdown("---")

        # Red Flags Definition
        st.markdown("### 🚨 Red Flags")
        red_flags_text = st.text_area(
            "K.O.-Kriterien (eine pro Zeile)",
            value=st.session_state.red_flags,
            height=120,
            help="Definiere Red Flags, die automatisch zu einer roten Ampel führen (z.B. 'Keine zahlenden Kunden', 'Founder hat bereits gekündigt', 'Regulatorische Probleme')"
        )
        st.session_state.red_flags = red_flags_text

        st.markdown("---")

        # Run analysis button
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.session_state.uploaded_file:
                if st.button("🚀 Analyse starten", type="primary", use_container_width=True):
                    st.session_state.page = 'results'
                    st.session_state.workflow_completed = False
                    st.session_state.results = None
                    st.session_state.chat_history = []
                    st.session_state.generated_email = None
                    st.rerun()
            else:
                st.button("🚀 Analyse starten", type="primary", use_container_width=True, disabled=True)
                st.info("Bitte lade eine PDF-Datei hoch, um fortzufahren")

        st.markdown('</div>', unsafe_allow_html=True)

# ===== ERGEBNISSEITE =====
# Zeigt die Analyse-Ergebnisse, E-Mail-Generierung und Chat-Interface
elif st.session_state.page == 'results':
    # Zurück-Button zur Konfigurationsseite
    if st.button("← Zurück zur Konfiguration"):
        st.session_state.page = 'config'
        st.rerun()

    st.markdown("---")

    # Führe Analyse-Workflow aus, falls noch nicht abgeschlossen
    if not st.session_state.workflow_completed:
        # Speichere hochgeladenes PDF temporär im tmp/ Ordner
        tmp_dir = Path("tmp")
        tmp_dir.mkdir(exist_ok=True)
        file_path = tmp_dir / st.session_state.uploaded_file.name

        with open(file_path, "wb") as f:
            f.write(st.session_state.uploaded_file.getbuffer())

        # Container für Fortschrittsanzeige
        progress_container = st.container()

        with progress_container:
            st.markdown('<div class="sub-header">Analyse-Fortschritt</div>', unsafe_allow_html=True)

            # Schritt 1: Pitch Deck Analyse
            with st.status("📊 Pitch Deck wird analysiert...", expanded=True) as status:
                st.write("PDF wird gelesen und ausgewertet...")

                # Erstelle Instruktion mit gewichteten Kriterien
                combined_instruction = build_instruction_with_weights(
                    criteria_weights=st.session_state.criteria_weights,
                    additional_criteria=st.session_state.additional_criteria
                )

                success, prediction, reasoning, missing = get_prediction(
                    client=client,
                    model=model,
                    instruction=combined_instruction,
                    pdf_filename=st.session_state.uploaded_file.name
                )

                if success:
                    st.write("✅ Pitch Deck Analyse abgeschlossen")
                    status.update(label="✅ Pitch Deck Analyse abgeschlossen", state="complete")
                else:
                    st.error("❌ Fehler bei der Pitch Deck Analyse")
                    status.update(label="❌ Fehler bei der Pitch Deck Analyse", state="error")
                    st.stop()

            # Schritt 2: Wettbewerber-Screening
            with st.status("🔍 Wettbewerber-Screening wird durchgeführt...", expanded=True) as status:
                st.write("Identifiziere und analysiere Wettbewerber...")

                competitor_success, competitor_analysis, competitor_sources = do_competitor_analysis(
                    client=client,
                    model=model,
                    startup_info=missing,
                    allowed_sources=st.session_state.allowed_sources
                )

                if competitor_success:
                    st.write("✅ Wettbewerber-Screening abgeschlossen")
                    status.update(label="✅ Wettbewerber-Screening abgeschlossen", state="complete")
                else:
                    st.error("❌ Fehler beim Wettbewerber-Screening")
                    status.update(label="❌ Fehler beim Wettbewerber-Screening", state="error")
                    st.stop()

            # Schritt 3: Web Research & Markt-Trends
            with st.status("🌐 Web-Recherche & Markt-Trends-Analyse...", expanded=True) as status:
                st.write(f"Suche nach zusätzlichen Informationen...")
                st.write(f"📊 Analysiere aktuelle Markt-Trends und Branchenentwicklungen...")

                web_success, web_prediction, web_reasoning, web_sources = do_websearch(
                    client=client,
                    model=model,
                    missing=missing,
                    allowed_sources=st.session_state.allowed_sources
                )

                if web_success:
                    st.write("✅ Web-Recherche und Markt-Trends-Analyse abgeschlossen")
                    status.update(label="✅ Web-Recherche und Markt-Trends abgeschlossen", state="complete")
                else:
                    st.error("❌ Fehler bei der Web-Recherche")
                    status.update(label="❌ Fehler bei der Web-Recherche", state="error")
                    st.stop()

            # Schritt 4: Red Flag Check
            triggered_red_flags = []
            red_flag_reasoning = ""

            if st.session_state.red_flags.strip():
                with st.status("🚨 Red Flags werden überprüft...", expanded=True) as status:
                    st.write("Prüfe K.O.-Kriterien...")

                    # Parse Red Flags Liste
                    red_flags_list = [flag.strip() for flag in st.session_state.red_flags.split('\n') if flag.strip()]

                    red_flag_success, triggered_red_flags, red_flag_reasoning = check_red_flags(
                        client=client,
                        model=model,
                        pitch_deck_analysis=reasoning,
                        web_research_analysis=web_reasoning,
                        competitor_analysis=competitor_analysis,
                        red_flags_list=red_flags_list
                    )

                    if red_flag_success:
                        if triggered_red_flags:
                            st.write(f"⚠️ {len(triggered_red_flags)} Red Flag(s) getroffen!")
                            status.update(label=f"⚠️ {len(triggered_red_flags)} Red Flag(s) getroffen!", state="complete")
                        else:
                            st.write("✅ Keine Red Flags getroffen")
                            status.update(label="✅ Keine Red Flags getroffen", state="complete")
                    else:
                        st.error("❌ Fehler beim Red Flag Check")
                        status.update(label="❌ Fehler beim Red Flag Check", state="error")
                        st.stop()

            # Schritt 5: Zusammenfassung erstellen
            with st.status("📝 Zusammenfassung wird erstellt...", expanded=True) as status:
                st.write("Ergebnisse werden zusammengeführt...")

                summary_success, summary_text, final_prediction = summary(
                    model=model,
                    text_1=reasoning,
                    text_2=web_reasoning,
                    score_1=prediction,
                    score_2=web_prediction
                )

                if summary_success:
                    st.write("✅ Zusammenfassung erstellt")
                    status.update(label="✅ Zusammenfassung erstellt", state="complete")
                else:
                    st.error("❌ Fehler beim Erstellen der Zusammenfassung")
                    status.update(label="❌ Fehler beim Erstellen der Zusammenfassung", state="error")
                    st.stop()

            # Ampel-Logik: Wenn Red Flags getroffen wurden, ist die Ampel immer rot
            if triggered_red_flags:
                final_prediction = "red"
                st.warning(f"⚠️ Finale Bewertung auf ROT gesetzt wegen {len(triggered_red_flags)} getroffener Red Flag(s)!")

            # Speichere Ergebnisse im Session State
            st.session_state.results = {
                'pitch_deck': {
                    'prediction': prediction,
                    'reasoning': reasoning
                },
                'competitor_analysis': {
                    'analysis': competitor_analysis,
                    'sources': competitor_sources
                },
                'web_research': {
                    'prediction': web_prediction,
                    'reasoning': web_reasoning,
                    'sources': web_sources
                },
                'red_flags': {
                    'triggered': triggered_red_flags,
                    'reasoning': red_flag_reasoning
                },
                'summary': summary_text,
                'final_prediction': final_prediction,
                'filename': st.session_state.uploaded_file.name
            }
            st.session_state.workflow_completed = True

            st.success("🎉 Analyse abgeschlossen!")
            st.rerun()

    # Display results if available
    if st.session_state.results:
        results = st.session_state.results

        st.markdown('<div class="sub-header">Analyse-Ergebnisse</div>', unsafe_allow_html=True)

        # Traffic light indicator
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            color_class = results['final_prediction']
            color_emoji = {
                'green': '🟢',
                'yellow': '🟡',
                'red': '🔴'
            }
            st.markdown(f"### {color_emoji[color_class]} Gesamtbewertung")
            st.markdown(f'<div class="traffic-light {color_class}"></div>', unsafe_allow_html=True)

            if color_class == 'green':
                st.success("Beide Analysen prognostizieren Erfolg")
            elif color_class == 'red':
                # Prüfe ob Red Flags der Grund für die rote Ampel sind
                if results.get('red_flags') and results['red_flags'].get('triggered'):
                    st.error(f"🚨 K.O.-Kriterium getroffen: {len(results['red_flags']['triggered'])} Red Flag(s)")
                else:
                    st.error("Beide Analysen prognostizieren Misserfolg")
            else:
                st.warning("Gemischte Prognosen - weitere Untersuchung empfohlen")

        # Red Flag Warnung (falls vorhanden)
        if results.get('red_flags') and results['red_flags'].get('triggered'):
            st.markdown("---")
            st.markdown("### 🚨 K.O.-Kriterien Warnung")

            # Erstelle eine auffällige Warnung
            warning_text = f"""
            <div style="
                background: linear-gradient(135deg, rgba(220, 53, 69, 0.2) 0%, rgba(255, 0, 0, 0.1) 100%);
                border: 2px solid rgba(220, 53, 69, 0.6);
                border-radius: 12px;
                padding: 20px;
                margin: 20px 0;
                box-shadow: 0 0 30px rgba(220, 53, 69, 0.4);
            ">
                <h4 style="color: #ff4444; margin-top: 0;">⚠️ {len(results['red_flags']['triggered'])} Red Flag(s) identifiziert</h4>
                <p style="color: #ffffff;">Die folgenden K.O.-Kriterien wurden getroffen. Die Bewertung wurde automatisch auf ROT gesetzt.</p>
            </div>
            """
            st.markdown(warning_text, unsafe_allow_html=True)

            # Zeige die Red Flags in einer Card
            st.markdown(f'<div class="result-card">{results["red_flags"]["reasoning"]}</div>', unsafe_allow_html=True)

        st.markdown("---")

        # Summary
        st.markdown("### 📝 Zusammenfassung")
        st.markdown(f'<div class="result-card">{results["summary"]}</div>', unsafe_allow_html=True)

        # PDF Export Button
        st.markdown("---")
        st.markdown("### 📄 Export")

        col_pdf1, col_pdf2, col_pdf3 = st.columns([1, 2, 1])
        with col_pdf2:
            st.info("💡 Exportiere eine professionelle PDF-Zusammenfassung mit allen wichtigen Ergebnissen")

            if st.button("📄 Executive Summary als PDF exportieren", type="secondary", use_container_width=True):
                try:
                    # Generiere PDF
                    with st.spinner("PDF wird generiert..."):
                        pdf_bytes = generate_executive_summary_pdf(results)

                    # Erstelle Dateinamen
                    startup_name = results.get('filename', 'startup').replace('.pdf', '').replace(' ', '_')
                    date_str = datetime.now().strftime("%Y%m%d")
                    pdf_filename = f"Executive_Summary_{startup_name}_{date_str}.pdf"

                    # Download Button
                    st.download_button(
                        label="⬇️ PDF herunterladen",
                        data=pdf_bytes,
                        file_name=pdf_filename,
                        mime="application/pdf",
                        use_container_width=True
                    )
                    st.success("✅ PDF erfolgreich generiert!")

                except Exception as e:
                    st.error(f"❌ Fehler beim Generieren der PDF: {str(e)}")
                    st.exception(e)

        st.markdown("---")

        # Detailed reasoning in accordions
        st.markdown("### 🔍 Detaillierte Analyse")

        with st.expander("📄 Pitch Deck Analyse", expanded=False):
            prediction_emoji = "✅" if results['pitch_deck']['prediction'] else "❌"
            st.markdown(f"**Prognose:** {prediction_emoji} {'Erfolg' if results['pitch_deck']['prediction'] else 'Misserfolg'}")
            st.markdown("**Begründung:**")
            st.markdown(results['pitch_deck']['reasoning'])

        # Red Flags Accordion (falls vorhanden)
        if results.get('red_flags') and results['red_flags'].get('triggered'):
            with st.expander("🚨 K.O.-Kriterien Check", expanded=True):
                st.markdown(f"**Status:** ❌ {len(results['red_flags']['triggered'])} Red Flag(s) getroffen")
                st.markdown("**Details:**")
                st.markdown(results['red_flags']['reasoning'])

        with st.expander("🔍 Wettbewerber-Screening", expanded=False):
            st.markdown(results['competitor_analysis']['analysis'])

            if results['competitor_analysis']['sources']:
                render_sources(results['competitor_analysis']['sources'])

        with st.expander("🌐 Web-Recherche & Markt-Trends", expanded=False):
            prediction_emoji = "✅" if results['web_research']['prediction'] else "❌"
            st.markdown(f"**Prognose:** {prediction_emoji} {'Erfolg' if results['web_research']['prediction'] else 'Misserfolg'}")
            st.markdown("**Analyse (inkl. aktueller Markt-Trends):**")
            st.markdown(results['web_research']['reasoning'])

            if results['web_research']['sources']:
                render_sources(results['web_research']['sources'])

        # Email Generation Section
        st.markdown("---")
        st.markdown('<div class="sub-header">E-Mail-Antwort generieren</div>', unsafe_allow_html=True)

        # Initialize email state if not exists
        if 'generated_email' not in st.session_state:
            st.session_state.generated_email = None

        col_email1, col_email2, col_email3 = st.columns([1, 2, 1])
        with col_email2:
            # Determine email type
            email_type = "invitation" if results['final_prediction'] == 'green' else "rejection"
            email_icon = "✅" if email_type == "invitation" else "📧"
            email_type_de = "Einladung" if email_type == "invitation" else "Absage"

            st.info(f"{email_icon} E-Mail-Typ: **{email_type_de}** - Basierend auf {'positiven' if email_type == 'invitation' else 'gemischten oder negativen'} Analyse-Ergebnissen")

            if st.button("📝 E-Mail generieren", type="primary", use_container_width=True):
                with st.spinner("Personalisierte E-Mail wird generiert..."):
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
                        st.success("✅ E-Mail erfolgreich generiert!")
                        st.rerun()

        # Display generated email if available
        if st.session_state.generated_email:
            st.markdown("### 📧 Generierte E-Mail")
            email_data = st.session_state.generated_email

            with st.container():
                st.markdown(f"**Betreff:** {email_data['subject']}")
                st.markdown("**Nachricht:**")
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
                            📬 In E-Mail-Programm öffnen
                        </button>
                    </a>
                """, unsafe_allow_html=True)

                st.caption("Klicken, um diese E-Mail in deinem Standard-E-Mail-Programm zu öffnen")

        # ===== CHAT-INTERFACE =====
        # Ermöglicht interaktive Fragen zu den Analyse-Ergebnissen mit Zugriff auf das PDF und Web-Suche
        st.markdown("---")
        st.markdown('<div class="sub-header">💬 Chat mit deinen Daten</div>', unsafe_allow_html=True)
        st.markdown("Stelle Fragen zu den Analyse-Ergebnissen")

        # Erstelle Kontext-Informationen aus den Analyse-Ergebnissen für den Chat
        red_flags_context = ""
        if results.get('red_flags') and results['red_flags'].get('triggered'):
            red_flags_context = f"""
        Red Flags: {len(results['red_flags']['triggered'])} K.O.-Kriterien getroffen
        Red Flag Details: {results['red_flags']['reasoning']}
        WICHTIG: Die Bewertung wurde wegen Red Flags auf ROT gesetzt!
        """

        context = f"""
        Pitch Deck Analyse-Ergebnisse für {results['filename']}:

        Gesamtbewertung: {results['final_prediction']}
        {red_flags_context}
        Pitch Deck Prognose: {'Erfolg' if results['pitch_deck']['prediction'] else 'Misserfolg'}
        Pitch Deck Begründung: {results['pitch_deck']['reasoning']}

        Web-Recherche Prognose: {'Erfolg' if results['web_research']['prediction'] else 'Misserfolg'}
        Web-Recherche Begründung: {results['web_research']['reasoning']}

        Zusammenfassung: {results['summary']}
        """

        # Zeige bisherigen Chat-Verlauf
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat-Eingabefeld
        if prompt := st.chat_input("Stelle eine Frage zur Analyse..."):
            # Füge Nutzer-Nachricht zum Chat-Verlauf hinzu
            st.session_state.chat_history.append({"role": "user", "content": prompt})

            # Zeige Nutzer-Nachricht sofort an
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generiere Antwort mit Claude
            with st.chat_message("assistant"):
                with st.spinner("Denke nach..."):
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
                        system=f"Du bist ein hilfreicher VC-Analyst-Assistent. Du hast Zugriff auf das ursprüngliche Pitch Deck PDF und die Analyse-Ergebnisse. Beantworte Fragen basierend auf dem PDF und dem folgenden Analyse-Kontext:\n\n{context}\n\nDu hast auch Zugriff auf eine Web-Suche, um bei Bedarf zusätzliche Informationen zu finden. Antworte immer auf Deutsch.",
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
                        assistant_message += "\n\n**Quellen:**\n"
                        for i, source in enumerate(chat_sources, 1):
                            assistant_message += f"{i}. [{source['title']}]({source['url']})\n"

                # Display assistant message
                st.markdown(assistant_message)

                # Add assistant message to chat history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": assistant_message
                })
