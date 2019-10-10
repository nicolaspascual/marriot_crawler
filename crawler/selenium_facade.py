from os.path import abspath, join
from pathlib import Path

from selenium import webdriver


class SeleniumFacade(webdriver.Firefox):
    """
    Class to encapsulate the functionality of the selenium driver in order
    to work with a wrapper and load the convenient configurations
    """
    driver_path = join(
        Path(abspath(__file__)).parent.parent, 'bin/geckodriver')

    def __init__(self, *args, **kwargs):
        super().__init__(
            executable_path=SeleniumFacade.driver_path,
            *args, **kwargs
        )

    def scroll_bottom(self):
        """
        Scrolls to the bottom of the page by using a JS script
        """
        self.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )

    def __del__(self):
        """
        Closes the driver on object deletion
        """
        self.quit()
