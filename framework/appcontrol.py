import requests

from configobj import ConfigObj
from loguru import logger

class AppControl:
    def __init__(self, cfg):
        ip=cfg.get('ip')
        self.url=f'http://{ip}'
        logger.debug(f"已设置IP地址为{ip}")
        logger.debug(f"已设置请求地址为{self.url}")
        pass
    def test_bind(self):
        endpoint=f'{self.url}/hello'
        response= requests.get(endpoint)
        logger.debug(f"请求地址为{endpoint}")
        logger.debug(f"已收到响应{response}")




if __name__ == '__main__':

    cfg=ConfigObj('./../config.ini', encoding='utf8')
    appcfg=cfg['app']
    app=AppControl(appcfg)