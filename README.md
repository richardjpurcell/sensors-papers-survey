# README.md

## Wildfire Sensor Papers Survey
**Analyzing Themes, Datasets, Problems, Solutions, Equations, and Metadata in Computer Science Wildfire Research PDFs**

---

## Description

This project analyzes a collection of PDFs related to computer science wildfire sensor research to extract **themes**, **datasets**, **problems**, **solutions**, **equations**, and **metadata**. The analysis aims to identify patterns, highlight relationships between **problem domain equations (PDE)** and **solution domain equations (SDE)**, and provide insights into wildfire detection and monitoring research trends. The ultimate goal is to model the **problems** and **solutions** expressed in the papers as equations, datasets, themes, and co-occurrences.

---

## Key Objectives

1. **Identify Equations**  
   - Extract mathematical or verbal equations from PDFs.
   - Classify equations into:
     - **Problem Domain Equations (PDE)**: Define the research problem.
     - **Solution Domain Equations (SDE)**: Provide methods, models, and solutions.

2. **Analyze Themes, Problems, and Solutions**  
   - Identify recurring themes, datasets, problems, and solutions using predefined keywords.
   - Analyze co-occurrences of themes, problems, and solutions across papers.

3. **Model Results**  
   - Express findings as equations, co-occurrence matrices, and visual summaries.
   - Quantify relationships between PDEs, SDEs, datasets, themes, and solutions.

4. **Visualize Trends**  
   - Generate visualizations to summarize:
     - Theme, problem, and solution frequencies.
     - Theme co-occurrences.
     - Dataset occurrences.
     - PDE and SDE subcategories.

---

## Input Data

The input consists of:
- **PDF Collection**: Wildfire research papers.
- **Keywords**: A `keywords.json` file specifying themes, datasets, problems, solutions, and equation categories.

---

## Workflow

### 1. **Metadata Analysis**
- **Script**: `classify_metadata.py`
- **Purpose**:  
   - Extract metadata from PDFs (e.g., author, year, title).  
   - Analyze patterns in metadata to complement theme, problem, and equation analysis.

---

## Outputs

1. **Text Reports**:  
   - Theme, problem, and solution analysis summary.
   - Equation classification summary.
   - Co-occurrence analysis report.

2. **Visualizations**:  
   - **Theme Co-Occurrence**: Heatmaps showing co-occurrences of themes.
   - **Problem and Solution Frequencies**: Bar charts summarizing identified issues and solutions.
   - **PDE and SDE Subcategory Distribution**: Charts visualizing equation types.
   - **Dataset Mentions**: Frequency and co-occurrence with themes.

3. **Research Insight Equation**:  
   The overall relationships can be expressed as:  

   ![Research Insight Equation](https://latex.codecogs.com/svg.latex?R=f\left(PDE(P),SDE(P),D(P),T(P),S(P)\right))

   Where:  
   - ![R](https://latex.codecogs.com/svg.latex?R): Research insights from the analysis.  
   - ![PDE(P)](https://latex.codecogs.com/svg.latex?PDE(P)): Problem Domain Equations in the PDFs \( P \).  
   - ![SDE(P)](https://latex.codecogs.com/svg.latex?SDE(P)): Solution Domain Equations in the PDFs \( P \).  
   - ![D(P)](https://latex.codecogs.com/svg.latex?D(P)): Datasets mentioned in the PDFs \( P \).  
   - ![T(P)](https://latex.codecogs.com/svg.latex?T(P)): Themes extracted from the PDFs \( P \).  
   - ![S(P)](https://latex.codecogs.com/svg.latex?S(P)): Solutions extracted from the PDFs \( P \).  

---

### 2. **Theme, Problem, and Solution Analysis**
- **Script**: `pdf_analyze_themes.py`
- **Purpose**:  
   - Extract and count mentions of predefined themes, problems, solutions, datasets, and regions.  
   - Identify co-occurrences between themes, problems, and solutions.

**Outputs**:
- A report listing:
  - Frequencies of themes, problems, and solutions.
  - Dataset mentions and co-occurrence statistics.

---

### 3. **Equation Analysis**
- **Script**: `pdf_analyze_equations.py`
- **Purpose**:  
   - Extract equations (mathematical and verbal) from PDFs.  
   - Categorize equations into:
     - **Problem Domain Equations (PDE)**: Problem formulation, boundary conditions, etc.
     - **Solution Domain Equations (SDE)**: Optimization techniques, predictive models, etc.  

**Outputs**:
- A report classifying equations by subcategory.
- Summary of PDFs with PDEs, SDEs, or both.

---

## Installation and Dependencies

### Prerequisites
- Python 3.x

### Required Libraries:
- pdfplumber
- PyPDF2
- matplotlib
- seaborn
- json
- pandas

---

## Future Enhancements

- Automate keyword updates in `keywords.json` using text mining.
- Integrate additional datasets and improve equation extraction.
- Develop interactive visualizations for co-occurrence and trend analysis.
