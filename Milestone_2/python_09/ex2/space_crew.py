#!/usr/bin/env python3
from enum import Enum
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field, model_validator, ValidationError


class Rank(str, Enum):

    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)

    @model_validator(mode='after')
    def validate_mission_rules(self) -> 'SpaceMission':
        if not self.mission_id.startswith('M'):
            raise ValueError("Mission ID must start with 'M'")
        has_leadership = False
        for m in self.crew:
            if m.rank == Rank.COMMANDER or m.rank == Rank.CAPTAIN:
                has_leadership = True
                break

        if not has_leadership:
            raise ValueError("Mission must have at"
                             " least one Commander or Captain")

        if self.duration_days > 365:
            exp_count = sum(1 for m in self.crew if m.years_experience >= 5)
            if exp_count / len(self.crew) < 0.5:
                raise ValueError("Long missions (> 365 days) need"
                                 " 50% experienced crew (5+ years)")

        if not all(m.is_active for m in self.crew):
            raise ValueError("All crew members must be active")
        return self


def main() -> None:

    print("Space Mission Crew Validation")
    print("=========================================")
    try:
        crew_list = [
            CrewMember(
                member_id="CM01",
                name="Sarah Connor",
                rank=Rank.COMMANDER,
                age=40,
                specialization="Mission Command",
                years_experience=15
            ),
            CrewMember(
                member_id="CM02",
                name="John Smith",
                rank=Rank.LIEUTENANT,
                age=32,
                specialization="Navigation",
                years_experience=6
            ),
            CrewMember(
                member_id="CM03",
                name="Alice Johnson",
                rank=Rank.OFFICER,
                age=28,
                specialization="Engineering",
                years_experience=5
            )
        ]

        valid_mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime(2001, 10, 28),
            duration_days=900,
            budget_millions=2500.0,
            crew=crew_list
        )

        print("Valid mission created:")
        print(f"Mission: {valid_mission.mission_name}")
        print(f"ID: {valid_mission.mission_id}")
        print(f"Destination: {valid_mission.destination}")
        print(f"Duration: {valid_mission.duration_days} days")
        print(f"Budget: ${valid_mission.budget_millions}M")
        print(f"Crew size: {len(valid_mission.crew)}")
        print("Crew members:")
        for m in valid_mission.crew:
            print(f" - {m.name} ({m.rank.value}) {m.specialization}")
        print()
    except ValidationError as err:
        print(f"Unexpected error: {err}\n")

    print("=========================================")
    print("Expected validation error:")
    try:
        invalid_crew = [
            CrewMember(
                member_id="CM04",
                name="Bob Builder",
                rank=Rank.OFFICER,
                age=30,
                specialization="Construction",
                years_experience=2
            )
        ]

        SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime(2001, 10, 28),
            duration_days=900,
            budget_millions=2500.0,
            crew=invalid_crew
        )
    except ValidationError as err:
        print(err.errors()[0]["msg"])


if __name__ == "__main__":
    main()
