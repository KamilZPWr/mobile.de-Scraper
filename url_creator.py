from enum import Enum
from typing import Union, List

import numpy
from bs4 import BeautifulSoup

from main import get


class SellerType(Enum):
    PRIVATE = 'ONLY_FSBO_ADS'
    DEALER = 'ONLY_DEALER_ADS'
    COMPANY = 'ONLY_COMMERCIAL_FSBO_ADS'


class Country(Enum):
    GERMANY = 'DE'


class URLCreator:
    SELLER_TYPE_ARG = 'adLimitation'
    COUNTRY_ARG = 'ce'
    MIN_PRICE_ARG = 'minPrice'
    MAX_PRICE_ARG = 'maxPrice'
    MAX_HORSE_STRENGTH_ARG = 'maxPowerAsArray'
    MIN_HORSE_STRENGTH_ARG = 'minPowerAsArray'
    MAX_POWER_TYPE = 'maxPowerAsArray=PS'
    MIN_POWER_TYPE = 'minPowerAsArray=PS'
    MAX_FIRST_REGISTRATION_DATE_ARG = 'maxFirstRegistrationDate'
    MIN_FIRST_REGISTRATION_DATE_ARG = 'minFirstRegistrationDate'
    MAX_MILEAGE_ARG = 'maxMileage'
    MIN_MILEAGE_ARG = 'minMileage'
    CAR_TYPE_ARG = 'ms'
    DEFAULT_URL = 'https://suchen.mobile.de/fahrzeuge/search.html?dam=0&isSearchRequest=true&sfmr=false&vc=Car&sortOption.sortBy=creationTime&sortOption.sortOrder=DESCENDING'

    def get_search_page_links(self, min_price: int, max_price: int,
                              base_url: str = DEFAULT_URL, seller_type: SellerType = None, country: Country = None,
                              min_horse_power: int = None, max_horse_power: int = None,
                              max_first_registration: int = None, min_first_registration: int = None,
                              min_mileage: int = None, max_mileage: int = None,
                              car_brand: int = None, car_type: Union[int, str] = None) -> List[str]:
        """
        Creates urls with search results. Mobile.de had limited number of search results to 50 pages (20 ads each) and
        if search results count more than 1000 ads then price filter will be divided into smaller slices.

        :param min_price: Min price in Euro
        :param max_price: Max price in Euro
        :param base_url: [Optional] Base search URL to which code will add expected filters
        :param seller_type: [Optional] Enum value of SellerType
        :param country: [Optional] Enum value of Country
        :param min_horse_power: [Optional] Min horse power
        :param max_horse_power: [Optional] Max horse power
        :param max_first_registration: [Optional] Max value of first registration year
        :param min_first_registration: [Optional] Min value of first registration year
        :param min_mileage: [Optional] Min mileage in km
        :param max_mileage: [Optional] Max mileage in km
        :param car_brand: [Optional] Car Brand id based on Dict with CAR_BRANDS
        :param car_type: [Optional] Car Type id based on Dict with CAR_BRANDS
        :return: List with created urls
        """

        url = self.create_url(
            base_url, seller_type, country,
            min_price, max_price,
            min_horse_power, max_horse_power,
            max_first_registration, min_first_registration,
            min_mileage, max_mileage,
            car_brand, car_type
        )

        number_of_results = self.check_number_of_results(url)

        if number_of_results > 1000:
            urls = []
            n = int(numpy.ceil((max_price - min_price) / 100))
            for i in range(n):
                tmp_min_price = min_price + (100 * i) + 1
                tmp_max_price = min_price + 100 * (i + 1)
                urls.append(
                    self.create_url(
                        base_url, seller_type, country,
                        tmp_min_price, tmp_max_price,
                        min_horse_power, max_horse_power,
                        max_first_registration, min_first_registration,
                        min_mileage, max_mileage,
                        car_brand, car_type
                    )
                )
            return urls

        return [url]

    @staticmethod
    def check_number_of_results(url):
        content = get(url)
        soup = BeautifulSoup(content)
        results_n_tag = soup.find('h1', {'class': 'h2 u-text-orange rbt-result-list-headline'})
        if results_n_tag:
            return int(results_n_tag.text.split(' ')[0].replace('.', ''))
        return None

    def create_url(self, base_url: str = DEFAULT_URL, seller_type: SellerType = None, country: Country = None,
                   min_price: int = None, max_price: int = None,
                   min_horse_power: int = None, max_horse_power: int = None,
                   max_first_registration: int = None, min_first_registration: int = None,
                   min_mileage: int = None, max_mileage: int = None,
                   car_brand: int = None, car_type: Union[int, str] = None) -> str:
        """
        Create search url

        :param min_price: [Optional] Min price in Euro
        :param max_price: [Optional] Max price in Euro
        :param base_url: [Optional] Base search URL to which code will add expected filters
        :param seller_type: [Optional] Enum value of SellerType
        :param country: [Optional] Enum value of Country
        :param min_horse_power: [Optional] Min horse power
        :param max_horse_power: [Optional] Max horse power
        :param max_first_registration: [Optional] Max value of first registration year
        :param min_first_registration: [Optional] Min value of first registration year
        :param min_mileage: [Optional] Min mileage in km
        :param max_mileage: [Optional] Max mileage in km
        :param car_brand: [Optional] Car Brand id based on Dict with CAR_BRANDS
        :param car_type: [Optional] Car Type id based on Dict with CAR_BRANDS
        :return: URL
        """

        url = base_url

        if min_horse_power or max_horse_power:
            url = self._add_horse_power(url, min_horse_power, max_horse_power)

        if min_price or max_price:
            url = self._add_price(url, min_price, max_price)

        if min_first_registration or max_first_registration:
            url = self._add_first_registration(url, min_horse_power, max_horse_power)

        if min_mileage or max_mileage:
            url = self._add_mileage(url, min_mileage, max_mileage)

        if country:
            url = self._add_country(url, country)

        if seller_type:
            url = self._add_seller_type(url, seller_type)

        if car_brand:
            url = self._add_car_type(url, car_brand, car_type)

        return url

    def _add_horse_power(self, url: str, min_horse_power: int, max_horse_power: int) -> str:
        if min_horse_power:
            url += f'&{self.MIN_POWER_TYPE}=PS&{self.MIN_HORSE_STRENGTH_ARG}={min_horse_power}'

        if max_horse_power:
            url += f'&{self.MAX_POWER_TYPE}=PS&{self.MAX_HORSE_STRENGTH_ARG}={max_horse_power}'

        return url

    def _add_price(self, url: str, min_price: int = None, max_price: int = None) -> str:
        if min_price:
            url += f'&{self.MIN_PRICE_ARG}={min_price}'

        if max_price:
            url += f'&{self.MAX_PRICE_ARG}={max_price}'

        return url

    def _add_first_registration(self, url: str, max_first_registration: int = None,
                                min_first_registration: int = None) -> str:
        if min_first_registration:
            url += f'&{self.MIN_FIRST_REGISTRATION_DATE_ARG}={min_first_registration}'

        if max_first_registration:
            url += f'&{self.MAX_FIRST_REGISTRATION_DATE_ARG}={max_first_registration}'

        return url

    def _add_mileage(self, url: str, min_mileage: int = None, max_mileage: int = None) -> str:
        if min_mileage:
            url += f'&{self.MIN_MILEAGE_ARG}={min_mileage}'

        if max_mileage:
            url += f'&{self.MAX_MILEAGE_ARG}={max_mileage}'

        return url

    def _add_country(self, url: str, country: Country) -> str:
        return url + f'&{self.COUNTRY_ARG}={country.value}'

    def _add_seller_type(self, url: str, seller_type: SellerType) -> str:
        return url + f'&{self.SELLER_TYPE_ARG}={seller_type.value}'

    def _add_car_type(self, url: str, car_brand: int, car_type: Union[int, str]):
        if car_type:
            return url + f'&{self.CAR_TYPE_ARG}={car_brand};{car_type}'
        return url + f'&{self.CAR_TYPE_ARG}={car_brand}'

