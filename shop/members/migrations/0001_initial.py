# Generated by Django 4.2.7 on 2023-12-02 11:51

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
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
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(blank=True, max_length=150, null=True, unique=True, verbose_name='ایمیل')),
                ('phone_number', models.BigIntegerField(blank=True, null=True, unique=True, verbose_name='شماره تلفن')),
                ('is_active', models.BooleanField(default=False, verbose_name='اجازه ورود')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربران',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Otp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.BigIntegerField(verbose_name='شماره موبایل')),
                ('code', models.IntegerField(verbose_name='کد تایید')),
                ('expire_time', models.DateTimeField(default=datetime.datetime(2023, 12, 2, 11, 56, 53, 445000), verbose_name='زمان انقضا')),
                ('otp_type', models.CharField(choices=[('sinup', 'sinup'), ('f_password', 'forget password')], max_length=10)),
            ],
            options={
                'verbose_name': 'کد تایید شماره',
                'verbose_name_plural': 'کد های تایید شماره',
            },
        ),
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(max_length=500, verbose_name='متن پیام')),
                ('email', models.CharField(blank=True, max_length=150, null=True, verbose_name='ایمیل')),
                ('send_time', models.DateTimeField(auto_now_add=True, verbose_name='زمان ارسال')),
                ('reciver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reciver', to=settings.AUTH_USER_MODEL, verbose_name='دریافت کننده')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL, verbose_name='ارسال کننده')),
            ],
            options={
                'verbose_name': 'کامند پشتیبانی',
                'verbose_name_plural': 'کامند های پشتیبانی',
                'ordering': ['send_time'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default='images/profiles/default-image-profile.png', null=True, upload_to='images/profiles/', verbose_name='عکس پروفایل')),
                ('coin', models.IntegerField(default=0, verbose_name='موجودی(ریال)')),
                ('invaited', models.CharField(blank=True, max_length=100, null=True, verbose_name='افراد دعوت شده')),
                ('nashnalcode', models.IntegerField(blank=True, null=True, verbose_name='کد ملی')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'پروفایل',
                'verbose_name_plural': 'پروفایل ها',
                'ordering': ['user', 'coin'],
            },
        ),
        migrations.CreateModel(
            name='Notifacation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(max_length=800, verbose_name='متن اعلان')),
                ('color', models.CharField(choices=[('bg-danger', 'danger'), ('bg-warning', 'warning'), ('bg-success', 'success'), ('bg-info', 'info'), ('bg-secondary', 'seccondry'), ('bg-primary', 'primary')], default='info', max_length=12, verbose_name='رنگ')),
                ('reciver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='دریافت کننده')),
            ],
            options={
                'verbose_name': 'نوتیفیکیشن',
                'verbose_name_plural': 'نوتیفیکیشن ها',
            },
        ),
    ]