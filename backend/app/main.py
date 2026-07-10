from fastapi import FastAPI

app = FastAPI(title="Ravel")

@app.get("/health")
def health_check():
    return {"status": "ok", "app": "Ravel", "version": "0.1.0"}
