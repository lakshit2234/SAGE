# SAGE

SAGE is an open-source platform designed to automate documentation generation for software repositories using machine learning and natural language processing techniques.

## Description

SAGE provides a comprehensive solution for generating, maintaining, and managing documentation for codebases. It leverages GitHub webhooks, machine learning models, and vector embeddings to automatically update documentation in real-time as changes are made to the repository. Key features include:

- **Automated Documentation Generation**: SAGE can generate READMEs, API docs, module docs, and architecture diagrams based on the codebase.
- **Real-Time Updates**: Documentation is updated automatically whenever changes are pushed to the repository via GitHub webhooks.
- **Machine Learning Models**: Utilizes advanced machine learning models for generating documentation and understanding code structure.
- **Vector Embeddings**: Employs vector embeddings for semantic search and similarity queries within the documentation.

## Features

- **Repository Management**: Connect, manage, and track repositories using SAGE's API.
- **Documentation Generation**: Automatically generate various types of documentation (READMEs, API docs, module docs) based on code changes.
- **Real-Time Updates**: Real-time updates to documentation triggered by GitHub webhooks.
- **Machine Learning Models**: Utilize machine learning models for enhanced documentation generation and understanding.
- **Vector Embeddings**: Perform semantic search and similarity queries within the generated documentation.

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

3. Install dependencies using pip:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

### Configuration

Before running SAGE, you need to configure it by setting up environment variables in a `.env` file located at the root of your project. Here is an example configuration:

```env
APP_ENV=dev
APP_HOST=0.0.0.0
APP_PORT=8000
LOG_LEVEL=INFO

POSTGRES_USER=sage
POSTGRES_PASSWORD=sage_dev_pw
POSTGRES_DB=sage
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

REDIS_URL=redis://localhost:6379/0

OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_LLM_MODEL=qwen2.5-coder:7b
OLLAMA_EMBED_MODEL=nomic-embed-text

CHROMA_PATH=./data/chroma

REPOS_DIR=./workspace/repos

GITHUB_OAUTH_CLIENT_ID=
GITHUB_OAUTH_CLIENT_SECRET=
GITHUB_OAUTH_CALLBACK_URL=http://localhost:8000/auth/github/callback

SESSION_SECRET=dev-only-change-me

GITHUB_WEBHOOK_SECRET=
```

### Running SAGE

To start the SAGE application, run:

```sh
python -m sage
```

This will start the SAGE server on `http://localhost:8000`.

### API Endpoints

SAGE provides a RESTful API for managing repositories and generating documentation. Below are some example endpoints:

- **Connect a Repository**:
  ```sh
  curl -X POST "http://localhost:8000/api/repos/connect" \
       -H "Content-Type: application/json" \
       -d '{"owner": "your_owner", "name": "your_repo", "default_branch": "main"}'
  ```

- **Get Repository Information**:
  ```sh
  curl -X GET "http://localhost:8000/api/repos/{repo_id}"
  ```

- **Trigger Documentation Generation**:
  ```sh
  curl -X POST "http://localhost:8000/api/repos/{repo_id}/doc_runs"
  ```

### Example Workflow

1. Connect a repository using the `/api/repos/connect` endpoint.
2. Trigger documentation generation for the connected repository using the `/api/repos/{repo_id}/doc_runs` endpoint.
3. Retrieve generated documentation using the `/api/repos/{repo_id}` endpoint.

## Project Structure

The project structure is organized as follows:

```
apps/backend/
├── migrations/
│   ├── env.py
│   └── versions/
│       ├── a2c4c225b2d9_init_repositories_doc_runs_doc_.py
│       └── f97d64bed461_add_github_access_token_to_repositories.py
├── sage/
│   ├── app.py
│   ├── __init__.py
│   ├── __main__.py
│   ├── api/
│   │   ├── routes_auth.py
│   │   ├── routes_docs.py
│   │   ├── routes_health.py
│   │   ├── routes_repos.py
│   │   ├── routes_users.py
│   │   ├── routes_webhooks.py
│   │   └── __init__.py
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── __init__.py
│   ├── db/
│   │   ├── base.py
│   │   ├── models.py
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── repository.py
│   │   └── __init__.py
│   ├── services/
│   │   ├── api_doc_generator.py
│   │   ├── api_extractor.py
│   │   ├── chunker.py
│   │   ├── dependency_graph.py
│   │   ├── doc_generator.py
│   │   ├── embeddings.py
│   │   ├── github_auth.py
│   │   ├── git_ops.py
│   │   ├── health.py
│   │   ├── llm.py
│   │   ├── mermaid_renderer.py
│   │   ├── module_docs.py
│   │   ├── pipeline.py
│   │   ├── prompts.py
│   │   └── vector_store.py
│   │   └── __init__.py
│   └── workers/
│       ├── celery_app.py
│       ├── tasks.py
│       └── __init__.py
```

This structure allows for a clean separation of concerns, making the codebase easy to navigate and maintain.