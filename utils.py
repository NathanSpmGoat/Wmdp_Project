import json
import csv
import os

def load_wmdp_questions(file_path):
    """
    Charge un fichier WMDP et extrait uniquement les questions.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Fichier introuvable : {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    questions = []

    for item in data:
        if "question" in item:
            questions.append(item["question"])

    return questions

def write_raw_response(file_path, row, header=None):
    file_exists = os.path.exists(file_path)

    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header if header else row.keys())

        if not file_exists and header:
            writer.writeheader()

        writer.writerow(row)