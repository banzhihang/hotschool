from django.contrib import admin

from user.models import User, School, Interest, UserData, UserDynamic, UserCollectFood, UserCollectQuestion



admin.site.site_title = "校园热搜"
admin.site.site_header = "校园热搜后台管理"
index_title = "校园热搜信息管理"


class UserAdmin(admin.ModelAdmin):
    search_fields = ['nick_name']


class SchoolAdmin(admin.ModelAdmin):
    pass


class InterestAdmin(admin.ModelAdmin):
    pass


class UserDataAdmin(admin.ModelAdmin):
    pass


class UserCollectFoodAdmin(admin.ModelAdmin):
    pass


class UserCollectQuestionAdmin(admin.ModelAdmin):
    pass


class UserDynamicAdmin(admin.ModelAdmin):
    pass


admin.site.register(User,UserAdmin)
admin.site.register(School,SchoolAdmin)
admin.site.register(Interest,InterestAdmin)
admin.site.register(UserData,UserDataAdmin)
admin.site.register(UserCollectFood,UserCollectFoodAdmin)
admin.site.register(UserCollectQuestion,UserCollectQuestionAdmin)
admin.site.register(UserDynamic,UserDynamicAdmin)
