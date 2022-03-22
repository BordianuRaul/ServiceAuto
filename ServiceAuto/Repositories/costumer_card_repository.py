from typing import Dict

import jsonpickle as jsonpickle

from Domain.costumer_card import CostumerCard


class CostumerCardRepository:
    """
    Repository pentru obiectele de tip CostumerCard
    """

    def __init__(self, file_path):
        self.filepath = file_path

    def __read_file(self):
        """
        Citeste dintr-un fisier elem de tip CostumerCard
        :return:
        """
        try:
            with open(self.filepath, 'r') as the_file:
                return jsonpickle.loads(the_file.read())
        except Exception:
            return {}

    def __write_file(self, objects: Dict[int, CostumerCard]):
        """
        Scrie intr-un fisier elem de tip CostumerCard
        :param objects:
        :return:
        """
        try:
            with open(self.filepath, 'w') as the_file:
                the_file.write(jsonpickle.dumps(objects))
        except Exception:
            pass

    def create(self, costumer_card: CostumerCard):
        """
        Creeaza un obiect de tip Car
        :param costumer_card:
        :return:
        """
        costumer_cards = self.__read_file()

        if self.read(costumer_card.id_entity) is not None:
            raise KeyError(f'Exista deja un card cu id-ul '
                           f'{costumer_card.id_entity}')

        costumer_cards[costumer_card.id_entity] = costumer_card
        self.__write_file(costumer_cards)

    def read(self, costumer_card_id: str):
        """
        Verifica daca exista un obiect de tip car
        :param costumer_card_id: id-ul obiectului cautat
        :return:
        """
        costumer_cards = self.__read_file()
        if costumer_card_id:
            if costumer_card_id in costumer_cards:
                return costumer_cards[costumer_card_id]
            else:
                return None
        return list(costumer_cards.values())

    def update(self, costumer_card: CostumerCard):
        """
        Actualizeaza un obiect de tip CostumerCard
        :param costumer_card: obiectul
        :return:
        """
        costumer_cards = self.__read_file()

        if self.read(costumer_card.id_entity) is None:
            raise KeyError(f'Nu exista un card cu id-ul'
                           f' {costumer_card.id_entity}')

        costumer_cards[costumer_card.id_entity] = costumer_card
        self.__write_file(costumer_cards)

    def delete(self, costumer_card_id):
        """

        :param costumer_card_id: Sterge un obiect de tip CostumerCard
        :return:
        """
        costumer_cards = self.__read_file()

        if self.read(costumer_card_id) is None:
            raise KeyError(f'Nu exista o masina cu id-ul {costumer_card_id}')

        del costumer_cards[costumer_card_id]
        self.__write_file(costumer_cards)
