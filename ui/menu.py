import sys
from pathlib import Path
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QPushButton, QTextBrowser, QApplication, QMessageBox
from configobj import ConfigObj
from loguru import logger

from framework.configlog import LogSetup


class menuWindow(QWidget):
    def __init__(self, loader):
        super().__init__()
        self.loader = loader
        self.initialization()
        self.ui.setWindowTitle("主菜单")
        logger.info("主菜单窗口初始化完成")

    def initialization(self):
        # 获取当前文件所在的目录
        base_dir = Path(__file__).resolve().parent
        logger.debug(f"基础目录: {base_dir}")
        # 构建UI文件的路径
        ui_file_path = base_dir / 'menu.ui'
        logger.debug(f"UI文件路径: {ui_file_path}")
        # 打开UI文件
        ui_file = QFile(str(ui_file_path))
        if not ui_file.open(QFile.ReadOnly):
            logger.error(f"无法打开UI文件: {ui_file_path}")
            return
        # 加载UI文件
        self.ui = self.loader.load(ui_file)
        logger.info("UI文件加载完成")
        # 设置UI窗口居中显示
        frame_geometry = self.ui.frameGeometry()
        screen_center = self.ui.screen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.ui.move(frame_geometry.topLeft())
        logger.debug("UI窗口已居中显示")
        # 关闭UI文件
        ui_file.close()
        # 显示UI窗口并激活
        self.ui.show()
        self.ui.activateWindow()
        logger.info("UI窗口已显示并激活")
        self.bind_button()
        logger.info("按钮绑定完成")

    def bind_button(self):
        # 定义按钮与方法的映射关系
        button_map = {
            'quit': self.quit_app,
            'bind': self.button_clicked
        }

        # 绑定按钮点击事件到相应的方法
        for button_name, handler in button_map.items():
            button = self.ui.findChild(QPushButton, button_name)
            if button is not None:
                button.clicked.connect(handler)
                logger.debug(f"按钮 '{button_name}' 已绑定到方法 '{handler.__name__}'")
            else:
                logger.warning(f"未找到按钮: {button_name}")

    def show_window(self):
        # 检查是否有ui属性且不为None
        if not hasattr(self, 'ui') or self.ui is None:
            logger.warning("UI对象不存在或为None，无法显示窗口")
            return
        # 显示UI窗口
        self.ui.show()
        # 激活窗口，使其获得焦点
        self.ui.activateWindow()
        logger.info("UI窗口已显示并激活")

    def quit_app(self):
        # 退出应用程序
        logger.info("退出应用程序")
        sys.exit()

    def console(self):
        text_browser = self.ui.findChild(QTextBrowser, 'textBrowser')
        return text_browser

    def button_clicked(self):
        self.console().append("按钮被点击了")
        logger.info("按钮被点击")

def main():
    try:
        # 创建UI加载器对象
        loader = QUiLoader()
        logger.info("UI加载器对象创建完成")

        # 创建应用程序对象
        app = QApplication(sys.argv)
        logger.info("应用程序对象创建完成")

        # 创建Stats对象，用于统计和展示数据
        stats = menuWindow(loader)
        stats.show_window()

        # 运行应用程序的主循环
        sys.exit(app.exec())
    except Exception as e:
        # 如果发生异常，退出程序，返回错误码1
        logger.exception("程序执行过程中发生异常")
        sys.exit(1)

if __name__ == "__main__":
    configFile = ConfigObj('./../config.ini', encoding='utf8')
    LogSetup(config=configFile['logger'])
    main()
