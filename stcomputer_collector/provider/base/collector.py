from abc import ABCMeta, abstractmethod
from typing import Iterable, List, Optional
from stcomputer_collector.product import ProductSpec
from .session import Session


class Collector(metaclass=ABCMeta):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def do_collect(self, session: Session, page: int) -> Optional[List[ProductSpec]]:
        pass

    def collect(self, page_limit: Optional[int]) -> 'CollectorIterator':
        return CollectorIterator(self, page_limit)


class CollectorIterator:
    collector: Collector
    page: int
    page_limit: Optional[int]
    _count: int

    def __init__(self, collector, page_limit: Optional[int]):
        self.collector = collector
        self.page = 0
        self.page_limit = page_limit
        self._count = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.page += 1
        if self.page > self.page_limit:
            print(f'[{type(self.collector).__name__}] Collection done. (Pagenation reached to page limit {self.page_limit})')
            print(f'[{type(self.collector).__name__}] Total count: {self._count}')
            raise StopIteration

        product_specs = self.collector.do_collect(self.collector.session, self.page)
        if product_specs is None:
            print(f'[{type(self.collector).__name__}] Collection done. (None returned by method Collector.do_collect)')
            raise StopIteration

        print(f'[{type(self.collector).__name__}] Collect page {self.page} done! Count of product specs is {len(product_specs)}.')
        self._count += len(product_specs)
        return product_specs


class QueryBasedCollector(Collector):
    session: Session
    query: str

    def __init__(self, session: Session, query: str):
        super().__init__(session)
        self.query = query

    def do_collect(self, session: Session, page: int) -> Optional[List[ProductSpec]]:
        return session.load_from_query(self.query, page)
