### Purpose Summary

This migration script initializes the database schema for a backend application by creating tables for `repositories`, `commit_events`, `doc_runs`, and `doc_artifacts`. Each table is designed to store specific types of data related to repository management, commit events, documentation runs, and artifacts generated from those runs.

### Key Functions/Classes

| Function/Class | Description |
|----------------|-------------|
| `upgrade()`    | Defines the operations to perform when upgrading the database schema. This includes creating tables and indexes for `repositories`, `commit_events`, `doc_runs`, and `doc_artifacts`. |
| `downgrade()`  | Defines the operations to perform when downgrading the database schema. This includes dropping all the tables created by the `upgrade()` function in reverse order. |

### Notable Dependencies or Side Effects

- **Alembic**: The script uses Alembic, a lightweight database migration tool for SQLAlchemy, to manage changes to the database schema.
- **SQLAlchemy**: SQLAlchemy is used to define and interact with the database tables.
- **PostgreSQL JSONB Type**: The `postgresql.JSONB` type is used to store JSON data in a binary format, which can be more efficient than storing it as text.

This migration script is crucial for setting up the initial database structure required by the backend application to manage repositories, track commit events, and handle documentation generation and artifact storage.