# LabMateAI Usage Guide

Welcome to the **LabMateAI Usage Guide**. This guide provides detailed instructions on how to use LabMateAI to discover and recommend scientific tools relevant to your research. Whether you're new to LabMateAI or looking to maximize its capabilities, this guide will help you navigate the application effectively.

---

## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
  - [Launching the CLI](#launching-the-cli)
  - [Navigating the Menu](#navigating-the-menu)
- [Features and Commands](#features-and-commands)
  - [1. Tool Similarity Recommendations](#1-tool-similarity-recommendations)
  - [2. Category-Based Recommendations](#2-category-based-recommendations)
  - [3. Keyword-Based Search](#3-keyword-based-search)
- [Advanced Usage](#advanced-usage)
- [Tips and Tricks](#tips-and-tricks)
- [FAQ](#faq)
- [Troubleshooting](#troubleshooting)
- [Contact Support](#contact-support)

---

## Introduction

**LabMateAI** is an AI-powered recommendation system designed to assist researchers in discovering laboratory tools and software tailored to their scientific needs. By leveraging advanced algorithms and data structures, LabMateAI provides personalized recommendations based on tool similarity, categories, and keyword searches.

---

## Getting Started

### Launching the CLI

After installing LabMateAI, you can launch the command-line interface (CLI) by simply typing:

```bash
labmateai
```

### Navigating the Menu

Upon launching, you'll be presented with a menu of options:

```
Welcome to LabMateAI!
Please select an option:
1. Recommend tools similar to a specific tool
2. Recommend tools in a specific category
3. Search for tools by keyword
4. Exit
Enter your choice (1-4):
```

- **Enter the number corresponding to your choice** and press **Enter**.
- Follow the prompts to input additional information as required.

---

## Features and Commands

### 1. Tool Similarity Recommendations

**Purpose**: Find tools that are similar to a specific tool you already use.

**Steps**:

1. **Select Option 1**: Enter `1` at the main menu and press **Enter**.
2. **Enter the Tool Name**: When prompted, type the name of the tool (e.g., `BLAST`) and press **Enter**.
3. **Specify Number of Recommendations**: Enter the number of recommendations you want (default is 5).
4. **View Recommendations**: LabMateAI will display a list of similar tools.

**Example**:

```
Enter the name of the tool you are using:
> BLAST
Enter the number of recommendations you would like (default is 5):
> 3
Here are 3 tools similar to BLAST:
1. Clustal Omega - A tool for multiple sequence alignment.
2. MAFFT - A fast multiple sequence alignment program.
3. MUSCLE - Advanced software for multiple sequence alignment.
```

### 2. Category-Based Recommendations

**Purpose**: Discover tools within a specific scientific category.

**Steps**:

1. **Select Option 2**: Enter `2` at the main menu and press **Enter**.
2. **Enter the Category Name**: Type the name of the category (e.g., `Genomics`) and press **Enter**.
3. **View Tools in Category**: LabMateAI will display a list of tools within that category.

**Example**:

```
Enter the category you are interested in:
> Genomics
Here are tools in the Genomics category:
1. BWA - A software package for mapping low-divergent sequences.
2. Bowtie2 - A fast and sensitive gapped read aligner.
3. HISAT2 - A fast and sensitive alignment program for mapping next-generation sequencing reads.
...
```

### 3. Keyword-Based Search

**Purpose**: Search for tools based on keywords related to your research.

**Steps**:

1. **Select Option 3**: Enter `3` at the main menu and press **Enter**.
2. **Enter the Keyword**: Type your keyword (e.g., `RNA-seq`) and press **Enter**.
3. **View Search Results**: LabMateAI will display tools that match your keyword.

**Example**:

```
Enter the keyword to search for tools:
> RNA-seq
Tools matching your search:
1. DESeq2 - Differential gene expression analysis based on the negative binomial distribution.
2. EdgeR - Empirical analysis of digital gene expression data in R.
3. Kallisto - A program for quantifying abundances of transcripts from RNA-Seq data.
...
```

---

## Advanced Usage

LabMateAI is designed to be straightforward, but here are some advanced tips:

- **Partial Tool Names**: You can enter partial tool names, and LabMateAI will attempt to find the closest match.
- **Case Insensitive**: Inputs are not case-sensitive, so `blast` and `BLAST` are treated the same.
- **Abbreviations**: Common abbreviations may be recognized (e.g., `NGS` for Next-Generation Sequencing).

---

## Tips and Tricks

- **Explore New Categories**: Don't hesitate to explore categories you're less familiar with; you might discover useful tools.
- **Combine Keywords**: Use general keywords to get broader results (e.g., `alignment`, `visualization`).
- **Stay Updated**: LabMateAI's tool database is regularly updated. Ensure you have the latest version installed.

---

## FAQ

### Q1: **I can't find a tool I'm looking for. What should I do?**

**A**: Try using different variations of the tool's name or check for spelling errors. If the tool is still not found, consider suggesting it for inclusion by contacting us.

### Q2: **How often is the tool database updated?**

**A**: We aim to update the database regularly. Check for updates by ensuring you have the latest version of LabMateAI installed:

```bash
pip install --upgrade labmateai
```

### Q3: **Can I contribute to LabMateAI's tool database?**

**A**: Yes! Contributions are welcome. Please refer to the [Contributing Guide](CONTRIBUTING.md) for instructions on how to contribute.

---

## Troubleshooting

### Issue: **LabMateAI command not found**

**Solution**: Ensure that the installation was successful. If using a virtual environment, make sure it's activated. Reinstall LabMateAI if necessary.

```bash
pip install labmateai
```

### Issue: **No recommendations are displayed**

**Solution**: Verify your input for typos or try using more general terms. If the problem persists, contact support.

### Issue: **Error messages during execution**

**Solution**: Note the error message and check the [FAQ](#faq) for possible solutions. If unresolved, consider reinstalling or reaching out to support.

---

## Contact Support

If you encounter any issues or have questions not covered in this guide, please contact us:

- **Email**: [tnoblin@health.ucsd.edu](mailto:tnoblin@health.ucsd.edu)
- **GitHub Issues**: Open an issue on the [LabMateAI repository](https://github.com/RLTree/LabMateAI/issues)
