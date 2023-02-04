
import os
from PIL import Image as PIL_Image
from openpyxl.drawing.image import Image


def file_path(file_name):
    """
    실행파일위치에서 파일명 절대위치 반환
    """
    return os.path.join(os.getcwd(), file_name)


def img_reduce_size(img_path):
    """
    이미지를 900x700 사이즈 변경
    """
    img = PIL_Image.open(img_path)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    img_resize = img.resize((900, 700))
    img_resize.save(img_path)

# image 클래스의 객체 img 선언


def xlsx_save(file_excle, sheet, img_path, data_list, file_name):
    """
    엑셀에 작성후 저장
    """
    # 이미지 저장
    img = Image(img_path)
    sheet.add_image(img, "A1")

    # 헤더쓰기
    sheet['M1'] = '번호'
    sheet['N1'] = '층수'
    sheet['O1'] = '거래방식'
    sheet['P1'] = '보증금'
    sheet['Q1'] = '월세'
    sheet['R1'] = '전용면적(평)'
    sheet['S1'] = '평단가'
    # 데이터 표시
    for number, data in enumerate(data_list, start=2):
        temp_data = list(data)
        sheet[f'S{number}'] = temp_data.pop()  # '평단가'
        sheet[f'R{number}'] = temp_data.pop()  # '전용면적'(평)
        temp_data.pop()                       # '전용면적'(m^2)
        sheet[f'Q{number}'] = temp_data.pop()  # '월세'
        sheet[f'P{number}'] = temp_data.pop()  # '보증금'
        sheet[f'O{number}'] = temp_data.pop()  # '거래방식'
        sheet[f'N{number}'] = temp_data.pop()  # '층수'
        sheet[f'M{number}'] = number-1
        # UNPAKING
        # sheet[f'N{number}'], sheet[f'O{number}'],sheet[f'P{number}'],sheet[f'Q{number}'],sheet[f'R{number}'],sheet[f'S{number}'] = data

    file_excle.save(f'{file_name}.xlsx')


def data_purify(data_list):
    """
    들어온 정보를 필요한부분 스플릿
    """
    result_data_list = []
    for data in data_list:
        price_data, area_data, *_ = data

        # 가격을 구함
        if price_data:
            way = price_data[:2]
            if way == "월세":
                deposit, price = price_data[2:].replace(',', '').split('/')
            elif way == '매매':
                temp_price = price_data[2:].replace(
                    '억', '0000+').replace(',', '')
                if temp_price[-1] != '+':
                    price = eval(temp_price)
                else:
                    price = temp_price[:-1]
                deposit = 0

        # 층과 평을 구함
        if area_data:
            temp_area, layer, *_ = area_data.split(',')

            layer = layer.split('층')[0] + '층'

            area1 = temp_area.split('/')[-1].strip()[:-2]
            area2 = format(int(area1) * 0.3025, '.2f')

        # 평단가
        if price and area2:
            average = format(int(price)/float(area2), '.3f')

        result_data_list.append(
            (layer, way, deposit, price, area1, area2, average))
    return result_data_list
