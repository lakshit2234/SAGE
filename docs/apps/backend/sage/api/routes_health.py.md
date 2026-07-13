### Purpose Summary

The `routes_health.py` module defines the health and readiness endpoints for the SAGE backend application using FastAPI. These endpoints provide simple checks to determine if the application is running (`/live`) and a more comprehensive check to verify the status of all dependencies (`/health`).

### Key Functions/Classes

| Function/Class | Description |
|----------------|-------------|
| `liveness()`   | Returns a simple JSON response indicating that the process is running. |
| `health()`     | Performs a deep health check by pinging all dependencies and returns a JSON response with the status of each component. |

### Notable Dependencies or Side Effects

- **Dependencies**: The `check_all` function from `sage.services.health` is used to perform the comprehensive health check.
- **Side Effects**: None. Both functions are stateless and do not have any side effects.