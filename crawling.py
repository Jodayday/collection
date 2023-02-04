
import time
import logging as log
from selenium.webdriver.support import expected_conditions as EC    # 요소가 있는지 검색함
from selenium.webdriver.support.wait import WebDriverWait  # 드라이버를 기달리게함
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import InvalidArgumentException

# URL = 'https://www.google.com/search?q=%EC%95%84%EC%9D%B4%EC%9C%A0&tbm=isch&ved=2ahUKEwjeq9-11_H8AhVRVPUHHSH0D9gQ2-cCegQIABAA&oq=%EC%95%84%EC%9D%B4%EC%9C%A0&gs_lcp=CgNpbWcQAzIICAAQgAQQsQMyCAgAEIAEELEDMgUIABCABDIFCAAQgAQyBQgAEIAEMggIABCABBCxAzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6CAgAELEDEIMBOgQIABADOgsIABCABBCxAxCDAVD9BliWCmC4C2gCcAB4AoABbogBnAWSAQM1LjKYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=j_jYY56oD9Go1e8Poei_wA0&bih=977&biw=1857'
# URL = 'https://new.land.naver.com/offices?ms=37.1273756,126.8564159,19&a=SG&e=RETAIL'


def open_windon(URL):
    # 브라우저가 뜨지않는 옵션
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(executable_path='chromedriver')
    # driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)
    driver.implicitly_wait(3)
    driver.maximize_window()
    try:
        driver.get(URL)
    except InvalidArgumentException:
        log.warning("URL이 잘못되었습니다.")
        exit()
    return driver


def such_css_selector_element(driver, action: int, css_selector: str):
    """
    action 1 : 명시적 대기
    action 2 : 요소하나 찾기
    action 3 : 요소들 찾기
    css_selector  : 선택자
    return : 실패시 False, 성공시 요소반환
    """
    try:
        if action == 1:
            result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        elif action == 2:
            result = driver.find_element(By.CSS_SELECTOR, css_selector)
        elif action == 3:
            result = driver.find_elements(By.CSS_SELECTOR, css_selector)
        else:
            result = False
        return result

    except NoSuchElementException:
        log.warning(" 매물를 찾지 못했습니다.")
        exit()


def data_extract(driver, element, filename):
    """
    선택된 매물 데이터 추출
    return list
    """
    data_list = []

    try:
        ActionChains(driver).move_to_element(
            element).click().perform()             # 요소 클릭하기
        circle_check = such_css_selector_element(driver, 1, 'a.is-hover')
    except ElementClickInterceptedException:
        log.warning(" 매물을 클릭하지 못했습니다.")
        return data_list

    time.sleep(0.3)
    # 명시적 기다림, 선택후 변경시
    such_css_selector_element(driver, 1, 'div.item_list.item_list--article')
    estate_list = such_css_selector_element(
        driver, 2, 'div.item_list.item_list--article')
    such_css_selector_element(driver, 1, 'a.is-hover')

    # 선택한 물건 스크롤 내리기
    last_height = driver.execute_script(
        "return arguments[0].scrollHeight", estate_list)
    while 1:
        driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollHeight", estate_list)
        time.sleep(0.5)
        new_height = driver.execute_script(
            "return arguments[0].scrollHeight", estate_list)
        if new_height == last_height:
            break
        last_height = new_height

    driver.save_screenshot(f'{filename}.jpg')

    # 웹페이지 스프에 담기
    soup = BeautifulSoup(driver.page_source, "html.parser")
    selector_price = 'div.price_line'
    selector_spec = 'p.line > span.spec'
    selector_spec = 'div.info_area'

    price_list = soup.select(selector_price)
    spec_list = soup.select(selector_spec)
    del soup

    for price, spec in zip(price_list, spec_list):
        text_price = price.text
        text_spec = spec.text
        data_list.append((text_price, text_spec))
    return data_list
# 선택할 요소가 로드될때까지 대기


# driver = open_windon(URL)
# display = such_css_selector_element(driver, 1, 'a.map_cluster--mix')
# elements = such_css_selector_element(driver, 3, 'a.map_cluster--mix')
# data_list = data_extract(elements)
# print(data_list)
# driver.close()
