from app.models.plant import SiteConditions, PlantingPlanRequest, PlantingPlanResponse
from app.repositories.plant_repository import PlantRepository
from app.services.recommendation import recommend_plants


def create_planting_plan(
    request: PlantingPlanRequest, repository: PlantRepository
) -> PlantingPlanResponse:
    site = request.site.model_copy(update={"limit": min(request.plant_count * 3, 100)})
    ranked = recommend_plants(repository.list_plants(), site)
    selected = ranked[: request.plant_count]

    notes = [
        "추천 결과는 대상지 조건과 입력된 식물 특성의 일치도를 이용한 1차 후보 목록입니다.",
        "실제 식재 전에는 현장 토양·광환경·배수·미기후와 식물의 성숙 크기를 확인해야 합니다.",
    ]
    limitations = [
        "현재 버전은 식재 수량, 식재 간격, 피복률, 군락 면적을 산출하지 않습니다.",
        "샘플 데이터는 기능 시연용이며 실제 설계나 시공 근거로 사용하면 안 됩니다.",
        "개화기와 생육 특성은 지역·품종·관리 조건에 따라 달라질 수 있습니다.",
    ]
    return PlantingPlanResponse(
        candidates=selected,
        design_notes=notes,
        limitations=limitations,
    )
