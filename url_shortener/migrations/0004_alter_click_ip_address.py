# Generated by Django 4.2.11 on 2024-03-12 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('url_shortener', '0003_url_click_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='click',
            name='ip_address',
            field=models.CharField(max_length=200, null=True),
        ),
    ]