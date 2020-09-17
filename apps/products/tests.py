from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from config.settings import MEDIA_ROOT
from products.models import Category, SubCategory, Brand, Product


class ProductTest(APITestCase):
    def setUp(self) -> None:
        image = MEDIA_ROOT + '/test.jpeg'
        test_image = SimpleUploadedFile(
            name='test.jpeg',
            content=open(image, 'rb').read(),
            content_type='image/jpeg'
        )
        self.category = Category.objects.create(name='category test')
        self.subcategory = SubCategory.objects.create(sub_name='subcategory test', category=self.category)
        self.brand = Brand.objects.create(
            name='brand test',
            intro='intro test',
            brand_img=test_image,
        )

        baker.make(Product, _quantity=3)
        self.products = Product.objects.first()

    def test_products_create(self):
        url = '/products/detail'

        data = {
            'category': self.category.id,
            'sub_category': self.subcategory.id,
            'brand': [
                {
                    'id': self.brand.id,
                    'name': self.brand.name
                }
            ],
            'name': 'product test',
            'price': 100000,
            'discount_rate': "0",
            'sales_count': 0,
            'delivery': 'OD',
            'status': 'FS'
        }
        response = self.client.post(url, data=data)
        print(response.data['brand'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.fail()

    def test_products_list(self):
        url = '/products/detail'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_products_retrieve(self):
        url = f'/products/detail/{self.products.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_partial_update(self):
        data = {
            'name': 'product name change'
        }
        response = self.client.patch(f'/products/detail/{self.products.id}', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['name'], response.data['name'])

    def test_product_delete(self):
        url = f'/products/detail/{self.products.id}'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CategoryTest(APITestCase):
    def setUp(self) -> None:
        baker.make(Category, _quantity=1)
        self.category = Category.objects.first()

    def test_products_create(self):
        url = '/products/category'

        data = {
            'name': 'category test',
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_products_list(self):
        url = '/products/category'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_products_retrieve(self):
        url = f'/products/category/{self.category.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_partial_update(self):
        data = {
            'name': 'category name change'
        }
        response = self.client.patch(f'/products/detail/{self.category.id}', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['name'], response.data['name'])

    def test_product_delete(self):
        url = f'/products/detail/{self.category.id}'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class BrandTest(APITestCase):
    def setUp(self) -> None:
        self.brand = Brand.objects.create(
            name='brand',
        )

    def test_products_create(self):
        url = '/products/brand'

        data = {
            'name': 'brand test'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_products_list(self):
        url = '/products/brand'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_products_retrieve(self):
        url = f'/products/brand/{self.brand.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_partial_update(self):
        data = {
            'name': 'brand name change'
        }
        response = self.client.patch(f'/products/brand/{self.brand.id}', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['name'], response.data['name'])

    def test_product_delete(self):
        url = f'/products/brand/{self.brand.id}'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
