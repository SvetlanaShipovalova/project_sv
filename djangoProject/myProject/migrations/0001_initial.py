# Generated by Django 4.2.6 on 2023-12-17 07:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import myProject.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='Введите имя заказчика', max_length=50, verbose_name='Имя заказчика')),
                ('last_name', models.CharField(help_text='Введите фамилию заказчика', max_length=50, verbose_name='Фамилия заказчика')),
                ('id_user', models.ForeignKey(blank=True, help_text='Выберите id пользователя', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='id пользователя')),
            ],
            options={
                'db_table': 'Customer',
            },
        ),
        migrations.CreateModel(
            name='Monitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.SlugField(help_text='Введите название модели', verbose_name='Название модели')),
                ('diagonal', models.IntegerField(help_text='Введите размер диагонали', verbose_name='Размер диагонали')),
                ('color', models.CharField(help_text='Введите цвет модели', max_length=50, verbose_name='Цвет')),
            ],
            options={
                'db_table': 'Monitor',
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, help_text='Введите имя поставщика', max_length=50, null=True, verbose_name='Имя поставщика')),
                ('last_name', models.CharField(blank=True, help_text='Введите фамилию поставщика', max_length=50, null=True, verbose_name='Фамилия поставщика')),
                ('id_user', models.ForeignKey(blank=True, help_text='Выберите id пользователя', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='id пользователя')),
            ],
            options={
                'db_table': 'Provider',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(help_text='Введите название местности', verbose_name='Регион местности')),
                ('address', models.CharField(help_text='Введите адрес', max_length=50, verbose_name='Адрес')),
            ],
            options={
                'db_table': 'Region',
            },
        ),
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monitor', models.ManyToManyField(to='myProject.monitor')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myProject.provider', verbose_name='Поставщик')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myProject.region', verbose_name='Регион')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', myProject.models.IntegerRangeField(verbose_name='Номер заказа')),
                ('amount', models.IntegerField(verbose_name='Количество')),
                ('order_date', models.DateField(verbose_name='Дата получения')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myProject.customer', verbose_name='Заказчик')),
                ('monitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myProject.monitor', verbose_name='Монитор')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myProject.provider', verbose_name='Поставщик')),
                ('statistics', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myProject.statistics', verbose_name='Статистика')),
            ],
            options={
                'db_table': 'Order',
            },
        ),
        migrations.AddField(
            model_name='customer',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myProject.region', verbose_name='Регион'),
        ),
    ]
