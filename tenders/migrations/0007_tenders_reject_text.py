# Generated by Django 4.1.1 on 2022-09-19 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenders', '0006_tenders_description_alter_tenders_date_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenders',
            name='reject_text',
            field=models.TextField(default='', verbose_name='Описание'),
        ),
    ]