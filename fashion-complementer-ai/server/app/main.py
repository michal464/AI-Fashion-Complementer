import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes.predict import router as predict_router
from app.routes.recommend import router as recommend_router

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="AI Fashion Complementer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_router, prefix="/api")
app.include_router(recommend_router, prefix="/api")

CATALOG_DIR = Path(__file__).parent.parent.parent / "catalog"
app.mount("/catalog", StaticFiles(directory=str(CATALOG_DIR)), name="catalog")


@app.get("/")
def health_check():
    return {"status": "ok"}
