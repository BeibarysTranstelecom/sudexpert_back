# Generated by Django 4.1.1 on 2022-09-06 19:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='???????????????? ??????????????????')),
            ],
            options={
                'verbose_name': '??????????????????',
                'verbose_name_plural': '??????????????????',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Structure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='???????????????? ??????????????')),
            ],
        ),
        migrations.CreateModel(
            name='Tenders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='???????????????? ??????????????')),
                ('date_start', models.DateField(blank=True, null=True)),
                ('date_end', models.DateField(blank=True, null=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[('CREATED', '??????????????'), ('ON_APPROVE', '???? ????????????????????????'), ('FINISHED', '??????????????????'), ('REJECTED', '??????????????????')], default='CREATED', verbose_name='????????????')),
                ('moderator_complate', models.BooleanField(default=False, verbose_name='???????????????? ????????????????????')),
                ('enable', models.BooleanField(default=False, verbose_name='????????????????')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tenders.category', verbose_name='??????????????????')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tender_customer', to=settings.AUTH_USER_MODEL, verbose_name='????????????????')),
                ('executor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tender_executor', to=settings.AUTH_USER_MODEL, verbose_name='??????????????????????')),
            ],
            options={
                'verbose_name': '??????????????',
                'verbose_name_plural': '??????????????',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(verbose_name='????????')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('executor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_executors', to=settings.AUTH_USER_MODEL, verbose_name='??????????????????????')),
                ('tender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='tenders.tenders', verbose_name='????????????')),
            ],
            options={
                'verbose_name': '??????????????',
                'verbose_name_plural': '??????????????',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('full_name', models.CharField(max_length=150, verbose_name='??????')),
                ('role', models.IntegerField(choices=[('MODERATOR', '??????????????????'), ('CUSTOMER', '????????????????'), ('EXECUTOR', '??????????????????????')], default='EXECUTOR', verbose_name='????????')),
                ('phone', models.CharField(max_length=255, verbose_name='???????????????????? ??????????')),
                ('date_regist', models.DateField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('structure', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tenders.structure', verbose_name='??????????????????')),
            ],
            options={
                'verbose_name': '??????????????',
                'verbose_name_plural': '??????????????',
                'ordering': ['-date_regist'],
            },
        ),
    ]
