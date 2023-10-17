from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import View, ListView
from .models import Shop, Product, Category, ProductImage
from .forms import (ShopAddForm, ShopEditeForm, CreateCategorysForm, EditeCategoryForm)

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


class DeleteProductView(View):
    def get(self, request, username, pk):
        if Shop.objects.filter(username=username, manager=request.user).exists():
            Product.objects.get(pk=pk).delete()
            return HttpResponseRedirect(redirect_to=f'/shops/managment/{username}/products/')
        else:
            return render(request, 'home/403.html', {})


class DetailsProductView(View):
    def get(self, request, username, pk):
        product = Product.objects.get(shop__username=username, id=pk)
        images = ProductImage.objects.filter(product=product)
        context = {
            'product': product,
            'product_images': images, 
        }
        return render(request, 'shopapp/shop_detail_product.html', context)


class CategoryManagerView(View):
    template_name = "shopapp/category_manager.html"

    def setup(self, request, username, *args, **kwargs):
        self.categorys = Category.objects.filter(shop__username=username, shop__manager=request.user)
        self.products = Product.objects.filter(shop__manager=request.user, shop__username=username)
        self.form_class = CreateCategorysForm()
        self.context = {
            'shop_username': username,
            'categorys': self.categorys,
            'form': self.form_class,
            'products_list': self.products
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
            products_str = request.POST['products']
            products_id = [int(i) for i in products_str]
            products = Product.objects.filter(id__in=[1, 2, 3], shop__username=username)
            # print(products_id) warring on get list of all selected values
            c = Category.objects.create(name=name, shop=Shop.objects.get(username=username), for_sell=for_sell, number_ordering=number_ordering)
            c.products.set(products)
            self.context.update({'msg': 'success'})
        else:
            self.context.update({'msg': 'failed'})
        return render(request, self.template_name, self.context)


class DeleteCategoryView(View):
    def get(self, request, username, pk):
        category_query = Category.objects.filter(shop__username=username, shop__manager=request.user, id=pk).delete()
        return redirect('categorys manager',username=username)


class EditeCategoryView(View):
    template_name = 'shopapp/category_edite.html'

    def setup(self, request, username, pk, *args, **kwargs):
        category = Category.objects.get(id=pk, shop__username=username, shop__manager=request.user)
        form_class = EditeCategoryForm(initial={'name':category.name, 'for_sell': category.for_sell, 'number_ordering': category.number_ordering})
        product_list = Product.objects.filter(shop__username=username, shop__manager=request.user)
        self.context = {
            'category':category,
            'form': form_class,
            'shop_username': username,
            'products_list': product_list,
        }
        return super().setup(request, username, pk, *args, **kwargs)
    
    def get(self, request, username, pk):
        return render(request, self.template_name, self.context)
    
    def post(self, request, username, pk):
        form = EditeCategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            for_sell = form.cleaned_data['for_sell']
            number_ordering = form.cleaned_data['number_ordering']
            products_list = request.POST.get('products')
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

