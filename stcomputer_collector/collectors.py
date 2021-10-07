from typing import Dict
import requests
from .provider.base.collector import Collector
from .provider.danawa.collector import DanawaCPUCollector, DanawaCollector, DanawaMainboardCollector, DanawaRAMCollector, DanawaVGACollector
from .provider.danawa.session import DanawaSession


__driver = requests.Session()
__driver.headers.update({
    # Windows User-Agent
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',

    # Mac OS User-Agent
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
})
__session = DanawaSession(__driver)

collectors: Dict[str, DanawaCollector] = {
    'CPU': DanawaCPUCollector(__session),
    '그래픽카드': DanawaVGACollector(__session),
    '메인보드': DanawaMainboardCollector(__session),
    'RAM': DanawaRAMCollector(__session),
}


def get_collector(name) -> Collector:
    if name not in collectors:
        raise KeyError(f'Collector "{name}" is not found. choose one of: {collectors.keys()}')
    
    return collectors[name]