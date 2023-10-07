from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View
from .forms import RegisterForm
# Create your views here.

def t(request):
    return render(request, 'home/base.html',{})

class RegisterUser(View):
    template_name = "members/notifacations.html"
    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(redirect_to='127.0.0.1:8000')
        return render(request, self.template_name, {'form': form})