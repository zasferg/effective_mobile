from selenium import webdriver


class WebDriverContextManager:
    def __init__(self, url):
        self.url = url
        self.driver = None

    def __enter__(self):

        service = webdriver.FirefoxService()
        self.driver = webdriver.Firefox(service=service)
        self.driver.get(self.url)
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()
        if exc_type:
            raise exc_val
        
        




