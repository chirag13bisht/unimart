import spacy
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Load the spaCy model once when the server starts
# This is crucial for performance!
nlp = spacy.load("chatbot_model")

def simple_intent_recognition(text):
    """
    A very simple keyword-based intent recognizer.
    This is our "Intent Recognition" for now.
    """
    text = text.lower()
    if "sell" in text or "list" in text:
        return "sell_item"
    elif "find" in text or "buy" in text or "look for" in text or "looking for" in text or "do you have" in text or "any" in text:
        return "find_item"
    elif "trade" in text:
        return "trade_item"
    elif "hello" in text or "hi" in text:
        return "greet"
    else:
        return "unknown"

@csrf_exempt  # Disable CSRF for this simple API endpoint
def chatbot_query(request):
    if request.method == "POST":
        try:
            # Get the user's message from the request body
            data = json.loads(request.body)
            message = data.get("message", "")
            
            if not message:
                return JsonResponse({"error": "No message provided"}, status=400)

            # 1. Intent Recognition
            intent = simple_intent_recognition(message)

            # 2. Entity Extraction
            doc = nlp(message)
            entities = []
            for ent in doc.ents:
                entities.append({
                    "text": ent.text,
                    "label": ent.label_  # e.g., "MONEY", "PRODUCT", "ORG"
                })

            # Build our response
            response = {
                "intent": intent,
                "entities": entities,
                "original_message": message
            }
            
            return JsonResponse(response)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)