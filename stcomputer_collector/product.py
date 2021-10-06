from typing import Optional
from datetime import date
from .classification import Classification
from .tag import Tags


class Product:
    id: str
    """제품 식별자"""
    variant: str
    """제품 타입 (정품, 중고 등. 빈 문자열 일 수도 있음)"""
    price: Optional[int]
    """제품 가격"""
    stock_state: str
    """제품 재고 상태"""

    def __init__(self, raw_product):
        if raw_product is not None:
            raw_product.assign_to(self)


class ProductSpec:
    id: str
    """제품 정보 식별자"""
    name: str
    """제품 이름"""
    thumbnail: str
    """제품 썸네일 URL"""
    tags: Tags
    """제품 태그(스펙) 목록"""
    registration_date: date
    """제품 등록일 (YYYY-MM-DD (ex. 2020-11-01))"""
    products: list[Product]
    """제품 정보 하위의 제품 목록 (정품, 중고 등)"""
    classification: Classification
    """제품 분류 정보"""

    def __init__(self, raw_product_spec):
        if raw_product_spec is not None:
            raw_product_spec.assign_to(self)