# Generated by Django 3.0 on 2020-08-31 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20200831_1845'),
    ]

    operations = [
        migrations.RenameField(
            model_name='brand',
            old_name='brand',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='category',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='subcategory',
            old_name='sub_category',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='product',
            name='discount_rate',
            field=models.DecimalField(decimal_places=1, max_digits=3),
        ),
        migrations.AlterField(
            model_name='productoption',
            name='color',
            field=models.CharField(blank=True, choices=[('WH', 'WHITE'), ('BL', 'BLACK'), ('GY', 'GRAY'), ('RD', 'RED'), ('BL', 'BLUE'), ('GR', 'GREEN'), ('YL', 'YELLOW'), ('PP', 'PURPLE'), ('BR', 'BROWN'), ('etc', 'etc')], max_length=3),
        ),
        migrations.AlterField(
            model_name='productoption',
            name='size',
            field=models.CharField(blank=True, choices=[('XS', 'X-SMALL'), ('S', 'SMALL'), ('M', 'MEDIUM'), ('L', 'LARGE')], max_length=2),
        ),
    ]