from selenium import webdriver

from modules.navigation import NavigationHelper

class Application:

    def __init__(self):
        self.options = webdriver.FirefoxOptions()
        self.options.add_argument('-headless')
        self.wd = webdriver.Firefox(options=self.options)
        print("Браузер успешно запущен...")
        self.main_page = 'https://grls.rosminzdrav.ru/GRLS.aspx'
        self.navigation = NavigationHelper(self)

    def start(self):
        self.open_main_page()
        print(f'Соединение с {self.main_page} успешно установлено....')

    def open_main_page(self):
        wd = self.wd
        wd.get(self.main_page)

    @classmethod
    def restart_app(cls, app):
        app.destroy()
        return Application()

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def destroy(self):
        self.wd.quit()
        print('Браузер успешно закрыт...')
