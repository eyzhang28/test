# HF_TOKENS local setup

This project can read one or more Hugging Face access tokens from an environment variable named `HF_TOKENS`.

## 1) Configure local environment variables

Copy the template file and add your real tokens locally:

```bash
cp .env.example .env
```

Then edit `.env` and set:

```env
HF_TOKENS="hf_token_1,hf_token_2"
```

Do not commit real tokens. The `.env` file is intentionally gitignored.

## 2) Read tokens in Python with `os.environ`

```python
import os

tokens = [token.strip() for token in os.environ.get("HF_TOKENS", "").split(",") if token.strip()]
```

## 3) Optional: load from `.env` with `python-dotenv`

If your environment does not automatically load `.env`, you can use `python-dotenv`:

```python
import os
from dotenv import load_dotenv

load_dotenv()  # loads values from .env into the process environment
tokens = [token.strip() for token in os.environ.get("HF_TOKENS", "").split(",") if token.strip()]
```
