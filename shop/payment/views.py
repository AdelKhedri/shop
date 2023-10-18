from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from .forms import CardForm, TransactionForm
from .models import Card, Transaction, Cart
from ShopApp.models import Product
from ShopApp.models import Shop
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

    def setup(self, request, username, *args, **kwargs):
        self.transaction_list = Transaction.objects.filter(user=request.user)
        self.cards = Card.objects.filter(user=request.user)
        return super().setup(request, *args, **kwargs)

    def get(self, request, username):
        context = {
            'form_transaction': TransactionForm(),
            'cards': self.cards,
            'transaction_list': self.transaction_list,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, username):
        form = TransactionForm(request.POST)
        context = {
            'form_transaction': TransactionForm(),
            'cards': self.cards,
            'transaction_list': self.transaction_list,
        }
        if form.is_valid():
            amount = form.cleaned_data['amount']
            transaction_type = form.cleaned_data['transaction_type']
            shop_username = request.POST['shop_username']
            shop = Shop.objects.get(manager=request.user, username=shop_username)
            if shop:
                if shop.is_active:
                    if amount > shop.coin and transaction_type == "withdraw":
                        context.update({'msg':'low coin', 'shop_lowe_coin': username})
                    else:
                        card = self.cards.get(id=request.POST.get('card'))
                        description = form.cleaned_data['description']
                        Transaction.objects.create(transaction_type=transaction_type, card=card, amount=amount, description=description, user=request.user, shop=shop)
                        context.update({'msg': 'success'})
                else:
                    context.update({'msg': 'shop not active'})
            else:
                context.update({'msg': 'shop not active'})
        else:
            context.update({'msg': 'failed'})
        return render(request, self.template_name, context)


class AddRemoveToCart(View):
    template_name = "payment/cart_manager.html"

    def setup(self, request, *args, **kwargs):
        self.carts = Cart.objects.filter(customer=request.user)
        return super().setup(request, *args, **kwargs)
    
    def get(self, request):
        context = {
            'carts': self.carts,
        }
        acction = request.GET.get('a')
        id_product = request.GET.get('p')
        id_cart = request.GET.get('c')
        if acction == 'del':
            try:
                Cart.objects.get(customer=request.user, id=id_cart).delete()
            except:
                pass
            context.update({'msg': 'del succes'})
        elif acction == 'add':
            try:
                product = Product.objects.get(id=id_product)
                Cart.objects.create(customer=request.user, product=product)
            except:
                pass
            context.update({"msg": 'add success'})
        else:
            pass

        redirect_page = request.GET.get('re')
        if redirect_page:
            return HttpResponseRedirect(redirect_to=redirect_page)
        return render(request, self.template_name, context)

def alllink(request):
    return render(request, 'home/all.html', {})