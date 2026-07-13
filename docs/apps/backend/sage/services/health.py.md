# Health Probes Module

## Purpose Summary

The `health.py` module provides asynchronous health check functions for PostgreSQL, Redis, and Ollama services. These checks are used to monitor the availability and status of these critical components in a larger system.

## Key Functions/Classes

| Function/Class | Description |
|----------------|-------------|
| `ComponentStatus` | A data class representing the status of a health check component, including its name, whether it is OK, and an optional detail message. |
| `check_postgres` | Asynchronously checks the connectivity and version of a PostgreSQL database using `asyncpg`. Returns a `ComponentStatus` object indicating the result. |
| `check_redis` | Asynchronously checks the connectivity and availability of a Redis server using `aioredis`. Returns a `ComponentStatus` object indicating the result. |
| `check_ollama` | Asynchronously checks the availability of specific models in an Ollama API by making an HTTP GET request. Returns a `ComponentStatus` object indicating the result. |
| `check_all` | Asynchronously gathers and returns the health check results for PostgreSQL, Redis, and Ollama using `asyncio.gather`. |

## Notable Dependencies and Side Effects

- **Dependencies**: This module depends on external libraries such as `asyncpg`, `httpx`, and `aioredis`.
- **Side Effects**: The functions log warnings if any health check fails. They also close connections to the database and Redis server after performing checks.