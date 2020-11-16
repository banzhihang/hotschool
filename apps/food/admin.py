from django.contrib import admin

# Register your models here.
from food.models import Flavour, Food, ShortComment, Discuss, FoodComment, FoodRevert, FoodMark, Eated, WantEat

admin.site.register([ShortComment,FoodComment,FoodRevert,FoodMark,Eated,WantEat])


class FoodAdmin(admin.ModelAdmin):
    search_fields = ['title']


class FlavourAdmin(admin.ModelAdmin):
    search_fields = ['name']


class DiscussAdmin(admin.ModelAdmin):
    search_fields = ['title']


admin.site.register(Food,FoodAdmin)
admin.site.register(Flavour,FlavourAdmin)
admin.site.register(Discuss,DiscussAdmin)
