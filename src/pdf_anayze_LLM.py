import os
import json
import re
import pdfplumber
from transformers import pipeline
from collections import defaultdict

# Load keyword lists from JSON file
with open('./code/keywords.json', 'r') as f:
    keyword_data = json.load(f)

# Extract the lists from the loaded JSON
pde_subcategories = keyword_data['pde_categories']
sde_subcategories = keyword_data['sde_categories']

# Initialize an LLM summarization pipeline (you can switch to OpenAI API if preferred)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")  # Hugging Face example

# Helper functions
def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""

def identify_subcategories(text, subcategories):
    """Identifies subcategories in the given text."""
    found_subcategories = []
    for subcat in subcategories:
        if re.search(r'\b' + re.escape(subcat) + r'\b', text, re.IGNORECASE):
            found_subcategories.append(subcat)
    return found_subcategories

def analyze_themes_with_llm(text):
    """Use LLM to find themes in the text."""
    try:
        summary = summarizer(text, max_length=200, min_length=100, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"Error analyzing themes with LLM: {e}")
        return "LLM analysis failed."

# Main analysis function
def analyze_pdfs_with_llm(folder_path):
    """Analyze each PDF for keywords and themes."""
    results = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            print(f"Analyzing {filename}...")

            # Extract text from the PDF
            text = extract_text_from_pdf(pdf_path)

            # Identify PDE and SDE subcategories
            pde_found = identify_subcategories(text, pde_subcategories)
            sde_found = identify_subcategories(text, sde_subcategories)

            # Analyze themes with LLM
            themes = analyze_themes_with_llm(text)

            # Store results
            results.append({
                "file": filename,
                "pde_subcategories": pde_found,
                "sde_subcategories": sde_found,
                "themes": themes
            })

    return results

# Generate summary report
def generate_summary_report(results):
    """Generates a summary report of the analysis."""
    report_path = './llm_analysis_summary.txt'
    with open(report_path, 'w') as report:
        for result in results:
            report.write(f"File: {result['file']}\n")
            report.write(f"  PDE Subcategories: {', '.join(result['pde_subcategories']) if result['pde_subcategories'] else 'None'}\n")
            report.write(f"  SDE Subcategories: {', '.join(result['sde_subcategories']) if result['sde_subcategories'] else 'None'}\n")
            report.write(f"  Themes: {result['themes']}\n")
            report.write("\n")

    print(f"Summary report saved at {report_path}")

# Folder containing PDFs
pdf_folder = "/Users/richardpurcell/Dropbox/dal04/PhD/papers/sensors_all/"

# Run the analysis
results = analyze_pdfs_with_llm(pdf_folder)

# Generate the summary report
generate_summary_report(results)

# Save results as JSON
with open('./llm_analysis_results.json', 'w') as f:
    json.dump(results, f, indent=4)

print("LLM-based theme analysis complete.")
