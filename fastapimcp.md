---
name: fastapi-mcp-server
description: >
  Build, scaffold, and extend production-grade Model Context Protocol (MCP)
  servers using Python and FastAPI. Use whenever the user wants to create an
  MCP server, add MCP tools/resources/prompts to an existing FastAPI app,
  implement MCP transports (SSE or stdio), or wire up authentication, error
  handling, and observability for an MCP endpoint. Do NOT use for plain REST
  APIs that have no MCP intent.
---

# FastAPI MCP Server Skill

## Overview

This skill guides Claude in producing **production-quality** Python MCP servers
built on FastAPI. Outputs must be runnable, typed, testable, and deployable
without modification.

Key outcomes:
- Correct MCP protocol implementation (tools, resources, prompts, sampling)
- FastAPI app with lifespan management, dependency injection, and proper routing
- Async-first, fully type-annotated Python (3.11+)
- Structured logging, error handling, and health checks baked in
- Docker-ready project layout
- Tests scaffolded alongside application code

---

## Pre-Flight Checklist

Before writing any code, Claude MUST:

1. **Identify MCP transport** — SSE (HTTP-based, default for web deployments)
   or stdio (for local CLI / desktop clients like Claude Desktop).
2. **Identify MCP primitives needed** — tools, resources, resource templates,
   prompts, and/or sampling.
3. **Identify auth requirements** — none, API key header, OAuth 2.0 bearer.
4. **Clarify external integrations** — databases, third-party APIs, file
   system, etc.
5. **Check for existing FastAPI app** — if one exists, extend it; do not
   replace it.

If any of these are ambiguous, ask the user ONE clarifying question covering
the most critical ambiguity before proceeding.

---

## Project Layout

Always generate or respect the following structure:

```
my_mcp_server/
├── pyproject.toml           # PEP 621 metadata + dependencies
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── README.md
│
├── src/
│   └── my_mcp_server/
│       ├── __init__.py
│       ├── main.py          # FastAPI app + lifespan + MCP mount
│       ├── config.py        # Pydantic Settings (env-driven)
│       ├── dependencies.py  # FastAPI dependency providers
│       ├── mcp/
│       │   ├── __init__.py
│       │   ├── server.py    # mcp.Server instance + registration
│       │   ├── tools/
│       │   │   ├── __init__.py
│       │   │   └── <domain>.py   # One module per logical tool group
│       │   ├── resources/
│       │   │   ├── __init__.py
│       │   │   └── <domain>.py
│       │   └── prompts/
│       │       ├── __init__.py
│       │       └── <domain>.py
│       └── services/        # Business logic, external API clients
│           └── <domain>.py
│
└── tests/
    ├── conftest.py
    ├── test_tools.py
    ├── test_resources.py
    └── test_integration.py
```

---

## Core Dependencies

Always include in `pyproject.toml`:

```toml
[project]
name = "my-mcp-server"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.115",
    "uvicorn[standard]>=0.30",
    "mcp>=1.0",              # official MCP Python SDK
    "pydantic>=2.7",
    "pydantic-settings>=2.3",
    "httpx>=0.27",           # async HTTP client
    "structlog>=24.1",       # structured logging
    "python-dotenv>=1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8",
    "pytest-asyncio>=0.23",
    "pytest-cov>=5",
    "httpx",                 # for TestClient
    "ruff>=0.4",
    "mypy>=1.10",
]
```

---

## Implementation Patterns

### 1. Configuration (`config.py`)

Always use Pydantic Settings. Never hardcode secrets.

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, AnyHttpUrl


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )

    app_name: str = "My MCP Server"
    debug: bool = False
    log_level: str = "INFO"

    # Auth — optional API key guard
    api_key: SecretStr | None = None

    # Example external service
    upstream_base_url: AnyHttpUrl = "https://api.example.com"
    upstream_api_key: SecretStr | None = None

    # MCP transport: "sse" | "stdio"
    mcp_transport: str = "sse"
    mcp_path: str = "/mcp"


settings = Settings()
```

### 2. Logging (`main.py` bootstrap)

Configure structlog before anything else. Always include request IDs.

```python
import structlog, logging

def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        format="%(message)s",
        level=getattr(logging, level.upper(), logging.INFO),
    )
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, level.upper(), logging.INFO)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )
```

### 3. FastAPI App with Lifespan (`main.py`)

```python
from contextlib import asynccontextmanager
from typing import AsyncIterator

import structlog
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import uuid

from .config import settings
from .mcp.server import create_mcp_server
from mcp.server.sse import SseServerTransport

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    configure_logging(settings.log_level)
    logger.info("startup", app=settings.app_name, transport=settings.mcp_transport)
    # Initialize connection pools, caches, etc. here
    yield
    logger.info("shutdown")


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    debug=settings.debug,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Tighten for production
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request ID middleware ──────────────────────────────────────────────────────
@app.middleware("http")
async def request_id_middleware(request: Request, call_next) -> Response:
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    structlog.contextvars.bind_contextvars(request_id=request_id)
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    structlog.contextvars.clear_contextvars()
    return response


# ── Health check ───────────────────────────────────────────────────────────────
@app.get("/health", tags=["ops"])
async def health() -> dict:
    return {"status": "ok", "app": settings.app_name}


# ── MCP SSE mount ──────────────────────────────────────────────────────────────
mcp_server = create_mcp_server()
sse_transport = SseServerTransport(settings.mcp_path)

@app.get(settings.mcp_path, tags=["mcp"])
async def mcp_sse_endpoint(request: Request) -> None:
    async with sse_transport.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await mcp_server.run(
            streams[0], streams[1], mcp_server.create_initialization_options()
        )

@app.post(settings.mcp_path + "/messages", tags=["mcp"])
async def mcp_post_messages(request: Request) -> Response:
    return await sse_transport.handle_post_message(request)
```

### 4. MCP Server Registration (`mcp/server.py`)

```python
import mcp.types as types
from mcp.server import Server
from mcp.server.models import InitializationOptions

import structlog

from .tools import register_tools
from .resources import register_resources
from .prompts import register_prompts

logger = structlog.get_logger()


def create_mcp_server() -> Server:
    server = Server("my-mcp-server")
    register_tools(server)
    register_resources(server)
    register_prompts(server)
    logger.info("mcp_server_created", server_name=server.name)
    return server
```

### 5. Tool Implementation Pattern (`mcp/tools/<domain>.py`)

Follow these rules for EVERY tool:

- Annotate inputs with a Pydantic model (not raw `dict`).
- Return `list[types.TextContent | types.ImageContent | types.EmbeddedResource]`.
- Always handle exceptions; return structured error content, never raise to the transport.
- Log entry/exit with structlog at DEBUG level; log errors at ERROR.
- Keep tools thin — delegate business logic to `services/`.

```python
from __future__ import annotations

import structlog
from mcp.server import Server
import mcp.types as types
from pydantic import BaseModel, Field

from ...services.weather import WeatherService

logger = structlog.get_logger()
_service = WeatherService()


class GetWeatherInput(BaseModel):
    location: str = Field(..., description="City name or lat,lon pair")
    units: str = Field("metric", description="'metric' or 'imperial'")


def register_weather_tools(server: Server) -> None:

    @server.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="get_weather",
                description="Fetch current weather for a location.",
                inputSchema=GetWeatherInput.model_json_schema(),
            )
        ]

    @server.call_tool()
    async def call_tool(
        name: str, arguments: dict
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        log = logger.bind(tool=name)
        log.debug("tool_called", arguments=arguments)

        if name == "get_weather":
            try:
                data = GetWeatherInput(**arguments)
                result = await _service.get_current(data.location, data.units)
                log.debug("tool_success")
                return [types.TextContent(type="text", text=result.model_dump_json())]
            except Exception as exc:
                log.error("tool_error", error=str(exc))
                return [
                    types.TextContent(
                        type="text",
                        text=f"Error fetching weather: {exc}",
                    )
                ]

        return [types.TextContent(type="text", text=f"Unknown tool: {name}")]
```

### 6. Resource Implementation Pattern (`mcp/resources/<domain>.py`)

```python
from mcp.server import Server
import mcp.types as types
import structlog

logger = structlog.get_logger()


def register_config_resources(server: Server) -> None:

    @server.list_resources()
    async def list_resources() -> list[types.Resource]:
        return [
            types.Resource(
                uri="config://app/settings",
                name="Application Settings",
                description="Read-only view of non-sensitive runtime configuration.",
                mimeType="application/json",
            )
        ]

    @server.read_resource()
    async def read_resource(uri: types.AnyUrl) -> str:
        logger.debug("resource_read", uri=str(uri))
        if str(uri) == "config://app/settings":
            from ...config import settings
            # Never expose secrets — use model_dump with exclusions
            safe = settings.model_dump(exclude={"api_key", "upstream_api_key"})
            import json
            return json.dumps(safe, default=str)
        raise ValueError(f"Unknown resource URI: {uri}")
```

### 7. Service Layer Pattern (`services/<domain>.py`)

```python
from __future__ import annotations

import httpx
import structlog
from pydantic import BaseModel

from ..config import settings

logger = structlog.get_logger()


class WeatherData(BaseModel):
    location: str
    temperature: float
    description: str
    humidity: int


class WeatherService:
    def __init__(self) -> None:
        self._client: httpx.AsyncClient | None = None

    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=str(settings.upstream_base_url),
                headers={"Authorization": f"Bearer {settings.upstream_api_key.get_secret_value()}"}
                if settings.upstream_api_key
                else {},
                timeout=10.0,
            )
        return self._client

    async def get_current(self, location: str, units: str = "metric") -> WeatherData:
        log = logger.bind(location=location, units=units)
        log.debug("weather_fetch")
        resp = await self.client.get(
            "/weather", params={"q": location, "units": units}
        )
        resp.raise_for_status()
        raw = resp.json()
        log.debug("weather_fetched")
        return WeatherData(
            location=raw["name"],
            temperature=raw["main"]["temp"],
            description=raw["weather"][0]["description"],
            humidity=raw["main"]["humidity"],
        )
```

### 8. Authentication Dependency (`dependencies.py`)

```python
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from .config import settings

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(key: str | None = Security(_api_key_header)) -> None:
    """No-op when API key is not configured; enforces key when it is."""
    if settings.api_key is None:
        return
    if key is None or key != settings.api_key.get_secret_value():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
```

Apply to MCP routes by adding `dependencies=[Depends(verify_api_key)]` to the
endpoint decorators.

---

## Error Handling Strategy

| Layer | How to handle |
|---|---|
| Tool handler | Catch all exceptions; return `TextContent` with error message |
| Resource handler | Raise `ValueError` for unknown URIs (MCP SDK maps to error response) |
| Service layer | Let exceptions propagate up to tool handler |
| FastAPI routes | Add exception handlers for `HTTPException` and catch-all 500 |
| Startup failures | Log and re-raise — let the process crash so orchestrators restart it |

Never silently swallow errors. Always log at ERROR with full context.

---

## Testing Patterns

### conftest.py

```python
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from my_mcp_server.main import app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture()
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
```

### Tool unit test pattern

```python
import pytest
from unittest.mock import AsyncMock, patch

from my_mcp_server.mcp.tools.weather import call_tool


@pytest.mark.asyncio
async def test_get_weather_success():
    with patch(
        "my_mcp_server.mcp.tools.weather._service.get_current",
        new_callable=AsyncMock,
    ) as mock_svc:
        from my_mcp_server.services.weather import WeatherData
        mock_svc.return_value = WeatherData(
            location="London", temperature=15.2,
            description="cloudy", humidity=72
        )
        result = await call_tool("get_weather", {"location": "London"})
    assert len(result) == 1
    assert "London" in result[0].text


@pytest.mark.asyncio
async def test_get_weather_service_error():
    with patch(
        "my_mcp_server.mcp.tools.weather._service.get_current",
        new_callable=AsyncMock,
        side_effect=RuntimeError("upstream timeout"),
    ):
        result = await call_tool("get_weather", {"location": "London"})
    assert "Error" in result[0].text
```

### Integration test (SSE endpoint alive)

```python
def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_mcp_sse_headers(client):
    # SSE endpoint should return 200 and begin the event stream
    with client.stream("GET", "/mcp") as resp:
        assert resp.status_code == 200
        assert "text/event-stream" in resp.headers["content-type"]
```

---

## Dockerfile

```dockerfile
FROM python:3.12-slim AS base
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

FROM base AS builder
RUN pip install --upgrade pip
COPY pyproject.toml .
RUN pip install --no-cache-dir ".[dev]" 2>/dev/null || pip install --no-cache-dir .

FROM base AS runtime
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY src/ src/
EXPOSE 8000
CMD ["uvicorn", "my_mcp_server.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## stdio Transport (Claude Desktop / local clients)

When `mcp_transport = "stdio"`, bypass FastAPI entirely and run the MCP server
directly via the SDK's stdio runner. Provide a separate entry point:

```python
# src/my_mcp_server/stdio_entry.py
import asyncio
from mcp.server.stdio import stdio_server
from .mcp.server import create_mcp_server
from .config import settings
from .main import configure_logging
import structlog

logger = structlog.get_logger()


async def main() -> None:
    configure_logging(settings.log_level)
    server = create_mcp_server()
    logger.info("stdio_transport_start")
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
```

Add to `pyproject.toml`:
```toml
[project.scripts]
my-mcp-server-stdio = "my_mcp_server.stdio_entry:main"
```

---

## Security Checklist

Claude must verify these are addressed before declaring the server complete:

- [ ] Secrets loaded from environment variables only (never committed)
- [ ] `SecretStr` used for all secret fields in Settings
- [ ] `model_dump(exclude={...})` applied before serializing settings as a resource
- [ ] API key auth dependency wired to MCP endpoints when `api_key` is set
- [ ] CORS origins restricted for production (not `*`)
- [ ] No raw `exec`/`eval` in tool implementations
- [ ] File-system tools path-validate inputs to prevent directory traversal
- [ ] External HTTP calls use timeouts (never `timeout=None`)

---

## Common Mistakes to Avoid

| Mistake | Correct pattern |
|---|---|
| Registering handlers outside `create_mcp_server()` | Always register inside the factory function |
| Using `@app.on_event` (deprecated) | Use `lifespan` async context manager |
| Returning plain strings from tool handlers | Always return `list[types.TextContent \| ...]` |
| Blocking I/O inside async tool handlers | Use `asyncio.to_thread()` or async libraries |
| Sharing a single `httpx.Client` (sync) across async handlers | Use `httpx.AsyncClient` |
| Forgetting `model_json_schema()` in Tool definition | Every tool needs `inputSchema` |
| Hardcoding the MCP path | Read it from `settings.mcp_path` |
| Not testing error paths | Every tool test suite MUST include an error-path test |

---

## Output Requirements

When this skill is invoked, Claude MUST produce:

1. All source files as runnable Python (not pseudocode).
2. `pyproject.toml` with pinned major versions.
3. `.env.example` with all required variables and safe placeholder values.
4. `Dockerfile` and `docker-compose.yml` if a containerized deployment was
   requested or implied.
5. At minimum: `tests/conftest.py`, `tests/test_tools.py` with at least one
   success and one error-path test per tool.
6. A `README.md` with: installation, environment setup, running locally, and
   running via Docker.

Do **not** produce skeleton stubs with `pass` bodies or `# TODO` comments
unless the user explicitly requested a minimal scaffold.

---

## Evals

### Eval 0 — Basic tool server

**Prompt**: "Create an MCP server with a single `echo` tool that returns the
input string. Use SSE transport."

**Expectations**:
- `main.py` imports from `mcp.server.sse`
- `SseServerTransport` is instantiated
- A tool named `echo` is registered via `@server.call_tool()`
- Tool returns `list[types.TextContent]`
- `pyproject.toml` lists `mcp>=1.0` and `fastapi>=0.115`
- `/health` endpoint is present
- At least one test file exists under `tests/`

### Eval 1 — Auth + external service

**Prompt**: "Add API key authentication and a `search_docs` tool that calls
https://api.example.com/search with a Bearer token from the environment."

**Expectations**:
- `dependencies.py` defines `verify_api_key`
- `Settings` has `api_key: SecretStr | None`
- `Settings` has an `upstream_api_key: SecretStr | None`
- Service layer uses `httpx.AsyncClient` with a timeout
- Tool handler catches `httpx.HTTPError` and returns error `TextContent`
- `.env.example` includes `API_KEY`, `UPSTREAM_API_KEY`

### Eval 2 — stdio transport

**Prompt**: "Generate a minimal MCP server that runs over stdio for use with
Claude Desktop."

**Expectations**:
- `stdio_entry.py` uses `mcp.server.stdio.stdio_server`
- No FastAPI or uvicorn imports in `stdio_entry.py`
- `pyproject.toml` declares a `[project.scripts]` entry pointing to the stdio module
- `README.md` includes Claude Desktop `mcpServers` JSON config example
