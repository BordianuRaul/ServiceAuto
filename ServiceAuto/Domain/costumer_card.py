from dataclasses import dataclass

from Domain.enitity import Entity


@dataclass(init=True)
class CostumerCard(Entity):
    """
    Clasa pentru obiectul CostumerCard
    """
    name: str
    first_name: str
    CNP: int
    birth_date: str
    date_of_registration: str
