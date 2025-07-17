from transformers import pipeline
from keybert import KeyBERT


print("Loading text analysis models...")
try:
    emotion_pipeline = pipeline(
        "text-classification", 
        model="joeddav/distilbert-base-uncased-go-emotions-student", 
        top_k=3
    )
    
    keyword_model = KeyBERT()
    print("Text analysis models loaded successfully.")
except Exception as e:
    print(f"Error loading text analysis models: {e}")
    emotion_pipeline = None
    keyword_model = None

def analyze_text(text: str) -> tuple[str, list[str]]:
    """
    Analyzes the input text to extract the primary emotion and core keywords.

    Args:
        text: The user-provided text string.

    Returns:
        A tuple containing:
        - The primary emotion (str).
        - A list of core keywords (list[str]).
    """
    if not emotion_pipeline or not keyword_model:
        return "neutral", []

    emotion_list = emotion_pipeline(text)[0]
    primary_emotion = emotion_list[0]['label'] if emotion_list else "neutral"

    keywords = keyword_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 1),  
        stop_words='english',          
        top_n=5                        
    )


    core_keywords = [kw[0] for kw in keywords if kw[1] > 0.4][:2]

    return primary_emotion, core_keywords
