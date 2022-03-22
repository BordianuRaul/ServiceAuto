from datetime import datetime

from Domain.add_operation import AddOperation
from Domain.delete_operation import DeleteOperation
from Domain.transaction import Transaction
from Domain.transaction_validator import TransactionValidator
from Domain.update_operation import UpdateOperation
from Domain.waterfall_deletion_operation import WaterfallDeletion
from Repositories.repository import Repository
from Services.car_service import CarService
from Services.costumer_card_service import CostumerCardService
from Services.sorted_clone import sorted_clone
from Services.undo_redo_service import UndoRedoService


class TransactionService:
    """
    Clasa care se ocupa de operatiunile pe obiectele de tip Transaction
    """

    def __init__(self, transaction_repository: Repository,
                 transaction_validator: TransactionValidator,
                 costumer_card_service: CostumerCardService,
                 costumer_card_repository:  Repository,
                 car_service: CarService,
                 car_repository: Repository,
                 undo_redo_service: UndoRedoService):

        self.transaction_repository = transaction_repository
        self.transaction_validator = transaction_validator
        self.costumer_card_service = costumer_card_service
        self.costumer_card_repository = costumer_card_repository
        self.car_repository = car_repository
        self.car_service = car_service
        self.undo_redo_service = undo_redo_service

    def add(self, transaction_id: str, car_id: str, costumer_card_id: str,
            cost_of_parts: float,
            cost_of_labor: float, date_and_time: str):
        """
        Adauga un obiect de tip Transaction in repository
        :param transaction_id:
        :param car_id:
        :param costumer_card_id:
        :param cost_of_parts:
        :param cost_of_labor:
        :param date_and_time:
        :return:
        """

        transaction = Transaction(transaction_id, car_id, costumer_card_id,
                                  cost_of_parts, cost_of_labor, date_and_time)
        transaction = self.costumer_card_discount(transaction)
        transaction = self.warranty_discount(transaction)

        self.transaction_validator.validate(transaction)
        self.transaction_repository.create(transaction)

        self.undo_redo_service.clear_redo()
        transaction_add_op = AddOperation(self.transaction_repository,
                                          transaction)
        self.undo_redo_service.add_operation(transaction_add_op)

    def update(self, transaction_id: str, car_id: str, costumer_card_id: str,
               cost_of_parts: float,
               cost_of_labor: float, date_and_time: str):
        """
        Actualizaeaza un obiect de tip Transaction din repository
        :param transaction_id:
        :param car_id:
        :param costumer_card_id:
        :param cost_of_parts:
        :param cost_of_labor:
        :param date_and_time:
        :return:
        """

        transaction_before_update = self.get_transaction(transaction_id)

        transaction = Transaction(transaction_id, car_id, costumer_card_id,
                                  cost_of_parts, cost_of_labor, date_and_time)

        transaction = self.costumer_card_discount(transaction)
        transaction = self.warranty_discount(transaction)
        self.transaction_validator.validate(transaction)
        self.transaction_repository.update(transaction)

        transaction_update_op = UpdateOperation(self.transaction_repository,
                                                transaction_before_update,
                                                transaction)

        self.undo_redo_service.clear_redo()
        self.undo_redo_service.update_operation(transaction_update_op)

    def delete(self, transaction_id):
        """
        Sterge un obiect de tip Transaction din repository
        :param transaction_id:
        :return:
        """

        transaction = self.get_transaction(transaction_id)

        self.transaction_repository.delete(transaction_id)

        transaction_delete_op = DeleteOperation(self.transaction_repository,
                                                transaction)
        self.undo_redo_service.clear_redo()
        self.undo_redo_service.delete_operation(transaction_delete_op)

    def get_transactions(self):
        """
        Returneaza o lista cu toate obiectele de tip Transaction din
        repository
        :return:
        """

        return self.transaction_repository.read(None)

    def get_transaction(self, transaction_id: str):
        """
        Returneaza tranzactia din repositorty cu id-ul transmis ca parametru
        :param transaction_id:
        :return:
        """

        return self.transaction_repository.read(transaction_id)

    def costumer_card_discount(self, transaction):
        """
        Ofera un discount de 10% daca exista un card client
        :param transaction:
        :return:
        """

        costumer_card_id = transaction.costumer_card_id
        if self.costumer_card_service.get_costumer_card(costumer_card_id)\
                is not None:
            print("Exista un card client, pretul pieselor va fi redus cu 10%.")
            transaction.cost_of_labor =\
                self.get_labor_discount(transaction.cost_of_labor)

        return transaction

    def get_labor_discount(self, cost_of_labor):
        """
        Se ocupa de reducerea de 10%
        :param cost_of_labor:
        :return:
        """

        reducere = cost_of_labor * (10/100)
        cost_of_labor = cost_of_labor - reducere

        return cost_of_labor

    def warranty_discount(self, transaction):
        """
        Ofera manopera gratis pentru masinile aflate in garantie
        :param transaction:
        :return:
        """

        car = self.car_service.get_car(transaction.car_id)

        if car.under_warranty == "da":
            print("Masina se afla in garantie, manopera va fi gratuita.")
            transaction.cost_of_parts = 0

        return transaction

    def all_transactions_from_an_interval(self, start: float, finish: float,
                                          transactions: list,
                                          transactions_list: list, index: int):
        """
        Returneaza o lista formata din tranzactiile cu suma totala a costurilor
        aflata intr-un interval
        :param start: capatul inferior al intervalului
        :param finish: capatul superior al intervalului
        :return:
        """

        if index in range(len(transactions)):

            if start < transactions[index].cost_of_labor + \
                    transactions[index].cost_of_parts < finish:

                transactions_list.append(transactions[index])

            return self.all_transactions_from_an_interval(start, finish,
                                                          transactions,
                                                          transactions_list,
                                                          index + 1)
        else:
            return transactions_list

    def ord_descending_by_cost_of_labor(self):
        """
        Ordoneaza tranzactiile descrescator dupa costul manoperei
        :return:
        """

        transactions = self.get_transactions()

        transactions_sorted = \
            sorted_clone(transactions,
                         lambda transaction: transaction.cost_of_labor,
                         True)

        return transactions_sorted

    def ord_descending_by_the_amount_of_discounts_applied(self):
        """
        Ordoneaza tranzactiile dupa cantitatea de reduceri aplicata
        :return:
        """

        transactions = self.get_transactions()

        transactions_with_card = []
        costumer_card_discount = []

        for transaction in transactions:

            if transaction.costumer_card_id is not None:

                transactions_with_card.append(transaction)

        transactions_with_card = sorted_clone(transactions_with_card,
                                              lambda transaction:
                                              (10*transaction.cost_of_labor)/9,
                                              True
                                              )

        for transaction in transactions_with_card:

            costumer_card_discount.append(self.costumer_card_service.
                                          get_costumer_card
                                          (transaction.costumer_card_id))

        return costumer_card_discount

    def delete_from_interval_of_time(self, date_1: str, date_2: str):

        """
        Sterge toate tranzactiile dintr-un interval de timp
        :param date_1:
        :param date_2:
        :return:
        """
        transactions = self.transaction_repository.read(None)

        date_1 = datetime.strptime(date_1, '%d.%m.%Y')
        date_1 = datetime.date(date_1)
        date_2 = datetime.strptime(date_2, '%d.%m.%Y')
        date_2 = datetime.date(date_2)

        operations = []

        self.undo_redo_service.clear_redo()

        for transaction in transactions:

            transaction_date = datetime.strptime(transaction.date_time,
                                                 '%d.%m.%Y %H:%M')
            transaction_date = datetime.date(transaction_date)

            if date_1 < transaction_date < date_2:

                transaction_op = DeleteOperation(self.transaction_repository,
                                                 transaction)
                operations.append(transaction_op)
                self.transaction_repository.delete(transaction.id_entity)
                self.undo_redo_service.delete_from_interval_of_time(operations)

    def waterfall_deletion(self, id_entity):

        """
        Sterge tranzactia cu id-ul transmis ca parametru dar si masina si
        cardoul de client asociate acestei tranzactii
        :param id_entity: id-ul tranzactiei
        :return:
        """

        if self.transaction_repository.read(id_entity) is None:
            raise ValueError("ID-ul introdus nu exista!")

        transaction = self.get_transaction(id_entity)

        costumer_card = self.costumer_card_service.get_costumer_card(
            transaction.costumer_card_id)

        car = self.car_service.get_car(transaction.car_id)

        self.car_service.delete(transaction.car_id)
        self.costumer_card_service.delete(transaction.costumer_card_id)
        self.delete(id_entity)

        water_fall_delete_op = WaterfallDeletion(self.transaction_repository,
                                                 self.costumer_card_repository,
                                                 self.car_repository,
                                                 transaction, costumer_card,
                                                 car)
        self.undo_redo_service.clear_redo()

        self.undo_redo_service.waterfall_deletion(water_fall_delete_op)
