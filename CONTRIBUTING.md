
# Contributing to LabMateAI

Thank you for your interest in contributing to **LabMateAI**! We welcome contributions from the community to help improve and expand this project. Whether you're fixing bugs, adding new features, improving documentation, or suggesting enhancements, your input is valuable.

---

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Fork the Repository](#fork-the-repository)
  - [Clone Your Fork](#clone-your-fork)
  - [Set Up the Development Environment](#set-up-the-development-environment)
  - [Setting Up Upstream Remote](#setting-up-upstream-remote)
- [Development Guidelines](#development-guidelines)
  - [Branch Naming Convention](#branch-naming-convention)
  - [Coding Standards](#coding-standards)
  - [Commit Messages](#commit-messages)
  - [Testing](#testing)
  - [Code Review Guidelines](#code-review-guidelines)
- [Submitting Your Contribution](#submitting-your-contribution)
  - [Pull Request Process](#pull-request-process)
  - [Issue Reporting Guidelines](#issue-reporting-guidelines)
- [Code of Conduct](#code-of-conduct)
- [Contact](#contact)
- [Local Development and Debugging Tips](#local-development-and-debugging-tips)
- [Linking to Documentation](#linking-to-documentation)
- [Screenshots or GIFs (Optional)](#screenshots-or-gifs-optional)

---

## Getting Started

### Prerequisites

Before contributing, ensure you have the following installed on your local machine:

- **Python 3.6+**: [Download Python](https://www.python.org/downloads/)
- **Git**: [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- **GitHub Account**: [Sign up for GitHub](https://github.com/signup)

### Fork the Repository

1. Navigate to the [LabMateAI repository](https://github.com/yourusername/LabMateAI) on GitHub.
2. Click the **Fork** button in the upper right corner to create your own copy of the repository.

### Clone Your Fork

Clone your forked repository to your local machine:

```bash
git clone https://github.com/yourusername/LabMateAI.git
cd LabMateAI
```

*Replace `yourusername` with your GitHub username.*

### Set Up the Development Environment

It's recommended to use a virtual environment to manage dependencies:

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

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Setting Up Upstream Remote

After cloning your forked repository, set the original repository as the upstream remote:

```bash
git remote add upstream https://github.com/yourusername/LabMateAI.git
```

Verify the new upstream repository you've specified for your fork:

```bash
git remote -v
```

**Expected Output:**

```
origin    https://github.com/yourusername/LabMateAI.git (fetch)
origin    https://github.com/yourusername/LabMateAI.git (push)
upstream  https://github.com/yourusername/LabMateAI.git (fetch)
upstream  https://github.com/yourusername/LabMateAI.git (push)
```

---

## Development Guidelines

### Branch Naming Convention

Create a new branch for your work:

```bash
git checkout -b feature/short-description
```

- Use `feature/` prefix for new features.
- Use `bugfix/` prefix for bug fixes.
- Use `docs/` prefix for documentation improvements.

**Example:**

- `feature/add-new-recommendation-algorithm`
- `bugfix/fix-cli-error`
- `docs/update-readme`

### Coding Standards

- **Language**: Python 3.6+
- **Style Guide**: Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code style.
- **Formatting**: Use tools like `flake8` and `black` to ensure consistent formatting.
- **Comments**: Write clear and concise comments where necessary.
- **Docstrings**: Use [Google Style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) for docstrings.

### Commit Messages

- Write clear and descriptive commit messages.
- Use the present tense (e.g., "Add feature" not "Added feature").
- Begin with a capital letter and do not end with a period.

**Example:**

```bash
git commit -m "Fix issue with tool recommendation loop"
```

### Testing

- Write unit tests for new features and bug fixes.
- Use the `pytest` framework for testing.
- Ensure all tests pass before submitting a pull request.

**Running tests:**

```bash
pytest tests/
```

### Code Review Guidelines

- **Be Respectful**: Provide constructive feedback and avoid personal criticisms.
- **Be Clear**: Clearly explain the reasoning behind your suggestions.
- **Be Open**: Be open to feedback and willing to make necessary changes.
- **Be Timely**: Respond to review comments promptly to keep the contribution process smooth.

---

## Submitting Your Contribution

### Pull Request Process

1. **Ensure your changes are up-to-date** with the main repository:

    ```bash
    git fetch upstream
    git checkout main
    git merge upstream/main
    ```

2. **Push your branch** to your forked repository:

    ```bash
    git push origin feature/your-feature-name
    ```

3. **Create a Pull Request**:

    - Go to your forked repository on GitHub.
    - Click on the **Compare & pull request** button.
    - Provide a clear and descriptive title for your pull request.
    - In the description, explain the changes you've made and why they're necessary.
    - Reference any related issues using `#issue_number`.

4. **Address Review Comments**:

    - Be responsive to feedback.
    - Make necessary changes and push them to your branch.
    - The pull request will automatically update.

5. **Merge Approval**:

    - Once your pull request is approved, it will be merged into the main branch.

### Issue Reporting Guidelines

If you encounter any issues or have suggestions for improvements, please open an issue in the [LabMateAI repository](https://github.com/yourusername/LabMateAI/issues). When reporting an issue, please provide the following information:

- **Title**: A clear and descriptive title.
- **Description**: Detailed information about the issue or suggestion.
- **Steps to Reproduce**: If applicable, provide step-by-step instructions to reproduce the issue.
- **Expected Behavior**: Describe what you expected to happen.
- **Actual Behavior**: Describe what actually happened.
- **Screenshots**: If applicable, add screenshots to help explain your problem.

---

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by its terms.

---

## Contact

If you have any questions or need assistance, feel free to reach out:

- **Email**: [support@labmateai.io](mailto:support@labmateai.io)
- **GitHub Issues**: Open an issue on the [LabMateAI repository](https://github.com/yourusername/LabMateAI/issues).

---

## Local Development and Debugging Tips

- **Running the CLI**: After setting up the environment, you can run the CLI using:

    ```bash
    python labmateai/cli.py
    ```

- **Logging**: Utilize the logging functionality to debug issues. Logs can be found in the console output during CLI operations.
- **Database Setup**: Ensure your `.env` file is correctly configured with your local database credentials.

---

## Linking to Documentation

Ensure that all links are functional and point to the correct resources within your repository or external sites.

- **[PEP 8](https://www.python.org/dev/peps/pep-0008/)**: Python's style guide.
- **[Google Style Docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)**: Guidelines for writing docstrings.
- **[LabMateAI Repository](https://github.com/yourusername/LabMateAI)**: Main repository link.

---

## Screenshots or GIFs (Optional)

If applicable, include screenshots or GIFs to visually guide contributors through certain processes.

### Example Screenshot

![CLI Example](path/to/cli-example.png)

*Figure 1: Example of the LabMateAI CLI in action.*

---

**Thank you for contributing to LabMateAI! Your efforts help advance scientific research by making tool discovery more accessible.**
