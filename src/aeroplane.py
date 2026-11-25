from typing import List


class Aeroplane:
    """Класс для представления самолета."""

    def __init__(
        self, callsign: str, country: str, velocity: float, altitude: float
    ) -> None:
        self.__callsign = callsign
        self.__country = country
        self.__velocity = velocity
        self.__altitude = altitude

    @property
    def callsign(self) -> str:
        return self.__callsign

    @property
    def country(self) -> str:
        return self.__country

    @property
    def velocity(self) -> float:
        return self.__velocity

    @property
    def altitude(self) -> float:
        return self.__altitude

    @classmethod
    def cast_to_object_list(cls, data: dict) -> List["Aeroplane"]:
        """Преобразует сырые данные из API в список объектов."""
        # Вот та самая строчка, которую хотел mypy:
        aeroplanes: List["Aeroplane"] = []

        if not data or "states" not in data or data["states"] is None:
            return aeroplanes

        for state in data["states"]:
            callsign = state[1].strip() if state[1] else "Unknown"
            country = state[2] if state[2] else "Unknown"
            velocity = state[9] if state[9] is not None else 0.0
            altitude = state[7] if state[7] is not None else 0.0

            try:
                aeroplane = cls(callsign, country, float(velocity), float(altitude))
                aeroplanes.append(aeroplane)
            except (ValueError, TypeError):
                continue

        return aeroplanes

    def __repr__(self) -> str:
        return (
            f"Aeroplane('{self.callsign}', '{self.country}', "
            f"{self.velocity}, {self.altitude})"
        )

    def __str__(self) -> str:
        return (
            f"Борт {self.callsign}, Страна: {self.country}, "
            f"Скорость: {self.velocity:.1f} м/с, Высота: {self.altitude:.1f} м."
        )

    def __lt__(self, other: "Aeroplane") -> bool:
        return (self.velocity, self.altitude) < (other.velocity, other.altitude)

    def __gt__(self, other: "Aeroplane") -> bool:
        return (self.velocity, self.altitude) > (other.velocity, other.altitude)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return False
        return self.velocity == other.velocity and self.altitude == other.altitude
