import requests
from django.core.files.uploadedfile import SimpleUploadedFile
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
import sys
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.develop")

import django

django.setup()

from products.models import *


# class CachedImage(models.Model):
#     url = models.CharField(max_length=255, unique=True)
#     photo = models.ImageField(upload_to=photo_path, blank=True)
#
#     def cache(self):
#         """Store image locally if we have a URL"""
#
#         if self.url and not self.photo:
#             result = urllib.urlretrieve(self.url)
#             self.photo.save(
#                     os.path.basename(self.url),
#                     File(open(result[0], 'rb'))
#                     )
#             self.save()

def simple_uploaded_file(url):
    basename = os.path.basename(url)
    response = requests.get(url)
    binary_data = response.content
    return SimpleUploadedFile(basename, binary_data)


def parse_brandi():
    data = {}
    how_many = 1
    sleep = 3

    driver = webdriver.Chrome('./chromedriver')
    driver.set_window_size(600, 800)
    driver.implicitly_wait(3)
    driver.get('https://www.brandi.co.kr/category')
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    for i in range(3):
        # 메인카테고리
        data['category'] = re.findall(r'(.*)\n', soup.select('.menu_title')[i].get_text())[0]
        sub_cate = soup.select('ul[data-v-867c5692]')[i].select('li')

        # 카테고리 저장
        # Category(name=data['category']).save()

        for j in range(1, len(sub_cate)):
            # 서브카테고리
            data['sub_category'] = sub_cate[j].get_text()
            link = 'https://www.brandi.co.kr' + sub_cate[j].a.get('href')

            # 서브카테고리 저장
            SubCategory(category=i+1, name=data['sub_category']).save()

            driver.get(link)
            time.sleep(sleep)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            for k in range(how_many):
                p_link = 'https://www.brandi.co.kr' + soup.select('.list_full a')[k].get('href')
                driver.get(p_link)
                time.sleep(sleep)
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # 제품 입장

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
                        data['model_size'] = data.get('model_size', '') + info[l].get_text().replace('\n', "") + '\n'
                else:
                    data['model_size'] = ''
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
                # i 메인 카테고리 번호 j 서브 카테고리 번호 k 제품 번호

                # Category(name=data['category']).save() 위에서 저장
                # SubCategory(category=i, name=data['sub_category']).save() 위에서 저장
                # 브랜드저장
                if not Brand.objects.exists(name=data['brand_name']):
                    img = simple_uploaded_file(data['brand_img'])
                    Brand(name=data['brand_name'], intro=data['intro'], brand_img=img).save()
                #제품저장
                Product(
                    sub_category=j+1,
                    brand=Brand.objects.get(name=data['brand_name']).id,
                    name=data['title'],
                    price=data['price'],
                    discount_rate=data['discount_rate'],
                    sales_count=data['sales_count'],
                    delivery=data['delivery'],
                ).save()
                #제품메인이미지저장
                for l in data['main_img']:
                    img = simple_uploaded_file(l)
                    ProductInfoImage(
                        product=k+1,
                        image=img,
                    )

                #제품정보저장
                ProductInfo(
                    product=k+1,
                    text=data['info_text'],
                )

                #제품정보이미지저장
                for l in data['info_img']:
                    img = simple_uploaded_file(l)
                    ProductInfoImage(
                        product=k+1,
                        image=img,
                    ).save()


                if data['company_name'] == '주식회사 브랜디':
                    SellingInfo(
                        product=k+1,
                        model_size=data['model_size'],
                    ).save()
                else:
                    SellingInfo(
                        product=k+1,
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
                    ).save()

                # 뒤로가기
                driver.back()
                time.sleep(sleep)
                sys.exit()

            driver.back()
            time.sleep(sleep)
    return print('성공')


if __name__ == '__main__':
    parse_brandi()
