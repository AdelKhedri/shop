# Generated by Django 4.2.7 on 2023-12-02 11:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ShopApp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.IntegerField(verbose_name='شماره کارت')),
                ('shaba_number', models.CharField(max_length=24, verbose_name='شماره شبا')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'کارت بانکی',
                'verbose_name_plural': 'کارت های بانکی',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('withdraw', 'برداشت'), ('deposit', 'پرداخت')], max_length=8, verbose_name='نوع تراکنش')),
                ('amount', models.IntegerField(verbose_name='مقدار')),
                ('transaction_time', models.DateTimeField(auto_now_add=True, verbose_name='زمان تراکنش')),
                ('is_payed', models.BooleanField(default=False, verbose_name='پرداخت شده')),
                ('ref_id', models.IntegerField(blank=True, null=True, verbose_name='ای دی رف')),
                ('description', models.CharField(blank=True, max_length=300, null=True, verbose_name='جزییات')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.card', verbose_name='کارت پرداخت کننده')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShopApp.shop', verbose_name='فروشگاه')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'تراکنش',
                'verbose_name_plural': 'تراکنش ها',
                'ordering': ['transaction_time'],
            },
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShopApp.product', verbose_name='محصول')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'پسندیده',
                'verbose_name_plural': 'پسندیده ها',
                'ordering': ['product__name'],
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1, verbose_name='تعداد')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='خریدار')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShopApp.product', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'سبدخرید',
                'verbose_name_plural': 'سبد های خرید',
            },
        ),
    ]