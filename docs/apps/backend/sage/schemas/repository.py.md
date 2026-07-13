# Repository Schemas Module

The `repository.py` module in the Sage backend provides Pydantic schemas for handling requests related to connecting and reading repositories. These schemas are used to validate and structure data when interacting with repository-related endpoints.

## Key Classes/Functions

| Class/Function | Description |
|----------------|-------------|
| `ConnectRepoRequest` | A Pydantic model representing a request to connect to a repository. It includes fields for the owner, name, and default branch of the repository. |
| `RepositoryOut` | A Pydantic model representing the output data for a repository. It includes fields for the repository's ID, owner, name, default branch, active status, and the SHA of the last indexed commit. The `model_config` specifies that attributes should be used to populate the model fields. |

## Dependencies

- **Pydantic**: Used for defining and validating data models.
- **UUID**: Used for generating unique identifiers for repositories.

This module is integral to the backend system as it ensures that all repository-related data is correctly formatted and validated before being processed or stored in the database.