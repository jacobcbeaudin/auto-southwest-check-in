from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import pytz

JSON = Dict[str, Any]

TZ_FILE_PATH = "utils/airport_timezones.json"


class Flight:
    """
    A helper class that parses flight information received from the Southwest API.

    The flight time is automatically translated from the flight's local timezone to UTC.
    """

    def __init__(self, flight_info: Dict[str, Any], confirmation_number: str) -> None:
        self.confirmation_number = confirmation_number
        self.departure_airport = flight_info["departureAirport"]["name"]
        self.destination_airport = flight_info["arrivalAirport"]["name"]
        self.departure_time = self._get_flight_time(flight_info)
        self.flight_number = self._get_flight_number(flight_info["flights"])

        # Track to notify the user of filling out their passport information.
        # Southwest only fills the country's value for international flights
        self.is_international = flight_info["arrivalAirport"]["country"] is not None

    def __eq__(self, other: object) -> bool:
        # Define how two flights are equal to each other
        return isinstance(other, Flight) and self.flight_number == other.flight_number

    def _get_flight_time(self, flight: JSON) -> datetime:
        flight_date = f"{flight['departureDate']} {flight['departureTime']}"
        departure_airport_code = flight["departureAirport"]["code"]
        airport_timezone = self._get_airport_timezone(departure_airport_code)
        flight_time = self._convert_to_utc(flight_date, airport_timezone)

        return flight_time

    def _get_airport_timezone(self, airport_code: str) -> Any:
        project_dir = Path(__file__).parents[1]
        tz_file = project_dir / TZ_FILE_PATH
        airport_timezones = json.loads(tz_file.read_text())

        airport_timezone = pytz.timezone(airport_timezones[airport_code])
        return airport_timezone

    def _convert_to_utc(self, flight_date: str, airport_timezone: Any) -> datetime:
        flight_date = datetime.strptime(flight_date, "%Y-%m-%d %H:%M")
        flight_time = airport_timezone.localize(flight_date)
        utc_time = flight_time.astimezone(pytz.utc).replace(tzinfo=None)

        return utc_time

    def _get_flight_number(self, flights: JSON) -> str:
        flight_number = ""
        for flight in flights:
            flight_number += flight["number"] + "/"

        return flight_number.rstrip("/")
