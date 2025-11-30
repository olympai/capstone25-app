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
        
        # Create message with base64-encoded PDF
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
                            "text": "Please evaluate this pitch deck and provide your prediction and reasoning in the specified format."
                        }
                    ]
                }
            ],
        )
        
        # Extract text from response
        result = message.content[0].text.strip()
        print(result)
        
        # Parse response to extract prediction and reasoning
        prediction = False
        reasoning = "No reasoning provided"
        missing = "Nothing missing"
        
        # Extract prediction
        if 'PREDICTION:' in result:
            pred_line = result.split('PREDICTION:')[1].split('\n')[0].strip().lower()
            if 'true' in pred_line:
                prediction = True
            elif 'false' in pred_line:
                prediction = False
        else:
            # Fallback to old parsing
            if 'true' in result.lower():
                prediction = True
            elif 'false' in result.lower():
                prediction = False
        
        # Extract reasoning
        if 'REASONING:' in result:
            reasoning = result.split('REASONING:')[1].strip()
            # Remove any trailing prediction markers
            reasoning = reasoning.split('PREDICTION:')[0].strip()

        # Extract What Missing
        if 'MISSING:' in result:
            missing = result.split('MISSING:')[1].strip()
            # Remove any trailing prediction markers
            missing = missing.split('REASONING:')[0].strip()
        
        return True, prediction, reasoning, missing
            
    except Exception as e:
        print(f"Error in prediction for {pdf_filename}: {e}")
        return False, False, f"Error: {str(e)}", ""
    
def do_websearch(model: str = model, missing: str = "", allowed_sources: list = []):
    try:
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"""You are a VC-research expert. Find out additional information based on these instructions: {missing}.
                    Focus on these sources: {allowed_sources}
                    
                    Output format:
                    PREDICTION: [Return "true", if the startup is likely to survive and succeed in the market, else "false"]
                    REASONING: [Provide a brief justification in 2–3 sentences explaining the key factors that led to your decision]
                    """
                }
            ],
            tools=[{
                "type": "web_search_20250305",
                "name": "web_search"
            }]
        )
        print(response)

        # Analyze response
        text = response["content"][3]["text"].strip()
        sources = response["content"][2]["content"]

        # Search in text
        # Extract prediction
        if 'PREDICTION:' in text:
            pred_line = text.split('PREDICTION:')[1].split('\n')[0].strip().lower()
            if 'true' in pred_line:
                prediction = True
            elif 'false' in pred_line:
                prediction = False
        else:
            # Fallback to old parsing
            if 'true' in text.lower():
                prediction = True
            elif 'false' in text.lower():
                prediction = False
        
        # Extract reasoning
        if 'REASONING:' in text:
            reasoning = text.split('REASONING:')[1].strip()
            # Remove any trailing prediction markers
            reasoning = reasoning.split('PREDICTION:')[0].strip()

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

        # summary
        message = client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"""You are a VC-analyst. You write a comprehensive summary based on the followeing to texts. 
                            1. Text (from a pitchdeck analyzer): {text_1}
                            2. Text (from Web Search assistant) {text_2}
                            """
                        }
                    ]
                }
            ],
        )
            
        # Extract text from response
        result = message.content[0].text.strip()
        return True, result, final_prediction
    except Exception as e:
        print(f"Error: {e}")
        return False, f"Error: {e}", "red"