from datetime import datetime

from Domain.transaction import Transaction


class TransactionValidator:
    """
    Valideaza un obiect de tip Transaction
    """
    def validate(self, transaction: Transaction):

        try:
            datetime.strptime(transaction.date_time, '%d.%m.%Y %H:%M')

        except TypeError as tp:
            print("Formatul datei trebuie sa fie: DD.MM.YYYY H:M", tp)
