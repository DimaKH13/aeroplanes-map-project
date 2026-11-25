from abc import ABC, abstractmethod
from typing import Optional

import requests


class AbstractAPI(ABC):
    """Абстрактный класс для работы с API."""

    @abstractmethod
    def get_aeroplanes(self, country: str) -> Optional[dict]:
        pass


class AeroplanesAPI(AbstractAPI):
    """Класс для получения данных о самолетах."""

    def __init__(self) -> None:
        self.openstreetmap_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all?"

    def get_aeroplanes(self, country: str) -> Optional[dict]:
        """Получает координаты страны и возвращает самолеты."""
        headers_nominatim = {"User-Agent": "test-app/1.0"}

        # Явно указываем, что тут строки и числа
        params_nominatim: dict[str, str | int] = {
            "country": country,
            "format": "json",
            "limit": 1,
        }

        try:
            response = requests.get(
                url=self.openstreetmap_url,
                params=params_nominatim,
                headers=headers_nominatim,
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            if not data:
                print(f"Страна '{country}' не найдена.")
                return None

            geo_coordinates = data[0].get("boundingbox")

            # А тут только строки
            params: dict[str, str] = {
                "lamin": str(geo_coordinates[0]),
                "lamax": str(geo_coordinates[1]),
                "lomin": str(geo_coordinates[2]),
                "lomax": str(geo_coordinates[3]),
            }

            response = requests.get(url=self.opensky_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()

        except (
            requests.exceptions.RequestException,
            ValueError,
            IndexError,
            KeyError,
        ) as e:
            print(f"Ошибка при запросе к API: {e}")
            return None
