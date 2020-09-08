
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time


def parse_brandi():
    # 데이터 임시 저장 딕셔너리
    data = {}
    # 크롤링할 카테고리 갯수
    cate_num = 5
    # 크롤링할 제품 갯수
    how_many = 20
    # 로딩 기다림
    sleep = 3
    error_code = 0

    # 도중에 중단됐을때 시작 지점
    # 기본값 0
    brand_page_num = 0
    # 기본값 0
    cate_page_num = 4
    # 기본값 1
    sub_page_num = 1
    # 기본값 0
    pd_page_num = 8

    brand_cate = ['/categories/all', '/categories/all/brand', '/categories/all/beauty']

    driver = webdriver.Chrome('./chromedriver')
    driver.set_window_size(600, 800)
    driver.implicitly_wait(3)
    driver.get('https://www.brandi.co.kr/category')
    time.sleep(2)

    for i in range(brand_page_num, 3):
        if brand_page_num != 0:
            brand_page_num = 0
        # 브랜드 카테고리
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        data['brand_cate'] = re.findall(r'(.*)\n', soup.select('.menu_title')[i].get_text())[0]
        link = 'https://www.brandi.co.kr' + brand_cate[i]
        driver.get(link)
        time.sleep(sleep)

        # 아우터 클릭로 스왑
        for j in range(cate_page_num, cate_num):
            if cate_page_num != 0:
                cate_page_num = 0
            button = driver.find_element_by_xpath(f"//ul[@id='sub_gnb']/li[{j + 1}]/a")
            driver.execute_script("arguments[0].click();", button)
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # 카테고리
            data['category'] = soup.select('li[data-v-1cf382de] a.active span')[0].get_text()
            sub_cate = soup.select('tr[data-v-506e5306] td')
            sub_cate_list = list()
            for z in sub_cate:
                sub_cate_b = z.get_text().strip()
                sub_cate_list.append(sub_cate_b)
            sub_cate_list = [v for v in sub_cate_list if v]

            for k in range(sub_page_num, len(sub_cate_list)):
                if sub_page_num != 1:
                    sub_page_num = 1
                # 서브카테고리
                data['sub_category'] = sub_cate_list[k]
                # 서브카테고리 클릭
                x = k // 3 + 1
                y = k % 3 + 1
                button = driver.find_element_by_xpath(f"//tbody[@data-v-506e5306]/tr[{x}]/td[{y}]")
                driver.execute_script("arguments[0].click();", button)
                time.sleep(2)
                # 서브카테고리에서 제품 입장
                for l in range(pd_page_num, how_many):
                    if pd_page_num != 0:
                        pd_page_num = 0
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    try:
                        link = 'https://www.brandi.co.kr' + soup.select('.list_full a')[l].get('href')
                    except:
                        # 제품이 더이상 없을때
                        error_code = 1

                    if error_code:
                        error_code = 0
                        break

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
                    try:
                        data['delivery'] = soup.select_one('.conts-more dd').get_text()
                    except:
                        data['delivery'] = '판매자 배송'
                    # product_text
                    data['info_text'] = soup.select_one('#info_container_1').get_text().replace('\n', '')
                    # product_img
                    img = soup.select('#info_container_1 img')
                    tmp_list = []
                    for n in img:
                        try:
                            tmp_list.append(n['src'])
                        except:
                            pass
                    data['info_img'] = tmp_list

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
                    try:
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
                                data['exchange_refund_info'] = data.get('exchange_refund_info',
                                                                        '') + l.get_text() + '\n'
                    except:
                        data['shipping_info'] = ''
                        data['exchange_refund_info'] = ''

                    # json파일 생성

                    with open(os.path.join(
                            f'./crawling/{data["brand_cate"]}-{data["category"]}-{data["sub_category"].replace("/", "_")}-{data["title"].replace("/", "_")}.json'),
                            'w+') as json_file:
                        json.dump(data, json_file)
                    # 뒤로가기
                    driver.back()
                    time.sleep(sleep)

        # 초기화면으로 가기
        driver.back()
        time.sleep(sleep)

    return print('성공')


if __name__ == '__main__':
    parse_brandi()
