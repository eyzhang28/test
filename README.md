# Health Check Service

This repository exposes a lightweight unauthenticated HTTP health endpoint:

- `GET /health`
- Response: `{"status":"ok"}`
- Status code: `200`
- Content-Type: `application/json`

## Run

```bash
python server.py
```

Optional port override:

```bash
PORT=9000 python server.py
```

## Smoke test

```bash
python -m unittest -v
```
