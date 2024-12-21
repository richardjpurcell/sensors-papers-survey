import os
import pdfplumber
import PyPDF2
import re
import json
from itertools import combinations
from collections import defaultdict

# Load keyword lists from JSON file
with open('./code/keywords.json', 'r') as f:
    keyword_data = json.load(f)

# Extract the lists from the loaded JSON
themes = keyword_data['themes']
datasets = keyword_data['datasets']
regions = keyword_data['regions']
dataset_variations = keyword_data['dataset_variations']
detection_variations = keyword_data['detection_variations']
prevention_variations = keyword_data['prevention_variations']
prediction_variations = keyword_data['prediction_variations']
management_variations = keyword_data['management_variations']
vegetation_variations = keyword_data['vegetation_variations']
elevation_variations = keyword_data['elevation_variations']

# Initialize counters for PDFs mentioning custom terms (not the total occurrences)
detection_count = 0
prevention_count = 0
prediction_count = 0
management_count = 0
vegetation_count = 0
elevation_count = 0

# Initialize dictionaries to track how many PDFs mention each theme, dataset, and region
theme_count = {theme: 0 for theme in themes}
dataset_count = {dataset: 0 for dataset in datasets}
region_count = {region: 0 for region in regions}

# Counters for regional and unclear/global papers
regional_focus_count = 0
unclear_focus_count = 0

# Dictionary to track co-occurrence of themes, theme-dataset, and region-dataset co-occurrences
theme_cooccurrence = defaultdict(int)
theme_dataset_cooccurrence = defaultdict(int)
region_dataset_cooccurrence = defaultdict(int)  # New dictionary for region-dataset co-occurrence

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

def extract_metadata_from_pdf(pdf_path):
    """Extracts metadata from a PDF file using PyPDF2 PdfReader."""
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            metadata = reader.metadata
        return metadata
    except Exception as e:
        print(f"Error extracting metadata from {pdf_path}: {e}")
        return {}

def search_for_keywords(text, keyword_list, count_dict):
    """Searches the text for each keyword, returns found keywords, and updates the count dictionary."""
    found_keywords = []
    for keyword in keyword_list:
        if re.search(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE):
            found_keywords.append(keyword)
            count_dict[keyword] += 1  # Count this as 1 mention for the entire PDF
            break  # Ensure we only count once per document for each term
    return found_keywords

def search_for_custom_terms(text):
    """Searches for detection, prevention, prediction, vegetation, elevation, and management mentions in a PDF."""
    global detection_count, prevention_count, prediction_count, management_count, vegetation_count, elevation_count

    for term in detection_variations:
        if re.search(r'\b' + re.escape(term) + r'\b', text, re.IGNORECASE):
            detection_count += 1
            break  # Only count once per document

    for term in prevention_variations:
        if re.search(r'\b' + re.escape(term) + r'\b', text, re.IGNORECASE):
            prevention_count += 1
            break

    for term in prediction_variations:
        if re.search(r'\b' + re.escape(term) + r'\b', text, re.IGNORECASE):
            prediction_count += 1
            break

    for term in management_variations:
        if re.search(r'\b' + re.escape(term) + r'\b', text, re.IGNORECASE):
            management_count += 1
            break

    for term in vegetation_variations:
        if re.search(r'\b' + re.escape(term) + r'\b', text, re.IGNORECASE):
            vegetation_count += 1
            break

    for term in elevation_variations:
        if re.search(r'\b' + re.escape(term) + r'\b', text, re.IGNORECASE):
            elevation_count += 1
            break

def search_for_datasets_and_following_words(text, variations):
    """Searches for variations of the word 'dataset' and captures following words."""
    found_datasets = []
    for variation in variations:
        matches = re.finditer(variation, text, re.IGNORECASE)
        for match in matches:
            start_pos = match.end()
            words_after = re.findall(r'\w+', text[start_pos:start_pos + 50])  # Adjust word count as needed
            if words_after:
                found_datasets.append(f"{match.group()}: {' '.join(words_after[:5])}")  # Limit to 5 following words
    return found_datasets

def track_cooccurrence(found_themes, found_datasets, found_regions):
    """Track how often themes appear together and with datasets or regions."""
    # Track theme co-occurrences
    if len(found_themes) > 1:
        for theme_combination in combinations(found_themes, 2):
            theme_cooccurrence[theme_combination] += 1
    
    # Track theme-dataset co-occurrences
    for theme in found_themes:
        for dataset in found_datasets:
            theme_dataset_cooccurrence[(theme, dataset)] += 1

    # Track region-dataset co-occurrences
    for region in found_regions:
        for dataset in found_datasets:
            region_dataset_cooccurrence[(region, dataset)] += 1

def analyze_pdfs_in_folder(folder_path):
    """Analyze each PDF in the folder for themes, datasets, region keywords, custom terms, and metadata."""
    global regional_focus_count, unclear_focus_count
    results = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            print(f"Analyzing {filename}...")
            
            # Extract text from the PDF
            text = extract_text_from_pdf(pdf_path)
            
            # Extract metadata from the PDF
            metadata = extract_metadata_from_pdf(pdf_path)
            
            # Combine text from PDF body and metadata
            combined_text = text
            if metadata:
                combined_text += ' '.join([str(value) for value in metadata.values()])

            # Search for custom terms in the text and update counts
            search_for_custom_terms(combined_text)
            
            # Search for themes, datasets, and regions in the text, updating counts
            found_themes = search_for_keywords(combined_text, themes, theme_count)
            found_datasets = search_for_keywords(combined_text, datasets, dataset_count)
            found_regions = search_for_keywords(combined_text, regions, region_count)
            
            # Track co-occurrences of themes and datasets
            track_cooccurrence(found_themes, found_datasets, found_regions)

            # Check if the paper is regional or global, and update counters
            if found_regions:
                regional_focus_count += 1
            elif 'global' not in combined_text.lower():
                unclear_focus_count += 1

            # Search for variations of the word 'dataset' and capture following words
            dataset_mentions = search_for_datasets_and_following_words(combined_text, dataset_variations)
            
            # Store results
            if found_themes or found_datasets or found_regions or dataset_mentions:
                results.append({
                    'file': filename,
                    'themes': found_themes,
                    'datasets': found_datasets,
                    'regions': found_regions,
                    'dataset_mentions': dataset_mentions
                })
    return results

def generate_summary_report(results):
    """Generates a summary report of the analysis and appends counts of themes, datasets, regions, and co-occurrences."""
    with open('pdf_analysis_report_2.txt', 'w') as report:
        # Write detailed results per PDF
        for result in results:
            report.write(f"File: {result['file']}\n")
            report.write(f"  Themes: {', '.join(result['themes']) if result['themes'] else 'None'}\n")
            report.write(f"  Datasets: {', '.join(result['datasets']) if result['datasets'] else 'None'}\n")
            report.write(f"  Regions: {', '.join(result['regions']) if result['regions'] else 'None'}\n")
            report.write(f"  Dataset Mentions: {', '.join(result['dataset_mentions']) if result['dataset_mentions'] else 'None'}\n")
            report.write("\n")

        # Write a summary of theme counts
        report.write("Summary of Theme Mentions (Number of PDFs that mention each theme):\n")
        for theme, count in theme_count.items():
            report.write(f"{theme}: {count}\n")
        
        # Write a summary of dataset counts
        report.write("\nSummary of Dataset Mentions (Number of PDFs that mention each dataset):\n")
        for dataset, count in dataset_count.items():
            report.write(f"{dataset}: {count}\n")

        # Write a summary of region counts
        report.write("\nSummary of Region Mentions (Number of PDFs that mention each region):\n")
        for region, count in region_count.items():
            report.write(f"{region}: {count}\n")

        # Write counts for regional and unclear/global papers
        report.write(f"\nNumber of papers mentioning specific regions or countries: {regional_focus_count}\n")
        report.write(f"Number of papers that don't explicitly indicate either a regional or global focus: {unclear_focus_count}\n")
        
        # Write a summary of theme co-occurrences
        report.write("\nSummary of Theme Co-occurrences (Pairs of themes appearing together):\n")
        for theme_pair, cooccurrence_count in theme_cooccurrence.items():
            report.write(f"{theme_pair}: {cooccurrence_count}\n")
        
        # Write a summary of theme-dataset co-occurrences
        report.write("\nSummary of Theme-Dataset Co-occurrences (Themes and Datasets appearing together):\n")
        for theme_dataset_pair, cooccurrence_count in theme_dataset_cooccurrence.items():
            report.write(f"{theme_dataset_pair}: {cooccurrence_count}\n")
        
        # Write a summary of region-dataset co-occurrences
        report.write("\nSummary of Region-Dataset Co-occurrences (Regions and Datasets appearing together):\n")
        for region_dataset_pair, cooccurrence_count in region_dataset_cooccurrence.items():
            report.write(f"{region_dataset_pair}: {cooccurrence_count}\n")

        # Write a summary of custom term mentions (detection, prevention, prediction, management, vegetation, elevation)
        report.write("\nSummary of Custom Term Mentions (Number of PDFs that mention detection, prevention, etc.):\n")
        report.write(f"Detection Mentions: {detection_count}\n")
        report.write(f"Prevention Mentions: {prevention_count}\n")
        report.write(f"Prediction Mentions: {prediction_count}\n")
        report.write(f"Long-term Management Mentions: {management_count}\n")
        report.write(f"Vegetation/Fuel Mentions: {vegetation_count}\n")
        report.write(f"Elevation/Topography Mentions: {elevation_count}\n")

    print("Summary report saved as 'pdf_analysis_report.txt'.")

# Folder where the PDFs are stored
pdf_folder = "/Users/richardpurcell/Dropbox/dal04/PhD/papers/weather_specific/"

# Run the analysis
pdf_analysis_results = analyze_pdfs_in_folder(pdf_folder)

# Generate a summary report of the findings, including counts
generate_summary_report(pdf_analysis_results)
