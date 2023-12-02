# Generated by Django 4.2.7 on 2023-12-02 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BuyProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='زمان')),
            ],
            options={
                'verbose_name': 'محصول خریداری شده',
                'verbose_name_plural': 'محصولات خریداری شده',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='نام')),
                ('for_sell', models.BooleanField(default=False, verbose_name='برای نمایش در صفحه اول فروشگاه')),
                ('number_ordering', models.IntegerField(blank=True, null=True, verbose_name='شماره ردیف')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='نام')),
                ('max_sel', models.IntegerField(blank=True, null=True, verbose_name='حداکثر فروش(تعداد فروش)')),
                ('price', models.IntegerField(default=0, verbose_name='قیمت')),
                ('description', models.CharField(blank=True, max_length=400, null=True, verbose_name='درباره')),
            ],
            options={
                'verbose_name': 'محضول',
                'verbose_name_plural': 'محصولات',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/products/', verbose_name='عکس محصول')),
            ],
            options={
                'verbose_name': 'عکس محصول',
                'verbose_name_plural': 'عکس محصولات',
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='نام ')),
                ('username', models.CharField(max_length=150, unique=True, verbose_name='ایدی')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='درباره')),
                ('small_image', models.ImageField(blank=True, default='images/shops/default-image-small.png', null=True, upload_to='images/shops/', verbose_name='عکس')),
                ('banner_image', models.ImageField(blank=True, default='images/shops/default-image-banner.png', null=True, upload_to='images/shops/', verbose_name='بنر')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال')),
                ('phone_number', models.BigIntegerField(blank=True, null=True, verbose_name='شماره تلفن')),
                ('coin', models.IntegerField(default=0, verbose_name='موجودی')),
            ],
            options={
                'verbose_name': 'فروشگاه',
                'verbose_name_plural': 'فروشگاها',
            },
        ),
        migrations.CreateModel(
            name='Social',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('instagram.com/', 'اینستاگرام'), ('t.me/', 'تلگرام'), ('snapchat.com/add/', 'اسنپ چت'), ('wa.me/', 'واتساپ'), ('Facebook.com/', 'فیسبوک')], max_length=100, verbose_name='نام')),
                ('address', models.CharField(max_length=100, verbose_name='نام کاربری')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShopApp.shop', verbose_name='فروشگاه')),
            ],
            options={
                'verbose_name': 'آدرس شبکه اجتماعی',
                'verbose_name_plural': 'آدرس شبکه های اجتماعی',
            },
        ),
    ]