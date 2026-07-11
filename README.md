# SAGE

**Self-updating Autonomous Generator for Engineering-docs**

An autonomous documentation agent for GitHub repositories. Connect a repo → SAGE reads the code, generates docs, updates them on every commit, produces architecture diagrams, and extracts API documentation.

## Status
🚧 Under active development — final-year B.Tech project.

## Stack
- **Backend**: FastAPI, Celery, Redis, PostgreSQL, ChromaDB
- **AI**: Ollama (Qwen2.5-Coder 7B + nomic-embed-text) — 100% local, zero-cost inference
- **Parsing**: Tree-sitter (Python, JS/TS, extensible)
- **Diagrams**: Mermaid + Graphviz
- **Frontend**: Next.js, Tailwind, shadcn/ui
- **Infra**: Docker Compose (local), Fly.io + Neon (prod)

## Repository layout

sage/
├── apps/
│   ├── backend/         FastAPI + workers
│   └── frontend/        Next.js dashboard (later)
├── infra/
│   ├── docker/          Dockerfiles
│   └── compose/         docker-compose files
├── scripts/             dev utilities
├── docs/                design notes
└── .github/workflows/   CI

## License
MIT

