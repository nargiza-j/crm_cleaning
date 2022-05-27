# Generated by Django 4.0.4 on 2022-05-24 14:21

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bonus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bonus', models.CharField(blank=True, max_length=300, null=True, verbose_name='Бонус')),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Сумма бонуса')),
            ],
            options={
                'verbose_name': 'Бонус',
                'verbose_name_plural': 'Бонусы',
                'db_table': 'bonus',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=75, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=75, verbose_name='Фамилия')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=15, region='KG', unique=True, verbose_name='Номер телефона')),
                ('organization', models.CharField(blank=True, max_length=120, null=True, verbose_name='Организация')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
                'db_table': 'client',
            },
        ),
        migrations.CreateModel(
            name='Fine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fine', models.CharField(blank=True, max_length=300, null=True, verbose_name='Штраф')),
                ('criteria', models.CharField(blank=True, max_length=255, null=True, verbose_name='Критерий')),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Сумма штрафа')),
                ('description', models.TextField(blank=True, max_length=500, null=True, verbose_name='Пояснение')),
            ],
            options={
                'verbose_name': 'Штраф',
                'verbose_name_plural': 'Штрафы',
                'db_table': 'fine',
            },
        ),
        migrations.CreateModel(
            name='FineCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Категория для штрафа',
                'verbose_name_plural': 'Категории для штрафа',
                'db_table': 'fine_category',
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Инвентарь')),
                ('description', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Инвентарь',
                'verbose_name_plural': 'Инвентари',
                'db_table': 'inventory',
            },
        ),
        migrations.CreateModel(
            name='InventoryOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество')),
                ('inventory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='inventories_order', to='crmapp.inventory', verbose_name='Инвентарь')),
            ],
            options={
                'verbose_name': 'Инвентарь заказа',
                'verbose_name_plural': 'Инвентари заказа',
                'db_table': 'inventory_in_order',
            },
        ),
        migrations.CreateModel(
            name='ObjectType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Тип объекта',
                'verbose_name_plural': 'Типы объекта',
                'db_table': 'object_types',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('new', 'Новый'), ('in_queue', 'В очереди'), ('in_progres', 'Выполняется'), ('done', 'Выполнен'), ('disputable', 'Спорный'), ('to_fix', 'Переделывается'), ('finished', 'Завершен')], default='new', max_length=50, verbose_name='Статус заказа')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания заказа')),
                ('work_start', models.DateTimeField(blank=True, null=True, verbose_name='Дата и время начала уборки')),
                ('cleaning_time', models.DurationField(blank=True, null=True, verbose_name='Время выполнения работ')),
                ('work_end', models.DateTimeField(blank=True, null=True, verbose_name='Дата и время окончания уборки')),
                ('address', models.CharField(max_length=256, verbose_name='Адрес')),
                ('review', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Отзыв')),
                ('payment_type', models.CharField(choices=[('cash', 'Наличная оплата'), ('visa', 'Безналичная оплата')], default='cash', max_length=25, verbose_name='Вид оплаты')),
                ('total_cost', models.PositiveIntegerField(blank=True, null=True, verbose_name='Общая сумма заказа')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Услуга')),
                ('unit', models.CharField(choices=[('square_meter', 'м²'), ('piece', 'шт.'), ('seat_place', 'посад/место'), ('sash', 'створка')], default='square_meter', max_length=350, verbose_name='Единица измерения')),
                ('price', models.PositiveIntegerField(verbose_name='Цена за единицу')),
                ('is_extra', models.BooleanField(verbose_name='Доп. услуга')),
            ],
            options={
                'verbose_name': 'Дополнительная услуга',
                'verbose_name_plural': 'Дополнительные услуги',
                'db_table': 'extra_services',
            },
        ),
        migrations.CreateModel(
            name='StaffOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_brigadier', models.BooleanField(default=False, verbose_name='Бригадир')),
                ('is_accept', models.BooleanField(blank=True, default=False, null=True, verbose_name='Принял заказ')),
                ('in_place', models.DateTimeField(blank=True, null=True, verbose_name='Время прибытия на заказ')),
                ('work_start', models.DateTimeField(blank=True, null=True, verbose_name='Время старта выполнения работ')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_cleaners', to='crmapp.order', verbose_name='Заказ')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cleaner_orders', to=settings.AUTH_USER_MODEL, verbose_name='Клинер')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='Объем работы')),
                ('rate', models.DecimalField(decimal_places=1, default=1, max_digits=2, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(3.0)], verbose_name='Коэффицент сложности')),
                ('total', models.PositiveIntegerField(blank=True, null=True, verbose_name='Стоимость услуги')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='order_services', to='crmapp.order', verbose_name='Заказ')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='service_orders', to='crmapp.service', verbose_name='Услуга')),
            ],
            options={
                'verbose_name': 'Услуга заказа',
                'verbose_name_plural': 'Услуги заказа',
                'db_table': 'service_order',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='cleaners',
            field=models.ManyToManyField(related_name='orders', through='crmapp.StaffOrder', to=settings.AUTH_USER_MODEL, verbose_name='Клинер'),
        ),
        migrations.AddField(
            model_name='order',
            name='client_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_client', to='crmapp.client', verbose_name='Информация клиента'),
        ),
        migrations.AddField(
            model_name='order',
            name='inventories',
            field=models.ManyToManyField(related_name='order_inventories', through='crmapp.InventoryOrder', to='crmapp.inventory', verbose_name='Инвентарь'),
        ),
        migrations.AddField(
            model_name='order',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='manager_order', to=settings.AUTH_USER_MODEL, verbose_name='Менеджер'),
        ),
        migrations.AddField(
            model_name='order',
            name='object_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='crmapp.objecttype', verbose_name='Тип объекта'),
        ),
        migrations.AddField(
            model_name='order',
            name='services',
            field=models.ManyToManyField(related_name='orders', through='crmapp.ServiceOrder', to='crmapp.service', verbose_name='Услуга'),
        ),
        migrations.CreateModel(
            name='ManagerReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary', models.IntegerField(verbose_name='Заработная плата')),
                ('fine', models.IntegerField(blank=True, default=0, null=True, verbose_name='Штраф')),
                ('bonus', models.IntegerField(blank=True, default=0, null=True, verbose_name='Бонус')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения')),
                ('comment', models.CharField(blank=True, max_length=255, null=True, verbose_name='Комментарий')),
                ('bonus_description', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='manager_reports', to='crmapp.bonus', verbose_name='Причина для бонуса')),
                ('cleaner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='manager_report', to=settings.AUTH_USER_MODEL, verbose_name='Клинер')),
                ('fine_description', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='manager_reports', to='crmapp.fine', verbose_name='Причина штрафа')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_manager', to='crmapp.order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Отчет менеджера',
                'verbose_name_plural': 'Отчеты менеджера',
                'db_table': 'manager_report',
            },
        ),
        migrations.AddField(
            model_name='inventoryorder',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='order_inventories', to='crmapp.order', verbose_name='Заказ'),
        ),
        migrations.CreateModel(
            name='ForemanReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expenses', models.PositiveIntegerField(blank=True, null=True, verbose_name='Расходы')),
                ('start_at', models.DateTimeField(blank=True, null=True, verbose_name='Дата и время начала работы')),
                ('end_at', models.DateTimeField(blank=True, null=True, verbose_name='Дата и время окончания работы')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='foreman_order_report', to='crmapp.order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Отчёт бригадира',
                'verbose_name_plural': 'Отчёты бригадира',
                'db_table': 'foreman_report',
            },
        ),
        migrations.CreateModel(
            name='ForemanPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_after', models.BooleanField(default=False, verbose_name='Фото после окончания работ')),
                ('image', models.ImageField(upload_to='photo_foreman/', verbose_name='Фото')),
                ('foreman_report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='foreman_photo', to='crmapp.foremanreport', verbose_name='Фото до начала работ')),
            ],
            options={
                'verbose_name': 'Фотография от бригадира',
                'verbose_name_plural': 'Фотографии от бригадира',
                'db_table': 'foreman_photo',
            },
        ),
        migrations.CreateModel(
            name='ForemanOrderUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='foreman_order_update', to='crmapp.order', verbose_name='Заказ')),
                ('services', models.ManyToManyField(related_name='foreman_order_update', to='crmapp.serviceorder', verbose_name='Услуга')),
            ],
            options={
                'verbose_name': 'Корректировка бригадира',
                'verbose_name_plural': 'Корректировки бригадиров',
                'db_table': 'foreman_order_update',
            },
        ),
        migrations.CreateModel(
            name='ForemanExpenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(verbose_name='Сумма расхода')),
                ('name', models.CharField(max_length=100, verbose_name='Название расхода')),
                ('description', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Описание расхода')),
                ('foreman_report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='foreman_expense', to='crmapp.foremanreport', verbose_name='Отчёт бригадира')),
            ],
        ),
        migrations.AddField(
            model_name='fine',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fines', to='crmapp.finecategory', verbose_name='Категория'),
        ),
    ]
