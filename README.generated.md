# SAGE

SAGE is an open-source platform for automatically generating and maintaining documentation for software projects. It leverages machine learning models to understand code and generate comprehensive documentation, including READMEs, API docs, and architecture diagrams.

## Features

- **Automated Documentation Generation**: SAGE can automatically generate documentation for your codebase.
- **GitHub Integration**: Connect your GitHub repositories to SAGE for real-time documentation updates.
- **Machine Learning Models**: Utilizes advanced machine learning models to understand and document code effectively.
- **Web-based UI**: Access the platform through a web interface for easy management and monitoring.

## Installation

To install SAGE, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/lakshit2234/SAGE.git
   ```

2. Navigate to the project directory:
   ```sh
   cd SAGE
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Set up environment variables by creating a `.env` file in the root directory and adding the necessary configuration.

## Usage

To start using SAGE, follow these steps:

1. Run the application:
   ```sh
   uvicorn apps.backend.sage:app --reload
   ```

2. Access the web interface at `http://localhost:8000/docs` to interact with the API and manage your repositories.

## Project Structure

The project is structured as follows:

- **apps/backend**: Contains the main application code.
  - **migrations**: Database migration scripts.
  - **sage**: Main application module.
    - **api**: Routes for different functionalities (auth, docs, health, repos, users).
    - **core**: Core configuration and utilities.
      - **config.py**: Application settings.
      - **logging.py**: Logging configuration.
    - **db**: Database models and base classes.
      - **base.py**: Base class for all ORM models.
      - **models.py**: Models representing database tables.
    - **schemas**: Pydantic schemas for data validation.
      - **repository.py**: Schemas related to repositories.
    - **services**: Business logic services.
      - Various service modules for different functionalities.
    - **workers**: Background tasks and workers.
  - **tests**: Test suite.

This structure ensures a clean separation of concerns, making the codebase easy to maintain and extend.