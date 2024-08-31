from selenium.webdriver.common.by import By


class Sidebar:
    STOCK_SELECTOR = (By.XPATH, "//div[@data-section='stock-selector']")
    SHOP = (By.XPATH, "//div[@class='shop']//div[@id='store']/p[1]")
    STOCK = (By.XPATH, "//div[@class='shop']//div[@id='store']/p[2]")
