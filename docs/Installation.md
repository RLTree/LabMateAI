# Installation Guide for LabMateAI

Welcome to the installation guide for **LabMateAI**, an AI-powered scientific tool recommendation system designed to help researchers discover relevant software for their needs. Follow the steps below to install and set up LabMateAI on your machine.

---

## Prerequisites

Before installing LabMateAI, make sure you have the following software installed:

1. **Python 3.6 or higher**:
   - You can download and install Python from [python.org](https://www.python.org/downloads/).

2. **pip** (Python package manager):
   - `pip` is usually installed automatically with Python. To check if you have `pip` installed, run the following in your terminal:
     ```bash
     pip --version
     ```
   - If you don’t have `pip` installed, you can follow the installation instructions [here](https://pip.pypa.io/en/stable/installation/).

---

## Installation Steps

### 1. Install LabMateAI via pip

You can install LabMateAI directly from PyPI using `pip`:

```bash
pip install labmateai
```

This command will download and install LabMateAI along with all necessary dependencies.

### 2. Verify the Installation

After installation, you can verify that LabMateAI is installed by checking its version:

```bash
labmateai --version
```

---

## Running LabMateAI

Once the installation is complete, you can start using **LabMateAI**.

### Launching the CLI

To run the LabMateAI command-line interface (CLI), simply enter:

```bash
labmateai
```

This will launch the CLI, allowing you to interact with the LabMateAI recommendation system. You can search for tools, get recommendations, and more.

---

## Optional: Set Up a Virtual Environment

While not required, it's recommended to use a virtual environment to manage dependencies for your projects. This can help avoid conflicts between packages used in different projects.

### Create and Activate a Virtual Environment

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

After activating the virtual environment, install LabMateAI as described above:

```bash
pip install labmateai
```

---

## Uninstalling LabMateAI

To uninstall LabMateAI, run the following command:

```bash
pip uninstall labmateai
```

If you created a virtual environment, you can simply deactivate and delete the environment to remove all related dependencies.

---

## Additional Resources

- For detailed usage instructions, refer to the [Usage Guide](usage_guide.md).
- For more advanced topics, visit the [LabMateAI Documentation](docs/README.md).
- If you encounter any issues, check the [FAQ](faq.md) or open an issue on the [GitHub repository](https://github.com/yourusername/LabMateAI/issues).

---

## Troubleshooting

If you encounter any problems during installation or running LabMateAI, consider the following:

- **Ensure Python and pip are correctly installed**: Verify their versions using `python --version` and `pip --version`.
- **Check your internet connection**: A stable internet connection is required to download packages.
- **Update pip**: Make sure you have the latest version of pip:
  ```bash
  pip install --upgrade pip
  ```
- **Permissions**: If you encounter permission issues, you may need to run the install command with `--user` or use a virtual environment.

---

## Contact Support

If you're still experiencing issues, please reach out:

- **Email**: [support@labmateai.io](mailto:tnoblin@health.ucsd.edu)
- **GitHub Issues**: Open an issue on the [LabMateAI repository](https://github.com/RLTree/LabMateAI/issues).
