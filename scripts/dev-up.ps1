# Start SAGE dev infrastructure
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    docker compose --env-file .env -f infra/compose/docker-compose.yml up -d
    Write-Host ""
    Write-Host "SAGE infra up:" -ForegroundColor Green
    Write-Host "  Postgres  -> localhost:5432  (user=sage db=sage)"
    Write-Host "  Redis     -> localhost:6379"
    Write-Host "  pgAdmin   -> http://localhost:5050  (admin@sage.local / sage_admin)"
} finally {
    Pop-Location
}