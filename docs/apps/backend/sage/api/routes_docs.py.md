### Purpose Summary

The `routes_docs.py` module in the Sage backend provides FastAPI routes for triggering documentation generation for connected repositories. It handles generating READMEs, module-level documentation, API documentation, and architecture diagrams. Each route interacts with a database session to track the status of documentation runs and store generated artifacts.

### Key Functions/Classes

| Function/Class | Description |
|----------------|-------------|
| `generate_readme_for_repo` | Triggers the generation of a README for a repository. |
| `generate_module_docs_for_repo` | Triggers the generation of module-level documentation for a repository. |
| `generate_api_docs_for_repo` | Triggers the generation of API documentation for a repository. |
| `generate_architecture_diagram` | Triggers the generation of an architecture diagram for a repository. |

### Notable Dependencies and Side Effects

- **Dependencies**: The routes depend on various services such as `chunk_repository`, `generate_readme`, `generate_module_docs`, `generate_api_docs`, and `render_module_graph`. These services handle the actual documentation generation logic.
  
- **Database Interaction**: Each route interacts with an asynchronous SQLAlchemy session to create, update, and retrieve `DocRun` and `DocArtifact` records. This ensures that the status of each documentation run and the generated artifacts are persisted.

- **Error Handling**: The routes include comprehensive error handling to manage exceptions during documentation generation. If an exception occurs, it updates the `DocRun` record with a failure status and logs the error.

- **Logging**: Each route logs important events using Sage's logging system, providing insights into the progress and outcomes of documentation runs.