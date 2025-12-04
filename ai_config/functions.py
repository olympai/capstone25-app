import anthropic
import base64
from typing import Tuple

from ai_config.config import client, model

def get_prediction(client: anthropic.Anthropic = client, model: str = model, instruction: str = "", pdf_filename: str = "") -> Tuple[bool, str]:
    """
    Get survival prediction and reasoning for a pitch deck PDF using Claude with base64 encoding.

    Args:
        client: Anthropic client
        model: Model name to use (e.g., "claude-sonnet-4-5")
        instruction: System instruction for evaluation
        pdf_path: Path to the PDF file
        pdf_filename: Name of the PDF file for error reporting

    Returns:
        Tuple[bool, str]: (prediction, reasoning) - True if startup survives, False if it fails, and reasoning text
    """
    try:
        # Load and encode the PDF as base64
        with open("tmp/" + pdf_filename, 'rb') as f:
            pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

        # Define the tool for structured output
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

        # Create message with base64-encoded PDF and tool
        message = client.messages.create(
            model=model,
            max_tokens=2048,
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
                            "text": "Please evaluate this pitch deck and provide your prediction and reasoning using the pitch_deck_evaluation tool."
                        }
                    ]
                }
            ],
            tools=[evaluation_tool],
            tool_choice={"type": "tool", "name": "pitch_deck_evaluation"}
        )

        # Extract structured output from tool use
        for content in message.content:
            if content.type == "tool_use" and content.name == "pitch_deck_evaluation":
                result = content.input
                prediction = result.get("prediction", False)
                reasoning = result.get("reasoning", "No reasoning provided")
                pitch = result.get("pitch", "")
                missing = pitch + result.get("missing", "")
                missing += " Research information regarding market and founders"

                print(f"Prediction: {prediction}")
                print(f"Reasoning: {reasoning}")
                print(f"Missing: {missing}")

                return True, prediction, reasoning, missing

        # Fallback if no tool use found
        return False, False, "No structured output received", ""

    except Exception as e:
        print(f"Error in prediction for {pdf_filename}: {e}")
        return False, False, f"Error: {str(e)}", ""
    
def do_websearch(client: anthropic.Anthropic = client, model: str = model, missing: str = "", allowed_sources: list = []):
    try:
        # Simple evaluation tool
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
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": f"""You are a VC-research expert. Find out additional information based on these instructions: {missing}.
                    Focus on these sources: {allowed_sources}

                    After your research, use the evaluation tool to provide your prediction and reasoning.
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

        # Extract prediction, reasoning, and sources
        prediction = False
        reasoning = "No reasoning provided"
        sources = []

        for content in response.content:
            if content.type == "tool_use" and content.name == "evaluation":
                result = content.input
                prediction = result.get("prediction", False)
                reasoning = result.get("reasoning", "No reasoning provided")
            elif content.type == "text":
                # Extract sources from citations if available
                if hasattr(content, 'citations') and content.citations:
                    for citation in content.citations:
                        if hasattr(citation, 'url') and citation.url:
                            source_info = {
                                'url': citation.url,
                                'title': getattr(citation, 'title', citation.url)
                            }
                            sources.append(source_info)
            elif hasattr(content, 'type') and 'web_search' in str(content.type):
                # Extract from web_search_tool_result
                if hasattr(content, 'content') and isinstance(content.content, list):
                    for item in content.content:
                        if hasattr(item, 'url'):
                            source_info = {
                                'url': item.url,
                                'title': getattr(item, 'title', item.url)
                            }
                            sources.append(source_info)

        # Remove duplicate URLs
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
    
# summarize results
def summary(model: str = model, text_1: str = "", text_2: str = "", score_1: bool = False, score_2: bool = False):
    try:
        # rating
        final_prediction = "red"
        if score_1 == score_2:
            if score_1:
                final_prediction = "green"
            else:
                final_prediction = "red"
        else:
            final_prediction = "yellow"

        # summary
        message = client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"""You are a VC-analyst. Write a comprehensive summary based on the following two texts:
                    1. Text (from a pitchdeck analyzer): {text_1}
                    2. Text (from Web Search assistant): {text_2}

                    Provide a well-structured analysis that synthesizes insights from both sources.
                    """
                }
            ]
        )

        # Extract text from response
        result = message.content[0].text.strip()
        print(f"Summary: {result}")
        return True, result, final_prediction

    except Exception as e:
        print(f"Error: {e}")
        return False, f"Error: {e}", "red"

def generate_email(model: str = model, final_prediction: str = "red", pitch_deck_reasoning: str = "", web_research_reasoning: str = "", summary_text: str = "", startup_name: str = ""):
    """
    Generate personalized email response to founders based on analysis results.

    Args:
        model: Model name to use
        final_prediction: "green", "yellow", or "red"
        pitch_deck_reasoning: Reasoning from pitch deck analysis
        web_research_reasoning: Reasoning from web research
        summary_text: Executive summary
        startup_name: Name of the startup

    Returns:
        Tuple[bool, str, str]: (success, subject, body) - Email subject and body
    """
    try:
        # Determine email type
        email_type = "invitation" if final_prediction == "green" else "rejection"

        prompt = f"""You are a professional VC partner writing an email to startup founders.

Based on the following analysis of {startup_name if startup_name else "the startup"}:

Executive Summary: {summary_text}

Pitch Deck Analysis: {pitch_deck_reasoning}

Web Research Findings: {web_research_reasoning}

Write a {"warm invitation email for a next meeting to discuss investment opportunities" if email_type == "invitation" else "polite rejection email"}.

The email should:
- Be professional but personable
- {"Highlight the specific strengths that impressed us and propose next steps for a meeting" if email_type == "invitation" else "Be respectful and constructive, briefly mentioning that we're unable to proceed at this time"}
- Be concise (3-4 paragraphs maximum)
- {"End with proposed meeting times or a request to schedule a call" if email_type == "invitation" else "Wish them well in their future endeavors"}
- Sign off as "The Investment Team"

Format the response as:
SUBJECT: [email subject line]
BODY: [email body]
"""

        message = client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Extract text from response
        result = message.content[0].text.strip()

        # Parse subject and body
        subject = ""
        body = ""

        if "SUBJECT:" in result and "BODY:" in result:
            parts = result.split("BODY:", 1)
            subject = parts[0].replace("SUBJECT:", "").strip()
            body = parts[1].strip()
        else:
            # Fallback if format not followed
            lines = result.split("\n", 1)
            subject = lines[0].strip()
            body = lines[1].strip() if len(lines) > 1 else result

        print(f"Email Subject: {subject}")
        print(f"Email Body: {body}")

        return True, subject, body

    except Exception as e:
        print(f"Error generating email: {e}")
        return False, "Follow-up", f"Error generating email: {str(e)}"