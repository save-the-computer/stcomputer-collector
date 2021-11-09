import sys
import argparse
import jsonpickle
from stcomputer_collector.collectors import collectors


parser = argparse.ArgumentParser(
    description=
        '''쇼핑몰 서비스(danawa 등)로부터 제품 목록 데이터를 크롤링합니다.
Collector를 지정하면 해당 Collector를 사용하여 제품 목록을 가져옵니다.
제품 목록 데이터는 json 포맷으로 outputs 폴더에 저장됩니다.''',
    formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument('collector', choices=collectors, help=f'사용할 Collector입니다.')
parser.add_argument('--page-limit', type=int, default=1, help='크롤링할 페이지 수를 지정합니다. 기본값은 1입니다.')


def main():
    args = parser.parse_args()
    
    collector_name = args.collector
    collector = collectors[collector_name]
    print(f'"{collector_name}" Collector를 사용하여 크롤링을 시작합니다 ...')
    
    product_specs = []
    for batch_product_specs in collector.collect(args.page_limit):
        product_specs += batch_product_specs
    
    # jsonpickle 모듈 환경설정
    jsonpickle.set_preferred_backend('json')
    jsonpickle.set_encoder_options('json', ensure_ascii=False)

    filename = f'outputs/{collector_name}.json'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(jsonpickle.encode(product_specs, unpicklable=False, indent=4))
    
    print(f'완료하였습니다! 결과는 {filename}에 저장되었습니다.')


if __name__ == '__main__':
    main()
