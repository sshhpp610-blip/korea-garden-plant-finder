from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Korea Garden Plant Finder API",
    description="Plant database, explainable plant recommendations, and planting design support.",
    version="0.1.0",
)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "korea-garden-plant-finder"}
