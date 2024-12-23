from configobj import ConfigObj
from loguru import logger

class AppControl:
    def __init__(self, cfg):
        self.ip=cfg.get('ip')
        logger.debug(f"已设置IP地址为{self.ip}")
        pass






if __name__ == '__main__':

    cfg=ConfigObj('./../config.ini', encoding='utf8')
    appcfg=cfg['app']
    app=AppControl(appcfg)