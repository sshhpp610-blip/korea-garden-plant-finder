from app.models.plant import Plant, SiteConditions
from app.services.recommendation import recommend_plants


def test_matching_plant_scores_higher():
    matching = Plant(
        plant_id="1",
        scientific_name="Aster test",
        korean_name="테스트국화",
        sun="full_sun",
        moisture="medium",
        soil="loam",
        purposes=["pollinator"],
    )
    mismatching = Plant(
        plant_id="2",
        scientific_name="Hosta test",
        korean_name="테스트비비추",
        sun="shade",
        moisture="moist",
        soil="clay",
        purposes=["shade"],
    )
    site = SiteConditions(
        sun="full_sun",
        moisture="medium",
        soil="loam",
        purpose=["pollinator"],
        limit=10,
    )

    results = recommend_plants([mismatching, matching], site)

    assert results[0].plant.plant_id == "1"
    assert results[0].score > results[1].score
