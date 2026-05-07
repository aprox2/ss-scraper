from dataclasses import dataclass


@dataclass
class CarListing:
    id: str
    url: str
    title: str
    model: str
    year: str
    engine: str
    mileage: str
    price: str
    make_name: str


@dataclass
class CarDetails:
    id: str
    url: str
    make: str
    model: str
    year: str
    engine: str
    fuel_type: str
    mileage: str
    tech_inspection: str
    price: str
