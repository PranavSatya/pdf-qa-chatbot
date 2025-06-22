import os
import re
import csv
from langchain_community.document_loaders import PyMuPDFLoader

PDF_DIR = "pyq_data/pyq"
CSV_PATH = "pyq_data/questions.csv"

pattern = re.compile(
    r"(\d+)\.\s*(.*?)\nA\.\s*(.*?)\nB\.\s*(.*?)\nC\.\s*(.*?)\nD\.\s*(.*?)\nAnswer:\s*(\w)\n(?:Explanation:\s*(.*?))?(?=\n\d+\.|\Z)",
    re.S
)

def extract_from_pdf(pdf_path):
    loader = PyMuPDFLoader(pdf_path)
    pages = loader.load()
    text = "\n".join([page.page_content for page in pages])
    return pattern.findall(text)

def parse_subject(filename):
    return os.path.splitext(filename)[0].capitalize()

def determine_difficulty(question_text: str):
    length = len(question_text.strip().split())
    if length < 10:
        return "Easy"
    elif length < 25:
        return "Medium"
    return "Hard"

def main():
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["question", "option_a", "option_b", "option_c", "option_d", "answer", "subject", "difficulty", "explanation"])

        for file in os.listdir(PDF_DIR):
            if file.endswith(".pdf"):
                subject = parse_subject(file)
                entries = extract_from_pdf(os.path.join(PDF_DIR, file))
                for _, q, a, b, c, d, ans_letter, explanation in entries:
                    try:
                        options = [a, b, c, d]
                        correct = options[ord(ans_letter.upper()) - ord('A')]
                        difficulty = determine_difficulty(q)
                    except Exception as e:
                        print(f"⚠️ Skipping malformed question in {file}: {e}")
                        continue
                    writer.writerow([
                        q.strip(), a.strip(), b.strip(), c.strip(), d.strip(),
                        correct.strip(), subject, difficulty, (explanation or "").strip()
                    ])
                print(f"✅ Extracted from: {file}")

if __name__ == "__main__":
    main()
