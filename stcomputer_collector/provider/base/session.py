from abc import ABCMeta, abstractmethod
from typing import Dict, List, Optional
import requests

from stcomputer_collector.tag import TagsDictionary
from .product import RawProductSpec


class Session(metaclass=ABCMeta):
    name = 'unknown'
    driver: requests.Session
    latest_response: Optional[requests.Response]

    def __init__(self, driver: requests.Session):
        self.driver = driver
        self.latest_response = None

    def page_loaded(self) -> bool:
        return self.latest_response is not None

    def assert_page_loaded(self):
        assert self.page_loaded(), f'Page is not loaded. Please use page_loaded() before using content.'

    @abstractmethod
    def load_from_query(self, query: str, page: int = 1):
        pass

    @abstractmethod
    def get_product_specs(self) -> List[RawProductSpec]:
        pass

    @abstractmethod
    def get_search_tags_dictionary(self) -> TagsDictionary:
        pass