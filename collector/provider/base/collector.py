from abc import ABCMeta, abstractmethod
from typing import Iterable, Optional
from collector.product import ProductSpec
from .session import Session


class Collector(metaclass=ABCMeta):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def do_collect(self, session: Session, page: int) -> Optional[list[ProductSpec]]:
        pass

    def collect(self, page_limit: Optional[int]) -> Iterable:
        return CollectorIterator(self, page_limit)


class CollectorIterator:
    collector: Collector
    page: int
    page_limit: Optional[int]

    def __init__(self, collector, page_limit: Optional[int]):
        self.collector = collector
        self.page = 0
        self.page_limit = page_limit

    def __iter__(self):
        return self

    def __next__(self):
        self.page += 1
        if self.page > self.page_limit:
            raise StopIteration

        product_specs = self.collector.do_collect(self.collector.session, self.page)
        if product_specs is None:
            raise StopIteration
        
        return product_specs


class QueryBasedCollector(Collector):
    session: Session
    query: str

    def __init__(self, session: Session, query: str):
        super().__init__(session)
        self.query = query

    def do_collect(self, session: Session, page: int) -> Optional[list[ProductSpec]]:
        return session.load_from_query(self.query, page)
