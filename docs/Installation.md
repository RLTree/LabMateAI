
# Installation Guide for LabMate

Welcome to the installation guide for **LabMate**, a scientific tool recommendation system designed to help researchers discover relevant software for their needs. Follow the steps below to install and set up LabMate on your machine.

---

## Prerequisites

Before installing LabMate, make sure you have the following software installed:

1. **Python 3.6+**:
   - You can download and install Python from [python.org](https://www.python.org/downloads/).

2. **pip** (Python package manager):
   - pip is usually installed automatically with Python. To check if you have pip installed, run the following in your terminal:
     ```bash
     pip --version
     ```
   - If you don’t have pip installed, you can follow the installation instructions [here](https://pip.pypa.io/en/stable/installation/).

---

## Step-by-Step Installation

### 1. Clone the Repository

To get started, clone the LabMate repository to your local machine:

```bash
git clone https://github.com/your-repo/labmate.git
```

Navigate to the cloned repository directory:

```bash
cd labmate
```

### 2. Set Up a Virtual Environment (Optional but Recommended)

It's recommended to use a virtual environment to manage dependencies for your project. You can create and activate a virtual environment using the following commands:

#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

After setting up the virtual environment, install the required dependencies listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

This will install all necessary libraries and dependencies for LabMate to run properly.

---

## Running LabMate

Once the installation is complete, you can start using **LabMate**.

### 1. Running the CLI

To run the LabMate command-line interface (CLI), use the following command:

```bash
python cli.py
```

This will launch the CLI, allowing you to interact with the LabMate recommendation system. You can search for tools, get recommendations, and more.

---

## Uninstalling LabMate

To uninstall LabMate and remove all its dependencies, run the following command:

```bash
pip uninstall -r requirements.txt
```

If you created a virtual environment, you can simply deactivate and delete the environment to remove all related dependencies.

---

## Additional Resources

- For detailed usage instructions, refer to the [Usage Guide](usage_guide.md).
- For more advanced topics, visit the [LabMate Documentation](docs/README.md).

---

This installation guide should help you get LabMate up and running smoothly. If you encounter any issues, feel free to [reach out](mailto:support@labmate.io) for support.
