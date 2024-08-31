from selenium.webdriver.common.by import By


class Product:
    NAME = (By.XPATH, "//a[@class='itemName']/h3")
    FIND_IN_STORE_LINK = (By.XPATH, "//a[@id='findIt-inStore_link']")
