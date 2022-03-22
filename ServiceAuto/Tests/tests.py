from Domain.car import Car
from Domain.car_validator import CarValidator
from Domain.costumer_card import CostumerCard
from Domain.costumer_card_validator import CostumerCardValidator
from Domain.transaction import Transaction
from Domain.transaction_validator import TransactionValidator
from Repositories.file_repository import FileRepository
from Services.car_service import CarService
from Services.costumer_card_service import CostumerCardService
from Services.full_text_search import FullTextSearch
from Services.sorted_clone import sorted_clone
from Services.transaction_service import TransactionService
from Services.undo_redo_service import UndoRedoService
from utils import clear_file


def test_car_repository():

    filename = 'test_cars.json'
    clear_file(filename)
    car_repository = FileRepository(filename)
    added = Car("1", "golf", 2001, 300, "da")
    """
    Test pentru create.
    """
    car_repository.create(added)

    assert car_repository.read(added.id_entity) == added
    """
     Test pentru update.
    """

    car_repository.update(added)

    assert car_repository.read(added.id_entity) == added
    """
    Test pentru delete.
    """

    car_repository.delete(added.id_entity)

    assert car_repository.read(added.id_entity) is None


def test_costumer_card_repository():

    filename = 'test_costumer_card.json'
    clear_file(filename)
    costumer_card_repository = FileRepository(filename)
    """
    Test pentru create.
    """
    added = CostumerCard("1", "Popescu", "George", 5020513070025,
                         "13-05-2002", "20-07-2020")

    costumer_card_repository.create(added)

    assert costumer_card_repository.read(added.id_entity) == added
    """
    Test pentru update.
    """

    added = CostumerCard("1", "Georgescu", "Paul", 5020513070025,
                         "13-05-2002", "20-07-2020")
    costumer_card_repository.update(added)

    assert costumer_card_repository.read(added.id_entity) == added
    """
    Test pentru delete
    """
    costumer_card_repository.delete(added.id_entity)

    assert costumer_card_repository.read(added.id_entity) is None

    added = CostumerCard("1", "Popescu", "George", 5020513070025,
                         "13-05-2002", "20-07-2020")

    costumer_card_repository.create(added)


def test_transaction_repository():

    """
    Test pentru create
    :return:
    """
    filename = 'test_transaction.json'
    clear_file(filename)
    transaction_repository = FileRepository(filename)

    added = Transaction("1", "1", "1", 120, 100, "17-06-2020 12:23")
    transaction_repository.create(added)

    assert transaction_repository.read(added.id_entity) == added
    """
    Test pentru update
    """

    added = Transaction("1", "1", "1", 421.32, 250, "17-06-2020")
    transaction_repository.update(added)

    assert transaction_repository.read(added.id_entity) == added
    """
    Test pentru delete
    """
    transaction_repository.delete(added.id_entity)

    assert transaction_repository.read(added.id_entity) is None


def test_ord_descending_by_cost_of_labor():

    filename = 'test_ord_desc_by_cost_of_labor.json'
    clear_file(filename)

    undo_redo_service = UndoRedoService()

    transaction_repository = FileRepository(filename)
    transaction_validator = TransactionValidator()

    costumer_card_repository = FileRepository('test_costumer_card.json')
    clear_file('test_costumer_card.json')
    costumer_card_validator = CostumerCardValidator()
    costumer_card_service = CostumerCardService(costumer_card_repository,
                                                costumer_card_validator,
                                                undo_redo_service)

    car_repository = FileRepository('test_cars.json')
    clear_file('test_cars.json')
    car_validator = CarValidator()
    car_service = CarService(car_repository,
                             car_validator,
                             undo_redo_service)

    transaction_service = TransactionService(transaction_repository,
                                             transaction_validator,
                                             costumer_card_service,
                                             costumer_card_repository,
                                             car_service,
                                             car_repository,
                                             undo_redo_service
                                             )

    added = Transaction("1", "1", "1", 421.32, 250, "17-06-2020")

    transaction_repository.create(added)

    added = Transaction("2", "2", "0", 421.32, 400, "17-05-2020")

    transaction_repository.create(added)

    added = Transaction("3", "3", "0", 421.32, 500, "17-05-2020")

    transaction_repository.create(added)

    assert transaction_service.ord_descending_by_cost_of_labor() == \
        [
            Transaction("3", "3", "0", 421.32, 500, "17-05-2020"),
            Transaction("2", "2", "0", 421.32, 400, "17-05-2020"),
            Transaction("1", "1", "1", 421.32, 250, "17-06-2020")
        ]


def test_full_text_search():

    filename = 'test_full_text_sarch.json'
    clear_file(filename)

    undo_redo_service = UndoRedoService()

    costumer_card_repository = FileRepository('test_costumer_card.json')
    clear_file('test_costumer_card.json')
    costumer_card_validator = CostumerCardValidator()
    costumer_card_service = CostumerCardService(costumer_card_repository,
                                                costumer_card_validator,
                                                undo_redo_service)

    car_repository = FileRepository('test_cars.json')
    clear_file('test_cars.json')
    car_validator = CarValidator()
    car_service = CarService(car_repository,
                             car_validator,
                             undo_redo_service)

    full_text_search = FullTextSearch(car_service,
                                      costumer_card_service)

    added = Car("1", "Audi A5", 2018, 50000, "da")
    car_repository.create(added)

    added = Car("2", "BMW 522i", 2018, 50000, "da")
    car_repository.create(added)

    added = CostumerCard("1", "Marcel", "Didinescu", 5211209016749,
                         "12-12-2000", "10-10-2020")
    costumer_card_repository.create(added)

    assert full_text_search.search_full_text("di") == (
        [Car("1", "Audi A5", 2018, 50000, "da")],
        [CostumerCard("1", "Marcel", "Didinescu", 5211209016749,
                      "12-12-2000", "10-10-2020")]

    )


def test_all_transactions_from_an_interval():

    filename = 'test_ord_desc_by_cost_of_labor.json'

    undo_redo_service = UndoRedoService()

    clear_file(filename)
    transaction_repository = FileRepository(filename)
    transaction_validator = TransactionValidator()

    costumer_card_repository = FileRepository('test_costumer_card.json')
    clear_file('test_costumer_card.json')
    costumer_card_validator = CostumerCardValidator()
    costumer_card_service = CostumerCardService(costumer_card_repository,
                                                costumer_card_validator,
                                                undo_redo_service)

    car_repository = FileRepository('test_cars.json')
    clear_file('test_cars.json')
    car_validator = CarValidator()
    car_service = CarService(car_repository,
                             car_validator,
                             undo_redo_service)

    transaction_service = TransactionService(transaction_repository,
                                             transaction_validator,
                                             costumer_card_service,
                                             costumer_card_repository,
                                             car_service,
                                             car_repository,
                                             undo_redo_service
                                             )

    added = Transaction("1", "1", "1", 421.32, 250, "17-06-2020")

    transaction_repository.create(added)

    added = Transaction("2", "2", "0", 421.32, 400, "17-05-2020")

    transaction_repository.create(added)

    added = Transaction("3", "3", "0", 421.32, 500, "17-05-2020")

    transaction_repository.create(added)

    transactions = transaction_service.get_transactions()

    assert transaction_service.all_transactions_from_an_interval(400, 900,
                                                                 transactions,
                                                                 [],
                                                                 0) == \
        [
            Transaction("1", "1", "1", 421.32, 250, "17-06-2020"),
            Transaction("2", "2", "0", 421.32, 400, "17-05-2020")
        ]


def test_ord_descending_by_the_amount_of_discounts_applied():

    filename = 'test_ord_desc_by_cost_of_labor.json'
    clear_file(filename)

    undo_redo_service = UndoRedoService()

    transaction_repository = FileRepository(filename)
    transaction_validator = TransactionValidator()

    costumer_card_repository = FileRepository('test_costumer_card.json')
    clear_file('test_costumer_card.json')
    costumer_card_validator = CostumerCardValidator()
    costumer_card_service = CostumerCardService(costumer_card_repository,
                                                costumer_card_validator,
                                                undo_redo_service)

    car_repository = FileRepository('test_cars.json')
    clear_file('test_cars.json')
    car_validator = CarValidator()
    car_service = CarService(car_repository,
                             car_validator,
                             undo_redo_service)

    transaction_service = TransactionService(transaction_repository,
                                             transaction_validator,
                                             costumer_card_service,
                                             costumer_card_repository,
                                             car_service,
                                             car_repository,
                                             undo_redo_service
                                             )
    added = Car("1", "Golf IV", 2001, 300, "nu")
    car_repository.create(added)
    added = Car("2", "Audi A5", 20015, 50000, "da")
    car_repository.create(added)
    added = Car("3", "Toyota Avensis", 2020, 1000, "da")
    car_repository.create(added)

    added = CostumerCard("1", "Popescu", "George", 5020513070025,
                         "13-05-2002", "20-07-2020")
    costumer_card_repository.create(added)

    added = CostumerCard("2", "Mihai", "Ifrim", 5020513070039,
                         "19-03-2000", "20-06-2020")
    costumer_card_repository.create(added)

    added = CostumerCard("3", "Iulian", "Marcescu", 5020513090018,
                         "20-10-2001", "20-07-2021")
    costumer_card_repository.create(added)

    added = Transaction("1", "1", "1", 421.32, 250, "17-06-2020")

    transaction_repository.create(added)

    added = Transaction("2", "2", "2", 421.32, 400, "17-05-2020")

    transaction_repository.create(added)

    added = Transaction("3", "3", "3", 421.32, 500, "17-05-2020")

    transaction_repository.create(added)

    assert transaction_service\
        .ord_descending_by_the_amount_of_discounts_applied() == [

            CostumerCard("3", "Iulian", "Marcescu", 5020513090018,
                         "20-10-2001", "20-07-2021"),
            CostumerCard("2", "Mihai", "Ifrim", 5020513070039,
                         "19-03-2000", "20-06-2020"),
            CostumerCard("1", "Popescu", "George", 5020513070025,
                         "13-05-2002", "20-07-2020")

        ]


def test_delete_from_interval_of_time():

    """
    Test pentru stergerea tuturor tranzactiilor dintr-un interval si
    undo/redo pentru aceeasi functionalitate.
    :return:
    """

    filename = 'test_ord_desc_by_cost_of_labor.json'
    clear_file('test_ord_desc_by_cost_of_labor.json')

    undo_redo_service = UndoRedoService()

    transaction_repository = FileRepository(filename)
    transaction_validator = TransactionValidator()

    costumer_card_repository = FileRepository('test_costumer_card.json')
    clear_file('test_costumer_card.json')
    costumer_card_validator = CostumerCardValidator()
    costumer_card_service = CostumerCardService(costumer_card_repository,
                                                costumer_card_validator,
                                                undo_redo_service)

    car_repository = FileRepository('test_cars.json')
    clear_file('test_cars.json')
    car_validator = CarValidator()
    car_service = CarService(car_repository,
                             car_validator,
                             undo_redo_service)

    transaction_service = TransactionService(transaction_repository,
                                             transaction_validator,
                                             costumer_card_service,
                                             costumer_card_repository,
                                             car_service,
                                             car_repository,
                                             undo_redo_service
                                             )

    car_service.add("1", "golf", 2001, 300, "nu")
    car_service.add("2", "audi A4", 2019, 70000, "nu")
    car_service.add("3", "C Klasse", 2001, 300, "nu")

    transaction_service.add("1", "1", "1", 421.32, 250, "17.06.2020 12:23")

    transaction_service.add("2", "2", "2", 421.32, 400, "17.05.2020 12:23")

    transaction_service.add("3", "3", "3", 421.32, 500, "12.12.2021 12:23")

    transaction_service.delete_from_interval_of_time("1.01.2000", "12.12.2020")
    transactions = transaction_repository.read(None)

    assert len(transactions) == 1

    undo_redo_service.undo()

    transactions = transaction_repository.read(None)

    assert len(transactions) == 3

    undo_redo_service.redo()

    transactions = transaction_repository.read(None)

    assert len(transactions) == 1


def test_update_warranty():
    """
    Test pentru actualizarea tuturor garantiilor si
    undo/redo pentru aceeasi functionalitate.
    :return:
    """

    filename = 'test_cars.json'
    clear_file(filename)

    undo_redo_service = UndoRedoService()

    car_repository = FileRepository(filename)
    car_validator = CarValidator()
    car_service = CarService(car_repository, car_validator,
                             undo_redo_service)
    added = Car("1", "golf", 2001, 300, "da")

    car_repository.create(added)

    added = Car("2", "audi A4", 2019, 70000, "da")

    car_repository.create(added)

    car_service.update_warranty()

    assert car_repository.read(None) == \
        [
            Car("1", "golf", 2001, 300, "nu"),
            Car("2", "audi A4", 2019, 70000, "nu")
        ]

    undo_redo_service.undo()

    assert car_repository.read(None) == \
        [
            Car("1", "golf", 2001, 300, "da"),
            Car("2", "audi A4", 2019, 70000, "da")
        ]

    undo_redo_service.redo()

    assert car_repository.read(None) == \
        [
            Car("1", "golf", 2001, 300, "nu"),
            Car("2", "audi A4", 2019, 70000, "nu")
        ]


def test_waterfall_deletion():

    filename = 'test_ord_desc_by_cost_of_labor.json'
    clear_file('test_ord_desc_by_cost_of_labor.json')

    undo_redo_service = UndoRedoService()

    transaction_repository = FileRepository(filename)
    transaction_validator = TransactionValidator()

    costumer_card_repository = FileRepository('test_costumer_card.json')
    clear_file('test_costumer_card.json')
    costumer_card_validator = CostumerCardValidator()
    costumer_card_service = CostumerCardService(costumer_card_repository,
                                                costumer_card_validator,
                                                undo_redo_service)

    car_repository = FileRepository('test_cars.json')
    clear_file('test_cars.json')
    car_validator = CarValidator()
    car_service = CarService(car_repository,
                             car_validator,
                             undo_redo_service)

    transaction_service = TransactionService(transaction_repository,
                                             transaction_validator,
                                             costumer_card_service,
                                             costumer_card_repository,
                                             car_service,
                                             car_repository,
                                             undo_redo_service
                                             )

    added = Car("1", "golf", 2001, 300, "da")

    car_repository.create(added)

    added = Car("2", "audi A4", 2006, 300000, "da")

    car_repository.create(added)

    added = CostumerCard("1", "Popescu", "George", 5020513070025,
                         "13-05-2002", "20-07-2020")

    costumer_card_repository.create(added)

    added = Transaction("1", "1", "1", 421.32, 250, "17.06.2020")

    transaction_repository.create(added)

    added = Transaction("2", "2", "2", 421.32, 400, "17.05.2020")

    transaction_repository.create(added)

    added = Transaction("3", "3", "3", 421.32, 500, "12.12.2021")

    transaction_repository.create(added)

    transaction_service.waterfall_deletion("1")

    assert car_repository.read(None) == [
        Car("2", "audi A4", 2006, 300000, "da")
    ]

    assert costumer_card_repository.read(None) == []

    assert transaction_repository.read(None) == [
        Transaction("2", "2", "2", 421.32, 400, "17.05.2020"),
        Transaction("3", "3", "3", 421.32, 500, "12.12.2021")
    ]


def test_undo_redo():

    undo_redo_service = UndoRedoService()

    filename = 'test_undo_redo.json'
    clear_file(filename)
    car_repository = FileRepository(filename)
    car_validator = CarValidator()
    car_service = CarService(car_repository,
                             car_validator,
                             undo_redo_service)

    car_id = "1"
    model = "Golf IV"
    year_of_acquisition = 2000
    nr_km = 30000
    under_warranty = "da"

    car_service.add(car_id, model, year_of_acquisition, nr_km, under_warranty)
    car_before_update =\
        Car(car_id, model, year_of_acquisition, nr_km, under_warranty)
    assert len(car_service.get_cars()) == 1

    undo_redo_service.undo()

    assert len(car_service.get_cars()) == 0

    undo_redo_service.redo()

    assert len(car_service.get_cars()) == 1

    car_service.delete("1")

    undo_redo_service.undo()

    assert len(car_service.get_cars()) == 1

    undo_redo_service.redo()

    assert len(car_service.get_cars()) == 0

    undo_redo_service.undo()

    year_of_acquisition = 2020
    under_warranty = "da"

    car_service.update(car_id,
                       model, year_of_acquisition, nr_km, under_warranty)

    car_after_update = Car(car_id,
                           model, year_of_acquisition, nr_km, under_warranty)

    undo_redo_service.undo()

    assert car_service.get_car(car_id) == car_before_update

    undo_redo_service.redo()

    assert car_service.get_car(car_id) == car_after_update


def test_sorted_clone():

    random_list = [3, 1, 2]

    ord_list = sorted_clone(random_list, lambda x: x, True)

    assert ord_list == [3, 2, 1]
