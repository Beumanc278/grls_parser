import time

from selenium.webdriver.support.abstract_event_listener import AbstractEventListener


class InstructionEventListener(AbstractEventListener):

    def before_navigate_to(self, url, driver):
        print(f'Before navigate to {url}')

    def after_navigate_to(self, url, driver):
        print(f'After navigate to {url}')

    def before_find(self, by, value, driver):
        print(f'Searching for element with {by}={value} on {driver.current_url}\n')

    def after_find(self, by, value, driver):
        print(f'Found element with {by}={value} on {driver.current_url}\n')

    def before_click(self, element, driver):
        print(f'Before click to element {element}')

    def after_click(self, element, driver):
        print(f'After click to element {element}')
        time.sleep(2)

    def before_execute_script(self, script, driver):
        print(f'Before executing script {script}\n')

    def after_execute_script(self, script, driver):
        print(f'After executing script {script}\n')
