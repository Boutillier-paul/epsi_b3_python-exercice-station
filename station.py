from __future__ import annotations

from position import Position
from pompe import Pompe

from dataclasses import dataclass

import json
import requests

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
            services = data["services_service"].split("//") if "services_service" in data else []
        )

    @staticmethod
    def parse_from_text(data: str) -> dict:
        stations_raw_list = json.loads(data)["records"]
        stations_list = list()

        for s_raw in stations_raw_list:
            station = Station.from_dict(s_raw["fields"])
            merged = False

            for s in stations_list:
                if station.id == s.id:
                    stations_list[stations_list.index(s)].pompes.append(s.pompes[0])
                    merged = True

            if not merged:
                stations_list.append(station)

        return stations_list

    @staticmethod
    def filter_by_service(stations: list, searched_service: str) -> list:
        searched_service_stations_list = list()
        
        for s in stations:
            if searched_service in s.services:
                searched_service_stations_list.append(s)
        
        return searched_service_stations_list

    @staticmethod
    def sort_by_carburant(stations: list, fuel_type: str) -> list:
        searched_fuel_stations_list = [s for s in stations for fuel in s.pompes if fuel_type == fuel.libelle]
        sorted_stations = sorted(searched_fuel_stations_list, key=lambda s: next((fuel.price for fuel in s.pompes if fuel.libelle == fuel_type),float("inf")))
        return sorted_stations

    
class StationService:
    def __init__(self):
        pass

    def find_station_by_ville(self, ville: str) -> list:
        url = "https://data.economie.gouv.fr/api/records/1.0/search/?"
        params = {"dataset": "prix-carburants-fichier-instantane-test-ods-copie", "q": f"ville={ville.upper()}"}
        request = requests.get(url=url, params=params)
        data = Station.parse_from_text(request.content)
        return data

