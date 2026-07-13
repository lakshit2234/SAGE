## Purpose Summary

The `sage/db/base.py` module provides the foundational classes and utilities for interacting with a PostgreSQL database using SQLAlchemy in an asynchronous manner. It defines a base class for ORM models, a mixin for automatically managing timestamps, and sets up an async engine and session factory for database operations.

## Key Functions/Classes

| Name | Description |
|------|-------------|
| `Base` | A declarative base class for all ORM models, inheriting from SQLAlchemy's `DeclarativeBase`. |
| `TimestampMixin` | A mixin class that adds `created_at` and `updated_at` fields to ORM models, automatically managing their values using SQLAlchemy's `mapped_column`. |
| `get_session` | An asynchronous generator function used as a FastAPI dependency to yield an async DB session for database operations. |

## Notable Dependencies

- **SQLAlchemy**: The core library for ORM and SQL interactions.
- **asyncio**: For handling asynchronous operations.
- **sage.core.config.get_settings()**: Retrieves configuration settings, specifically the PostgreSQL DSN (Data Source Name) used to create the async engine.

This module is crucial for setting up a robust database interaction layer in an asynchronous FastAPI application, ensuring that all ORM models are properly structured and that timestamps are automatically managed.