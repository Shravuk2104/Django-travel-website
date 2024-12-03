from django.contrib import admin
from Travelapp.models import package

# Register your models here.

class packageAdmin(admin.ModelAdmin):
        list_display=['id', 'name','price','pdetails','cat','is_active']
        list_filter=['price','cat','is_active']

admin.site.register(package,packageAdmin)