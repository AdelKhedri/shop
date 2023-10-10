from django.shortcuts import render
from django.views import View
# Create your views here.

class CardManager(View):
    template_name = "payment/card-manager.html"

    def get(self, request):
        return render(request, self.template_name, {})