import requests
from configobj import ConfigObj
from loguru import logger
from PIL import Image
from io import BytesIO

class AppControl:
    def __init__(self, cfg):
        ip = cfg.get('ip')
        self.url = f'http://{ip}:8080'
        logger.debug(f"已设置IP地址为{ip}")
        logger.debug(f"已设置请求地址为{self.url}")

    def contains(self, response, expected_text):
        if expected_text in response.text:
            logger.info(f"响应内容包含预期的文字'{expected_text}'，断言成功")
            return True
        else:
            logger.error(f"响应内容不包含预期的文字'{expected_text}'")
            return False

    def not_contains(self, response, expected_text):
        if expected_text not in response.text:
            logger.info(f"响应内容不包含预期的文字'{expected_text}'，断言成功")
            return True
        else:
            logger.error(f"响应内容包含预期的文字'{expected_text}'")
            return False

    def test_bind(self):
        endpoint = f'{self.url}/hello'
        response = requests.get(endpoint)
        logger.debug(f"请求地址为{endpoint}")

        if self.contains(response, "手机http服务器已正常启动"):
            logger.info("测试链接成功")

    def get_image(self):
        endpoint = f'{self.url}/capimg'
        response = requests.get(endpoint)
        logger.debug(f"请求地址为{endpoint}")
        if self.not_contains(response, "http response err"):
            image = Image.open(BytesIO(response.content))
            logger.debug(f"成功截取图片，格式为 {image.format}")
            return image
        else:
            rep = requests.get(f'{self.url}/capimgpermission')
            if self.contains(rep, "ok"):
                logger.debug(f"截图权限申请成功")
                image = Image.open(BytesIO(rep.content))
                logger.debug(f"成功截取图片，格式为 {image.format}")
                return image
            else:
                logger.error("截图失败，并且截图权限申请失败")
                return None



if __name__ == '__main__':
    cfg = ConfigObj('./../config.ini', encoding='utf8')
    appcfg = cfg['app']
    app = AppControl(appcfg)
    app.test_bind()
