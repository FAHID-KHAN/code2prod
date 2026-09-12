# bytebangla-api

The backend service behind ByteBangla's marketplace app.

## Run locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Then visit `http://localhost:8000/` — you should see `{"message": "ByteBangla API"}`.
