# Generated by Django 4.1.1 on 2022-09-19 18:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tenders', '0007_tenders_reject_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenders',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tender_winner', to=settings.AUTH_USER_MODEL, verbose_name='Победитель'),
        ),
    ]
