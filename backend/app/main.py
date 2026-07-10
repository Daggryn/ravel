from fastapi import FastAPI
from app.database import engine
from app import models
from app.routes import auth as auth_router
from app.seed import seed_users

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ravel API")

app.include_router(auth_router.router)


@app.on_event("startup")
def on_startup():
    seed_users()


@app.get("/health")
def health_check():
    return {"status": "ok", "app": "Ravel"}
