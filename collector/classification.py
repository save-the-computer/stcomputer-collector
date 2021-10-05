from typing import Dict, Optional


class Classification:
    category: str
    """제품 카테고리 (예: CPU, 메인보드)"""
    level1: str
    """분류 기준 첫 번째. (예: 제품 브랜드(삼성, LG 등), 표준(DDR4, DDR3 등))"""
    level2: Optional[str]
    """분류 기준 두 번째. (예: 제품 시리즈(RTX 3090, AMD 버미어 등), 제품 브랜드(삼성, LG 등))"""

    def __init__(self, category: str, level1: str, level2: Optional[str]):
        self.category = category
        self.level1 = level1
        self.level2 = level2
