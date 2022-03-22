from datetime import datetime

from Services.car_service import CarService
from Services.costumer_card_service import CostumerCardService
from Services.entity_generator import Generator
from Services.full_text_search import FullTextSearch
from Services.transaction_service import TransactionService
from Services.undo_redo_service import UndoRedoService


class Console:
    """
    Clasa pentru gestionarea consolei cu care interactioneaza utilizatorul
    """

    def __init__(self, car_service: CarService,
                 costumer_card_service: CostumerCardService,
                 transaction_service: TransactionService,
                 full_text_search: FullTextSearch,
                 generator: Generator,
                 undo_redo_service: UndoRedoService):
        self.car_service = car_service
        self.costumer_card_service = costumer_card_service
        self.transaction_service = transaction_service
        self.generator = generator
        self.full_text_search = full_text_search
        self.undo_redo_service = undo_redo_service

    def show_menu(self):

        print("a[car|card|tranz]- adaugare masina, card client sau tranzactie")
        print("u[car|card|tranz]- update masina, card client sau tranzactie")
        print("d[car|card|tranz]- delete masina, card client sau tranzactie")
        print("s[car|card|tranz]- show all masina, card client sau tranzactie")
        print("rcar- generare de n masini in mod aleatoriu")
        print("1- Cautare full text pentru masini si carduri client")
        print("2- Afișarea tuturor tranzacțiilor cu suma dintr-un interval")
        print("3- Afisarea masinilor descrescator dupa pretul manoperei.")
        print("4- Afișarea cardurilor client ordonate descrescător după"
              " valoarea reducerilor obținute.")
        print("5- Sterge toate tranzactiile dintr-un interval de timp")
        print("6- Actualizeaza garantiile tuturor masinilor")
        print("7- Stergere in cascada")
        print("u- Undo")
        print("r- Redo")
        print("x- Iesire")

    def run_console(self):

        while True:
            self.show_menu()
            optiune = input("Selectati optiunea: ")

            if optiune == "acar":
                self.handle_add_car()

            elif optiune == "acard":
                self.handle_add_costumer_card()

            elif optiune == "atranz":
                self.handle_add_transaction()

            elif optiune == "ucar":
                self.handle_update_car()

            elif optiune == "ucard":
                self.handle_update_costumer_card()

            elif optiune == "utranz":
                self.handle_update_transaction()

            elif optiune == "dcar":
                self.handle_delete_car()

            elif optiune == "dcard":
                self.handle_delete_costumer_card()

            elif optiune == "dtranz":
                self.handle_delete_transaction()

            elif optiune == "scar":
                self.handle_show_all(self.car_service.get_cars())

            elif optiune == "scard":
                self.handle_show_all(
                    self.costumer_card_service.get_costumers_cards())

            elif optiune == "stranz":
                self.handle_show_all(
                    self.transaction_service.get_transactions())

            elif optiune == "rcar":
                self.handle_random_generator()

            elif optiune == "1":
                self.handle_full_text_search()

            elif optiune == "2":
                self.handle_show_all_transactions_from_interval()

            elif optiune == "3":
                self.handle_ord_descending_by_cost_of_labor()

            elif optiune == "4":
                self.handle_ord_descending_by_the_amount_of_discounts_applied()

            elif optiune == "5":
                self.handle_delete_from_interval_of_time()

            elif optiune == "6":
                self.handle_update_warranty()

            elif optiune == "7":
                self.handle_waterfall_deletion()

            elif optiune == "u":
                self.undo_redo_service.undo()

            elif optiune == "r":
                self.undo_redo_service.redo()

            elif optiune == "x":
                break

            else:
                print("Opitune invalida!"
                      "Reincercati")

    def handle_add_car(self):
        try:
            car_id = input("Introduceti ID-ul masinii: ")
            model = input("Introduceti modelul: ")

            year_of_acquisition = int(input("Introduceti anulul achizitiei: "))
            if year_of_acquisition < 0:
                raise ValueError("Anul nu poate fi negativ.")

            nr_km = int(input("Introduceti numarul de km: "))
            if nr_km < 0:
                raise ValueError("Numarul de km nu poate fi mai mic decat 0.")

            under_warranty = input("Este in garantie? [da/nu]: ")

            self.car_service.add(car_id, model, year_of_acquisition, nr_km,
                                 under_warranty)

        except ValueError as ve:
            print("Eroare de validare.", ve)
        except KeyError as ke:
            print("Eroare de id.", ke)
        except Exception as ex:
            print("Eroare.", ex)

    def handle_add_costumer_card(self):
        try:

            costumer_card_id = input("Introduceti ID-ul cardului de client: ")
            name = input("Introduceti numele: ")
            first_name = input("Introduceti prenumele: ")
            cnp = int(input("Introduceti CNP-ul: "))
            if cnp < 0:
                raise ValueError("CNP-ul nu poate fi un numar negativ.")
            birth_date = input("Introduceti data de nastere (dd-mm-yyyy): ")
            date_of_registration = input("Introduceti data inregistrarii"
                                         " (dd-mm-yyyy): ")

            self.costumer_card_service.add(costumer_card_id, name, first_name,
                                           cnp, birth_date,
                                           date_of_registration)
        except ValueError as ve:
            print("Eroare de validare.", ve)
        except KeyError as ke:
            print("Eroare de id.", ke)
        except Exception as ex:
            print("Eroare.", ex)

    def handle_add_transaction(self):

        try:

            transaction_id = input("Introduceti ID-ul tranzactiei: ")
            car_id = input("Introcetu ID-ul masinii: ")
            costumer_card_id = input("Introduceti ID-ul cardului de client: ")
            cost_of_parts = float(input("Introduceti suma pieselor: "))
            cost_of_labor = float(input("Introduceti suma manoperei: "))
            date_and_time = input("Introduceti data si ora"
                                  " [dd.mm.yyyy hh:mm]: ")

            self.transaction_service.add(transaction_id, car_id,
                                         costumer_card_id, cost_of_parts,
                                         cost_of_labor, date_and_time)

            transaction =\
                self.transaction_service.get_transaction(transaction_id)

            total_price = transaction.cost_of_parts + transaction.cost_of_labor
            print(f'Pretul platit este in total de {total_price} de lei.')

        except ValueError as ve:
            print("Eroare de validare.", ve)
        except TypeError as te:
            print("Eroare de id.", te)
        except Exception as ex:
            print("Eroare.", ex)

    def handle_update_car(self):

        try:

            car_id = input("Introduceti ID-ul masinii"
                           " pe care doriti o modificati: ")
            model = input("Introduceti modelul: ")

            year_of_acquisition = int(input("Introduceti anulul achizitiei: "))
            if year_of_acquisition < 0:
                raise ValueError("Anul nu poate fi negativ.")

            nr_km = int(input("Introduceti numarul de km: "))
            if nr_km < 0:
                raise ValueError("Numarul de km nu poate fi mai mic decat 0.")

            under_warranty = input("Este in garantie? [da/nu]: ")

            self.car_service.update(car_id, model, year_of_acquisition,
                                    nr_km, under_warranty)

        except ValueError as ve:
            print("Eroare de validare.", ve)
        except KeyError as ke:
            print("Eroare de id.", ke)
        except Exception as ex:
            print("Eroare.", ex)

    def handle_update_costumer_card(self):
        try:

            costumer_card_id = input("Introduceti ID-ul cardului de client"
                                     " pe care doriti sa il modificati: ")
            name = input("Introduceti numele: ")
            first_name = input("Introduceti prenumele: ")
            cnp = int(input("Introduceti CNP-ul: "))
            if cnp < 0:
                raise ValueError("CNP-ul nu poate fi un numar negativ.")

            birth_date = input("Introduceti data de nastere (dd.mm.yyyy): ")
            date_of_registration = input("Introduceti data inregistrarii"
                                         " (dd-mm-yyyy): ")

            self.costumer_card_service.update(costumer_card_id, name,
                                              first_name, cnp, birth_date,
                                              date_of_registration)
        except ValueError as ve:
            print("Eroare de validare.", ve)
        except KeyError as ke:
            print("Eroare de id.", ke)
        except Exception as ex:
            print("Eroare.", ex)

    def handle_update_transaction(self):

        try:

            transaction_id = input("Introduceti ID-ul tranzactiei"
                                   " pe care doriti sa o modificati: ")
            car_id = input("Introcetu ID-ul masinii: ")
            costumer_card_id = input("Introduceti ID-ul cardului de client: ")
            cost_of_parts = float(input("Introduceti suma pieselor: "))
            cost_of_labor = float(input("Introduceti suma manoperei: "))
            date_and_time = input("Introduceti data si ora"
                                  " [dd-mm-yyyy hh:mm]: ")

            self.transaction_service.update(transaction_id, car_id,
                                            costumer_card_id, cost_of_parts,
                                            cost_of_labor, date_and_time)

            transaction =\
                self.transaction_service.get_transaction(transaction_id)
            total_price = transaction.cost_of_parts + transaction.cost_of_labor
            print(f'Pretul platit este in total de {total_price} de lei.')

        except ValueError as ve:
            print("Eroare de validare.", ve)
        except TypeError as te:
            print("Eroare de id.", te)
        except Exception as ex:
            print("Eroare.", ex)

    def handle_delete_car(self):

        try:

            id_car = input("Introduceti ID-ul masinii pe care doriti"
                           " sa o stergeti: ")

            self.car_service.delete(id_car)

        except TypeError as te:
            print("Eroare de id", te)
        except Exception as ex:
            print("Eroare", ex)

    def handle_delete_costumer_card(self):

        try:

            id_costumer_card = input("Introduceti ID-ul cardului pe care"
                                     " doriti sa o stergeti: ")

            self.costumer_card_service.delete(id_costumer_card)

        except TypeError as te:
            print("Eroare de id", te)
        except Exception as ex:
            print("Eroare", ex)

    def handle_delete_transaction(self):

        try:

            id_transaction = input("Introduceti ID-ul tranzactiei pe care"
                                   " doriti sa o stergeti: ")

            self.transaction_service.delete(id_transaction)

        except TypeError as te:
            print("Eroare de id", te)
        except Exception as ex:
            print("Eroare", ex)

    def handle_show_all(self, objects):

        for obj in objects:
            print(obj)

    def handle_random_generator(self):

        """
                Random car generator
                :return:
                """

        try:
            n = int(input("Introduceti numarul de masini formate aleatoriu: "))
            for i in range(0, n):
                self.car_service.add(self.generator.generate_id(),
                                     self.generator.generate_nume(),
                                     self.generator.generate_an(),
                                     self.generator.generate_km(),
                                     self.generator.generate_garantie())

        except ValueError as ve:
            print('Eroare', ve)

    def handle_show_all_transactions_from_interval(self):

        try:

            start = float(input("Introduceti marginea"
                                " inferioara a intervalului: "))
            finish = float(input("Introduceti marginea"
                                 " superioara a intervalului: "))

            transactions = self.transaction_service.get_transactions()

            transactions_list =\
                self.transaction_service.\
                all_transactions_from_an_interval(start, finish,
                                                  transactions, [],
                                                  0)

            print("Rezultatele sunt: ")
            for transaction in transactions_list:

                print(transaction)

        except ValueError as ve:
            print("Eroare de validare", ve)

        except Exception as ex:
            print("Eroare", ex)

    def handle_ord_descending_by_cost_of_labor(self):

        transactions_sorted = \
            self.transaction_service.ord_descending_by_cost_of_labor()

        for transaction in transactions_sorted:

            print(self.car_service.get_car(transaction.car_id))

    def handle_full_text_search(self):

        text = input("Introduceti text-ul dupa care sa se caute masinile si "
                     "cardurile de client: ")

        cars_searched, cards_searched =\
            self.full_text_search.search_full_text(text)

        print(f"Masini: {cars_searched}")
        print(f"Carduri client: {cards_searched}")

    def handle_ord_descending_by_the_amount_of_discounts_applied(self):

        cards_clients_sorted = \
            self.transaction_service.\
            ord_descending_by_the_amount_of_discounts_applied()

        for card_client in cards_clients_sorted:
            print(card_client)

    def handle_delete_from_interval_of_time(self):

        """
        Sterge toate tranzactiile dintr-un interval de timp
        :return:
        """
        try:
            date_1 = input("Introduceti prima data(dd.mm.yyyy): ")
            datetime.strptime(date_1, '%d.%m.%Y')
            date_2 = input("Introduceti a doua data(dd.mm.yyyy) ")
            datetime.strptime(date_2, '%d.%m.%Y')

            self.transaction_service.\
                delete_from_interval_of_time(date_1, date_2)

        except ValueError as ve:
            print("Data introdusa nu este valida(dd.mm.yyyy).", ve)
        except Exception as ex:
            print("Eroare", ex)

    def handle_update_warranty(self):
        """
        Actualizeaza garantia tuturor masinilor.
        :return:
        """

        self.car_service.update_warranty()

    def handle_waterfall_deletion(self):

        try:

            id_transaction = input("Introduceti id-ul transactiei pentru"
                                   "care sa se execute stergerea in cascada: ")

            self.transaction_service.waterfall_deletion(id_transaction)
        except ValueError as ve:
            print("Eroare de validare.", ve)
        except TypeError as te:
            print("Eroare de id", te)
        except Exception as ex:
            print("Eroare", ex)
