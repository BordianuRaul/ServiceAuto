from dataclasses import dataclass

from Domain.enitity import Entity


@dataclass(init=True)
class Car(Entity):
    """
    Clasa pentru obiectul Car
    """

    model: str
    year_of_acquisition: int
    nr_km: int
    under_warranty: str
