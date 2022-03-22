from typing import Protocol, Type, Union, Optional, List

from Domain.enitity import Entity


class Repository(Protocol):

    def create(self, entity: Entity) -> None:

        ...

    def read(self, entity_id: object = None) \
            -> Type[Union[Optional[Entity], List[Entity]]]:

        ...

    def update(self, entity: Entity) -> None:

        ...

    def delete(self, entity_id: str) -> None:

        ...
