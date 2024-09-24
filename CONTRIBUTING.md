# Contributing to LabMateAI

Thank you for your interest in contributing to **LabMateAI**! We welcome contributions from the community to help improve and expand this project. Whether you're fixing bugs, adding new features, improving documentation, or suggesting enhancements, your input is valuable.

---

## Table of Contents

- [Getting Started](#getting-started)
  - [Fork the Repository](#fork-the-repository)
  - [Clone Your Fork](#clone-your-fork)
  - [Set Up the Development Environment](#set-up-the-development-environment)
- [Development Guidelines](#development-guidelines)
  - [Branch Naming Convention](#branch-naming-convention)
  - [Coding Standards](#coding-standards)
  - [Commit Messages](#commit-messages)
  - [Testing](#testing)
- [Submitting Your Contribution](#submitting-your-contribution)
  - [Pull Request Process](#pull-request-process)
- [Code of Conduct](#code-of-conduct)
- [Contact](#contact)

---

## Getting Started

### Fork the Repository

1. Navigate to the [LabMateAI repository](https://github.com/yourusername/LabMateAI) on GitHub.
2. Click the **Fork** button in the upper right corner to create your own copy of the repository.

### Clone Your Fork

Clone your forked repository to your local machine:

```bash
git clone https://github.com/yourusername/LabMateAI.git
cd LabMateAI
```

Replace `yourusername` with your GitHub username.

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

Example:

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

Example:

```bash
git commit -m "Fix issue with tool recommendation loop"
```

### Testing

- Write unit tests for new features and bug fixes.
- Use the `pytest` framework for testing.
- Ensure all tests pass before submitting a pull request.

Running tests:

```bash
pytest tests/
```

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

---

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by its terms.

---

## Contact

If you have any questions or need assistance, feel free to reach out:

- **Email**: [support@labmateai.io](mailto:support@labmateai.io)
- **GitHub Issues**: Open an issue on the [LabMateAI repository](https://github.com/yourusername/LabMateAI/issues).

---

**Thank you for contributing to LabMateAI! Your efforts help advance scientific research by making tool discovery more accessible.**