# SAGE API Reference

This document provides an overview of the RESTful API for SAGE, a platform designed to manage and generate documentation for repositories.

## Root Endpoint

### GET /

**Description:** Returns basic information about the SAGE service.

**Response:**
```json
{
  "name": "SAGE",
  "version": "0.1.0",
  "docs": "/docs"
}
```

## Authentication Endpoints

### GET /login

**Description:** Initiates the OAuth login process with GitHub.

**Response:**
- Redirects to the GitHub authorization page.

### GET /callback

**Description:** Handles the callback from GitHub after user authentication.

**Request Parameters:**
- `code`: The authorization code provided by GitHub.
- `state`: A state parameter used for security purposes.

**Response:**
- Redirects to `/auth/me` upon successful authentication.

### GET /logout

**Description:** Logs out the current user and clears the session.

**Response:**
```json
{
  "status": "logged_out"
}
```

## User Endpoints

### GET /repos/github

**Description:** Lists GitHub repositories for the authenticated user.

**Response:**
- An array of repository objects.

### GET /auth/me

**Description:** Returns information about the currently authenticated user.

**Response:**
- User information object.

## Repository Management and Documentation Generation Endpoints

### POST /{owner}/{name}/generate/readme

**Description:** Generates a README file for the specified repository.

**Request Parameters:**
- `owner`: The owner of the repository.
- `name`: The name of the repository.

**Response:**
- A success message or an error if the repository is not connected.

### POST /{owner}/{name}/generate/modules

**Description:** Generates documentation for modules in the specified repository.

**Request Parameters:**
- `owner`: The owner of the repository.
- `name`: The name of the repository.

**Response:**
- A success message or an error if the repository is not connected.

### POST /{owner}/{name}/generate/api-docs

**Description:** Generates API documentation for the specified repository.

**Request Parameters:**
- `owner`: The owner of the repository.
- `name`: The name of the repository.

**Response:**
- A success message or an error if the repository is not connected.

### POST /{owner}/{name}/generate/architecture

**Description:** Generates an architecture diagram for the specified repository.

**Request Parameters:**
- `owner`: The owner of the repository.
- `name`: The name of the repository.

**Response:**
- A success message or an error if the repository is not connected.

### GET /{owner}/{name}/runs

**Description:** Lists documentation generation runs for the specified repository.

**Request Parameters:**
- `owner`: The owner of the repository.
- `name`: The name of the repository.

**Response:**
- An array of documentation run objects.

### POST /connect

**Description:** Connects a repository to SAGE.

**Response:**
- A success message or an error if the connection fails.

## Route Reference

| Method | Path | Handler | Location |
|---|---|---|---|
| `GET` | `/` | root | `apps/backend/sage/app.py:53` |
| `GET` | `/auth/me` | me | `apps/backend/sage/api/routes_users.py:18` |
| `GET` | `/callback` | callback | `apps/backend/sage/api/routes_auth.py:25` |
| `POST` | `/connect` | connect_repo | `apps/backend/sage/api/routes_repos.py:27` |
| `GET` | `/health` | health | `apps/backend/sage/api/routes_health.py:18` |
| `GET` | `/live` | liveness | `apps/backend/sage/api/routes_health.py:12` |
| `GET` | `/login` | login | `apps/backend/sage/api/routes_auth.py:18` |
| `GET` | `/logout` | logout | `apps/backend/sage/api/routes_auth.py:47` |
| `GET` | `/repos/github` | list_github_repos | `apps/backend/sage/api/routes_users.py:27` |
| `POST` | `/{owner}/{name}/generate/api-docs` | generate_api_docs_for_repo | `apps/backend/sage/api/routes_docs.py:150` |
| `POST` | `/{owner}/{name}/generate/architecture` | generate_architecture_diagram | `apps/backend/sage/api/routes_docs.py:208` |
| `POST` | `/{owner}/{name}/generate/modules` | generate_module_docs_for_repo | `apps/backend/sage/api/routes_docs.py:84` |
| `POST` | `/{owner}/{name}/generate/readme` | generate_readme_for_repo | `apps/backend/sage/api/routes_docs.py:26` |
| `GET` | `/{owner}/{name}/runs` | list_doc_runs | `apps/backend/sage/api/routes_docs.py:258` |
| `GET` | `/{owner}/{name}/search` | search_repo_chunks | `apps/backend/sage/api/routes_repos.py:74` |
