import json
import os
from abc import ABC, abstractmethod
from typing import Any, List

from src.aeroplane import Aeroplane


class AbstractSaver(ABC):
    """Абстрактный класс для работы с хранилищем."""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        pass

    @abstractmethod
    def get_aeroplanes(self, **criteria: Any) -> List[dict]:
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        pass


class JSONSaver(AbstractSaver):
    """Класс для работы с JSON-файлом."""

    def __init__(self, filename: str = "data/aeroplanes.json") -> None:
        self.filename = filename
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

    def _load_data(self) -> List[dict]:
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        data = self._load_data()
        data.append(
            {
                "callsign": aeroplane.callsign,
                "country": aeroplane.country,
                "velocity": aeroplane.velocity,
                "altitude": aeroplane.altitude,
            }
        )
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def get_aeroplanes(self, **criteria: Any) -> List[dict]:
        data = self._load_data()
        if not criteria:
            return data
        result = []
        for item in data:
            match = True
            for key, value in criteria.items():
                if item.get(key) != value:
                    match = False
                    break
            if match:
                result.append(item)
        return result

    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        data = self._load_data()
        new_data = [item for item in data if item.get("callsign") != aeroplane.callsign]
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)
