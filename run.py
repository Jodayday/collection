import os
import openpyxl
from excle import file_path
from excle import img_reduce_size
from excle import xlsx_save
from excle import data_purify
from crawling import open_windon
from crawling import such_css_selector_element
from crawling import data_extract
# URL 입력
if __name__ == '__main__':
    # URL = input("가격을 취합할 URL를 입력하세요")
    URL = 'https://new.land.naver.com/offices?ms=37.4000887,126.7285763,19&a=SG&e=RETAIL&ad=true'
    try:
        # 드라이버 작동
        driver = open_windon(URL)

        # 동그라미 표시 확인
        display = such_css_selector_element(driver, 1, 'a.map_cluster--mix')

        # 동그라미 전체 체크
        elements = such_css_selector_element(driver, 3, 'a.map_cluster--mix')

        # 선택된 동그라미의 매물 데이터 뽑기
        for i, element in enumerate(elements, start=1):
            data_list = data_extract(driver, element, f'result/img{i}')

            # 표시하도록 데이터 가공
            result_data_list = data_purify(data_list)

            # 이미지 파일 위치
            img_path = file_path(f'result/img{i}.jpg')

            # 이미지 크기 줄이기
            img_reduce_size(img_path)

            # print(result_data_list)

            file_excle = openpyxl.Workbook()
            sheet = file_excle.active

            xlsx_save(file_excle, sheet, img_path,
                      result_data_list, f'result/result{i}')

        driver.close()
    except Exception:
        exit()
