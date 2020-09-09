import requests
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.develop")
file_path = "./crawling/"
file_list = os.listdir(file_path)
import django

django.setup()

from products.models import *



def simple_uploaded_file(url):
    basename = os.path.basename(url)
    response = requests.get(url, verify=False)
    binary_data = response.content
    return SimpleUploadedFile(basename, binary_data)


def create_data(data_count):
    start_num = 120
    for i in range(start_num, data_count):
        input_dic = []
        with open(f'./crawling/{file_list[i]}', 'r') as json_file:
            data = json.load(json_file)
            # 카테고리
        category = data['category']
        trf = Category.objects.filter(name=category).exists()
        if not trf:
            input_dic = dict(
                name=category
            )
            Category.objects.create(**input_dic)

        # 서브카테고리
        sub_category = data['sub_category']
        cate_ins = Category.objects.get(name=category)
        trf = SubCategory.objects.filter(sub_name=sub_category).exists()
        if not trf:
            input_dic = dict(
                category=cate_ins,
                sub_name=sub_category
            )
            SubCategory.objects.create(**input_dic)

        # 브랜드
        brand_name = data['brand_name']
        trf = Brand.objects.filter(name=brand_name).exists()
        if not trf:
            try:
                brand_cate = data['brand_cate']
                intro = data['intro']
                img = simple_uploaded_file(data['brand_img'])
                input_dic = dict(
                    brand_cate=brand_cate,
                    name=brand_name,
                    intro=intro,
                    brand_img=img
                )
                Brand.objects.create(**input_dic)
            except:
                pass
        # 제품
        title = data['title'],
        trf = Product.objects.filter(name=title).exists()
        if not trf:
            price = data['price']
            discount_rate = data['discount_rate'] / 100
            sales_count = data['sales_count']
            sub_ins = SubCategory.objects.get(sub_name=sub_category)
            brand_ins = Brand.objects.get(name=brand_name)
            input_dic = dict(
                category=cate_ins,
                sub_category=sub_ins,
                brand=brand_ins,
                name=title,
                price=price,
                discount_rate=discount_rate,
                sales_count=sales_count,
            )
            Product.objects.create(**input_dic)

        # 제품정보
        product_ins = Product.objects.get(name=title)
        trf = ProductInfo.objects.filter(product=product_ins).exists()
        if not trf:
            input_dic = dict(
                product=product_ins,
                text=data['info_text'],
            )
            ProductInfo.objects.create(**input_dic)

        # 판매정보

        trf = SellingInfo.objects.filter(product=product_ins).exists()
        if not trf:
            company_name = data['company_name']
            try:
                model_size = data['model_size']
            except:
                model_size = ""
            if company_name == '주식회사 브랜디':
                input_dic = dict(
                    product=product_ins,
                    model_size=model_size,
                )
            else:
                representative = data['representative']
                license_num = data['license_num']
                mail_order_num = data['mail_order_num']
                biz_location = data['biz_location']
                business_hour = data['business_hour']
                company_email = data['company_email']
                company_call = data['company_call']
                shipping_info = data['shipping_info']
                exchange_refund_info = data['exchange_refund_info']
                input_dic = dict(
                    product=product_ins,
                    company_name=company_name,
                    representative=representative,
                    license_num=license_num,
                    mail_order_num=mail_order_num,
                    biz_location=biz_location,
                    biz_hour=business_hour,
                    company_email=company_email,
                    company_call=company_call,
                    model_size=model_size,
                    shipping_info=shipping_info,
                    exchange_refund_info=exchange_refund_info,
                )
            SellingInfo.objects.create(**input_dic)

        # 제품메인이미지저장
        for url in data['main_img']:
            trf = ProductImage.objects.filter(image=url).exists()
            if not trf:
                try:
                    img = simple_uploaded_file(url)
                    input_dic = dict(
                        product=product_ins,
                        image=img
                    )
                    ProductImage.objects.create(**input_dic)
                except:
                    pass

        # 제품정보이미지저장
        product_info_ins = ProductInfo.objects.get(product=product_ins)
        for url in data['info_img']:
            trf = ProductImage.objects.filter(image=url).exists()
            if not trf:
                try:
                    img = simple_uploaded_file(url)
                    input_dic = dict(
                        product_info=product_info_ins,
                        image=img
                    )
                    ProductInfoImage.objects.create(**input_dic)
                except:
                    pass

        print(f'{i+1}번째 등록완료')
    return print('성공')


if __name__ == '__main__':
    create_data(1327)
