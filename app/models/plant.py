from typing import Literal
from pydantic import BaseModel, Field

Sun = Literal["full_sun", "partial_shade", "shade", "unknown"]
Moisture = Literal["dry", "medium", "moist", "wet", "unknown"]
Soil = Literal["sand", "loam", "clay", "varied", "unknown"]


class Plant(BaseModel):
    plant_id: str
    scientific_name: str
    korean_name: str
    sun: Sun = "unknown"
    moisture: Moisture = "unknown"
    soil: Soil = "unknown"
    height_cm: float | None = Field(default=None, ge=0)
    flowering_start_month: int | None = Field(default=None, ge=1, le=12)
    flowering_end_month: int | None = Field(default=None, ge=1, le=12)
    purposes: list[str] = Field(default_factory=list)
    native_status: Literal["native", "introduced", "unknown"] = "unknown"
    data_source: str | None = None
    data_confidence: Literal["verified", "reference", "expert_estimate", "unknown"] = "unknown"


class SiteConditions(BaseModel):
    sun: Sun = "unknown"
    moisture: Moisture = "unknown"
    soil: Soil = "unknown"
    purpose: list[str] = Field(default_factory=list)
    limit: int = Field(default=10, ge=1, le=100)


class PlantRecommendation(BaseModel):
    plant: Plant
    score: float
    reasons: list[str]


class PlantingPlanRequest(BaseModel):
    site: SiteConditions
    plant_count: int = Field(default=5, ge=1, le=30)


class PlantingPlanResponse(BaseModel):
    candidates: list[PlantRecommendation]
    design_notes: list[str]
    limitations: list[str]
