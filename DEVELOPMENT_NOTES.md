## Development Notes

### Implementation walkthrough
1) Bootstrapped a minimal FastAPI app with versioned routes, Pydantic models,
   and a consistent error envelope.
2) Integrated `ip-api.com` with an async HTTP client and explicit error mapping.
3) Added unit and integration tests with upstream mocking.
4) Added OpenAPI export script and spec files, plus pre-commit hooks.
5) Documented setup, usage, and decisions in `README.md`.

### Total time spent
Approx. 2-3 hours.

### Challenges & solutions
- Async testing with lifespan initialization: addressed with explicit lifespan
  management in test fixtures.
- Upstream error mapping: normalized failures to a stable error response.
- Pre-commit tooling: resolved type stubs for PyYAML in hook dependencies.

### GenAI usage
Used to scaffold structure, draft tests, and iterate on FastAPI patterns.
Manual review and adjustments applied for correctness and clarity.

### API design decisions
- Versioning via `/v1` prefix.
- Consistent error shape for all endpoints.
- Thin routers with business logic in services.
- Resource initialization in `lifespan` for explicit, testable startup.
- OpenAPI spec stored in `openapi/openapi.yaml` as the source of truth.

### Third-party API selection
Chose `ip-api.com` for its simple integration, no-auth free tier, and
acceptable rate limits for a demo service. Trade-offs include rate limiting
and reliance on external availability.

### Production readiness (next steps)
- Add rate limiting and request throttling per client.
- Introduce caching for hot IPs.
- Add structured logging and request tracing.
- Add metrics and health checks.
- Secure deployment configuration (secrets management, TLS).
- CI pipeline with tests and static analysis.
- Retry/backoff strategy for upstream calls.
- Support for IPv6 and extended fields.
- Configurable timeouts and circuit breaking.
