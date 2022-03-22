from Domain.car import Car


class CarValidator:
    """
    Valideaza un obiect de tip Car
    """
    def validate(self, car: Car):
        under_waranty = ["da", "nu"]

        if car.under_warranty not in under_waranty:
            raise ValueError(f'{car.under_warranty} is not an allowed value.')
