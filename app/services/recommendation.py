from app.models.plant import Plant, SiteConditions, PlantRecommendation


def score_plant(plant: Plant, site: SiteConditions) -> PlantRecommendation:
    score = 0.0
    reasons: list[str] = []

    # Suitability is scored only when both the site and plant value are known.
    # Unknown values are neutral: they neither add nor subtract points.
    dimensions = [
        ("sun", site.sun, plant.sun, 35.0, "일조 조건"),
        ("moisture", site.moisture, plant.moisture, 35.0, "수분 조건"),
        ("soil", site.soil, plant.soil, 20.0, "토양 조건"),
    ]

    for _, requested, actual, weight, label in dimensions:
        if requested == "unknown" or actual == "unknown":
            continue
        if requested == actual or (label == "토양 조건" and actual == "varied"):
            score += weight
            reasons.append(f"{label} 적합")
        else:
            reasons.append(f"{label} 불일치: 대상지 {requested}, 식물 데이터 {actual}")

    if site.purpose:
        matched = sorted(set(site.purpose).intersection(plant.purposes))
        if matched:
            score += 10.0 * len(matched) / len(set(site.purpose))
            reasons.append("목적 태그 일치: " + ", ".join(matched))
        else:
            reasons.append("요청한 목적 태그와 일치하는 항목 없음")

    if not reasons:
        reasons.append("비교 가능한 환경 특성이 부족함")

    return PlantRecommendation(
        plant=plant,
        score=round(min(score, 100.0), 1),
        reasons=reasons,
    )


def recommend_plants(
    plants: list[Plant], site: SiteConditions
) -> list[PlantRecommendation]:
    ranked = [score_plant(plant, site) for plant in plants]
    ranked.sort(key=lambda item: (-item.score, item.plant.korean_name))
    return ranked[: site.limit]
