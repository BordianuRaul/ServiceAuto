import jsonpickle
import random


class Generator:

    def generate_id(self) -> str:
        """
        Creeaza un id random pt fiecare masina
        json_str -> fisierul citit
        :return:
        """
        file = open("cars.json")
        json_str = file.read()
        car_list = []
        try:
            cars = jsonpickle.decode(json_str)
            for i in cars.keys():
                car_list.append(cars[i].id)
        except Exception as ex:
            print("Eroare", ex)

        file.close()

        while True:
            car_id = str(random.randint(1, 150))
            if car_id in car_list:
                continue
            else:
                return car_id

    def generate_nume(self) -> str:
        """
        Genereaza un numar random pt fiecare masina
        :return:
        """
        nume_posibile = ['Ford', 'Dacia', 'Ferrari',
                         'Lamborghini', 'BMW', 'WW',
                         'Audi', 'Mercedes',
                         'Hyundai', 'Fiat']
        return random.choice(nume_posibile)

    def generate_an(self) -> int:
        """
        Genereaza un an random pt fiecare masina
        :return:
        """
        an_posible = [2012, 2013, 2014, 2015,
                      2016, 2017, 2018, 2019,
                      2020, 2021]
        return random.choice(an_posible)

    def generate_km(self) -> int:
        """
        Genereaza un numar random de km pentru fiecare masina
        :return:
        """
        km_posible = [12342, 10000, 250, 0, 5004, 300213,
                      100, 25000, 75000, 99, 14234]
        return random.choice(km_posible)

    def generate_garantie(self) -> str:
        """
        Genreaza o valoare random pentru garantie
        :return:
        """
        garantie = ['da', 'da', 'nu', 'da', 'nu',
                    'nu', 'da', 'da', 'nu', 'da']
        return random.choice(garantie)
