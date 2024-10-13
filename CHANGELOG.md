
# CHANGELOG.md

# LabMateAI Changelog

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2024-10-11

### Added

- **Database Integration**:  
  Integrated **SQLAlchemy ORM** to manage interactions with the Heroku PostgreSQL database (`labmateai-db`), enhancing data handling and scalability.

- **Alembic Migrations**:  
  Implemented **Alembic** for seamless database schema migrations, ensuring consistent database structures across different environments.

- **Enhanced CLI Functionality**:  
  Updated the **Command-Line Interface (CLI)** to automatically prompt users to rate recommended tools immediately after receiving recommendations, improving user engagement and feedback collection.

- **Automated Interaction Logging**:  
  Configured the CLI to automatically log all interaction data (`interaction_id`, `user_id`, `tool_id`, `rating`, `usage_frequency`, `timestamp`) into the `interactions` table, ensuring comprehensive tracking of user interactions.

- **Continuous Integration (CI) Enhancements**:  
  Updated `.travis.yml` to include **PostgreSQL** service, run migrations before tests, and handle secure environment variables, thereby streamlining the CI pipeline.

- **Improved Testing Setup**:  
  Enhanced the test suite to include database integration tests, ensuring that all interactions are properly logged and that the system behaves as expected under various scenarios.

- **Deployment Enhancements**:  
  Improved deployment configurations for secure and reliable **PyPI** deployments, facilitating smoother releases and updates.

- **Documentation Updates**:  
  Updated `README.md` and other documentation files to reflect the latest changes, providing clear setup and usage instructions for users and contributors.

### Changed

- **Project Structure Refactoring**:  
  Refactored project directories to support ORM models, migrations, and improved code organization, enhancing maintainability and scalability.

- **CLI Workflow Modification**:  
  Modified the CLI workflow to remove the separate rating option and integrate rating prompts directly after recommendations, resulting in a more intuitive user experience.

- **Configuration Management Enhancements**:  
  Enhanced configuration files (`alembic.ini`, `.travis.yml`, `.env`) to support secure and efficient CI/CD pipelines, ensuring better security and performance.

### Fixed

- **Naming Conflicts Resolved**:  
  Resolved naming conflicts between the ORM `ToolModel` and custom `Tool` classes by using aliases (`ToolModel` for ORM and `CustomTool` for the custom class), preventing import and reference issues.

- **Import Errors Fixed**:  
  Fixed `ModuleNotFoundError` issues by adjusting import statements and ensuring proper package structure, ensuring that all modules are correctly accessible.

- **Test Failures Addressed**:  
  Fixed failing tests caused by package renaming and import errors, ensuring that all tests pass successfully and maintain high code quality standards.

---

## [1.0.0] - 2024-09-23

### Added

- **Initial Release of LabMateAI**:  
  Renamed the project from **LabMate** to **LabMateAI** and launched the first version.

- **AI-Powered Recommendation System**:  
  Implemented an **AI-powered system** for recommending laboratory tools and software, leveraging advanced algorithms to provide accurate and relevant suggestions.

- **Command-Line Interface (CLI)**:  
  Introduced an interactive **CLI** for user-friendly interaction, allowing users to navigate and utilize the recommendation features efficiently.

- **Features**:
  - **Tool Similarity Recommendations**:  
    Find tools similar to a specified tool, enabling users to discover alternatives and related solutions.
  
  - **Category-Based Recommendations**:  
    Discover tools within a specific scientific category, assisting users in finding relevant tools tailored to their field.
  
  - **Keyword-Based Search**:  
    Search for tools based on keywords related to research, facilitating quick and targeted tool discovery.

- **Documentation**:
  - Updated `README.md` with comprehensive installation and usage instructions.
  - Created `CONTRIBUTING.md` outlining guidelines for contributing to the project.
  - Added `CODE_OF_CONDUCT.md` to establish community standards and ensure a welcoming environment.
  - Updated `API.md` with detailed API documentation for developers.
  - Updated `INSTALLATION.md` with new installation instructions tailored to the updated project structure.
  - Created `USAGE_GUIDE.md` to help users navigate and utilize the application effectively.

- **Testing**:
  - Updated and expanded the **test suite** using `pytest`, covering all major functionalities.
  - Ensured all tests pass after package renaming and structural updates, maintaining high code quality and reliability.

### Changed

- **Package Renaming**:  
  Changed the package name from `labmate` to `labmateai`, reflecting the integration of AI-powered features.
  - Updated all module imports and references to align with the new package name.
  - Adjusted the directory structure to use `labmateai` as the root package directory.

- **Setup Configuration**:
  - Updated `setup.py` with the new package name and metadata, ensuring correct packaging and distribution.
  - Adjusted the console script entry point to `labmateai`, facilitating seamless CLI access.

- **Documentation Updates**:
  - Revised all documentation files to replace references to **LabMate** with **LabMateAI**, maintaining consistency across all materials.
  - Updated code examples and command-line instructions in documentation to reflect the new package structure and functionalities.

### Fixed

- **Import Errors**:  
  Resolved `ModuleNotFoundError` issues due to incorrect import statements by changing absolute imports to relative imports within package modules.

- **Test Failures**:  
  Fixed failing tests caused by package renaming and import errors by updating test cases to align with the new package structure, ensuring all tests pass successfully.

---

## [0.1.0] - 2024-09-22

### Added

- **Initial Development Release as LabMate**:  
  Laid the groundwork for the recommendation system under the original project name **LabMate**.
  - Implemented basic **CLI** functionality, allowing initial user interactions.
  - Developed core classes: `Graph`, `Tree`, `Recommender`, and `CLI`, forming the foundation of the recommendation system.
  - Created an initial **test suite** to ensure basic functionalities operate as expected.

---

*Note*: Replace `YYYY-MM-DD` with the actual dates of the releases.

