# Generated by Django 3.0 on 2020-09-09 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_brand_brand_cate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='main_img', to='products.Product', verbose_name='상품이미지'),
        ),
        migrations.AlterField(
            model_name='productinfoimage',
            name='product_info',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='info_img', to='products.ProductInfo', verbose_name='상품정보이미지'),
        ),
    ]