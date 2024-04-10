from typing import Any, Optional
from pydantic import BaseModel, model_validator


class PropertyDetails(BaseModel):
    title: str

    price_geo: Optional[float] = None
    unit_price_geo: Optional[float] = None
    price_usd: Optional[float] = None
    unit_price_usd: Optional[float] = None

    city: Optional[str] = None
    district: Optional[str] = None
    subdistrict: Optional[str] = None
    street: Optional[str] = None

    real_estate_type: str
    deal_type: str
    date: str

    air_conditioning: bool
    balcony: bool
    basement: bool
    cable_television: bool
    drinking_water: bool
    electricity: bool
    elevator: bool
    fridge: bool
    furniture: bool
    garage: bool
    glazed_windows: bool
    heating: bool
    hot_water: bool
    internet: bool
    iron_door: bool
    last_floor: bool
    natural_gas: bool
    security_alarm: bool
    sewage: bool
    storage: bool
    telephone: bool
    tv: bool
    washing_machine: bool
    water: bool
    wifi: bool
    pool: bool
    area: float 
    rooms: int
    bedrooms: int 
    toilet: Optional[str] = None
    floor: Optional[str] = None
    building_floors: Optional[str] = None
    project: Optional[str] = None
    status: Optional[str] = None
    state: Optional[str] = None

    agency_name: Optional[str] = None
    company_name: Optional[str] = None
    project_name: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def validate_description(cls, data: Any) -> str:
        normalized = {}
        normalized["title"] = data["title"]
        normalized["price_geo"] = data["price"]["priceGeo"]
        normalized["unit_price_geo"] = data["price"]["unitPriceGeo"]
        normalized["price_usd"] = data["price"]["priceUsd"]
        normalized["unit_price_usd"] = data["price"]["unitPriceUsd"]
        normalized["city"] = data["address"]["cityTitle"]
        normalized["district"] = data["address"]["districtTitle"]
        normalized["subdistrict"] = data["address"]["subdistrictTitle"]
        normalized["street"] = data["address"]["streetTitle"]
        normalized["real_estate_type"] = data["realEstateType"]
        normalized["deal_type"] = data["realEstateDealType"]
        normalized["date"] = data["orderDate"]
        normalized["date"] = data["orderDate"]
        normalized["air_conditioning"] = data["airConditioning"]
        normalized["balcony"] = data["balcony"]
        normalized["basement"] = data["basement"]
        normalized["cable_television"] = data["cableTelevision"]
        normalized["drinking_water"] = data["drinkingWater"]
        normalized["electricity"] = data["electricity"]
        normalized["elevator"] = data["elevator"]
        normalized["fridge"] = data["fridge"]
        normalized["furniture"] = data["furniture"]
        normalized["garage"] = data["garage"]
        normalized["glazed_windows"] = data["glazedWindows"]
        normalized["heating"] = data["heating"]
        normalized["hot_water"] = data["hotWater"]
        normalized["internet"] = data["internet"]
        normalized["iron_door"] = data["ironDoor"]
        normalized["last_floor"] = data["lastFloor"]
        normalized["natural_gas"] = data["naturalGas"]
        normalized["security_alarm"] = data["securityAlarm"]
        normalized["sewage"] = data["sewage"]
        normalized["storage"] = data["storage"]
        normalized["telephone"] = data["telephone"]
        normalized["tv"] = data["tv"]
        normalized["washing_machine"] = data["washingMachine"]
        normalized["water"] = data["water"]
        normalized["wifi"] = data["wiFi"]
        normalized["pool"] = data["withPool"]
        normalized["area"] = data["totalArea"]
        normalized["rooms"] = data["rooms"]
        normalized["bedrooms"] = data["bedrooms"]
        normalized["toilet"] = data["toilet"]
        normalized["floor"] = data["floor"]
        normalized["building_floors"] = data["floors"]
        normalized["project"] = data["project"]
        normalized["status"] = data["status"]
        normalized["state"] = data["state"]
        normalized["agency_name"] = data["agencyName"]
        normalized["company_name"] = data["companyName"]
        normalized["project_name"] = data["projectName"]

        return normalized
