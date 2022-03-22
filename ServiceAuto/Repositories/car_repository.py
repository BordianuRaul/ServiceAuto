from typing import Dict

import jsonpickle as jsonpickle

from Domain.car import Car


class CarRepository:
    """
    Repository pentru obiectele de tip Car
    """

    def __init__(self, file_path):
        self.filepath = file_path

    def __read_file(self):
        """
        Citeste dintr-un fisier elem de tip Car
        :return:
        """
        try:
            with open(self.filepath, 'r') as the_file:
                return jsonpickle.loads(the_file.read())
        except Exception:
            return {}

    def __write_file(self, objects: Dict[int, Car]):
        """
        Scrie intr-un fisier elem de tip Car
        :param objects:
        :return:
        """
        try:
            with open(self.filepath, 'w') as the_file:
                the_file.write(jsonpickle.dumps(objects))
        except Exception:
            pass

    def create(self, car: Car):
        """
       Creeaz a un obiect de tip Car
        :param car:
        :return:
        """
        cars = self.__read_file()

        if self.read(car.id_entity) is not None:
            raise KeyError(f'Exista deja o masina cu id-ul {car.id_entity}')

        cars[car.id_entity] = car
        self.__write_file(cars)

    def read(self, car_id: str):
        """
        Verifica daca exista un obiect de tip car
        :param car_id: id-ul obiectului cautat
        :return:
        """
        cars = self.__read_file()

        if car_id:
            if car_id in cars:
                return cars[car_id]
            else:
                return None

        return list(cars.values())

    def update(self, car: Car):
        """
        Actualizeaza un obiect de tip Car
        :param car: obiectul
        :return:
        """
        cars = self.__read_file()

        if self.read(car.id_entity) is None:
            raise KeyError(f'Nu exista o masina cu id-ul {car.id_entity}')

        cars[car.id_entity] = car
        self.__write_file(cars)

    def delete(self, car_id):
        """
        Sterge un obiect de tip Car
        :param car_id: id-ul obiectului
        :return:
        """
        cars = self.__read_file()

        if self.read(car_id) is None:
            raise KeyError(f'Nu exista o masina cu id-ul {car_id}')

        del cars[car_id]
        self.__write_file(cars)
