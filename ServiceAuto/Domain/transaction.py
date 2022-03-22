from dataclasses import dataclass

from Domain.enitity import Entity


@dataclass(init=True)
class Transaction(Entity):
    """
    Clasa pentru obiectul Transaction
    """
    car_id: str
    costumer_card_id: str
    cost_of_parts: float
    cost_of_labor: float
    date_time: str
