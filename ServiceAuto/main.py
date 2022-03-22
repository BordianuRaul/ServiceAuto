from Domain.car_validator import CarValidator
from Domain.costumer_card_validator import CostumerCardValidator
from Domain.transaction_validator import TransactionValidator
from Repositories.file_repository import FileRepository
from Services.car_service import CarService
from Services.costumer_card_service import CostumerCardService
from Services.entity_generator import Generator
from Services.full_text_search import FullTextSearch
from Services.transaction_service import TransactionService
from Services.undo_redo_service import UndoRedoService
from Tests.tests import test_transaction_repository, \
    test_costumer_card_repository, test_car_repository, \
    test_ord_descending_by_cost_of_labor, test_full_text_search, \
    test_all_transactions_from_an_interval, \
    test_ord_descending_by_the_amount_of_discounts_applied, \
    test_delete_from_interval_of_time, test_update_warranty, \
    test_waterfall_deletion, test_undo_redo, test_sorted_clone
from user_interface.console import Console


def main():

    undo_redo_service = UndoRedoService()

    car_repository = FileRepository('cars.json')
    car_validator = CarValidator()
    car_service = CarService(car_repository, car_validator,
                             undo_redo_service)

    costumer_card_repository = FileRepository('costumer_card.json')
    costumer_card_validator = CostumerCardValidator()
    costumer_card_service = CostumerCardService(costumer_card_repository,
                                                costumer_card_validator,
                                                undo_redo_service)

    transaction_repository = FileRepository('transaction.json')
    transaction_validator = TransactionValidator()
    generator = Generator()
    full_text_search = FullTextSearch(car_service, costumer_card_service)
    transaction_service = TransactionService(transaction_repository,
                                             transaction_validator,
                                             costumer_card_service,
                                             costumer_card_repository,
                                             car_service,
                                             car_repository,
                                             undo_redo_service)

    console = Console(car_service, costumer_card_service, transaction_service,
                      full_text_search,
                      generator,
                      undo_redo_service)
    console.run_console()


if __name__ == '__main__':

    test_car_repository()
    test_costumer_card_repository()
    test_transaction_repository()
    test_full_text_search()
    test_all_transactions_from_an_interval()
    test_ord_descending_by_cost_of_labor()
    test_ord_descending_by_the_amount_of_discounts_applied()
    test_delete_from_interval_of_time()
    test_update_warranty()
    test_waterfall_deletion()
    test_undo_redo()
    test_sorted_clone()

    main()
