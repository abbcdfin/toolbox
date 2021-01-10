from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
import time

import bs4
from bs4 import BeautifulSoup

base_url='http://www.ceair.com/booking/syd-hgh-210205_CNY.html'
timeout = 6

options = Options()
options.headless = True
driver=webdriver.Firefox(options=options)
driver.get(base_url)

elem_ready_status_check = {
    "clickable": EC.element_to_be_clickable,
    "located": EC.presence_of_element_located,
}

elem_located_by_dict = {
    "id": By.ID,
    "class_name": By.CLASS_NAME,
    "name": By.NAME,
}

def web_interact(interact):
    ready_status = interact[0]
    located_by = interact[1]
    address = interact[2]
    action = interact[3]

    if len(interact) > 4:
        wait_sec = interact[4]
        time.sleep(wait_sec)
        print("wait {} seconds to act".format(wait_sec))

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

def native_string(tag):
    for c in tag.children:
        if isinstance(c, bs4.element.NavigableString):
            return(c)

interactions = [
    ("clickable", "id", "okay", "click"),
    ("clickable", "id", "okay", "click"),
    ("clickable", "name", "lowest", "click", 3),
]

# Get to the wanted page
for i in interactions:
    web_interact(i)

# Parsing the wanted page
soup = BeautifulSoup(driver.page_source, 'html.parser')

l = soup.find_all('dd', {"name": "lowest"})
lowest = native_string(l[0])
print("The lowest price is {}".format(lowest))

k = soup.find("div", {"class": "product-list active"})
price = k.find_all("dd", {"class": "p-p"})
for q in price:
    if lowest == native_string(q):
        print("match lowest price {}".format(lowest))
        print(q.next_sibling.find("div", {"class": "bbottom"}).string)
