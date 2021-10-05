from typing import Optional
from stcomputer_collector.product import Product, ProductSpec
from stcomputer_collector.tag import Tags


class RawProduct:
    id: str
    """제품 식별자"""
    variant: str
    """제품 타입 (정품, 중고 등. 빈 문자열 일 수도 있음)"""
    price: Optional[int]
    """제품 가격"""
    stock_state: str
    """제품 재고 상태"""

    def assign_to(self, product: Product):
        product.id = self.id
        product.variant = self.variant
        product.price = self.price
        product.stock_state = self.stock_state


class RawProductSpec:
    id: str
    """제품 정보 식별자"""
    name: str
    """제품 이름"""
    thumbnail: str
    """제품 썸네일 URL"""
    tags: Tags
    """제품 태그(스펙) 목록"""
    registration_date: str
    """제품 등록일 (YYYY-MM-DD (ex. 2020-11-01))"""
    category: list[str]
    """제품 카테고리 계층(예: PC주요부품 > CPU > AMD)"""
    products: list[RawProduct]
    """제품 정보 하위의 제품 목록 (정품, 중고 등)"""

    def assign_to(self, product_spec: ProductSpec):
        product_spec.id = self.id
        product_spec.name = self.name
        product_spec.thumbnail = self.thumbnail
        product_spec.tags = self.tags
        product_spec.registration_date = self.registration_date
        product_spec.products = [*map(lambda raw_product: Product(raw_product), self.products)]