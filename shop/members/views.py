import datetime
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View, ListView
from .forms import RegisterForm, SininForm, ChangePasswordForm, ProfileUpdateForm, UserUpdateForm, ForgetPasswordForm, ConfirmForgetPasswordForm
from .models import User, Otp, Notifacation, Profile, Support, BlockIPAddress
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from mylib.apis import sendcode
import random
import datetime
from django.db.models import F
from mylib.functions import get_ipaddress
# Create your views here.

def home(request):
    return render(request, 'home/base.html',{})


class FakeAdminPage(View):
    template_name = 'members/fake_page_admin.html'

    def setup(self, request, *args, **kwargs):
        self.all_block_ip = BlockIPAddress.objects.all()
        self.ip_address = get_ipaddress(request)
        self.context = {
            'ipaddress': self.ip_address,
            'all_block_ip': self.all_block_ip
            }
        return super().setup(request, args, kwargs)
    

    def get(self, request):
        """
        ایپی کاربر در قالب یک پیام هشدار به ادمین ارسال میشه
        """
        # user = User.objects.get(username=request.user.username).get_all_permissions()
        # print(user)
        # sendcode("", {'sender': '10008663', 'receptor': phone_number, 'message': f'هشدار: یک کاربر با ای پی {ip_address} صفحه ادمین تله را باز کرده.'})
        return render(request, self.template_name, self.context)
    

    def post(self, request):
        if not self.all_block_ip.filter(ipaddress=self.ip_address).exists():
            BlockIPAddress.objects.create(ipaddress=self.ip_address)
        return render(request, self.template_name, self.context)


class FreeIp(View):
    def get(self, request):
        ipaddress = get_ipaddress(request)
        object_ipaddress = BlockIPAddress.objects.filter(ipaddress=ipaddress)
        if object_ipaddress.exists():
            object_ipaddress.delete()
        return HttpResponseRedirect('/admin')


class RegisterUser(View):
    template_name = "members/sinup.html"
    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        context = {'form': form}

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password == password2:
                phone_number = form.cleaned_data['phone_number']
                user = User.objects.create(username=username, email=email, phone_number=phone_number)
                user.set_password(password)
                user.save()
                Profile.objects.create(user=user)
                code = random.randint(123456, 989876)
                print(code)
                # frist parameter of sendcode is API of cavenegar. get it from this url: https://panel.kavenegar.com/client/Tour/GetStarted
                # sender parameter of sendcode get it from this url: https://panel.kavenegar.com/client/Lines
                #sendcode('', {'sender': '10008663', 'receptor': phone_number, 'message': f'کد ثبت نام :\n {code}'})
                otpp = Otp.objects.create(number=int(phone_number), code=code, otp_type = "sinup", expire_time=datetime.datetime.now() + datetime.timedelta(seconds=300))
                otpp.save()
                request.session['phone_number'] = phone_number
                return HttpResponseRedirect(redirect_to='/profile/sinup/confirm_phone/')
            else:
                context.update({'msg': 'password not match'})
        return render(request, self.template_name, context)


class RegisterPhone(View):
    template_name = "members/confirm_phone.html"

    def setup(self, request, *args, **kwargs):
        self.phone_number = request.session.get('phone_number')
        return super().setup(request, *args, **kwargs)
    

    def get(self, request):
        context = {
            'phone_number': self.phone_number,
        }
        return render(request, self.template_name, context)
    

    def post(self, request):
        verifay_code = request.POST.get('verifay_code')
        
        if Otp.objects.filter(code=int(verifay_code), number=int(self.phone_number), expire_time__lte=datetime.datetime.now(), otp_type='sinup').exists():
            user = User.objects.get(phone_number=self.phone_number)
            user.is_active = True
            user.save()
            return HttpResponseRedirect(redirect_to="/home/")
        else:
            return render(request, self.template_name, {'msg': 'code not mached.'})


class SininUser(View):
    template_name = "members/sinin.html"

    def get(self, request):
        context = {
            'form': SininForm()
        }
        return render(request, self.template_name, context)
    

    def post(self ,request):
        form = SininForm(request.POST)
        context = {'form': form}

        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None:
                login(request, user)
                if request.GET.get('next'):
                    return HttpResponseRedirect(request.GET.get('next'))
                return HttpResponseRedirect('/profile/')
            else:
                context.update({'msg': 'password failed'})
        return render(request, self.template_name, context)


class ForgetPasswordView(View):
    template_name = "members/forget_password.html"

    def get(self, request):
        form = ForgetPasswordForm()
        return render(request, self.template_name, {'form': form})


    def post(self, request):
        form = ForgetPasswordForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            code = random.randint(121212, 989898)
            print(code)
            otp = Otp.objects.create(number=phone_number, otp_type='f_password', code=code)
            # sendcode('', {'sender': '10008663', 'receptor': phone_number, 'message': f' کد تغییر پسورد:\n {password}'})
            context.update({'msg': 'success'})
            return HttpResponseRedirect('confirm/')
        return render(request, self.template_name, context)


class ConfirmForgetPasswordView(View):
    template_name = "members/confirm_forget_password.html"

    def get(self, request):
        form = ConfirmForgetPasswordForm()
        return render(request, self.template_name, {'form': form})
    

    def post(self, request):
        form = ConfirmForgetPasswordForm(request.POST)
        context = { 'form' : form}
        
        if form.is_valid():
            code = form.cleaned_data['code']
            new_password = form.cleaned_data['new_password']
            phone_number = form.cleaned_data['phone_number']
            if Otp.objects.filter(number=phone_number, code=code, otp_type='f_password', expire_time__gte=datetime.datetime.now()).exists():
                user = User.objects.get(phone_number=phone_number)
                user.set_password(new_password)
                user.save()
                return HttpResponseRedirect('/profile/')
            else:
                context.update({'msg': 'code filed'})
        return render(request, self.template_name, context)
    

class ChangePassword(LoginRequiredMixin, View):
    template_name = 'members/change_password.html'

    def get(self, request):
        form = ChangePasswordForm()
        return render(request, self.template_name, {"form": form})


    def post(self, request):
        form = ChangePasswordForm(request.POST)
        
        if form.is_valid():
            context = {
                    'form': form,
                    'msg': "old_password",
                }
            
            old_password = form.cleaned_data.get('old_password')
            new_password = form.cleaned_data.get('new_password1')
            new_password2 = form.cleaned_data.get('new_password2')
            if new_password == new_password2:
                user = request.user
                password_check = authenticate(request, phone_number=user.phone_number, password=old_password)

                if password_check is not None:
                    user.set_password(new_password)
                    user.save()
                    return render(request, self.template_name, {"msg": "success"})
                else:
                    context.update({'msg': "old_password"})
            else:
                context.update({'msg': "passwords not match",})
        return render(request, self.template_name, context)



class NotifacationView(LoginRequiredMixin, ListView):
    template_name = "members/notifacations.html"
    model = Notifacation
    context_object_name = "notifacations"
    paginate_by = 8


    def get_queryset(self):
        query = Notifacation.objects.filter(reciver=self.request.user)
        return query


class ProfileUpdate(LoginRequiredMixin, View):
    template_name = 'members/profile.html'

    def get(self, request):
        form_profile = ProfileUpdateForm(instance=request.user.profile)
        form_user = UserUpdateForm(instance=request.user)
        context = {
            'form_profile': form_profile,
            'form_user': form_user,
        }
        return render(request, self.template_name, context)


    def post(self, request):
        form_profile = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        form_user = UserUpdateForm(request.POST, instance=request.user)
        context = {
            'form_profile': form_profile,
            'form_user': form_user,
        }
        if form_profile.is_valid():
            form_profile.save()
            context.update({'msg_profile': 'update profile success'})
        # else:
        #     context.update({'msg_profile': 'update profile filed'})
        if form_user.is_valid():
            username = form_user.cleaned_data['username']
            email = form_user.cleaned_data['email']
            phone_number = form_user.cleaned_data['phone_number']
            users = User.objects.all()
            if username != request.user.username and users.filter(username=username).exists():
                context.update({'msg_user':'username error'})
            elif email != request.user.email and users.filter(email=email).exists():
                context.update({'msg_user':'email error'})
            elif phone_number != request.user.phone_number and users.filter(phone_number=phone_number).exists():
                context.update({'msg_user':'phone_number error'})
            else:
                if phone_number == 11:
                    phone_number = phone_number[1:]
                elif phone_number == 10:
                    pass
                user = users.get(id=request.user.id)
                if phone_number != user.phone_number:
                    user.is_active =False
                    user.phone_number = phone_number
                    user.save()
                    request.session['phone_number'] = phone_number
                    code = random.randint(123456, 989876)
                    print(code)
                    otpp = Otp.objects.create(number=int(phone_number), code=code, otp_type = "sinup")
                    # send_code() 
                    return HttpResponseRedirect(redirect_to="/profile/sinup/confirm_phone/")
                form_user.save()
                context.update({'msg_user': 'update user success'})
        else:
            context.update({'msg_user': 'update user filed'})
        return render(request, self.template_name, context)



class SupportView(LoginRequiredMixin, View):
    template_name = 'members/support.html'

    def setup(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages = Support.objects.filter(Q(reciver=request.user) | Q(sender=request.user))
            self.context ={"messages": messages}
        return super().setup(request, *args, **kwargs)
    

    def get(self, request):
        return render(request, self.template_name, self.context)


    def post(self, request):
        message = request.POST.get('message')
        Support.objects.create(sender=request.user, message=message)
        return render(request, self.template_name, self.context)


def custom_404(request, exception):
    return render(request, 'home/404.html', status=404)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/profile/sinin/')
