import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMainWindow, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import webbrowser
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
import os


class ChatGPTAutomator:
    def __init__(self):
        self.element_xpath = [
            "//*[@id='__next']/div[1]/div[2]/div[1]/div/div/button[1]",
            "//*[@id='root']/div/main/section/div[2]/button",
            "/html/body/div[1]/main/section/div/div/div/form/div[2]/button",
            "//*[@id='__next']/div[1]/div[1]/div/div/div/div/nav/div[2]/div[3]/div/span[1]/div[1]/ol/li[1]"
        ]

        self.element_id =[
            'email-input',
            'password'
        ]

        self.user_inf = {
            "username": os.environ.get('CHATGPT_USERNAME'),
            "password": os.environ.get('CHATGPT_PASSWORD')
        }
        self.driver = self.initialize_driver()
        self.open_chat()
        self.login()
        self.current_url = self.get_current_url()
        print(self.current_url)
        self.quit()

    def initialize_driver(self):
        # ドライバの初期設定
        driver_path = '/Users/user/Desktop/project/launcher_web/chromedriver'
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service)
        return driver

    def open_chat(self):
        # サイトを開く
        self.driver.get("https://chat.openai.com/")


    def getElement(self, way, path):
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((way, path)))
        return element

    def login(self):
        # loginボタンを押す
        self.getElement(By.XPATH, self.element_xpath[0]).click()

        # メールアドレスを入力
        self.getElement(By.ID, self.element_id[0]).send_keys(self.user_inf['username'])
        # 続けるボタンを押す
        self.getElement(By.XPATH, self.element_xpath[1]).click()
        # パスワードを入力
        self.getElement(By.ID, self.element_id[1]).send_keys(self.user_inf['password'])
        # 続けるボタンを押す
        self.getElement(By.XPATH, self.element_xpath[2]).click()

    def open_latest_chat(self):
        # 最新のチャットを開く
        self.getElement(By.XPATH, self.element_xpath[3]).click()

    def get_current_url(self):
        # 現在のURL取得
        return self.driver.current_url

    def quit(self):
        # 終了
        self.driver.quit()


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
        self.Automator = ChatGPTAutomator()
        webbrowser.open(self.Automator.get_current_url())

    def exit_app(self):
        QApplication.quit()

    def run(self):
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    tray_icon_app = TrayIconApp()
    tray_icon_app.run()
