from src.parser.webdriver import WebDriverContextManager
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from src.utils.parse import load_excel



def parser(url: str, stop_year):
    with WebDriverContextManager(url) as driver:
        terms_elmnt = driver.find_element(By.XPATH,"/html/body/div[5]/div[2]/div[3]/form/input[4]")
        terms_elmnt.click()
        sleep(1)

        stop = False

        while not stop:
            sleep(1)
            elements = driver.find_element(By.CSS_SELECTOR, "div.accordeon-inner:nth-child(1)").find_elements(By.CLASS_NAME, "accordeon-inner__item")
            for element in elements:
                date_of_document = element.find_element(By.CLASS_NAME,"accordeon-inner__item-inner__title").find_element(By.CSS_SELECTOR,"p").text
                date_for_check = date_of_document.split(".")[-1]
                print(date_of_document)
                if date_for_check == str(stop_year):
                    stop = True
                    print(f"Загрузка документов до {int(stop_year)-1} года завершена.")
                    break
                table = element.find_element(By.CLASS_NAME,"accordeon-inner__header").find_element(By.CSS_SELECTOR,"a").get_attribute("href")
                load_excel(table=table, date=date_of_document)
            
            if not stop:
                button = driver.find_element(By.CSS_SELECTOR, ".bx-pag-next > a:nth-child(1)")
                driver.execute_script("arguments[0].scrollIntoView();", button)

                actions = ActionChains(driver)
                actions.move_to_element(button).perform()
                sleep(1)
                button.click()
                        
