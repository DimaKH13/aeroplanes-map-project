import os
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from src.aeroplane import Aeroplane
from src.api import AeroplanesAPI
from src.json_saver import JSONSaver


def test_aeroplane_init_and_str() -> None:
    plane = Aeroplane("UAL1621", "United States", 268.79, 10203.18)
    assert plane.callsign == "UAL1621"
    assert "Борт UAL1621" in str(plane)


def test_aeroplane_comparison() -> None:
    plane1 = Aeroplane("A1", "CountryA", 200.0, 10000.0)
    plane2 = Aeroplane("A2", "CountryB", 300.0, 12000.0)
    assert plane1 < plane2
    assert plane2 > plane1


def test_cast_to_object_list() -> None:
    mock_data = {
        "states": [
            [
                "4b1812",
                "SWR438A ",
                "Switzerland",
                0,
                0,
                0.0,
                0.0,
                4267.2,
                False,
                189.7,
                0,
                0,
                None,
                0,
                "",
                False,
                0,
            ],
            [
                "4b1813",
                None,
                "France",
                0,
                0,
                0.0,
                0.0,
                3000.0,
                False,
                150.0,
                0,
                0,
                None,
                0,
                "",
                False,
                0,
            ],
        ]
    }
    planes = Aeroplane.cast_to_object_list(mock_data)
    assert len(planes) == 2
    assert planes[0].callsign == "SWR438A"
    assert planes[1].callsign == "Unknown"


def test_cast_to_object_list_empty() -> None:
    assert Aeroplane.cast_to_object_list({}) == []
    assert Aeroplane.cast_to_object_list({"states": None}) == []


@patch("src.api.requests.get")
def test_api_get_aeroplanes_success(mock_get: Mock) -> None:
    mock_nominatim_resp = Mock()
    mock_nominatim_resp.status_code = 200
    mock_nominatim_resp.json.return_value = [
        {"boundingbox": ["40.0", "50.0", "-10.0", "10.0"]}
    ]

    mock_opensky_resp = Mock()
    mock_opensky_resp.status_code = 200
    mock_opensky_resp.json.return_value = {"states": []}

    mock_get.side_effect = [mock_nominatim_resp, mock_opensky_resp]

    api = AeroplanesAPI()
    result = api.get_aeroplanes("Spain")

    assert result == {"states": []}
    assert mock_get.call_count == 2


@patch("src.api.requests.get")
def test_api_get_aeroplanes_not_found(
    mock_get: Mock, capsys: pytest.CaptureFixture
) -> None:
    mock_nominatim_resp = Mock()
    mock_nominatim_resp.status_code = 200
    mock_nominatim_resp.json.return_value = []

    mock_get.return_value = mock_nominatim_resp

    api = AeroplanesAPI()
    result = api.get_aeroplanes("Narnia")

    assert result is None
    captured = capsys.readouterr()
    assert "не найдена" in captured.out


def test_json_saver(tmp_path: Path) -> None:
    test_file = tmp_path / "test_planes.json"
    saver = JSONSaver(filename=str(test_file))
    plane = Aeroplane("TEST1", "Russia", 200.0, 10000.0)

    saver.add_aeroplane(plane)
    assert os.path.exists(test_file)

    data = saver.get_aeroplanes()
    assert len(data) == 1
    assert data[0]["callsign"] == "TEST1"

    saver.delete_aeroplane(plane)
    data_after = saver.get_aeroplanes()
    assert len(data_after) == 0
