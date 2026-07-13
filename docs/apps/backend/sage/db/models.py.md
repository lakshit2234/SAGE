### Purpose Summary

The `sage/db/models.py` file defines the core ORM models for the SAGE backend application. These models represent entities such as repositories, documentation runs, artifacts, and commit events, which are essential for managing and tracking documentation generation processes within a repository.

### Key Functions/Classes

| Class/Function | Description |
|----------------|-------------|
| `DocRunStatus` | An enumeration representing the possible statuses of a documentation run (e.g., pending, running, success, failed). |
| `ArtifactType` | An enumeration defining different types of artifacts that can be generated (e.g., README, module doc, API doc). |
| `Repository` | Represents a software repository and includes details like owner, name, default branch, and associated documentation runs. |
| `DocRun` | Represents a single documentation-generation pass triggered manually or by a commit, including its status, artifacts, and error messages. |
| `DocArtifact` | Represents a specific generated artifact (e.g., README file), linked to a particular documentation run. |
| `CommitEvent` | Represents a raw webhook event log for auditing and debugging purposes, capturing details about repository commits. |

### Notable Dependencies or Side Effects

- **SQLAlchemy**: The models are defined using SQLAlchemy ORM, which provides an Object-Relational Mapping (ORM) layer to interact with the database.
- **UUIDs**: UUIDs are used as primary keys for most entities to ensure uniqueness and avoid conflicts across different instances of the application.
- **Foreign Keys**: Relationships between entities are established using foreign keys, ensuring referential integrity and enabling efficient querying.
- **Indexes**: Indexes are created on certain columns (e.g., `repository_id` in `DocRun`) to improve query performance.

These models form the backbone of the SAGE backend's data model, facilitating the management and retrieval of documentation-related data efficiently.