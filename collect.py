import sys
import jsonpickle
from collectors import collectors


def help():
    print(
        '쇼핑몰 서비스(danawa 등)로부터 제품 목록 데이터를 크롤링합니다.\n'
        'Collector를 지정하면 해당 Collector를 사용하여 제품 목록을 가져옵니다.\n'
        '제품 목록 데이터는 json 포맷으로 outputs 폴더에 저장됩니다.\n'
        '\n'
        '사용법\n'
        '\tcollect.py <collector>\n'
        '\n'
        '사용 가능한 collectors 목록'
    )
    for collector_name in collectors.keys():
        print(f'\t{collector_name}')
        print(f'\t\t{collector_name} 카테고리의 제품 목록을 크롤링합니다.')
        print()


def main():
    params = sys.argv[1:]
    if len(params) == 0:
        help()
        return
    
    collector_name = params[0]
    if collector_name not in collectors:
        print(f'"{collector_name}" 는 존재하지 않는 Collector입니다.')
        return
    
    collector = collectors[collector_name]
    print(f'"{collector_name}" Collector를 사용하여 크롤링을 시작합니다 ...')
    
    product_specs = []
    for batch_product_specs in collector.collect(1):
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
