import logging

from configs import SETTINGS
from elements.product import Product
from elements.sidebar import Sidebar
from helpers.bot_helper import BotHelper as bot
from helpers.driver_helper import DriverHelper
from helpers.logging_helper import LoggerHelper
from helpers.telegram_helper import send


def main():
    LoggerHelper()
    urls = SETTINGS.urls
    for url in urls:
        message = ""
        driver = bot(DriverHelper().driver)
        driver.visit(url)

        product_name = driver.find(Product.NAME)
        logging.info(f"Product name: {product_name.text}")
        message += f"{product_name.text} 的庫存狀況：\n"

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.2);")
        driver.wait_element_appear(Product.FIND_IN_STORE_LINK)
        driver.click(Product.FIND_IN_STORE_LINK)
        driver.click(Sidebar.STOCK_SELECTOR)

        shops = driver.find_all(Sidebar.SHOP)
        stocks = driver.find_all(Sidebar.STOCK)

        if len(shops) == len(stocks):
            for shop, stock in zip(shops, stocks):
                shop_name = shop.text.strip() or shop.get_attribute("innerText").strip()
                stock_value = (
                    stock.text.strip() or stock.get_attribute("innerText").strip()
                )
                logging.info(f"Shop: {shop_name}, Stock: {stock_value}")
                if "缺貨" in shop_name:
                    message += f"• {shop_name.split(' ')[1]}：缺貨 QQ\n"
                else:
                    message += f"• {shop_name}：{stock_value}\n"
        else:
            logging.error("Number of shops and stocks do not match!")

        send(message)

    driver.close()


if __name__ == "__main__":
    main()
