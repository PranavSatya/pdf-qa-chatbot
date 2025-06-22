import os
import csv
import random
from fpdf import FPDF

# Path to the CSV file containing questions
CSV_PATH = "pyq_data/questions.csv"

# Directory where generated PDFs will be stored
PDF_OUTPUT_DIR = "generated_pdfs"

# Ensure the output directory exists
os.makedirs(PDF_OUTPUT_DIR, exist_ok=True)

# Load questions from CSV as a list of dictionaries
def load_questions():
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

# Main function to generate test PDF
def generate_test_pdf(subject, difficulty, count):
    # Filter questions matching the selected subject and difficulty
    questions = [q for q in load_questions() if q['subject'] == subject and q['difficulty'] == difficulty]

    # Check if there are enough questions
    if len(questions) < count:
        return None, f"Only {len(questions)} questions available."

    # Randomly select the required number of questions
    selected = random.sample(questions, count)

    # Create output filename and path
    filename = f"{subject}_{difficulty}_test.pdf"
    filepath = os.path.join(PDF_OUTPUT_DIR, filename)

    # Initialize PDF document
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add header to the test
    pdf.cell(200, 10, txt=f"{subject} Practice Test ({difficulty})", ln=True, align="C")
    pdf.ln(10)

    # Add each question and options
    for i, q in enumerate(selected, 1):
        pdf.multi_cell(0, 10, f"{i}. {q['question']}")
        pdf.cell(0, 10, f"   A. {q['option_a']}", ln=True)
        pdf.cell(0, 10, f"   B. {q['option_b']}", ln=True)
        pdf.cell(0, 10, f"   C. {q['option_c']}", ln=True)
        pdf.cell(0, 10, f"   D. {q['option_d']}", ln=True)
        pdf.ln(5)

    # Add a new page for the answer key and explanations
    pdf.add_page()
    pdf.cell(200, 10, txt="Answer Key & Explanations", ln=True, align="C")
    pdf.ln(10)

    for i, q in enumerate(selected, 1):
        pdf.multi_cell(0, 10, f"{i}. {q['answer']}")
        pdf.set_text_color(100)  # Use gray color for explanation text
        pdf.multi_cell(0, 8, f"Explanation: {q['explanation']}")
        pdf.set_text_color(0)  # Reset text color to black
        pdf.ln(5)

    # Save the PDF to disk
    pdf.output(filepath)

    # Return the filename and None to indicate success
    return filename, None
