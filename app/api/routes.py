from fastapi import APIRouter, Depends, HTTPException, Query

from app.models.plant import Plant, SiteConditions, PlantingPlanRequest, PlantingPlanResponse
from app.repositories.plant_repository import CsvPlantRepository, PlantRepository
from app.services.recommendation import recommend_plants
from app.services.planting_design import create_planting_plan

router = APIRouter()


def get_repository() -> PlantRepository:
    # Replace this provider with a production database adapter after
    # confirming the existing 정원백과 database schema and access method.
    import os
    return CsvPlantRepository(os.getenv("PLANT_DATA_PATH", "data/sample_plants.csv"))


@router.get("/plants", response_model=list[Plant])
def list_plants(
    q: str | None = Query(default=None, description="Search Korean or scientific name"),
    sun: str | None = None,
    moisture: str | None = None,
    repository: PlantRepository = Depends(get_repository),
):
    try:
        plants = repository.list_plants()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    if q:
        query = q.casefold()
        plants = [
            p for p in plants
            if query in p.korean_name.casefold()
            or query in p.scientific_name.casefold()
        ]
    if sun:
        plants = [p for p in plants if p.sun == sun]
    if moisture:
        plants = [p for p in plants if p.moisture == moisture]
    return plants


@router.post("/recommend")
def recommend(
    site: SiteConditions,
    repository: PlantRepository = Depends(get_repository),
):
    try:
        return recommend_plants(repository.list_plants(), site)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/planting-plan", response_model=PlantingPlanResponse)
def planting_plan(
    request: PlantingPlanRequest,
    repository: PlantRepository = Depends(get_repository),
):
    try:
        return create_planting_plan(request, repository)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
