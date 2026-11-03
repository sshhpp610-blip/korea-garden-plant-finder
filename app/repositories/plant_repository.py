import csv
import os
from pathlib import Path
from typing import Protocol

from app.models.plant import Plant


class PlantRepository(Protocol):
    def list_plants(self) -> list[Plant]: ...


class CsvPlantRepository:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def list_plants(self) -> list[Plant]:
        if not self.path.exists():
            raise FileNotFoundError(f"Plant data file not found: {self.path}")

        plants: list[Plant] = []
        with self.path.open("r", encoding="utf-8-sig", newline="") as file:
            for row in csv.DictReader(file):
                purposes = [
                    item.strip()
                    for item in (row.get("purposes") or "").split("|")
                    if item.strip()
                ]
                plants.append(
                    Plant(
                        plant_id=row["plant_id"],
                        scientific_name=row["scientific_name"],
                        korean_name=row["korean_name"],
                        sun=row.get("sun") or "unknown",
                        moisture=row.get("moisture") or "unknown",
                        soil=row.get("soil") or "unknown",
                        height_cm=float(row["height_cm"]) if row.get("height_cm") else None,
                        flowering_start_month=int(row["flowering_start_month"])
                        if row.get("flowering_start_month") else None,
                        flowering_end_month=int(row["flowering_end_month"])
                        if row.get("flowering_end_month") else None,
                        purposes=purposes,
                        native_status=row.get("native_status") or "unknown",
                        data_source=row.get("data_source") or None,
                        data_confidence=row.get("data_confidence") or "unknown",
                    )
                )
        return plants
