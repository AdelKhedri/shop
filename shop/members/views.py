from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View, ListView
from .forms import RegisterForm, SininForm, ChangePasswordForm, ProfileUpdateForm, UserUpdateForm
from .models import User, Otp, Notifacation, Profile, Support
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

# Create your views here.

def t(request):
    return render(request, 'home/base.html',{})

class RegisterUser(View):
    template_name = "members/sinup.html"
    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            phone_number = form.cleaned_data['phone_number']

            if phone_number == 11:
                phone_number = phone_number[1:]
            
            user = User.objects.create(username=username, email=email, phone_number=phone_number)
            user.set_password(password)
            user.save()
            Profile.objects.create(user=user)
            otpp = Otp.objects.create(number=int(phone_number), code=145269)
            otpp.save()
            request.session['phone_number'] = phone_number
            return HttpResponseRedirect(redirect_to='/profile/sinup/confirm_phone/')
        return render(request, self.template_name, {'form': form})


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

        if Otp.objects.filter(code=int(verifay_code), number=int(self.phone_number)).exists():
            user = User.objects.get(phone_number=self.phone_number)
            user.is_active = True
            user.save()
            return HttpResponseRedirect(redirect_to="/home/")
        else:
            return render(request, self.template_name, {})


class SininUser(View):
    template_name = "members/sinin.html"

    def get(self, request):
        context = {
            'form': SininForm()
        }
        return render(request, self.template_name, context)
    
    def post(self ,request):
        form = SininForm(request.POST)

        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            if len(str(phone_number)) == 11:
                phone_number = phone_number[1:10]
            user = authenticate(request, username=phone_number, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/home/')
        context = {'form': form}
        return render(request, self.template_name, context)


class ChangePassword(View):
    template_name = 'members/change_password.html'

    def get(self, request):
        form = ChangePasswordForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = ChangePasswordForm(request.POST)
        
        if form.is_valid():
            old_password = form.cleaned_data.get('old_password')
            new_password = form.cleaned_data.get('new_password1')
            user = User.objects.get(username=request.user.username)
            password_check = authenticate(request, phone_number=user.phone_number, password=old_password)

            if password_check is not None:
                user.set_password(new_password)
                user.save()
                return render(request, self.template_name, {"msg": "success"})
            else:
                context = {
                    'form': form,
                    'msg': "old_password",
                }
                return render(request, self.template_name, context)
        return render(request, self.template_name, {'form': form})


class NotifacationView(ListView):
    template_name = "members/notifacations.html"
    model = Notifacation
    context_object_name = "notifacations"
    paginate_by = 8

    def get_queryset(self):
        query = Notifacation.objects.filter(reciver=self.request.user)
        return query


class ProfileUpdate(View):
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
                    user.save()
                    request.session['phone_number'] = phone_number
                    # send_code() this method already is not created.
                    return HttpResponseRedirect(redirect_to="/sinup/confirm_phone/")
                form_user.save()
                context.update({'msg_user': 'update user success'})
        else:
            context.update({'msg_user': 'update user filed'})
        return render(request, self.template_name, context)



class SupportView(View):
    template_name = 'members/support.html'

    def setup(self, request, *args, **kwargs):
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