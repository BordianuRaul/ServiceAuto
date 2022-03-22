from typing import Dict

import jsonpickle as jsonpickle

from Domain.transaction import Transaction


class TransactionRepository:
    """
     Repository pentru obiectele de tip Transaction
    """

    def __init__(self, file_path):
        self.filepath = file_path

    def __read_file(self):
        """
        Citeste dintr-un fisier elem de tip Transaction
        :return:
        """
        try:
            with open(self.filepath, 'r') as the_file:
                return jsonpickle.loads(the_file.read())
        except Exception:
            return {}

    def __write_file(self, objects: Dict[int, Transaction]):
        """
        Scrie intr-un fisier elem de tip Transaction
        :param objects:
        :return:
        """
        try:
            with open(self.filepath, 'w') as the_file:
                the_file.write(jsonpickle.dumps(objects))
        except Exception:
            pass

    def create(self, transaction: Transaction):
        """
        Creeaz a un obiect de tip Transaction
        :param transaction:
        :return:
        """
        transactions = self.__read_file()

        if self.read(transaction.id_entity) is not None:
            raise KeyError(f'Exista deja o masina cu id-ul'
                           f' {transaction.id_entity}')

        transactions[transaction.id_entity] = transaction
        self.__write_file(transactions)

    def read(self, transaction_id: str):
        """
        Verifica daca exista un obiect de tip Transaction
        :param transaction_id: id-ul obiectului cautat
        :return:
        """
        transactions = self.__read_file()

        if transaction_id:
            if transaction_id in transactions:
                return transactions[transaction_id]
            else:
                return None
        return list(transactions.values())

    def update(self, transaction: Transaction):
        """
        Actualizeaza un obiect de tip Transaction
        :param transaction: obiectul
        :return:
        """
        transactions = self.__read_file()

        if self.read(transaction.id_entity) is None:
            raise KeyError(f'Nu exista o masina cu id-ul'
                           f' {transaction.id_entity}')

        transactions[transaction.id_entity] = transaction
        self.__write_file(transactions)

    def delete(self, transaction_id):
        """
        Sterge un obiect de tip Transaction
        :param transaction_id: id-ul obiectului
        :return:
        """
        transactions = self.__read_file()

        if self.read(transaction_id) is None:
            raise KeyError(f'Nu exista o masina cu id-ul {transaction_id}')

        del transactions[transaction_id]
        self.__write_file(transactions)
