from src.aeroplane import Aeroplane
from src.api import AeroplanesAPI
from src.json_saver import JSONSaver


def get_aeroplanes_by_altitude(
    aeroplanes: list[Aeroplane], min_alt: float, max_alt: float
) -> list[Aeroplane]:
    """Фильтрует самолеты по диапазону высоты."""
    return [plane for plane in aeroplanes if min_alt <= plane.altitude <= max_alt]


def user_interaction() -> None:
    api = AeroplanesAPI()
    saver = JSONSaver()

    print("Добро пожаловать в программу поиска самолетов!")
    country = input("Введите название страны (на английском, например Spain): ")

    raw_data = api.get_aeroplanes(country)
    if not raw_data:
        print(
            "Не удалось получить данные. Проверьте название страны "
            "или попробуйте позже."
        )
        return

    aeroplanes = Aeroplane.cast_to_object_list(raw_data)
    if not aeroplanes:
        print(
            "В воздушном пространстве этой страны сейчас нет самолетов "
            "(или они не передают данные)."
        )
        return

    # Фильтрация по высоте
    altitude_input = input(
        "Введите диапазон высот полета (например, 10000-15000) "
        "или Enter, чтобы пропустить: "
    )
    if "-" in altitude_input:
        try:
            min_alt_str, max_alt_str = altitude_input.split("-")
            min_alt = float(min_alt_str.strip())
            max_alt = float(max_alt_str.strip())
            aeroplanes = get_aeroplanes_by_altitude(aeroplanes, min_alt, max_alt)
            if not aeroplanes:
                print("Нет самолетов в указанном диапазоне высот.")
                return
        except ValueError:
            print("Некорректный ввод диапазона высот. Пропускаем фильтр.")

    # Топ N по высоте
    try:
        top_n_input = input(
            "Введите количество самолетов для вывода в Топ N (по высоте): "
        )
        top_n = int(top_n_input)
        sorted_by_altitude = sorted(aeroplanes, key=lambda x: x.altitude, reverse=True)
        top_aeroplanes = sorted_by_altitude[:top_n]

        print(f"\nТоп {top_n} самолетов по высоте:")
        for plane in top_aeroplanes:
            print(plane)
    except ValueError:
        print("Некорректный ввод количества.")

    # Фильтрация по стране регистрации
    filter_country = input(
        "\nВведите страну регистрации для фильтрации " "(или Enter, чтобы пропустить): "
    )
    filtered_planes = []
    if filter_country:
        filtered_planes = [
            p for p in aeroplanes if p.country.lower() == filter_country.lower()
        ]
        print(f"\nНайдено {len(filtered_planes)} самолетов из {filter_country}:")
        for plane in filtered_planes:
            print(plane)
    else:
        filtered_planes = aeroplanes

    # Сохранение
    save_choice = input("\nСохранить данные в JSON-файл? (да/нет): ").lower()
    if save_choice == "да":
        for plane in filtered_planes:
            saver.add_aeroplane(plane)
        print("Данные успешно сохранены в data/aeroplanes.json")


if __name__ == "__main__":
    user_interaction()
