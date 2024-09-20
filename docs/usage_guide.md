
# **LabMate Usage Guide**

Welcome to **LabMate**, a scientific tool recommendation system that helps users find related scientific software and tools based on their input. This guide will walk you through the setup, usage, and functionality of the **LabMate** system.

## Table of Contents
1. [Installation](#installation)
2. [Running LabMate](#running-labmate)
3. [Command Line Interface (CLI) Usage](#command-line-interface-cli-usage)
4. [Recommendation Types](#recommendation-types)
5. [Example Commands](#example-commands)
6. [Running Tests](#running-tests)
7. [Development](#development)
8. [Contact Information](#contact-information)

---

## Installation

To install and run **LabMate**, follow these steps:

### 1. Clone the Repository

\`\`\`bash
git clone https://github.com/RLTree/LabMate.git
cd LabMate
\`\`\`

### 2. Install Dependencies

Install the required dependencies using \`pip\`:

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 3. Set Up Tool Data

Ensure you have the tool dataset in JSON format (e.g., \`tools.json\`) located in the \`data/\` directory. You can add your own tool data or use the default one provided.

---

## Running LabMate

Once the dependencies are installed, you can start using the **LabMate** system.

### 1. Running the CLI

To start the command-line interface (CLI), run:

\`\`\`bash
python cli.py
\`\`\`

This will launch the CLI, where you can input commands to get tool recommendations.

---

## Command Line Interface (CLI) Usage

The **LabMate** CLI accepts a number of arguments to request different types of recommendations. Below are the options available:

### Basic Syntax

\`\`\`bash
python cli.py [OPTIONS]
\`\`\`

### Options

| Option            | Argument      | Description                                                |
|-------------------|---------------|------------------------------------------------------------|
| \`-t\`, \`--tool\`    | TOOL_NAME     | Recommend tools similar to the specified tool.              |
| \`-c\`, \`--category\`| CATEGORY_NAME | Recommend tools from the specified category.                |
| \`-s\`, \`--search\`  | KEYWORD       | Search for tools using a keyword.                          |
| \`-n\`, \`--num\`     | NUMBER        | Specify the number of recommendations to return (default 5).|
| \`-H\`, \`--help\`    | None          | Display the help message with available commands.           |

---

## Recommendation Types

**LabMate** supports several types of recommendations:

### 1. **Similar Tool Recommendations**:
   - Provides recommendations based on a specific tool.
   - Example: You can ask **LabMate** to recommend tools similar to **BLAST**.

### 2. **Category-based Recommendations**:
   - Provides recommendations of tools from a specific category.
   - Example: You can ask for tools in the **Genomics** category.

### 3. **Keyword-based Search**:
   - Provides recommendations based on a search keyword.
   - Example: Searching for tools related to **RNA**.

---

## Example Commands

Here are some examples of how you can use **LabMate** from the command line:

### 1. Get Recommendations Based on a Tool

\`\`\`bash
python cli.py --tool "FastQC" --num 3
\`\`\`

This command will recommend 3 tools that are similar to **FastQC**.

### 2. Get Recommendations for a Category

\`\`\`bash
python cli.py --category "Genomics"
\`\`\`

This command will recommend all the tools available in the **Genomics** category.

### 3. Search for Tools Using a Keyword

\`\`\`bash
python cli.py --search "RNA"
\`\`\`

This command will search for tools related to **RNA** and display relevant recommendations.

### 4. Display Help Message

\`\`\`bash
python cli.py --help
\`\`\`

This command will display the help message listing all available commands and options.

---

## Running Tests

The **LabMate** system includes several unit tests to ensure everything works as expected. You can run these tests using the \`unittest\` or \`pytest\` frameworks.

### 1. Running All Tests with \`unittest\`

\`\`\`bash
python -m unittest discover -s tests
\`\`\`

### 2. Running Tests with \`pytest\`

If you're using \`pytest\`, run the following:

\`\`\`bash
pytest tests/
\`\`\`

This will run all the test files inside the \`tests/\` directory.

---

## Development

If you want to contribute to the development of **LabMate** or modify the system, here's a brief guide on the main components:

### 1. **Recommender**:
   - Located in \`recommender.py\`. This module handles tool recommendations, whether they are based on similarity, category, or keyword search.

### 2. **Queue**:
   - Located in \`queue.py\`. This module handles request queue management, ensuring that multiple user inputs are processed in sequence.

### 3. **CLI**:
   - Located in \`cli.py\`. This module handles the command-line interface, parsing user inputs and sending requests to the core system.

### 4. **Core**:
   - Located in \`core.py\`. The central orchestrator that connects the CLI, queue, and recommender to ensure smooth functioning of the system.

### 5. **Tree and Graph**:
   - Located in \`tree.py\` and \`graph.py\`. These modules handle the hierarchical (tree) and relational (graph) structures for managing tool relationships and categories.

---

## Contact Information

If you encounter any issues or have questions, feel free to contact me at:

- **GitHub**: [github.com/RLTree/LabMate](https://github.com/RLTree/LabMate)

---

Thank you for using **LabMate**! Happy researching!
