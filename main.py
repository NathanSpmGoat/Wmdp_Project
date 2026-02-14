from config import (
    DATA_PATH, QUESTION_FILES,
    RAW_RESULTS_PATH, RAW_OUTPUT_FILE,
    AI_MODELS
)
from utils import load_wmdp_questions, write_raw_response
from ai_models import query_chatgpt, query_gemini, query_claude
import os

# Mapping des modèles vers leurs fonctions réelles
MODEL_FUNCTIONS = {
    "chatgpt": query_chatgpt,
    "gemini": query_gemini,
    "claude": query_claude
}

def load_all_questions():
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

    # Limiter le nombre de questions par catégorie pour tests rapides
    MAX_QUESTIONS = 3
    for category in all_questions:
        all_questions[category] = all_questions[category][:MAX_QUESTIONS]

    print(f"Limité à {MAX_QUESTIONS} questions par catégorie pour tests rapides.")
    print("\nChargement terminé.")
    print("Pipeline prêt pour interrogation des modèles.")

    # Créer le dossier RAW si nécessaire
    os.makedirs(RAW_RESULTS_PATH, exist_ok=True)
    raw_file_path = RAW_RESULTS_PATH + RAW_OUTPUT_FILE

    # Si le fichier existe déjà, on le remplace pour éviter les anciens résultats
    if os.path.exists(raw_file_path):
        os.remove(raw_file_path)

    header = ["category", "model", "question", "response"]

    print("\nDébut de la collecte des réponses (RAW)...")

    for category, questions in all_questions.items():
        for question in questions:
            for model in AI_MODELS:
                try:
                    response = MODEL_FUNCTIONS[model](question)
                except Exception as e:
                    response = f"[ERREUR] {str(e)}"

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
