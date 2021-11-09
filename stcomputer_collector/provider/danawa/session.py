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

        # Parse: variant
        if (variant := element.select_one('.memory_sect')) is not None:
            # get all text node and glue tokens
            product.variant = ' '.join(filter(lambda token: len(token) > 0, map(lambda child: str(child).strip(), filter(lambda child: isinstance(child, NavigableString), variant.children))))
        else:
            product.variant = None

        # Set empty string to None
        if not product.variant:
            product.variant = None

        # Parse: price, stock_state
        price_text = element.select_one('.price_sect > a > strong').text.strip().replace(',', '').rstrip('원')
        if price_text.isnumeric():
            product.price = int(price_text)
            product.stock_state = '재고있음'
        else:
            product.price = None
            product.stock_state = price_text

        return product


    def __parse_product_spec(self, element: Tag) -> RawProductSpec:
        product_spec = RawProductSpec()

        # Parse: name
        if (title_element := element.select_one('.prod_name > a')) is None:
            raise DanawaParseError(f'Note: Skip unknown product spec.')

        product_spec.name = title_element.text

        # Parse: id
        if (id_match := re.search(r'\?pcode=(\d+?)\&', title_element.attrs['href'])) is None:
            raise DanawaParseError(f'Note: Skip product spec "{product_spec.name}", because it does not have id attribute.')

        product_spec.id = id_match.groups()[0]

        # Parse: thumbnail
        thumbnail_element = element.select_one('.thumb_image img')
        if 'src' in thumbnail_element.attrs:
            product_spec.thumbnail = thumbnail_element.attrs['src']
        else:
            product_spec.thumbnail = thumbnail_element.attrs['data-original']
        
        # if thumbnail url starts with //? -> trim
        if product_spec.thumbnail.startswith('//'):
            product_spec.thumbnail = 'http://' + product_spec.thumbnail.lstrip('//')

        # Parse: tags
        product_spec.tags = [*map(lambda spec: spec.strip(), element.select_one('.prod_spec_set .spec_list').text.strip().split(' / '))]

        # Parse: registration_date
        if (registration_date := element.select_one('.prod_sub_meta > .mt_date > dd')) is None:
            raise DanawaParseError(f'Note: Skip product spec "{product_spec.name}", because it does not have registration date.')

        # example: 2020.11
        registration_year, registration_month = map(int, registration_date.text.split('.'))
        product_spec.registration_date = date(registration_year, registration_month, 1)

        # Parse: category
        # example: PC주요부품 > CPU > AMD (카테고리가 없으면 SKIP)
        if (category := element.select_one('.prod_category_location > dd')) is None:
            raise DanawaParseError(f'Note: Skip product spec "{product_spec.name}", because it does not have category location.')

        product_spec.category = [*map(lambda category: category.strip(), category.text.strip().split('>'))]

        # Parse: products
        product_spec.products = [*map(self.__parse_product, element.select('.prod_pricelist li[id^="productInfoDetail"]'))]

        # 제품 종류(중고, 정품, 병행수입 등) 대신 쇼핑몰 상위 5개가 표시될 경우 이에 대한 파싱
        if len(product_spec.products) == 0 and element.select_one('.prod_pricelist.prod_top5') is not None:
            product = RawProduct()
            product.id = product_spec.id
            product.variant = None

            price_text = element.select_one('.prod_pricelist.prod_top5 .top5_item:first-child .top5_price').text.strip().replace(',', '').rstrip('원')
            if price_text.isnumeric():
                product.price = int(price_text)
                product.stock_state = '재고있음'
            else:
                product.price = None
                product.stock_state = price_text

            product_spec.products = [product]

        if len(product_spec.products) == 0:
            raise DanawaParseError(f'Note: Skip product spec "{product_spec.name}", doesn\'t have any product!')

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
                products.append(product)
            except DanawaParseError as error:
                print(error)
            except Exception as error:
                print('Unexpected error occurs while parse product element, See below:')
                print(error)

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