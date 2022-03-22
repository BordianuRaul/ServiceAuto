from typing import Dict, Type, Union, Optional, List

import jsonpickle

from Domain.enitity import Entity
from Repositories.exceptions import DuplicateID, NoSuchID
from Repositories.repository import Repository


class FileRepository(Repository):

    def __init__(self, file_path):

        self.file_path = file_path

    def __read_file(self):
        """
        Citeste dintr-un fisier elem de tip entity
        :return:
        """
        try:
            with open(self.file_path, 'r') as the_file:
                return jsonpickle.loads(the_file.read())
        except Exception:
            return {}

    def __write_file(self, objects: Dict[int, Entity]):
        """
        Scrie intr-un fisier elem de tip entity
        :param objects:
        :return:
        """
        try:
            with open(self.file_path, 'w') as the_file:
                the_file.write(jsonpickle.dumps(objects))
        except Exception:
            pass

    def create(self, entity: Entity) -> None:
        """
       Creeaz a un obiect de tip entity
        :param entity:
        :return:
        """
        cars = self.__read_file()

        if self.read(entity.id_entity) is not None:
            raise DuplicateID(f'Exista deja o entitate cu id-ul '
                              f'{entity.id_entity}')

        cars[entity.id_entity] = entity
        self.__write_file(cars)

    def read(self, entity_id: str = None) -> \
            Type[Union[Optional[Entity], List[Entity]]]:
        """
        Verifica daca exista un obiect de tip entity
        :param entity_id: id-ul entitatii cautate
        :return:
        """
        entities = self.__read_file()

        if entity_id:

            if entity_id in entities:
                return entities[entity_id]
            else:
                return None

        return list(entities.values())

    def update(self, entity: Entity) -> None:
        """
        Actualizeaza un obiect de tip entity
        :param entity: obiectul
        :return:
        """
        entities = self.__read_file()

        if self.read(entity.id_entity) is None:
            raise NoSuchID(f'Nu exista o entitate cu id-ul {entity.id_entity}')

        entities[entity.id_entity] = entity
        self.__write_file(entities)

    def delete(self, entity_id: str) -> None:
        """
        Sterge un obiect de tip entity
        :param entity_id: id-ul obiectului
        :return:
        """
        entities = self.__read_file()

        if self.read(entity_id) is None:
            raise NoSuchID(f'Nu exista o entitate cu id-ul {entity_id}')

        del entities[entity_id]
        self.__write_file(entities)
