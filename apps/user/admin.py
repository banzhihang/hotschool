from django.contrib import admin

from user.models import User, School, Interest, UserData, UserDynamic, UserCollectFood, UserCollectQuestion

admin.site.register(User)
admin.site.register(School)
admin.site.register(Interest)
admin.site.register(UserData)
admin.site.register(UserDynamic)
admin.site.register(UserCollectFood)
admin.site.register(UserCollectQuestion)

