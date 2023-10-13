from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import View, ListView
from .models import Shop, Product, Category, ProductImage
from .forms import (ShopAddForm, ShopEditeForm,)

# Create your views here.


class SopeCreateView(View):
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
        if form.is_valid():
            name = form.cleaned_data['name']
            username = form.cleaned_data['username']
            description = form.cleaned_data['description']
            small_image = form.cleaned_data['small_image']
            banner_image = form.cleaned_data['banner_image']
            phone_number = form.cleaned_data['phone_number']
            if Shop.objects.filter(username=username).exists():
                self.context.update({'msg': 'username'})
                return render(request, self.tesmplate_name, self.context)
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


class ShopEditeView(View):
    template_name = 'shopapp/shop_edite.html'

    def setup(self, request, username, *args, **kwargs):
        self.shop = Shop.objects.get(username=username, manager=request.user)
        self.form_class = ShopEditeForm(instance=self.shop)
        self.context = {
            'form_edite': self.form_class,
            'shop': self.shop
        }
        return super().setup(request, username, *args, **kwargs)
    
    def get(self, request, username):
        return render(request, self.template_name, self.context)

    def post(self, request, username):
        form = ShopEditeForm(request.POST, request.FILES, instance=self.shop)
        if form.is_valid():
            form.save()
            self.context.update({"msg":"success"})
        else:
            self.context.update({"msg":"failed"})
        return render(request, self.template_name, self.context)

class ShopDeleteView(View):
    def get(self, request, username):
        shop = Shop.objects.get(username=username, manager=request.user).delete()
        return redirect('add shop')


class ShopManagerView(ListView):
    template_name = 'shopapp/shops_manager.html'
    paginate_by = 12
    context_object_name = 'shop_list'

    def get_queryset(self):
        query = Shop.objects.filter(manager=self.request.user)
        return query
    

class ShopMnagementView(View):
    template_name = 'shopapp/shop_dashboard.html'

    def setup(self, request, username, *args, **kwargs):
        self.shop = Shop.objects.get(username=username, manager=request.user)
        self.context = {
            'shop': self.shop,
            'shop_username': self.shop.username,
        }
        return super().setup(request, username, *args, **kwargs)
    
    def get(self, request, username):
        return render(request, self.template_name, self.context)


class ShopAddListProductView(View):
    template_name = 'shopapp/shop_product.html'

    def setup(self, request, username, *args, **kwargs):
        # self.form_class = AddProductForm()
        self.products = Product.objects.filter(shop__username=username, shop__manager=request.user)
        self.context = {
            # 'form_add_product': self.form_class,
            'products_list': self.products,
            'shop_username': username,
        }
        return super().setup(request, username,*args,**kwargs)
    
    def get(self, request, username):
        return render(request, self.template_name, self.context)
    
    def post(self, request, username):
        # form = AddProductForm(request.POST)
        print(request.body)
        # if form.is_valid():
        name = request.POST['name']
        max_sel = request.POST['max_sel']
        price = request.POST['price']
        # shop = form.cleaned_data['shop']
        category = request.POST['category']
        description = request.POST['description']
        if category:
            product = Product.objects.create(name=name, max_sel=max_sel, price=price, shop=Shop.objects.get(username=username), category=Category.objects.get(name=category), description=description)
        else:
            product = Product.objects.create(name=name, max_sel=max_sel, price=price, shop=Shop.objects.get(username=username), description=description)
        self.context.update({'msg': 'success'})
        list_images = []
        number = 1
        while True:
            if f'image_{number}' in request.body:
                list_images.append(f'image_{number}')
            else:
                break
        print(list_images)
        images = 0
        for image in list_images:
            ProductImage.objects.create(product=product, image=request.POST[image])
            images += 1
        self.context.update({'img_count': images})
        # else:
        #     print(22222)
        #     self.context.update({'msg': 'filed'})
        return render(request, self.template_name, self.context)


class DeleteProduct(View):
    def get(self, request, username, pk):
        if Shop.objects.filter(username=username, manager=request.user).exists():
            Product.objects.get(pk=pk).delete()
            return HttpResponseRedirect(redirect_to=f'/shops/managment/{username}/products/')
        else:
            return render(request, 'home/403.html', {})