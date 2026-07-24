import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.routers import admin, annotations, audio, auth, export, phrases, syntax, verification

app = FastAPI(title="NLP Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

audio_dir = Path(settings.LOCAL_AUDIO_DIR)
audio_dir.mkdir(parents=True, exist_ok=True)
app.mount("/audio", StaticFiles(directory=str(audio_dir)), name="audio")

app.include_router(auth.router)
app.include_router(audio.router)
app.include_router(phrases.router)
app.include_router(annotations.router)
app.include_router(syntax.router)
app.include_router(verification.router)
app.include_router(export.router)
app.include_router(admin.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "Assamese NLP Platform API is running"}
