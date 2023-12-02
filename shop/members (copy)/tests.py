from django.test import TestCase
from .models import User, Profile, Otp, Notifacation
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
import time
import os

# Create your tests here.

class TestUserModel(TestCase):

    @classmethod
    def setUpClass(cls):
        User.objects.create(first_name="vahid", last_name="vahidi", username='vahid48', email="vahid@gmail.com", phone_number=9929941459, is_active=True, is_staff=True)
        return super().setUpClass()
    
    def test_user(self):
        ins = User.objects.get(username='vahid48')
        self.assertEqual(ins.first_name, "vahid")
        self.assertEqual(ins.last_name, "vahidi")
        self.assertEqual(ins.email, "vahid@gmail.com")
        self.assertEqual(ins.phone_number, 9929941459)
        self.assertTrue(ins.username, "vahid48")
        self.assertTrue(ins.is_active, True)
        self.assertTrue(ins.is_staff, True)
        self.assertFalse(ins.is_superuser, True)


class TestProfileModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="username", email="email@gmail.com")
        Profile.objects.create(user=self.user, image=SimpleUploadedFile('img.png',content=open('/home/mrmirqaed/MyProjects/SitesProjects/myshop/shop/members/img.png', 'rb').read(), content_type='image/jpeg/png'))

    def test_profile(self):
        profile_user = Profile.objects.get(user=self.user)
        self.assertEqual(profile_user.user, self.user)
        self.assertEqual(profile_user.coin, 0)
        self.assertIsNone(profile_user.nashnalcode)
        self.assertEqual(profile_user.image.url, '/media/images/profiles/img.png')
        os.remove('/home/mrmirqaed/MyProjects/SitesProjects/myshop/shop/media/images/profiles/img.png') # delete uploaded last image
        self.assertFalse(profile_user.is_invaited(), False)


class TestOtpModel(TestCase):
    def setUp(self):
        Otp.objects.create(number=9929941450, code=648596)

    def test_otp(self):
        register_object = Otp.objects.get(number=9929941450)
        self.assertEqual(register_object.number, 9929941450)
        self.assertEqual(register_object.code, 648596)
        self.assertGreaterEqual(int(time.time())+300, register_object.expire_time) # assertEqual
        

class TestNotifacationModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="username", email="email@gmail.com")
        self.message = """jeobfnwef
        wefwekfjbwnfwe
        fwefwjbefnwlef
        wefwekfbwef"""
        Notifacation.objects.create(reciver=self.user, message=self.message, color="bg-danger")
    
    def test_notifacation(self):
        notifacation = Notifacation.objects.get(reciver=self.user)
        self.assertEqual(notifacation.reciver, self.user)
        self.assertEqual(notifacation.message, self.message)
        self.assertEqual(notifacation.color, "bg-danger")

class TestMemberPages(TestCase):
    def test_view_url_home(self):
        res = self.client.get('/profile/home/')
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/base.html')
    
    def test_view_url_sinup(self):
        res = self.client.get('/profile/sinup/')
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'members/sinup.html')
    
    def test_view_url_post_sinup(self):
        data = {
            'email': 'sohile@email.com',
            'username' : 'sohile',
            'phone_number' : '09988979969',
            'password1' : '12345678',
            'password2' : '12345678',
        }
        res = self.client.post(reverse('register'), data=data)
        new_user = User.objects.get(username="sohile") #user is created and is_active = False
        self.assertIsInstance(new_user, User)
        self.assertEqual(new_user.username, 'sohile')
        self.assertEqual(res.status_code, 302)


    def test_view_url_confirm_phone(self):
        res = self.client.get('/profile/sinup/confirm_phone/')
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'members/confirm_phone.html')
    
    def test_view_url_post_confirm_phone(self):
        data1 = {
            'email': 'sohile@email.com',
            'username' : 'sohile',
            'phone_number' : '09999999999',
            'password1' : '12345678',
            'password2' : '12345678',
        }
        res_post_1 = self.client.post('/profile/sinup/', data1)
        data2 = {
            'phone_number': self.client.session['phone_number'],
            'verifay_code':145269,
        }
        res_post_2 = self.client.post(res_post_1.url, data2)
        user = User.objects.get(username='sohile')
        self.assertTrue(user.is_active)
        # User.objects.create(first_name="vahid", last_name="vahidi", username='vahid48', email="vahid@gmail.com", phone_number=9999999999)
        # self.client.session['phone_number'] = 9999999999
        # self.client.get('/sinup/confirm_phone/')
        
    def test_view_url_sinin(self):
        res = self.client.get('/profile/sinin/')
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'members/sinin.html')
    
    def test_view_url_post_sinin(self):
        data = {
            'phone_number': 9999999999,
            'password': '12345678',
        }
        res = self.client.post('/profile/sinin/', data)
        self.assertEqual(res.status_code, 200)
    
    # def test_view_url_profile(self):
    #     self.client.login(phone_number=9929941452, password='12345')
    #     res = self.client.get('/profile/')
    #     self.assertEqual(res.status_code, 200)
    #     self.assertTemplateUsed(res, 'members/profile.html')
    
    # def test_view_url_notifacation(self):
    #     client = Client()
    #     client.login(phone_number=9929941452, password='12345')
    #     res = client.get('/profile/notifacations')
    #     self.assertEqual(res.status_code, 200)
    #     self.assertTemplateUsed(res, 'members/notifacations.html')
    
    # def test_view_url_change_password(self):
    #     self.client.login(phone_number=9929941452, password='12345')
    #     res = self.client.get('/profile/change_password/')
    #     self.assertEqual(res.status_code, 200)
    #     self.assertTemplateUsed(res, 'members/change_password.html')


class TestShopPages(TestCase):
    def test_view_url_admin(self):
        data = {
            'phone_number': 9929941452,
            'password': '12345',
        }
        res = self.client.post(r'http://127.0.0.1:8000/oq39r71t!7i6i67w@2fbh4&iyi76*23r(8o7834t-)ry521_trh79a+gre67-wef=12ew[w233]2ew3%7B23eq;234WFEW2%3E234%3C23Q,/', data)
        self.assertEqual(res.status_code, 302)