import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMainWindow, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os

print(os.environ.get('ChatGPT_USERNAME'))

# WebDriverのパスを指定（このパスを実際のchromedriverの場所に置き換えてください）
driver_path = '/Users/user/Desktop/project/launcher_web/chromedriver'

service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)

driver.get("https://chat.openai.com/")

driver.implicitly_wait(10)

# 現在のページのURLを取得
current_url = driver.current_url
print("現在のURL:", current_url)

driver.quit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tray Icon Window')
        self.setGeometry(100, 100, 640, 480)
        self.setWindowIcon(QIcon("images/icon/claude_icon.png"))
        self.label = QLabel("Hello, PyQt5!", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.center()

    def center(self):
        # ディスプレイの解像度を取得
        screen = QApplication.primaryScreen().geometry()
        screenWidth = screen.width()
        screenHeight = screen.height()

        # ウィンドウのサイズを取得
        windowWidth = self.frameSize().width()
        windowHeight = self.frameSize().height()

        # ウィンドウを画面の右の真ん中に配置
        self.move(screenWidth - windowWidth, (screenHeight - windowHeight) // 2)

class TrayIconApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        self.tray_icon = QSystemTrayIcon(QIcon("images/icon/claude_icon.png"), self.app)
        self.setup_tray_icon()

    def setup_tray_icon(self):
        menu = QMenu()
        open_website_action = menu.addAction("ウェブサイトを開く")
        exit_action = menu.addAction("終了")

        open_website_action.triggered.connect(self.open_website)
        exit_action.triggered.connect(self.exit_app)

        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()

    def open_website(self):
        webbrowser.open("https://chat.openai.com/")

    def exit_app(self):
        QApplication.quit()

    def run(self):
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    tray_icon_app = TrayIconApp()
    tray_icon_app.run()
