from huggingface_hub import InferenceClient
import os

HF_API_KEY = os.getenv("HF_API_KEY")

def analyze_sentiment(text):
    if not HF_API_KEY:
        raise Exception("HF_API_KEY non configurée")
    
    try:
        # Utiliser InferenceClient avec la nouvelle API
        client = InferenceClient(token=HF_API_KEY)
        
        # Appeler le modèle de classification
        result = client.text_classification(
            text=text,
            model="nlptown/bert-base-multilingual-uncased-sentiment"
        )
        
        # Le résultat est une liste de prédictions
        if result and len(result) > 0:
            # Trouver la prédiction avec le score le plus élevé
            best_prediction = max(result, key=lambda x: x['score'])
            label = best_prediction['label']
            
            # Extraire le score (1-5 stars)
            # Le label est au format "1 star", "2 stars", etc.
            score = int(label.split()[0])
            
            # Déterminer le sentiment
            if score <= 2:
                sentiment = "négatif"
            elif score == 3:
                sentiment = "neutre"
            else:
                sentiment = "positif"
            
            return {
                "score": score,
                "sentiment": sentiment,
                "confidence": best_prediction['score']
            }
        
        raise Exception("Aucune prédiction retournée par le modèle")
    
    except Exception as e:
        # Gestion d'erreurs spécifique pour les cas courants
        error_msg = str(e)
        if "503" in error_msg or "loading" in error_msg.lower():
            raise Exception("Modèle en chargement. Réessayez dans 20-30 secondes.")
        elif "401" in error_msg or "unauthorized" in error_msg.lower():
            raise Exception("Clé API Hugging Face invalide ou expirée")
        else:
            raise Exception(f"Erreur Hugging Face: {error_msg}")