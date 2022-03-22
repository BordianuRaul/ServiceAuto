from Services.car_service import CarService
from Services.costumer_card_service import CostumerCardService


class FullTextSearch:

    def __init__(self, car_service: CarService,
                 costumer_card_service: CostumerCardService):

        self.car_service = car_service
        self.costumer_card_service = costumer_card_service

    def search_full_text(self, text):
        """

        :param text:
        :return:
        """
        cars_cautate = self.car_search(text)
        cards_cautate = self.costumer_card_search(text)
        return cars_cautate, cards_cautate

    def car_search(self, text):

        cars = list(self.car_service.get_cars())

        cars_found = [car for car in cars if text in car.model or
                      text in str(car.year_of_acquisition) or
                      text in str(car.nr_km) or
                      text in car.under_warranty]

        return cars_found

    def costumer_card_search(self, text):

        costumers_cards = \
            list(self.costumer_card_service.get_costumers_cards())

        costumers_cards_found = [costumer_card for costumer_card in
                                 costumers_cards
                                 if text in costumer_card.name or
                                 text in costumer_card.first_name or
                                 text in str(costumer_card.CNP) or
                                 text in str(costumer_card.birth_date) or
                                 text in
                                 str(costumer_card.date_of_registration)]

        return costumers_cards_found
