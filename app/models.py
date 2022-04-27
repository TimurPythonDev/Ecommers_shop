from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


def get_product_url(obj,viewname):
    ct_model = obj.__class__._meta.model_name
    return reversed(viewname,kwargs={'ct_model':ct_model,'slug':obj.slug})


class LatestProdcutsManeger:

    def get_products_for_main_page(self,*args,**kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products,key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to),reverse=True
                    )
        return products



class LatestProducts:

    objects = LatestProdcutsManeger()


class Category(models.Model):

    name = models.CharField(max_length=255,verbose_name="Kategorya nomi")
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):

    class Meta:
        abstract = True

    category = models.ForeignKey(Category,verbose_name="Kategoriay",on_delete=models.CASCADE)
    title = models.CharField(max_length=255,verbose_name="Nomlanishi")
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name="Rasim")
    description = models.TextField(verbose_name="Ko'proq malumot")
    price = models.DecimalField(max_digits=9,decimal_places=2,verbose_name='Narxi')

    def __str__(self):
        return self.title

class Notebook(Product):

    dioganal = models.CharField(max_length=255,verbose_name='Dioganal')
    display_type = models.CharField(max_length=255,verbose_name='Display type')
    processor_freq = models.CharField(max_length=255,verbose_name='Protsessor')
    ram = models.CharField(max_length=255,verbose_name='Ichki hotira RAM')
    video = models.CharField(max_length=255,verbose_name='Grafik karta')
    time_with = models.CharField(max_length=255,verbose_name='Akumlyator quvvati')

    def __str__(self):
        return "{} : {}".format(self.category.name,self.title)

    def get_absolute_url(self):
        return get_product_url(self,'product_detail')

class Smartphone(Product):

    dioganal = models.CharField(max_length=255, verbose_name='Dioganal')
    display_type = models.CharField(max_length=255, verbose_name='Display type')
    resolution = models.CharField(max_length=255,verbose_name='Ekran olchami')
    accum_volume = models.CharField(max_length=255,verbose_name='Akumlyator amper')
    ram = models.CharField(max_length=255, verbose_name='Ichki hotira RAM')
    sd = models.BooleanField(default=True)
    sd_volume_max = models.CharField(max_length=255,verbose_name='Asosiy hotira')
    main_cam_mp = models.CharField(max_length=255,verbose_name='Asosiy kamera MP')
    frontal_cam_mp = models.CharField(max_length=255,verbose_name='Oldi kamera MP')

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self,'product_detail')

class CartProduct(models.Model):

    user = models.ForeignKey('Customer',verbose_name='Foydalanuvchi',on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart',verbose_name='Savatcha',on_delete=models.CASCADE,related_name='related_product')
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9,decimal_places=2,verbose_name='Umumiy Narxi')

    def __str__(self):
        return "Mahsulot: {} (savatcha uchun)".format(self.product)


class Cart(models.Model):

    owner  = models.ForeignKey('Customer',verbose_name="Yaratuvchi",on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct,blank=True,related_name='related_cart')
    total_product = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9,decimal_places=2,verbose_name='Umumiy Narxi')

    def __str__(self):
        return str(self.id)

class Customer(models.Model):

    user = models.ForeignKey(User,verbose_name="Foydalanuvchi",on_delete=models.CASCADE)
    phone = models.CharField(max_length=20,verbose_name="Telefon raqam")
    address = models.CharField(max_length=255,verbose_name="Manzil")

    def __str__(self):
        return "Sotib oluvchi: {} {}".format(self.user.first_name,self.user.last_name)



