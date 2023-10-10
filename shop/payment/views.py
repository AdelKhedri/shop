from django.shortcuts import render
from django.views import View
from .forms import CardForm, TransactionForm
from .models import Card, Transaction

# Create your views here.

class CardManager(View):
    template_name = "payment/card_manager.html"

    def setup(self, request, *args, **kwargs):
        self.cards = Card.objects.filter(user=request.user)
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        id_card = request.GET.get('card_id')
        if id_card:
            try:
                Card.objects.get(id=id_card).delete()
            except:
                pass
        
        form = CardForm()
        context = {
            'form': form,
            'cards': self.cards
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = CardForm(request.POST)
        context = {
            'form': CardForm(),
            'cards': self.cards,
        }
        if form.is_valid():
            card_number = form.cleaned_data['card_number']
            shaba_number = form.cleaned_data['shaba_number']
            Card.objects.create(card_number=card_number, shaba_number= shaba_number, user=request.user)
            context.update({'msg': 'success'})
        return render(request, self.template_name, context)



class RequestPaymentView(View):
    template_name = 'payment/request_payment.html'

    def setup(self, request, *args, **kwargs):
        self.transaction_list = Transaction.objects.filter(user=request.user)
        self.cards = Card.objects.filter(user=request.user)
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        context = {
            'form_transaction': TransactionForm(),
            'cards': self.cards,
            'transaction_list': self.transaction_list,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = TransactionForm(request.POST)
        context = {
            'form_transaction': TransactionForm(),
            'card': self.cards,
            'transaction_list': self.transaction_list,
        }
        if form.is_valid():
            transaction_type = form.cleaned_data['transaction_type']
            card = form.cleaned_data['card']
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']
            Transaction.objects.create(transaction_type=transaction_type, card=card, amount=amount, description=description, user=request.user)
            context.update({'msg': 'success'})
        else:
            context.update({'msg': 'failed'})
            
        return render(request, self.template_name, context)