# SAGE

SAGE is an open-source platform designed to automate documentation generation and management for software repositories. It leverages machine learning models and vector embeddings to provide intelligent insights and documentation.

## Description

SAGE automates the process of generating, maintaining, and querying documentation for software projects. It supports multiple types of artifacts such as READMEs, module docs, API docs, and architecture diagrams. The platform uses GitHub webhooks to trigger documentation generation on code changes and provides a RESTful API for interacting with its features.

## Features

- **Automated Documentation Generation**: SAGE automatically generates documentation based on the code in your repositories.
- **Semantic Search**: Perform semantic search over repository chunks using vector embeddings.
- **GitHub Integration**: Connect and manage GitHub repositories directly from the platform.
- **RESTful API**: Interact with SAGE's features via a comprehensive RESTful API.

## Installation

To install SAGE, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/lakshit2234/SAGE.git
   cd SAGE
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Set up environment variables by creating a `.env` file in the root directory and adding the necessary configuration.

## Usage

### Connecting a Repository

To connect a GitHub repository to SAGE, use the following API endpoint:

```http
POST /api/repos/connect
Content-Type: application/json

{
  "owner": "your-github-username",
  "name": "your-repository-name"
}
```

### Generating Documentation

Trigger documentation generation for a specific repository using its ID:

```http
POST /api/repos/{repo_id}/doc_runs
```

### Querying Semantic Search

Perform semantic search over a repository's chunks:

```http
GET /api/repos/{owner}/{name}/search?query_text=your-query-text
```

## Project Structure

The project is structured as follows:

- `apps/backend/migrations/`: Contains database migration scripts.
- `apps/backend/sage/`: Main application code.
  - `app.py`: Entry point of the application.
  - `api/`: Contains API routes for different functionalities.
    - `routes_auth.py`, `routes_docs.py`, etc.: Specific route files.
  - `core/`: Core utilities and configuration.
    - `config.py`: Configuration settings.
    - `logging.py`: Logging utilities.
  - `db/`: Database models and base classes.
    - `base.py`: Base class for all ORM models.
    - `models.py`: Various database models.
  - `schemas/`: Pydantic schemas for data validation.
    - `repository.py`: Schemas related to repositories.
  - `services/`: Business logic services.
    - `api_doc_generator.py`, `api_extractor.py`, etc.: Specific service files.
  - `workers/`: Background tasks and Celery app.
    - `celery_app.py`, `tasks.py`: Celery configuration and task definitions.

This README provides a comprehensive overview of SAGE, its features, installation steps, and usage instructions.