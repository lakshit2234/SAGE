### Purpose Summary

The `config.py` module in the SAGE backend is responsible for loading typed application settings from environment variables and a `.env` file. It provides a centralized configuration for various components such as the app itself, database connections (Postgres and Redis), external services (Ollama and ChromaDB), storage directories, GitHub OAuth, and session management.

### Key Functions/Classes

| Function/Class | Description |
|----------------|-------------|
| `Settings` | A Pydantic model that defines the application settings with type annotations and default values. It also includes properties to generate database connection strings. |
| `get_settings` | A cached function that returns an instance of the `Settings` class, ensuring that the configuration is loaded only once per application run. |

### Notable Dependencies or Side Effects

- **Pydantic**: Used for defining and validating the settings schema.
- **pydantic-settings**: Extends Pydantic to support loading settings from environment variables and `.env` files.
- **lru_cache**: Decorator used in `get_settings` to cache the configuration instance, reducing the overhead of repeated configuration loads.

This module is crucial for ensuring that all components of the SAGE backend have access to consistent and correctly configured settings.