import os
import pandas as pd
import spacy
import pycountry

# Folder containing your CSV files
folder_path = './notes/search_results'  # Replace with the actual folder path

# Load the SpaCy English model
nlp = spacy.load("en_core_web_sm")

# Define method and data type keywords
method_keywords = {
    'machine learning': ['machine learning', 'neural network', 'deep learning', 'classification', 'SVM', 'reinforcement learning'],
    'computer vision': ['computer vision', 'image processing', 'object detection', 'image recognition'],
    'wireless sensor networks': ['wireless sensor', 'WSN', 'IoT', 'sensor deployment', 'network'],
    'remote sensing': ['remote sensing', 'satellite', 'MODIS', 'Landsat', 'aerial imagery'],
    'simulation': ['simulation', 'modeling', 'fire spread model', 'BurnP3', 'FARSITE'],
    'data fusion': ['data fusion', 'data integration', 'multi-source data'],
    'optimization': ['optimization', 'genetic algorithm', 'greedy algorithm', 'dynamic grid', 'heuristics']
}

data_type_keywords = {
    'satellite data': ['satellite data', 'MODIS', 'Landsat', 'aerial imagery'],
    'sensor data': ['sensor data', 'WSN', 'IoT', 'sensor measurements'],
    'weather data': ['weather data', 'meteorological data', 'temperature', 'humidity', 'wind speed'],
    'fire data': ['fire data', 'burn probability', 'fire spread', 'fire intensity']
}

# Define a focused region/country keyword list for wildfire-prone regions
focused_region_keywords = {
    'USA': ['california', 'usa', 'united states', 'oregon', 'nevada', 'colorado', 'washington', 'arizona'],
    'Canada': ['canada', 'british columbia', 'alberta', 'nova scotia'],
    'Australia': ['australia', 'new south wales', 'victoria', 'queensland'],
    'Europe': ['spain', 'greece', 'portugal', 'france', 'italy'],
    'South America': ['brazil', 'chile', 'argentina', 'amazon'],
    'Africa': ['south africa', 'morocco', 'kenya'],
    'Asia': ['china', 'india', 'indonesia', 'siberia'],
    'Global': ['global', 'worldwide']
}

def combine_csv_files(folder_path):
    """
    Reads all CSV files from a folder and combines them into a single DataFrame.
    """
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    combined_df = pd.DataFrame()

    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        combined_df = pd.concat([combined_df, df], ignore_index=True)

    return combined_df

def classify_paper(text, keyword_dict):
    """
    Classify a paper based on the presence of keywords in the text.
    Returns a list of detected categories.
    """
    categories = []
    doc = nlp(text.lower())
    
    for category, keywords in keyword_dict.items():
        for keyword in keywords:
            if keyword in doc.text:
                categories.append(category)
                break  # No need to check other keywords once category is found
    return categories

def classify_region(text, region_dict):
    """
    Classify the region based on the presence of keywords in the text.
    Returns a list of detected regions.
    """
    regions = []
    doc = nlp(text.lower())
    
    for region, keywords in region_dict.items():
        for keyword in keywords:
            if keyword in doc.text:
                regions.append(region)
                break  # No need to check other keywords once region is found
    return regions

# Combine all CSV files from the folder
df = combine_csv_files(folder_path)

# Apply classification to abstracts and keywords in the DataFrame
df['Method'] = df['Abstract'].apply(lambda x: classify_paper(str(x), method_keywords))
df['Data Type'] = df['Abstract'].apply(lambda x: classify_paper(str(x), data_type_keywords))
df['Region'] = df['Abstract'].apply(lambda x: classify_region(str(x), focused_region_keywords))

# Display the classified DataFrame
print(df[['Document Title', 'Method', 'Data Type', 'Region']].head())

# Save the classified data to a new CSV file
df.to_csv('./results/classified_wildfire_papers.csv', index=False)
print("Combined and classified data saved to 'classified_wildfire_papers.csv'")
