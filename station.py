from __future__ import annotations

from position import Position
from pompe import Pompe

from dataclasses import dataclass

import json

@dataclass
class Station:
    id: int
    ville: str
    cp: str
    departement: str
    region: str
    adresse: str
    epci_nom: str
    flag_automate_24: bool
    position: Position
    pompes: list
    services: list

    @staticmethod
    def from_dict(data: dict) -> Station:
        return Station(
            id = data["id"],
            ville = data["ville"],
            cp = data["com_code"],
            departement = data["dep_name"],
            region = data["reg_name"],
            adresse = data["adresse"],
            epci_nom = data["epci_name"],
            position = Position(data["geom"][0], data["geom"][1]),
            flag_automate_24 = data["horaires_automate_24_24"],
            pompes = [Pompe(data["prix_valeur"], data["prix_nom"])],
            services = data["services_service"].split("//")
        )

    @staticmethod
    def parse_from_text(data: str) -> dict:
        stations_raw_list = json.loads(data)["records"]

        # Ca c'est pas bon
        stations_list = list({v['id']:v for v in stations_raw_list}.values())

        

        return stations_list