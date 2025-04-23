from src.parser.webdriver import WebDriverContextManager
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from src.utils.parse import load_excel
import asyncio


async def parser(url: str, stop_year):
    async with WebDriverContextManager(url) as driver:
        terms_elmnt = driver.find_element(By.XPATH,"/html/body/div[5]/div[2]/div[3]/form/input[4]")
        terms_elmnt.click()

        stop = False

        while not stop:

            elements = driver.find_element(By.CSS_SELECTOR, "div.accordeon-inner:nth-child(1)").find_elements(By.CLASS_NAME, "accordeon-inner__item")
            tasks = set()
            for element in elements:
                date_of_document = element.find_element(By.CLASS_NAME,"accordeon-inner__item-inner__title").find_element(By.CSS_SELECTOR,"p").text
                date_for_check = date_of_document.split(".")[-1]
                if date_for_check == str(stop_year):
                    stop = True
                    break
                table = element.find_element(By.CLASS_NAME,"accordeon-inner__header").find_element(By.CSS_SELECTOR,"a").get_attribute("href")
                tasks.add(asyncio.create_task(load_excel(table=table, date=date_of_document)))

            await asyncio.gather(*tasks)
   
            if not stop:
                button = driver.find_element(By.CSS_SELECTOR, ".bx-pag-next > a:nth-child(1)")
                driver.execute_script("arguments[0].scrollIntoView();", button)

                actions = ActionChains(driver)
                actions.move_to_element(button).perform()
                button.click()
