from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time

base_url='http://www.ceair.com/booking/syd-hgh-210205_CNY.html'
timeout = 6

driver=webdriver.Firefox()
driver.get(base_url)

elem_ready_status_check = {
    "clickable": EC.element_to_be_clickable,
    "located": EC.presence_of_element_located,
}

elem_located_by_dict = {
    "id": By.ID,
    "class_name": By.CLASS_NAME,
}

def web_interact(interact):
    ready_status = interact[0]
    located_by = interact[1]
    address = interact[2]
    action = interact[3]

    try:
        target = WebDriverWait(driver, timeout).until(
            elem_ready_status_check[ready_status](
                (elem_located_by_dict[located_by], address)
            )
        )
    except TimeoutException:
        print("{} timeout".format(address))
        return

    getattr(target, action)()
    print("{} {} executed".format(address, action))

interactions = [
    ("clickable", "id", "okay", "click"),
    ("clickable", "id", "okay", "click"),
]

for i in interactions:
    web_interact(i)
