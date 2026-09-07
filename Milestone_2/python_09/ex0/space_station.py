#!/usr/bin/env python3
from pydantic import BaseModel, Field, ValidationError
from typing import Optional
from datetime import datetime


class SpaceStation(BaseModel):

    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(default=None, max_length=200)


def main() -> None:

    print("Space Station Data Validation")
    print("========================================")
    try:
        mex18 = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime(2001, 10, 28),
            is_operational=True
            )
        print("Valid station created:")
        print(f"ID: {mex18.station_id}")
        print(f"Name: {mex18.name}")
        print(f"Crew: {mex18.crew_size}")
        print(f"Power: {mex18.power_level}")
        print(f"Oxygen: {mex18.oxygen_level}")
        status = "Operational" if mex18.is_operational else "Nonoperational"
        print(f"Status: {status}\n")
        print("========================================")
    except ValidationError as err:
        print(f"Unexpected validation error:\n{err}")

    try:
        mex18 = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=100,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime(2001, 10, 28),
            is_operational=True
            )
    except ValidationError as err:
        print("Expected validation error:")
        print(err.errors()[0]["msg"])


if __name__ == "__main__":
    main()
