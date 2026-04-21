from fastapi import FastAPI


app = FastAPI()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": "2.1"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
