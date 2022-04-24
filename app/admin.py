from django.forms import ModelChoiceField,ModelForm,ValidationError
from django.utils.safestring import mark_safe

from django.contrib import admin
from .models import *
from PIL import Image


class NotebookAdminForm(ModelForm):

    MIN_RESOLUTION = (400,400)
    MAX_RESOLUTION = (800,800)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['image'].help_text = mark_safe("<span style='color:red; font-size:17px;'>Rasimni ko'rsatilganidan Kam bo'lmasin {} x {} </span>".format(
            *Product.MIN_RESOLUTION
                                                                                                            ))

    def clean_image(self):
        image = self.cleaned_data['image']
        img  = Image.open(image)
        min_height,min_width = Product.MIN_RESOLUTION
        max_height,max_width = Product.MAX_RESOLUTION
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError("Rasim hajmi 3MB  oshmasligi kerak !")
        if img.height < min_height or img.width < min_width:
            raise ValidationError(f"Yuklangan rasim ko'rsatilganidan kichik {img.height} x {img.width}")
        if img.height > max_height or img.width > max_width:
            raise ValidationError(f"Yuklangan rasim ko'rsatilganidan Katta {img.height} x {img.width}")
        return image


class NotebookAdmin(admin.ModelAdmin):

    form = NotebookAdminForm


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(db_field,request,**kwargs)



class SmartphoneAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphones'))
        return super().formfield_for_foreignkey(db_field,request,**kwargs)


admin.site.register(Category)
admin.site.register(Smartphone,SmartphoneAdmin)
admin.site.register(Notebook,NotebookAdmin)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Customer)


