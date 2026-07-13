### Purpose Summary

The `routes_auth.py` module implements the GitHub OAuth login flow for the SAGE backend application. It provides endpoints to initiate the login process, handle the callback from GitHub, and log out users.

### Key Functions/Classes

| Function/Class | Description |
|----------------|-------------|
| `login(request: Request) -> RedirectResponse` | Initiates the GitHub OAuth login process by redirecting the user to the GitHub authorization URL. |
| `callback(request: Request, code: str, state: str) -> RedirectResponse` | Handles the callback from GitHub after the user authorizes the application. Exchanges the authorization code for an access token and fetches user information. If successful, logs the user in; otherwise, raises an exception. |
| `logout(request: Request) -> dict[str, str]` | Logs out the user by clearing their session and returns a success message. |

### Notable Dependencies or Side Effects

- **Dependencies**: This module depends on the `fastapi`, `sage.services.github_auth`, and `sage.core.logging` modules.
- **Side Effects**: The module modifies the user's session to store OAuth tokens and user information upon successful login, and clears the session upon logout. It also logs events related to the authentication process.