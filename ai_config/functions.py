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
    
def do_websearch(model: str = model, missing: str = "", allowed_sources: list = []):
    try:
        # Define the tool for structured output
        websearch_evaluation_tool = {
            "name": "websearch_evaluation",
            "description": "Provides a structured evaluation based on web search findings",
            "input_schema": {
                "type": "object",
                "properties": {
                    "prediction": {
                        "type": "boolean",
                        "description": "True if the startup is likely to survive and succeed in the market, False otherwise"
                    },
                    "reasoning": {
                        "type": "string",
                        "description": "Brief justification in 2-3 sentences explaining the key factors that led to the decision"
                    }
                },
                "required": ["prediction", "reasoning"]
            }
        }

        response = client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"""You are a VC-research expert. Find out additional information based on these instructions: {missing}.
                    Focus on these sources: {allowed_sources}

                    After gathering information, provide your evaluation using the websearch_evaluation tool.
                    """
                }
            ],
            tools=[
                {
                    "type": "web_search_20250305",
                    "name": "web_search"
                },
                websearch_evaluation_tool
            ]
        )
        print(response)

        # Extract structured output and sources
        prediction = False
        reasoning = "No reasoning provided"
        sources = []

        for content in response.content:
            if content.type == "tool_use" and content.name == "websearch_evaluation":
                result = content.input
                prediction = result.get("prediction", False)
                reasoning = result.get("reasoning", "No reasoning provided")
            elif content.type == "tool_result":
                # Extract web search sources if available
                if hasattr(content, 'content'):
                    sources.append(content.content)

        print(f"Prediction: {prediction}")
        print(f"Reasoning: {reasoning}")

        return True, prediction, reasoning, sources

    except Exception as e:
        print(f"Error: {e}")
        return False, False, f"Error: {str(e)}", ""
    
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

        # Define the tool for structured output
        summary_tool = {
            "name": "generate_summary",
            "description": "Generates a comprehensive summary combining pitch deck analysis and web search findings",
            "input_schema": {
                "type": "object",
                "properties": {
                    "summary": {
                        "type": "string",
                        "description": "A comprehensive summary that synthesizes insights from both the pitch deck analysis and web search findings"
                    }
                },
                "required": ["summary"]
            }
        }

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

                    Use the generate_summary tool to provide your analysis.
                    """
                }
            ],
            tools=[summary_tool],
            tool_choice={"type": "tool", "name": "generate_summary"}
        )

        # Extract structured output from tool use
        for content in message.content:
            if content.type == "tool_use" and content.name == "generate_summary":
                result = content.input.get("summary", "No summary provided")
                print(f"Summary: {result}")
                return True, result, final_prediction

        # Fallback if no tool use found
        return False, "No structured output received", final_prediction

    except Exception as e:
        print(f"Error: {e}")
        return False, f"Error: {e}", "red"