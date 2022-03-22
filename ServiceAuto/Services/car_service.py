from Domain.add_operation import AddOperation
from Domain.car import Car
from Domain.car_validator import CarValidator
from Domain.delete_operation import DeleteOperation
from Domain.update_operation import UpdateOperation
from Repositories.repository import Repository
from Services.undo_redo_service import UndoRedoService


class CarService:
    """
    Clasa care se ocupa de operatiunile pe obiectele de tip Car
    """

    def __init__(self, car_repository: Repository,
                 car_validator: CarValidator,
                 undo_redo_service: UndoRedoService):

        self.car_repository = car_repository
        self.car_validator = car_validator
        self.undo_redo_service = undo_redo_service

    def add(self, car_id: str, model: str, year_of_acquisition: int,
            nr_km: int, under_warranty: str):
        """
        Adauga un obiect de tip Car in repository
        """

        car = Car(car_id, model, year_of_acquisition, nr_km, under_warranty)

        self.car_validator.validate(car)
        self.car_repository.create(car)

        car_add_op = AddOperation(self.car_repository, car)
        self.undo_redo_service.clear_redo()
        self.undo_redo_service.add_operation(car_add_op)

    def update(self, car_id: str, model: str,
               year_of_acquisition: int, nr_km: int, under_warranty: str):
        """
        Actualizaeaza un obiect de tip Car din repository
        """

        car_before_update = self.get_car(car_id)

        car = Car(car_id, model, year_of_acquisition, nr_km, under_warranty)
        self.car_validator.validate(car)
        self.car_repository.update(car)

        car_update_op = UpdateOperation(self.car_repository,
                                        car_before_update,
                                        car)

        self.undo_redo_service.clear_redo()
        self.undo_redo_service.update_operation(car_update_op)

    def delete(self, car_id: str):
        """
        Sterge un obiect de tip Car din repository
        :param car_id:
        :return:
        """

        car = self.car_repository.read(car_id)
        self.car_repository.delete(car_id)

        car_delete_op = DeleteOperation(self.car_repository,
                                        car)
        self.undo_redo_service.clear_redo()
        self.undo_redo_service.delete_operation(car_delete_op)

    def get_cars(self):
        """
        Returneaza o lista care contine toate obiectele de tip car din
        repository
        :return:
        """

        return self.car_repository.read(None)

    def get_car(self, car_id: str):
        """
        Returneaza obiectul de tip car cu id-ul transmis ca parametru
        :param car_id:
        :return:
        """

        return self.car_repository.read(car_id)

    def update_warranty(self):
        """
        Actualizeaza garantia pentru fiecare masina
        :return:
        """

        cars = self.car_repository.read(None)
        operations = []

        cars_under_warranty = [car for car in cars
                               if 2021 - car.year_of_acquisition <= 3 and
                               car.nr_km <= 60000]

        cars_not_under_warranty = [car for car in cars
                                   if 2021 - car.year_of_acquisition > 3 or
                                   car.nr_km > 60000]

        for car in cars_under_warranty:

            car_before_update = self.get_car(car.id_entity)

            car.under_warranty = "da"
            self.car_repository.update(car)

            car_after_update = self.get_car(car.id_entity)

            car_update_op = UpdateOperation(self.car_repository,
                                            car_before_update,
                                            car_after_update)

            operations.append(car_update_op)

        for car in cars_not_under_warranty:
            car_before_update = self.get_car(car.id_entity)

            car.under_warranty = "nu"
            self.car_repository.update(car)

            car_after_update = self.get_car(car.id_entity)

            car_update_op = UpdateOperation(self.car_repository,
                                            car_before_update,
                                            car_after_update)

            operations.append(car_update_op)

        self.undo_redo_service.update_warranty(operations)
