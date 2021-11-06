from typing import List
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
import re
from datetime import date
from stcomputer_collector.tag import TagsDictionary
from ..base.product import RawProduct, RawProductSpec
from ..base.session import Session


class DanawaParseError(Exception):
    pass


class DanawaSession(Session):
    name = 'danawa'

    def __parse_product(self, element: Tag) -> RawProduct:
        product = RawProduct()
        product.id = re.search(r'productInfoDetail_(\d+)', element.attrs['id']).groups()[0]

        if (variant := element.select_one('.memory_sect')) is not None:
            # get all text node and glue tokens
            product.variant = ' '.join(filter(lambda token: len(token) > 0, map(lambda child: str(child).strip(), filter(lambda child: isinstance(child, NavigableString), variant.children))))
        else:
            product.variant = None

        price_text = element.select_one('.price_sect > a > strong').text.strip().replace(',', '')
        if price_text.isnumeric():
            product.price = int(price_text)
            product.stock_state = '재고있음'
        else:
            product.price = None
            product.stock_state = price_text

        return product


    def __parse_product_spec(self, element: Tag) -> RawProductSpec:
        product_spec = RawProductSpec()

        if (title_element := element.select_one('.prod_name > a')) is None:
            raise DanawaParseError(f'Note: Skip unknown product spec.')

        product_spec.name = title_element.text

        if (id_match := re.search(r'\?pcode=(\d+?)\&', title_element.attrs['href'])) is None:
            raise DanawaParseError(f'Note: Skip product spec "{product_spec.name}", because it does not have id attribute.')

        product_spec.id = id_match.groups()[0]

        thumbnail_element = element.select_one('.thumb_image img')
        if 'src' in thumbnail_element.attrs:
            product_spec.thumbnail = thumbnail_element.attrs['src']
        else:
            product_spec.thumbnail = thumbnail_element.attrs['data-original']

        product_spec.tags = [*map(lambda spec: spec.strip(), element.select_one('.prod_spec_set .spec_list').text.strip().split(' / '))]

        if (registration_date := element.select_one('.prod_sub_meta > .mt_date > dd')) is None:
            raise DanawaParseError(f'Note: Skip product spec "{product_spec.name}", because it does not have registration date.')

        # example: 2020.11
        registration_year, registration_month = map(int, registration_date.text.split('.'))
        product_spec.registration_date = date(registration_year, registration_month, 1)

        # example: PC주요부품 > CPU > AMD (카테고리가 없으면 SKIP)
        if (category := element.select_one('.prod_category_location > dd')) is None:
            raise DanawaParseError(f'Note: Skip product spec "{product_spec.name}", because it does not have category location.')

        product_spec.category = [*map(lambda category: category.strip(), category.text.strip().split('>'))]
        product_spec.products = [*map(self.__parse_product, element.select('.prod_pricelist li'))]

        return product_spec


    def load_from_query(self, query: str, page: int = 1):
        self.latest_response = self.driver.get(f'http://search.danawa.com/dsearch.php?query={query}&page={page}&limit=120')


    def get_product_specs(self) -> List[RawProductSpec]:
        self.assert_page_loaded()

        soup = BeautifulSoup(self.latest_response.content, 'html.parser')
        products = []

        for product_element in soup.select('#productListArea .product_list > .prod_item'):
            # 파싱에 필요한 속성(id)가 부족함
            if not ('id' in product_element.attrs and product_element.attrs['id'].startswith('productItem')):
                continue
            
            try:
                product = self.__parse_product_spec(product_element)
            except DanawaParseError as error:
                print(error)
            except Exception as error:
                print('Unexpected error occurs while parse product element, See below:')
                print(error)

            products.append(product)

        return products


    def get_search_tags_dictionary(self) -> TagsDictionary:
        self.assert_page_loaded()

        soup = BeautifulSoup(self.latest_response.content, 'html.parser')
        groups = {}
        for group_area in soup.select('.basic_cate_area'):
            group_name = group_area.select_one('.cate_head').text.strip()

            keywords = group_area.select_one('.basic_sub_area') or group_area.select_one('.basic_top_area')
            groups[group_name] = [*map(lambda element: element.text.strip(), keywords.select('.basic_cate_item'))]

        return groups