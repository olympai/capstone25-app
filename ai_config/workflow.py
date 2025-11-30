from ai_config.functions import get_prediction, do_websearch, summary

# start workflow
def start_workflow(file_name: str = "", allowed_sources: list = []):
    alert = {}
    """
    Returns: Ampel Score, Zusammenfassung, Ampel/Zusammenfassung PDA, Ampel/Zusammenfassung WS
    """
    # PDA
    success_1, prediction_1, reasoning_1, missing = get_prediction(pdf_filename=file_name)
    if not success_1:
        alert = {"error": reasoning_1}
        return alert

    # missing information, websearch
    success_2, prediction_2, reasoning_2, sources = do_websearch(missing=missing, allowed_sources=allowed_sources)
    if not success_2:
        alert = {"error": reasoning_2}
        return alert

    # conclusion
    final_success, final_result, final_prediction = summary(text_1=reasoning_1,
                                                            text_2=reasoning_2,
                                                            score_1=prediction_1,
                                                            score_2=prediction_2
                                                            )
    if not final_success:
        alert = {"error": final_result}
        return alert

    return final_prediction, final_result, (prediction_1, reasoning_1), (prediction_2, reasoning_2, sources)

if __name__ == "__main__":
    start_workflow("yoolox.pdf")