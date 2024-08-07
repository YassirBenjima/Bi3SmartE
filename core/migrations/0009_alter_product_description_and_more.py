# Generated by Django 5.0.3 on 2024-04-30 03:42

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_product_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, default='This is the product', null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='specefications',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, default='This is the vendor', null=True),
        ),
    ]
