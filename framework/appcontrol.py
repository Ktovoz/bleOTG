import requests
from configobj import ConfigObj
from loguru import logger
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
import time

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

    def real_time_preview(self, fps=20, scale_factor=0.37):
        """
        实时预览截图
        :param fps: 帧率
        :param scale_factor: 缩放因子，默认为1.0（不缩放）
        """
        interval = 1.0 / fps
        while True:
            start_time = time.time()
            image = self.get_image()
            if image is not None:
                # 将PIL图像转换为OpenCV格式
                open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                original_height, original_width = open_cv_image.shape[:2]

                # 计算新的宽度和高度
                new_width = int(original_width * scale_factor)
                new_height = int(original_height * scale_factor)

                # 缩放图像
                resized_image = cv2.resize(open_cv_image, (new_width, new_height))

                cv2.imshow('Real Time Preview', resized_image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            end_time = time.time()
            elapsed_time = end_time - start_time
            if elapsed_time < interval:
                time.sleep(interval - elapsed_time)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    cfg = ConfigObj('./../config.ini', encoding='utf8')
    appcfg = cfg['app']
    app = AppControl(appcfg)
    app.test_bind()
    app.real_time_preview()
