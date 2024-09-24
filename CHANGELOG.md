# CHANGELOG.md

# LabMateAI Changelog

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2024-09-23

### Added

- **Initial Release of LabMateAI**: Renamed the project from LabMate to LabMateAI.
- **AI-Powered Recommendation System**: Implemented an AI-powered system for recommending laboratory tools and software.
- **Command-Line Interface (CLI)**: Introduced an interactive CLI for user-friendly interaction.
- **Features**:
  - **Tool Similarity Recommendations**: Find tools similar to a specified tool.
  - **Category-Based Recommendations**: Discover tools within a specific scientific category.
  - **Keyword-Based Search**: Search for tools based on keywords related to research.
- **Documentation**:
  - Updated `README.md` with installation and usage instructions.
  - Created `CONTRIBUTING.md` for guidelines on how to contribute.
  - Added `CODE_OF_CONDUCT.md` to establish community standards.
  - Updated `API.md` with detailed API documentation.
  - Updated `INSTALLATION.md` with new installation instructions.
  - Created `USAGE_GUIDE.md` to help users navigate the application.
- **Testing**:
  - Updated and expanded the test suite using `pytest`.
  - Ensured all tests pass after package renaming and updates.

### Changed

- **Package Renaming**: Changed the package name from `labmate` to `labmateai`.
  - Updated all module imports and references to reflect the new package name.
  - Adjusted the directory structure to use `labmateai` as the root package directory.
- **Setup Configuration**:
  - Updated `setup.py` with the new package name and metadata.
  - Adjusted the console script entry point to `labmateai`.
- **Documentation Updates**:
  - Revised all documentation files to replace references to LabMate with LabMateAI.
  - Updated code examples and command-line instructions in documentation.

### Fixed

- **Import Errors**: Resolved `ModuleNotFoundError` issues due to incorrect import statements.
  - Changed absolute imports to relative imports within the package modules.
  - Ensured all test files correctly import modules from `labmateai`.
- **Test Failures**: Fixed failing tests caused by package renaming and import errors.
  - Updated test cases to align with the new package structure.
  - Verified that all tests pass successfully.

---

## [0.1.0] - 2024-09-22

### Added

- **Initial Development Release as LabMate**: Laid the groundwork for the recommendation system.
  - Implemented basic CLI functionality.
  - Developed core classes: `Graph`, `Tree`, `Recommender`, and `CLI`.
  - Created initial test suite.

---

*Note*: Replace `YYYY-MM-DD` with the actual dates of the releases.
