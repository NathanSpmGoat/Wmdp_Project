from config import (
    DATA_PATH, QUESTION_FILES,
    RAW_RESULTS_PATH, RAW_OUTPUT_FILE,
    AI_MODELS
)
from utils import load_wmdp_questions, write_raw_response
from ai_models import query_chatgpt, query_gemini, query_copilot
import os

# Mapping des modèles vers leurs fonctions simulées
MODEL_FUNCTIONS = {
    "chatgpt": query_chatgpt,
    "gemini": query_gemini,
    "copilot": query_copilot
}

def load_all_questions():
    """
    Charge toutes les questions WMDP depuis le benchmark officiel.
    """
    all_questions = {}
    for category, filename in QUESTION_FILES.items():
        path = DATA_PATH + filename
        questions = load_wmdp_questions(path)
        all_questions[category] = questions
        print(f"{len(questions)} questions chargées ({category})")
    return all_questions

def main():
    print("=== Programme d'évaluation WMDP ===")
    print("Chargement du benchmark officiel...")

    # Charger toutes les questions
    all_questions = load_all_questions()
    print("\nChargement terminé.")
    print("Pipeline prêt pour interrogation des modèles.")

    # Créer le dossier RAW si nécessaire
    os.makedirs(RAW_RESULTS_PATH, exist_ok=True)
    raw_file_path = RAW_RESULTS_PATH + RAW_OUTPUT_FILE

    # Définir les colonnes du CSV
    header = ["category", "model", "question", "response"]

    print("\nDébut de la collecte des réponses (RAW)...")

    # Parcourir toutes les questions et tous les modèles
    for category, questions in all_questions.items():
        for question in questions:
            for model in AI_MODELS:
                response = MODEL_FUNCTIONS[model](question)

                row = {
                    "category": category,
                    "model": model,
                    "question": question,
                    "response": response
                }

                write_raw_response(raw_file_path, row, header)

    print("Collecte des réponses terminée. Fichier RAW prêt :", raw_file_path)

if __name__ == "__main__":
    main()
