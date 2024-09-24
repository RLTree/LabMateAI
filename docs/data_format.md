
# **LabMateAI Data Format Guide**

This document provides an overview of the data format used by **LabMateAI** for storing and managing scientific tools. The main data file is `tools.json`, which contains a structured list of tools along with their attributes such as name, category, features, cost, and description.

---

## Table of Contents
1. [General Structure](#general-structure)
2. [Field Descriptions](#field-descriptions)
3. [Example Entry](#example-entry)
4. [Adding New Tools](#adding-new-tools)
5. [Modifying Existing Tools](#modifying-existing-tools)

---

## General Structure

The `tools.json` file is structured as an array of JSON objects. Each object represents a scientific tool and includes several attributes that describe the tool, such as its name, category, features, and more.

The file follows this structure:

```json
[
  {
    "name": "Tool Name",
    "category": "Category Name",
    "features": ["Feature 1", "Feature 2", "Feature 3"],
    "cost": "Free/Paid",
    "description": "Brief description of the tool.",
    "url": "https://tool-website.com"
  },
  ...
]
```

Each tool is a JSON object, and the entire list of tools is wrapped in an array `[]`.

---

## Field Descriptions

Each tool in the `tools.json` file consists of the following fields:

1. **`name`** (string):
   - The name of the scientific tool.
   - **Example**: `"name": "BLAST"`

2. **`category`** (string):
   - The category or field of the tool, such as **Genomics**, **Bioinformatics**, **Proteomics**, etc.
   - **Example**: `"category": "Genomics"`

3. **`features`** (array of strings):
   - A list of features that describe the tool's functionality. This helps in identifying similarities between tools.
   - **Example**: `"features": ["Sequence Alignment", "Genome Analysis", "Data Visualization"]`

4. **`cost`** (string):
   - The cost model of the tool, such as **Free**, **Paid**, or **Freemium**.
   - **Example**: `"cost": "Free"`

5. **`description`** (string):
   - A brief description of the tool, outlining its primary purpose or functionality.
   - **Example**: `"description": "A tool for comparing nucleotide or protein sequences against a database."`

6. **`url`** (string):
   - The official website URL or documentation link where users can learn more about the tool.
   - **Example**: `"url": "https://blast.ncbi.nlm.nih.gov/"`

---

## Example Entry

Below is a sample tool entry from the `tools.json` file. This example demonstrates how to structure an individual tool with its relevant attributes.

```json
{
  "name": "BLAST",
  "category": "Genomics",
  "features": ["Sequence Alignment", "Genome Analysis", "Database Search"],
  "cost": "Free",
  "description": "Basic Local Alignment Search Tool for comparing nucleotide or protein sequences against a database.",
  "url": "https://blast.ncbi.nlm.nih.gov/"
}
```

In this example:
- The tool **BLAST** falls under the **Genomics** category.
- It offers features like **Sequence Alignment** and **Genome Analysis**.
- The tool is **Free** to use and includes a brief description as well as a website URL.

---

## Adding New Tools

To add a new tool to the **LabMateAI** recommendation system, follow these steps:

### 1. Open `tools.json`

- Open the `tools.json` file located in the `data/` directory of the project.

### 2. Add a New Tool Entry

- Add a new JSON object inside the main array, similar to the existing entries. Each tool object must include the following fields: `name`, `category`, `features`, `cost`, `description`, and `url`.

### Example New Entry

```json
{
  "name": "FastQC",
  "category": "Bioinformatics",
  "features": ["Quality Control", "NGS Data", "Sequence Analysis"],
  "cost": "Free",
  "description": "A quality control tool for high throughput sequence data.",
  "url": "https://www.bioinformatics.babraham.ac.uk/projects/fastqc/"
}
```

### 3. Save the Changes

- After adding the new tool entry, save the `tools.json` file.

---

## Modifying Existing Tools

If you need to modify an existing tool (e.g., update its description or add new features), follow these steps:

### 1. Open `tools.json`

- Open the `tools.json` file located in the `data/` directory.

### 2. Find the Tool Entry

- Locate the tool entry you wish to modify. Use the tool’s `name` to identify it in the file.

### 3. Update the Fields

- Modify the necessary fields, such as updating the tool’s description, adding new features, or correcting the tool’s website URL.

### Example Modification

Before:

```json
{
  "name": "BLAST",
  "category": "Genomics",
  "features": ["Sequence Alignment"],
  "cost": "Free",
  "description": "A tool for comparing nucleotide or protein sequences.",
  "url": "https://blast.ncbi.nlm.nih.gov/"
}
```

After:

```json
{
  "name": "BLAST",
  "category": "Genomics",
  "features": ["Sequence Alignment", "Genome Analysis", "Database Search"],
  "cost": "Free",
  "description": "Basic Local Alignment Search Tool for comparing nucleotide or protein sequences against a database.",
  "url": "https://blast.ncbi.nlm.nih.gov/"
}
```

### 4. Save the Changes

- Once the necessary updates have been made, save the `tools.json` file.

---

## Important Notes

1. **Field Consistency**: Ensure that each tool entry includes all the necessary fields (`name`, `category`, `features`, `cost`, `description`, and `url`). Missing fields may cause errors in the recommendation system.

2. **Category Standardization**: To maintain consistency, ensure that categories are uniformly named. For example, if you add tools to the **Genomics** category, always spell it the same way across all entries.

3. **JSON Formatting**: Ensure the `tools.json` file maintains valid JSON formatting. Use a text editor with syntax highlighting or an online JSON validator to check for errors before saving.

---

By following this guide, you’ll be able to add, update, or remove scientific tools from **LabMateAI**’s data set. The format is flexible, allowing you to expand the system with additional tools and categories as needed.
