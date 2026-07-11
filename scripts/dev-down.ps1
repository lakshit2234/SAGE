$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    docker compose --env-file .env -f infra/compose/docker-compose.yml down
} finally {
    Pop-Location
}