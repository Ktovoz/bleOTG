import sys
from pathlib import Path
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QPushButton, QTextBrowser, QApplication, QMessageBox
from loguru import logger

class menuWindow(QWidget):
    def __init__(self, loader):
        super().__init__()
        self.loader = loader
        self.initialization()
        self.ui.setWindowTitle("主菜单")
        logger.info("主菜单窗口初始化完成")

    def initialization(self):
        base_dir = Path(__file__).resolve().parent
        ui_file_path = base_dir / 'menu.ui'
        ui_file = QFile(str(ui_file_path))
        self.ui = self.loader.load(ui_file)
        frame_geometry = self.ui.frameGeometry()
        screen_center = self.ui.screen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.ui.move(frame_geometry.topLeft())
        ui_file.close()
        self.ui.show()
        self.ui.activateWindow()
        logger.info("UI文件加载完成")
        # 方法映射
        button_map = {
            'quit': self.quit_app,
            'bind': self.button_clicked
        }
        # 绑定方法
        for button_name, handler in button_map.items():
            self.ui.findChild(QPushButton, button_name).clicked.connect(handler)
        logger.info("按钮绑定完成")
    def show_window(self):
        # 检查是否有ui属性且不为None
        if not hasattr(self, 'ui') or self.ui is None:
            return
        # 显示UI窗口
        self.ui.show()
        # 激活窗口，使其获得焦点
        self.ui.activateWindow()

    def quit_app(self):
        # 退出应用程序
        logger.info("退出应用程序")
        sys.exit()
    def console(self):
        text_browser = self.ui.findChild(QTextBrowser, 'textBrowser')
        return text_browser

    def button_clicked(self):
        self.console().append("按钮被点击了")
def main():
    """
    程序的主入口点。

    参数:
    src -- 源文件路径，用于加载UI或其他资源。

    此函数负责初始化应用程序，加载UI，并显示主窗口。
    如果在执行过程中遇到异常，则退出程序，返回错误码1。
    """
    try:
        # 创建UI加载器对象
        loader = QUiLoader()

        # 创建应用程序对象
        app = QApplication(sys.argv)

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
    main()