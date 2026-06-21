# Awsar Setu v2

A production-grade social infrastructure platform for multi-tiered, age-specific welfare scheme routing.

## What it includes

- FastAPI backend in `main.py`
- Web interface served from `index.html`
- Scheme API at `/api/v2/schemes`
- Health check at `/health`
- Deploy support for Render/Heroku-style Python hosts through `Procfile`
- Docker support through `Dockerfile`
- GitHub Actions smoke test

## Run locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000`.

Example API call:

```bash
curl "http://127.0.0.1:8000/api/v2/schemes?age=25&state=Odisha"
```

## Deploy

### Render

This repository includes `render.yaml`. Create a new Render Blueprint from the repo, or configure a Python web service manually:

- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Health check path: `/health`

### Docker

```bash
docker build -t awsar-setu-v2 .
docker run -p 8000:8000 awsar-setu-v2
```
