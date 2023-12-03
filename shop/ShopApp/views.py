from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import JsonResponse
from django.core import serializers
from django.views.generic import View, ListView
from .models import Shop, Product, Category, ProductImage, BuyProduct
from payment.models import Transaction, Card, Cart, Likes
from payment.forms import TransactionForm
from .forms import (ShopAddForm, ShopEditeForm, CreateCategorysForm, EditeCategoryForm, UpdateProductForm)
import datetime
from django.db.models import Count, Max, Sum
import json
from django.db.models import F, Subquery
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class SopeCreateView(LoginRequiredMixin, View):
    tesmplate_name = "shopapp/shop_create_list.html"

    def setup(self, request, *args, **kwargs):
        self.shop_list = Shop.objects.filter(manager = request.user)
        self.context = {
            'shop_list': self.shop_list,
            'form_shop': ShopAddForm(),
        }
        return super().setup(request, *args, **kwargs)
    
    def get(self, request):
        return render(request, self.tesmplate_name, self.context)

    def post(self, request):
        form = ShopAddForm(request.POST, request.FILES)
        self.context.update({'form_shop': form})
        if form.is_valid():
            name = form.cleaned_data['name']
            username = form.cleaned_data['username']
            description = form.cleaned_data['description']
            small_image = form.cleaned_data['small_image']
            banner_image = form.cleaned_data['banner_image']
            phone_number = form.cleaned_data['phone_number']
            if (small_image is None and banner_image is None) or len(banner_image) < 4 and len(small_image) < 4:
                Shop.objects.create(manager=request.user, name=name, username=username, description=description, phone_number=phone_number)
            elif small_image is None or len(small_image) < 4:
                Shop.objects.create(manager=request.user, name=name, username=username, description=description, banner_image=banner_image, phone_number=phone_number)
            elif banner_image is None or len(banner_image) < 4:
                Shop.objects.create(manager=request.user, name=name, username=username, description=description, small_image=small_image, phone_number=phone_number)
            else:
                Shop.objects.create(manager=request.user, name=name, username=username, description=description, small_image=small_image, banner_image=banner_image, phone_number=phone_number)
            self.context.update({"msg": "success"})
        else:
            self.context.update({'msg':'failed'})
        return render(request, self.tesmplate_name, self.context)


class ShopEditeView(LoginRequiredMixin, View):
    template_name = 'shopapp/shop_create_list.html'

    def setup(self, request, username, *args, **kwargs):
        self.shop_list = Shop.objects.filter(manager = request.user)
        self.shop = Shop.objects.get(username=username, manager=request.user)
        form_class = ShopEditeForm(instance=self.shop)
        self.context = {
            'shop_list': self.shop_list,
            'form_shop': form_class,
            'shop': self.shop
        }
        return super().setup(request, username, *args, **kwargs)
    

    def get(self, request, username):
        return render(request, self.template_name, self.context)


    def post(self, request, username):
        form = ShopEditeForm(request.POST, request.FILES, instance=self.shop)
        if form.is_valid():
            form.save()
            print(False)
            self.context.update({"msg":"success"})
        else:
            print(True)
            self.context.update({"msg":"failed"})
        return render(request, self.template_name, self.context)


class ShopDeleteView(LoginRequiredMixin, View):
    def get(self, request, username):
        shop = Shop.objects.get(username=username, manager=request.user).delete()
        return redirect('add shop')


class ShopManagerView(LoginRequiredMixin, ListView):
    template_name = 'shopapp/shops_manager.html'
    paginate_by = 12
    context_object_name = 'shop_list'

    def get_queryset(self):
        query = Shop.objects.filter(manager=self.request.user)
        return query
    

class ShopMnagementView(LoginRequiredMixin, View):
    template_name = 'shopapp/shop_dashboard.html'

    def setup(self, request, username, *args, **kwargs):
        shop = Shop.objects.get(username=username, manager=request.user)
        # all_sells =  BuyProduct.objects.filter(shop__manager__username=request.user.username,shop__username=username).count()
        self.context = {
            'shop': shop,
            'shop_username': username,
        }
        return super().setup(request, username, *args, **kwargs)
    
    def get(self, request, username):
        return render(request, self.template_name, self.context)


class ShopAddListProductView(LoginRequiredMixin, View):
    template_name = 'shopapp/shop_product.html'

    def setup(self, request, username, *args, **kwargs):
        # self.form_class = AddProductForm()
        products = Product.objects.filter(shop__username=username, shop__manager=request.user)
        categorys_list = Category.objects.filter(shop__username=username, shop__manager=request.user)
        self.context = {
            # 'form_add_product': self.form_class,
            'categorys_list': categorys_list,
            'products_list': products,
            'shop_username': username,
        }
        return super().setup(request, username,*args,**kwargs)
    
    def get(self, request, username):
        return render(request, self.template_name, self.context)
    
    def post(self, request, username):
        # form = AddProductForm(request.POST)
        # if form.is_valid():
        name = request.POST.get('name')
        max_sel = request.POST.get('max_sel')
        price = request.POST.get('price')
        categorys_list = request.POST.getlist('category')
        description = request.POST.get('description')
        product = Product.objects.create(name=name, max_sel=max_sel, price=price, shop=Shop.objects.get(username=username), description=description)
        if categorys_list:
            categorys_list_obj=Category.objects.filter(id__in=categorys_list, shop__username=username)
            for i in categorys_list_obj:
                i.products.add(product)
        self.context.update({'msg': 'success',})

        list_images = []
        number = 1
        while True:
            if request.FILES.getlist(f'image_{number}'):
                list_images.append(f'image_{number}')
                number+=1
            else:
                break
        images = 0
        for image in list_images:
            ProductImage.objects.create(product=product, image=request.FILES[image])
            images += 1
        self.context.update({'img_count': images})

        return render(request, self.template_name, self.context)


class DeleteProductView(LoginRequiredMixin, View):
    def get(self, request, username, pk):
        if Shop.objects.filter(username=username, manager=request.user).exists():
            Product.objects.get(pk=pk).delete()
            # BuyProduct.objects.filter(product__id=pk).delete()
            return HttpResponseRedirect(redirect_to=f'/shops/managment/{username}/products/')
        else:
            return render(request, 'home/403.html', {})


class DetailsProductView(LoginRequiredMixin, View):
    def get(self, request, username, pk):
        product = Product.objects.get(shop__username=username, id=pk)
        images = ProductImage.objects.filter(product__id=pk)
        categorys = Category.objects.filter(shop__username=username, products=product)
        print(categorys)

        i = 1
        today = datetime.datetime.now()
        context = {
            'product': product,
            'category_lists': categorys,
            'product_images': images, 
            'shop_username': username,
        }
        while i <= 7:
            yesterday = today-datetime.timedelta(days=1)
            product_info = BuyProduct.objects.filter(product=product, shop__username=username, shop__manager=request.user, time__range=(yesterday, today), is_payed=True).values('price').aggregate(sum_price=Sum('price'), count=Count('price'))
            # print(product_info)
            context.update({f'info_{i}_day': product_info, f'info_{i}_day_time': today.date})
            today=yesterday
            i+=1
        i=1
        return render(request, 'shopapp/shop_detail_product.html', context)


class UpdateProductView(LoginRequiredMixin, View):
    template_name = 'shopapp/shop_product_update.html'
    def setup(self, request, username, pk, *args, **kwargs):
        product = Product.objects.get(id=pk, shop__manager=request.user, shop__username=username)
        categorys_list = Category.objects.filter(shop__username=username, shop__manager=request.user)
        form_class = UpdateProductForm(instance=product)
        product_images_list = ProductImage.objects.filter(product=product)
        self.context = {
            'categorys_list': categorys_list,
            'form_product': form_class,
            'product': product,
            'products_image': product_images_list,
            'shop_username': username,
        }
        return super().setup(request, username, pk, *args, **kwargs)
    
    def get(self, request, username, pk):
        return render(request, self.template_name, self.context)
    
    def post(self, request, username, pk):
        form = UpdateProductForm(request.POST, instance=self.product)
        if form.is_valid():
            form.save()
            self.context.update({
                'form_product': UpdateProductForm(request.POST),
                'msg': 'success'
                })

            category_client_list = request.POST.getlist('category')
            category_add = [int(i) for i in category_client_list]
            categorys_product = Category.objects.filter(products__id=self.product.id)
            category_remove = [] #remove the product from this categorys list

            for cate_db in categorys_product:
                if cate_db.id not in category_add: # if a category do not selected
                    category_remove.append(cate_db.id)
                else: # if the category is already selected
                    category_add.remove(cate_db.id)
            
            for i in category_add:
                category = Category.objects.get(shop__username=username, shop__manager=request.user, id=i)
                category.products.add(self.product)
            for i in category_remove:
                category = Category.objects.get(shop__username=username, shop__manager=request.user, id=i)
                category.products.remove(self.product)
            
            # images_add = []
            # images_remove = []
            # number = 1
            # while True:
            #     if request.FILES.getlist(f'image_{number}'):
            #         images_add.append(request.FILES.getlist(f'image_{number}'))
            #     else:
            #         break

            # for image in self.product_images_list:
            #     x1 = str(image.image).rfind('/')
            #     name = str(image.image)[x1+1:]
            #     if name in images_add:
            #         images_add.remove(name)
            #     else:
            #         images_remove.append(name)
        return render(request, self.template_name, self.context)

class CategoryManagerView(LoginRequiredMixin, View):
    template_name = "shopapp/category_manager.html"

    def setup(self, request, username, *args, **kwargs):
        categorys = Category.objects.filter(shop__username=username, shop__manager=request.user)
        products = Product.objects.filter(shop__manager=request.user, shop__username=username)
        form_class = CreateCategorysForm()
        self.context = {
            'shop_username': username,
            'categorys': categorys,
            'form': form_class,
            'products_list': products,
            'title': 'مدیریت دسته بندی ها'
        }
        return super().setup(request, username, *args, **kwargs)
    
    
    def get(self, request, username):
        return render(request, self.template_name, self.context)


    def post(self, request, username):
        form = CreateCategorysForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            for_sell = form.cleaned_data['for_sell']
            number_ordering = form.cleaned_data['number_ordering']
            products_list = request.POST.getlist('products')
            products_list_obj = Product.objects.filter(id__in=products_list, shop__username=username)
            # print(products_id) warring on get list of all selected values
            c = Category.objects.create(name=name, shop=Shop.objects.get(username=username), for_sell=for_sell, number_ordering=number_ordering)
            c.products.set(products_list_obj)
            self.context.update({'msg': 'success'})
        else:
            self.context.update({'msg': 'failed'})
        return render(request, self.template_name, self.context)


class DeleteCategoryView(LoginRequiredMixin, View):
    def get(self, request, username, pk):
        category_query = Category.objects.filter(shop__username=username, shop__manager=request.user, id=pk).delete()
        return redirect('categorys manager',username=username)


class EditeCategoryView(LoginRequiredMixin, View):
    template_name = 'shopapp/category_manager.html'

    def setup(self, request, username, pk, *args, **kwargs):
        category = Category.objects.get(id=pk, shop__username=username, shop__manager=request.user)
        form_class = CreateCategorysForm(initial={'name':category.name, 'for_sell': category.for_sell, 'number_ordering': category.number_ordering})
        product_list = Product.objects.filter(shop__username=username, shop__manager=request.user)
        self.context = {
            'category':category,
            'form': form_class,
            'shop_username': username,
            'products_list': product_list,
            'title': f'ویرایش دسته بندی {category.name}'
        }
        return super().setup(request, username, pk, *args, **kwargs)
    
    def get(self, request, username, pk):
        return render(request, self.template_name, self.context)
    
    def post(self, request, username, pk):
        form = CreateCategorysForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            for_sell = form.cleaned_data['for_sell']
            number_ordering = form.cleaned_data['number_ordering']
            products_list = request.POST.getlist('products')
            products_list_obj = Product.objects.filter(id__in=products_list)
            category = Category.objects.get(id=pk, shop__username=username, shop__manager=request.user)
            category.name=name
            category.for_sell=for_sell
            category.number_ordering=number_ordering
            category.shop__username=username
            category.products.set(products_list_obj)
            category.save()
            self.context.update({'msg':'success'})
            self.context.update({'form': EditeCategoryForm(initial={'name':category.name, 'for_sell': category.for_sell, 'number_ordering': category.number_ordering})})
        else:
            self.context.update({'msg':'filed'})
        return render(request, self.template_name, self.context)



class OrderListView(LoginRequiredMixin, View):
    def get(self, request, username):
        orderlist = BuyProduct.objects.filter(shop__username=username, shop__manager=request.user, is_payed=True).values('product', 'price', 'time')
        context = {
            'orders_list': orderlist,
            'shop_username': username,
        }
        return render(request, 'shopapp/order_product_list.html', context)


class InfoSellView(LoginRequiredMixin, View):
    def get(self, request, username):
        i=1
        context = {'shop_username':username}
        today = datetime.datetime.now()
        while i <= 7:
            yesterday = today-datetime.timedelta(days=1)
            info_days = BuyProduct.objects.filter(shop__username=username, shop__manager=request.user, time__range=(yesterday,today, ) , is_payed=True).values('price',).aggregate(count=Count('price'), sum_price=Sum('price'))
            today=yesterday
            context.update({f'info_{i}_day': info_days, f'info_{i}_day_time': today.date})
            i+=1
        i=1
        return render(request, 'shopapp/info_sells.html', context)


class RequestPaymentView(LoginRequiredMixin, View):
    template_name = 'payment/request_payment.html'

    def setup(self, request, username, *args, **kwargs):
        self.transaction_list = Transaction.objects.filter(user=request.user, shop__username=username, shop__is_active=True)
        self.cards = Card.objects.filter(user=request.user)
        self.shop_list = Shop.objects.filter(manager=request.user, is_active=True)
        self.context = {
            'form_transaction': TransactionForm(),
            'cards': self.cards,
            'shops_list': self.shop_list,
            'shop_username': username,
            'transaction_list': self.transaction_list,
        }
        return super().setup(request, *args, **kwargs)

    def get(self, request, username):
        return render(request, self.template_name, self.context)
    
    def post(self, request, username):
        form = TransactionForm(request.POST)
        self.context.update({'form_transaction': TransactionForm()})
        if form.is_valid():
            amount = form.cleaned_data['amount']
            transaction_type = form.cleaned_data['transaction_type']
            shop_username = request.POST['shop_username']
            shop = Shop.objects.get(manager=request.user, username=shop_username)
            if shop:
                if shop.is_active:
                    if amount > shop.coin and transaction_type == "withdraw":
                        self.context.update({'msg':'low coin', 'shop lowe coin': username})
                    else:
                        card = self.cards.get(id=request.POST.get('card'))
                        description = form.cleaned_data['description']
                        Transaction.objects.create(transaction_type=transaction_type, card=card, amount=amount, description=description, user=request.user, shop=shop)
                        self.context.update({'msg': 'success'})
                else:
                    self.context.update({'msg': 'shop not active'})
            else:
                self.context.update({'msg': 'shop not found'})
        else:
            self.context.update({'msg': 'failed'})
        return render(request, self.template_name, self.context)


class ShopView(View):
    def get(self, request, username):
        shop = Shop.objects.get(username=username)
        all_sell = BuyProduct.objects.filter(shop__username=username, is_payed=True).count()
        categorys = Category.objects.filter(shop__username=username)
        # cat = Category.objects.filter(shop__username=username).prefetch_related('products').annotate(left_over_sel=F('products__max_sel'))
        # for a in cat:
        #     print(a.left_over_sel)
        #     for b in a.products.all():
        #         print(b)
        products = Product.objects.filter(shop__username=username)
        products_ids = [p.id for p in products]
        imgs_product = ProductImage.objects.filter(product__in=products_ids)
        context = {
            'shop': shop,
            'all_sell': all_sell,
            'categorys_list': categorys,
            'imgs_list': imgs_product
        }


        if request.user.is_authenticated:
            print(request.user)
            likes = Likes.objects.filter(user=request.user).values('product__id')
            likes_list = [item['product__id'] for item in likes]
            context.update({'likes_list': likes_list,})
        
        
        return render(request, 'shopview/shop_info.html', context)


class ShopCategorysView(View):
    def get(self, request, username):

        categorys = list(Category.objects.filter(shop__username=username, for_sell=True).values())
        context = {
            'categorys_list': categorys,
        }
        return JsonResponse(context, safe=False, json_dumps_params={'ensure_ascii':False})


class ShopProductsView(View):
    def get(self, request, username):

        products = list(Product.objects.filter(shop__username=username).values())
        context = {
            'products_list': products,
        }
        return JsonResponse(context, safe=False, json_dumps_params={'ensure_ascii': False})


class CartManagerView(LoginRequiredMixin, View):
    template_name = 'shopapp/cart_manager.html'

    def get(self, request):
        carts = Cart.objects.filter(customer=request.user)
        context = {
            'carts_list': carts,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        product_id = request.POST.get('product')
        count = request.POST.get('product_count')
        if product_id is not None:
            product = Product.objects.get(id=product_id)
            context = {'msg': 'created'}
            try:
                cart = Cart.objects.get(customer=request.user, product__id=product_id)
                cart.count = count
                cart.save()
                context.update({'msg' : 'updated'})
            except:
                cart = Cart.objects.create(customer=request.user, product=product, count=count)
            
            cart_serialized = serializers.serialize('json', [cart])
            product_serialized = serializers.serialize('json', [product])
            context.update({
                'product': product_serialized,
                'cart': cart_serialized})
            
            return JsonResponse(json.dumps(context),safe=False)
        else:
            return JsonResponse({'msg': 'product must a integer'}, safe=False)



class DeleteCart(View):
    def post(self, request):
        product_id = request.POST.get('product')
        print(product_id)
        if product_id is not None:
            context = {'msg': 'created'}
            cart = Cart.objects.get(customer=request.user, product__id=product_id)
            print(cart)
            cart.delete()
            context.update({'msg' : 'deleted'})
            return JsonResponse(context)
        return JsonResponse({'msg': 'product must be a integer'})


class LikeView(View):
    template_name = 'shopapp/like.html'
    
    def get(self, request):
        likes = Likes.objects.filter(user=request.user)
        p_ids = [i.product.id for i in likes]
        imgs_product = ProductImage.objects.filter(product__in=p_ids)
        print(imgs_product)
        context = {
            'likes_list': likes,
            'imgs_list': imgs_product,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        product_id = request.POST.get('product_like')
        if product_id is not None:
            try:
                product = Product.objects.get(id=product_id)
                try:
                    Likes.objects.get(user=request.user, product__id=product_id).delete()
                    return JsonResponse({'msg': 'deleted'})
                except:
                    Likes.objects.create(product=product, user=request.user)
                    return JsonResponse({'msg': 'success'})
            except:
                return JsonResponse({'msg': 'product not found'})


class ShopView2(View):
    def get(self, request, username):
        return render(request, 'shopview/d.html', {})