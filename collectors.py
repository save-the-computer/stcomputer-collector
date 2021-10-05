from typing import Dict
import requests
from collector.provider.danawa.collector import DanawaCPUCollector, DanawaCollector, DanawaMainboardCollector, DanawaRAMCollector, DanawaVGACollector
from collector.provider.danawa.session import DanawaSession


__driver = requests.Session()
__driver.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
})
__session = DanawaSession(__driver)

collectors: Dict[str, DanawaCollector] = {
    'CPU': DanawaCPUCollector(__session),
    '그래픽카드': DanawaVGACollector(__session),
    '메인보드': DanawaMainboardCollector(__session),
    'RAM': DanawaRAMCollector(__session),
}