from typing import Optional
import re
from stcomputer_collector.classification import Classification
from stcomputer_collector.product import Product, ProductSpec
from stcomputer_collector.tag import resolve_tag
from ..base.collector import Collector
from .session import DanawaSession


class DanawaCollector(Collector):
    session: DanawaSession

    def __init__(self, session: DanawaSession):
        super().__init__(session)


class DanawaCPUCollector(DanawaCollector):
    def do_collect(self, session: DanawaSession, page: int) -> Optional[list[ProductSpec]]:
        product_specs = []
        session.load_from_query('CPU', page)

        for raw_product_spec in session.get_product_specs():
            if raw_product_spec.category[-2:] == ['CPU', 'AMD']:
                brand = 'AMD'
            elif raw_product_spec.category[-2:] == ['CPU', '인텔']:
                brand = '인텔'
            else:
                print(f'Note: Skip "{raw_product_spec.name}" is not a CPU')
                continue

            product_spec = ProductSpec(raw_product_spec)

            # find pattern (*****) in '인텔 코어i5-10세대 10400 (코멧레이크S) (정품)'
            if (match := re.search(r'\((.+?)\)', product_spec.name)) is not None:
                match_groups = match.groups()
                if len(match_groups) > 0:
                    series = match_groups[0]

            product_spec.classification = Classification(
                category='CPU',
                level1=brand,
                level2=series,
            )
            product_specs.append(product_spec)

        return product_specs


class DanawaVGACollector(DanawaCollector):
    def do_collect(self, session: DanawaSession, page: int) -> Optional[list[ProductSpec]]:
        product_specs = []

        session.load_from_query('그래픽카드', page)
        tags_dictionary = session.get_search_tags_dictionary()

        for raw_product_spec in session.get_product_specs():
            if raw_product_spec.category[-1:] != ['그래픽카드(VGA)']:
                print(f'Note: Skip "{raw_product_spec.name}" is not a 그래픽카드')
                continue

            product_spec = ProductSpec(raw_product_spec)
            series_if_nvidia = resolve_tag(product_spec.tags, tags_dictionary.get('NVIDIA 칩셋', []))
            series_if_amd = resolve_tag(product_spec.tags, tags_dictionary.get('AMD 칩셋', []))

            if series_if_nvidia is not None:
                brand = 'NVIDIA'
                series = series_if_nvidia
            elif series_if_amd is not None:
                brand = 'AMD'
                series = series_if_amd
            else:
                print(f'Note: Skip "{product_spec.name}" cannot resolve series')
                continue

            product_spec.classification = Classification(
                category='그래픽카드',
                level1=brand,
                level2=series,
            )
            product_specs.append(product_spec)

        return product_specs


class DanawaMainboardCollector(DanawaCollector):
    def do_collect(self, session: DanawaSession, page: int) -> Optional[list[ProductSpec]]:
        product_specs = []

        session.load_from_query('메인보드', page)
        tags_dictionary = session.get_search_tags_dictionary()

        for raw_product_spec in session.get_product_specs():
            if raw_product_spec.category[-1:] != ['메인보드']:
                print(f'Note: Skip "{raw_product_spec.name}" is not a 메인보드')
                continue

            product_spec = ProductSpec(raw_product_spec)
            chipset = resolve_tag(product_spec.tags, tags_dictionary.get('세부 칩셋', []))
            
            if chipset is None:
                print(f'Note: Skip "{product_spec.name}" cannot resolve chipset')
                continue

            chipset_match = re.search(r'\((.+?)\)', chipset)
            if chipset_match is None or (brand := chipset_match.groups()[0]) is None:
                print(f'Note: Skip "{product_spec.name}" cannot resolve brand')
                continue
            
            product_spec.classification = Classification(
                category='메인보드',
                level1=brand,
                level2=chipset,
            )
            product_specs.append(product_spec)
        
        return product_specs


class DanawaRAMCollector(DanawaCollector):
    def do_collect(self, session: DanawaSession, page: int) -> Optional[list[ProductSpec]]:
        product_specs = []

        session.load_from_query('RAM', page)
        tags_dictionary = session.get_search_tags_dictionary()

        for raw_product_spec in session.get_product_specs():
            if raw_product_spec.category[-1:] != ['RAM']:
                print(f'Note: Skip "{raw_product_spec.name}" is not a RAM')
                continue

            product_spec = ProductSpec(raw_product_spec)
            target_device = resolve_tag(product_spec.tags, tags_dictionary.get('사용 장치', []))
            series = resolve_tag(product_spec.tags, tags_dictionary.get('제품 분류', []))
            clock_speed = resolve_tag(product_spec.tags, tags_dictionary.get('동작클럭(대역폭)', []))

            if clock_speed is not None:
                series = f'{series} {clock_speed}'

            product_spec.classification = Classification(
                category='RAM',
                level1=target_device,
                level2=series,
            )
            product_specs.append(product_spec)
        
        return product_specs
