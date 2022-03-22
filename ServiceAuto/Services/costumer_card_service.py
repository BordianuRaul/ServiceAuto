from Domain.add_operation import AddOperation
from Domain.costumer_card import CostumerCard
from Domain.costumer_card_validator import CostumerCardValidator
from Domain.delete_operation import DeleteOperation
from Domain.update_operation import UpdateOperation
from Repositories.repository import Repository
from Services.undo_redo_service import UndoRedoService


class CostumerCardService:
    """
        Clasa care se ocupa de operatiunile pe obiectele de tip CostumerCard
        """

    def __init__(self, costumer_card_repository: Repository,
                 costumer_card_validator: CostumerCardValidator,
                 undo_redo_service: UndoRedoService):

        self.costumer_card_repository = costumer_card_repository
        self.costumer_card_validator = costumer_card_validator
        self.undo_redo_service = undo_redo_service

    def add(self, costumer_card_id: str, name: str, first_name: str,
            cnp: int, birth_date: str, date_of_registration: str):

        """

        Adauga un obiect de tip CostumerCard in repository

        """

        if not self.cnp_unique(cnp):
            raise ValueError("Pentru acest CNP exista deja un card.")

        costumer_card = CostumerCard(costumer_card_id, name, first_name,
                                     cnp, birth_date, date_of_registration)

        self.costumer_card_validator.validate(costumer_card)
        self.costumer_card_repository.create(costumer_card)

        self.undo_redo_service.clear_redo()
        costumer_card_add_op = AddOperation(self.costumer_card_repository,
                                            costumer_card)
        self.undo_redo_service.add_operation(costumer_card_add_op)

    def update(self, costumer_card_id: str, name: str, first_name: str,
               cnp: int, birth_date: str, date_of_registration: str):

        """

            Actualizaeaza un obiect de tip car din repository

        """

        if not self.cnp_unique(cnp):
            raise ValueError("Pentru acest CNP exista deja un card.")

        costumer_card_before_update = self.get_costumer_card(costumer_card_id)

        costumer_card = CostumerCard(costumer_card_id, name, first_name,
                                     cnp, birth_date, date_of_registration)

        self.costumer_card_validator.validate(costumer_card)
        self.costumer_card_repository.update(costumer_card)

        costumer_card_update_op = UpdateOperation(
            self.costumer_card_repository,
            costumer_card_before_update,
            costumer_card)

        self.undo_redo_service.clear_redo()
        self.undo_redo_service.update_operation(costumer_card_update_op)

    def delete(self, costumer_card_id: str):
        """
                Sterge un obiect de tip CostumerCard din repository
                :return:
        """

        costumer_card = self.get_costumer_card(costumer_card_id)

        self.costumer_card_repository.delete(costumer_card_id)

        costumer_card_delete_op = DeleteOperation(
            self.costumer_card_repository,
            costumer_card)
        self.undo_redo_service.clear_redo()
        self.undo_redo_service.delete_operation(costumer_card_delete_op)

    def get_costumers_cards(self):
        """
        Returneaza o lista care contine toate obiectele de tip
        CostumerCard din repository
        :return:
        """
        return self.costumer_card_repository.read(None)

    def get_costumer_card(self, costumer_card_id: str):
        """
        Returneaza obiectul de tip CostumerCard cu id-ul transmis ca parametru
        :param costumer_card_id:
        :return:
        """

        if not costumer_card_id:
            return None
        return self.costumer_card_repository.read(costumer_card_id)

    def cnp_unique(self, cnp=None):
        """
        Verifica daca cnp-ul clientului este unic
        :param cnp:cnp-ul clientului
        :return:
        """

        cards = self.get_costumers_cards()

        for elem in cards:

            if elem.CNP == cnp:
                return False
        return True
