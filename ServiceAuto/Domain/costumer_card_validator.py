from datetime import datetime

from Domain.costumer_card import CostumerCard


class CostumerCardValidator:
    """
    Valideaza un obiect de tip CostumerCard
    """
    def validate(self, costumer_card: CostumerCard):

        try:
            datetime.strptime(costumer_card.birth_date, '%d-%m-%Y')
            datetime.strptime(costumer_card.date_of_registration, '%d-%m-%Y')

        except TypeError as tp:
            print("Formatul datei trebuie sa fie: DD-MM-YYYY", tp)
