import requests
from django.core.files.uploadedfile import SimpleUploadedFile
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
import sys
import os
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.develop")

import django

django.setup()

from products.models import *


def simple_uploaded_file(url):
    basename = os.path.basename(url)
    response = requests.get(url)
    binary_data = response.content
    return SimpleUploadedFile(basename, binary_data)


def parse_brandi():
    # 데이터 임시 저장 딕셔너리
    data = {}
    # 크롤링할 카테고리 갯수
    cate_num = 5
    # 크롤링할 제품 갯수
    how_many = 20
    # 로딩 기다림
    sleep = 3
    brand_cate = ['/categories/all', '/categories/all/brand', '/categories/all/beauty']

    driver = webdriver.Chrome('./chromedriver')
    driver.set_window_size(600, 800)
    driver.implicitly_wait(3)
    driver.get('https://www.brandi.co.kr/category')
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    for i in brand_cate:
        # 브랜드 카테고리
        data['brand_cate'] = re.findall(r'(.*)\n', soup.select('.menu_title')[1].get_text())[0]
        link = 'https://www.brandi.co.kr' + i
        driver.get(link)
        time.sleep(sleep)

        # 아우터 클릭로 스왑
        for j in range(cate_num):
            button = driver.find_element_by_xpath(f"//ul[@id='sub_gnb']/li[{j + 1}]/a")
            driver.execute_script("arguments[0].click();", button)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            # 카테고리
            data['category'] = soup.select('li[data-v-1cf382de] a.active span')[0].get_text()
            sub_cate = soup.select('tr[data-v-506e5306] td')
            for k in range(1, len(sub_cate)):
                # 서브카테고리
                data['sub_category'] = sub_cate[k].get_text().strip()
                # 서브카테고리 클릭
                button = driver.find_element_by_xpath(f"//tr[@data-v-506e5306]/td[{k + 1}]")
                driver.execute_script("arguments[0].click();", button)

                # 서브카테고리에서 제품 입장
                for l in range(how_many):
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    link = 'https://www.brandi.co.kr' + soup.select('.list_full a')[l].get('href')

                    # 제품 입장
                    driver.get(link)
                    time.sleep(sleep)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')

                    # 메인 이미지
                    img = soup.select_one('.swiper-wrapper').select('[data-thumb]')
                    data['main_img'] = [n['data-thumb'] for n in img]
                    # 브랜드 이미지
                    brand_img = soup.select_one('.seller-info div')
                    data['brand_img'] = re.findall(r'url[(]["](.*)["]', brand_img['style'])[0]
                    # 브랜드 이름
                    data['brand_name'] = soup.select_one('.info strong.name').get_text()
                    # 브랜드 소개
                    data['intro'] = soup.select_one('.info p.txt').get_text()
                    # 제품 이름
                    data['title'] = soup.select_one('.detail_title').get_text()
                    # 할인율
                    try:
                        discount = soup.select_one('strong.dc').get_text()
                        data['discount_rate'] = int(re.findall(r'\d*', discount)[0].replace('%', ''))
                    except:
                        data['discount_rate'] = 0
                    # 제품가격
                    try:
                        data['price'] = int(soup.select_one('.detail_price .cost .number').get_text().replace(',', ''))
                    except:
                        data['price'] = int(soup.select_one('.detail_price .price .number').get_text().replace(',', ''))
                    # 판매량
                    try:
                        count = soup.select_one('.total-sales').get_text()
                        try:
                            Purchase_count = int(re.findall(r'\d*[,]\d*', count)[0].replace(',', ''))
                        except:
                            Purchase_count = int(re.findall(r'\d*', count)[0])
                    except:
                        Purchase_count = 0
                    data['sales_count'] = Purchase_count
                    # 배송정보
                    data['delivery'] = soup.select_one('.conts-more dd').get_text()
                    # product_text
                    data['info_text'] = soup.select_one('#info_container_1').get_text().replace('\n', '')
                    # product_img
                    img = soup.select('#info_container_1 img')
                    data['info_img'] = [n['src'] for n in img]

                    # 스토어 정보 - 상호명,대표자,사업자등록번호,통신판매업번호,사업장소재지
                    info = soup.select('p.txt-info')
                    slist = ['company_name', 'representative', 'license_num', 'mail_order_num', 'biz_location']
                    for num, field in enumerate(slist):
                        var = info[num].get_text().replace('\n', "")
                        data[field] = re.findall(r'[:]\s*(.*)', var)[0].rstrip()
                    # 스토어 고객센터 - 영업시간,이메일,전화번호
                    data['business_hour'] = soup.select('p.txt-info')[5].get_text()
                    slist = ['company_email', 'company_call']
                    for num, field in enumerate(slist):
                        var = info[num + 6].get_text().replace('\n', "")
                        data[field] = re.findall(r'[:]\s*(.*)', var)[0].rstrip()
                    # 모델 사이즈 정보
                    if soup.find('h4', text="[ 모델 사이즈 정보 ]"):
                        for l in range(8, 12):
                            data['model_size'] = data.get('model_size', '') + info[l].get_text().replace('\n',
                                                                                                         "") + '\n'
                    # 배송정보
                    var = soup.select('h4')[4].parent.select('[data-v-4ced9216]')
                    count = 0
                    page = 1
                    for l in var:

                        if re.match('<h4', str(l)):

                            if count == page:
                                break
                            count += 1
                            continue
                        if count == page:
                            data['shipping_info'] = data.get('shipping_info', '') + l.get_text() + '\n'

                    # 교환/환불정보
                    count = 0
                    page = 2
                    for l in var:

                        if re.match('<h4', str(l)):

                            if count == page:
                                break
                            count += 1
                            continue
                        if count == page:
                            data['exchange_refund_info'] = data.get('exchange_refund_info', '') + l.get_text() + '\n'
                    # 저장하기
                    # 카테고리
                    if not Category.objects.get(name=data['category']):
                        input_dic = dict(name=data['category'])
                        with open('result.json', 'w+') as json_file:
                            json.dump(input_dic, json_file)
                            json_data = json.load(json_file)
                            Category.objects.get_or_create(**json_data)

                    # 서브카테고리
                    cate_ins = Category.objects.get(name=data['category'])
                    if not SubCategory.objects.get(category=cate_ins):
                        input_dic = dict(category=cate_ins, sub_name=data['sub_category'])
                        with open('result.json', 'w+') as json_file:
                            json.dump(input_dic, json_file)
                            json_data = json.load(json_file)
                            SubCategory.objects.get_or_create(**json_data)

                    # 브랜드
                    if not Brand.objects.get(name=data['brand_name']):
                        img = simple_uploaded_file(data['brand_img'])
                        input_dic = dict(
                            brand_cate=data['brand_cate'],
                            name=data['brand_name'],
                            intro=data['intro'],
                            brand_img=img
                        )
                        with open('result.json', 'w+') as json_file:
                            json.dump(input_dic, json_file)
                            json_data = json.load(json_file)
                            Brand.objects.create(**json_data)
                    # 제품
                    if not Product.objects.get(name=data['title']):
                        sub_ins = SubCategory.objects.get(sub_name=data['sub_category'])
                        brand_ins = Brand.objects.get(name=data['brand_name'])
                        input_dic = dict(
                            sub_category=sub_ins,
                            brand=brand_ins,
                            name=data['title'],
                            price=data['price'],
                            discount_rate=data['discount_rate'],
                            sales_count=data['sales_count'],
                        )
                        with open('result.json', 'w+') as json_file:
                            json.dump(input_dic, json_file)
                            json_data = json.load(json_file)
                            Product.objects.create(**json_data)

                    # 제품정보
                    product_ins = Product.objects.get(name=data['title'])
                    if not ProductInfo.objects.get(product=product_ins):
                        input_dic = dict(
                            product=product_ins,
                            text=data['info_text'],
                        )
                        with open('result.json', 'w+') as json_file:
                            json.dump(input_dic, json_file)
                            json_data = json.load(json_file)
                            ProductInfo.objects.create(**json_data)

                    # 판매정보
                    if not SellingInfo.objects.get(product=product_ins):
                        if data['company_name'] == '주식회사 브랜디':
                            input_dic = dict(
                                product=product_ins,
                                model_size=data['model_size'],
                            )
                        else:
                            input_dic = dict(
                                product=product_ins,
                                company_name=data['company_name'],
                                representative=data['representative'],
                                license_num=data['license_num'],
                                mail_order_num=data['mail_order_num'],
                                biz_location=data['biz_location'],
                                business_hour=data['business_hour'],
                                company_email=data['company_email'],
                                company_call=data['company_call'],
                                model_size=data['model_size'],
                                shipping_info=data['shipping_info'],
                                exchange_refund_info=data['exchange_refund_info'],
                            )
                        with open('result.json', 'w+') as json_file:
                            json.dump(input_dic, json_file)
                            json_data = json.load(json_file)
                            SellingInfo.objects.create(**json_data)

                    # 제품메인이미지저장
                    # 이미지 검사 how?
                    for url in data['main_img']:
                        img = simple_uploaded_file(url)
                        input_dic = dict(
                            product=product_ins,
                            image=img
                        )
                        with open('result.json', 'w+') as json_file:
                            json.dump(input_dic, json_file)
                            json_data = json.load(json_file)
                            ProductImage.objects.create(**json_data)

                    # 제품정보이미지저장
                    # 이미지 검사 how?
                    product_info_ins = ProductInfo.objects.get(product=product_ins)
                    for url in data['info_img']:
                        img = simple_uploaded_file(url)
                        input_dic = dict(
                            product_info=product_info_ins,
                            image=img
                        )
                        with open('result.json', 'w+') as json_file:
                            json.dump(input_dic, json_file)
                            json_data = json.load(json_file)
                            ProductInfoImage.objects.create(**json_data)
                    # 뒤로가기
                    driver.back()
                    time.sleep(sleep)
        # 초기화면으로 가기
        driver.back()
        time.sleep(sleep)

    return print('성공')


if __name__ == '__main__':
    parse_brandi()
