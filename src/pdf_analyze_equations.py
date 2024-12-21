import os
import pdfplumber
import re
import json
from collections import defaultdict
import matplotlib.pyplot as plt

# Load keyword lists from JSON file
with open('./code/keywords.json', 'r') as f:
    keyword_data = json.load(f)

# Extract the lists from the loaded JSON
pde_subcategories = keyword_data['pde_categories']
sde_subcategories = keyword_data['sde_categories']

# Initialize counters and dictionaries
paper_categories = {"PDE-only": 0, "SDE-only": 0, "Both PDE and SDE": 0, "Neither": 0}
paper_filenames = {"PDE-only": [], "SDE-only": [], "Both PDE and SDE": [], "Neither": []}
pde_subcategory_counts = {subcat: 0 for subcat in pde_subcategories}
sde_subcategory_counts = {subcat: 0 for subcat in sde_subcategories}

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

def categorize_paper(text):
    """Categorizes the paper into PDE-only, SDE-only, Both, or Neither."""
    has_pde = any(re.search(r'\b' + re.escape(subcat) + r'\b', text, re.IGNORECASE) for subcat in pde_subcategories)
    has_sde = any(re.search(r'\b' + re.escape(subcat) + r'\b', text, re.IGNORECASE) for subcat in sde_subcategories)

    if has_pde and has_sde:
        return "Both PDE and SDE"
    elif has_pde:
        return "PDE-only"
    elif has_sde:
        return "SDE-only"
    else:
        return "Neither"

def identify_subcategories(text, subcategories):
    """Identifies subcategories in the given text."""
    found_subcategories = []
    for subcat in subcategories:
        if re.search(r'\b' + re.escape(subcat) + r'\b', text, re.IGNORECASE):
            found_subcategories.append(subcat)
    return found_subcategories

# Main analysis function
def analyze_pdfs_in_folder(folder_path):
    """Analyze each PDF in the folder for PDE and SDE categorization and subcategories."""
    results = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            print(f"Analyzing {filename}...")

            # Extract text from the PDF
            text = extract_text_from_pdf(pdf_path)

            # Categorize the paper
            category = categorize_paper(text)
            paper_categories[category] += 1
            paper_filenames[category].append(filename)

            # Identify PDE and SDE subcategories
            pde_found = identify_subcategories(text, pde_subcategories)
            sde_found = identify_subcategories(text, sde_subcategories)

            # Update subcategory counts
            for subcat in pde_found:
                pde_subcategory_counts[subcat] += 1
            for subcat in sde_found:
                sde_subcategory_counts[subcat] += 1

            # Store results
            results.append({
                "file": filename,
                "category": category,
                "pde_subcategories": pde_found,
                "sde_subcategories": sde_found
            })

    return results

# Generate summary report and visualizations
def generate_summary_report(results):
    """Generates a summary report and visualizations."""
    report_path = './equation_analysis_summary_updated.txt'
    with open(report_path, 'w') as report:
        # Write detailed results
        for result in results:
            report.write(f"File: {result['file']}\n")
            report.write(f"  Category: {result['category']}\n")
            report.write(f"  PDE Subcategories: {', '.join(result['pde_subcategories']) if result['pde_subcategories'] else 'None'}\n")
            report.write(f"  SDE Subcategories: {', '.join(result['sde_subcategories']) if result['sde_subcategories'] else 'None'}\n")
            report.write("\n")

        # Write category summary with filenames
        report.write("\nPaper Categorization Summary:\n")
        for category, count in paper_categories.items():
            report.write(f"{category}: {count}\n")
            report.write(f"  Files: {', '.join(paper_filenames[category]) if paper_filenames[category] else 'None'}\n")

        # Write subcategory summaries
        report.write("\nPDE Subcategory Counts:\n")
        for subcat, count in pde_subcategory_counts.items():
            report.write(f"{subcat}: {count}\n")

        report.write("\nSDE Subcategory Counts:\n")
        for subcat, count in sde_subcategory_counts.items():
            report.write(f"{subcat}: {count}\n")

    print(f"Summary report saved at {report_path}")

    # Generate visualizations
    # Paper categorization
    plt.figure(figsize=(8, 6))
    plt.bar(paper_categories.keys(), paper_categories.values(), color="skyblue")
    plt.title("Paper Categorization")
    plt.xlabel("Category")
    plt.ylabel("Number of Papers")
    plt.savefig('./paper_categorization_updated.png')
    plt.close()

    # PDE subcategory distribution
    plt.figure(figsize=(12, 8))  # Slightly larger figure size
    plt.barh(list(pde_subcategory_counts.keys()), list(pde_subcategory_counts.values()), color="lightgreen")
    plt.title("PDE Subcategory Distribution", fontsize=18)  # Larger title font
    plt.xlabel("Frequency", fontsize=14)  # Larger x-axis label font
    plt.ylabel("Subcategories", fontsize=14)  # Added y-axis label
    plt.xticks(fontsize=12)  # Larger tick labels for x-axis
    plt.yticks(fontsize=16, rotation=0)  # Larger and angled tick labels for y-axis
    plt.tight_layout()
    plt.savefig('./pde_subcategory_distribution_updated.png')
    plt.close()


    # SDE subcategory distribution
    plt.figure(figsize=(12, 8))  # Slightly larger figure size
    plt.barh(list(sde_subcategory_counts.keys()), list(sde_subcategory_counts.values()), color="lightcoral")
    plt.title("SDE Subcategory Distribution", fontsize=18)  # Larger title font
    plt.xlabel("Frequency", fontsize=14)  # Larger x-axis label font
    plt.ylabel("Subcategories", fontsize=14)  # Added y-axis label
    plt.xticks(fontsize=12)  # Larger tick labels for x-axis
    plt.yticks(fontsize=16, rotation=0)  # Larger and angled tick labels for y-axis
    plt.tight_layout()
    plt.savefig('./sde_subcategory_distribution_updated.png')
    plt.close()


    print("Visualizations saved as PNG files.")

# Folder containing PDFs
pdf_folder = "/Users/richardpurcell/Dropbox/dal04/PhD/papers/weather_specific/"

# Run the analysis
results = analyze_pdfs_in_folder(pdf_folder)

# Generate summary report and visualizations
generate_summary_report(results)
