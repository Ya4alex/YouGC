from django.contrib import admin
from .models import (Authme, KonlineOnline, KonlineList, KactivityLeaderboard, SiteProduct, SiteProductCategory,
                     EmailConfirm, SiteProductQueue)


# Register your models here.
class AuthmeAdminModel(admin.ModelAdmin):
    list_display = ['realname', 'ip', 'is_superuser', 'email', 'password']
    search_list = ('realname', 'ip', 'email',)

    class Meta:
        model = Authme


class KonlineOnlineAdminModel(admin.ModelAdmin):
    list_display = ['server', 'long_name', 'players', 'status']

    class Meta:
        model = KonlineOnline


class KonlineListAdminModel(admin.ModelAdmin):
    list_display = ['server_id', 'player', 'date']

    class Meta:
        model = KonlineList


class KactivityLeaderboardAdminModel(admin.ModelAdmin):
    list_display = ['place', 'name', 'balance', 'gotbalance']

    class Meta:
        model = KactivityLeaderboard


class SiteProductAdminModel(admin.ModelAdmin):
    list_display = ['name', 'long_name', 'description', 'price', 'category', 'buyers_count', ]

    class Meta:
        model = SiteProduct


class SiteProductCategoryAdminModel(admin.ModelAdmin):
    list_display = ['name', 'long_name']

    class Meta:
        model = SiteProductCategory


class KactivityListAdminModel(admin.ModelAdmin):
    list_display = ['name', 'status', 'balance', 'gotbalance', 'server', 'access_until']

    class Meta:
        model = None


class EmailConfirmAdminModel(admin.ModelAdmin):
    list_display = ['user', 'date', 'uid', 'token']

    class Meta:
        model = EmailConfirm


class SiteProductQueueAdminModel(admin.ModelAdmin):
    list_display = ['name', 'product_text', 'server', 'product']

    class Meta:
        model = SiteProductQueue


admin.site.register(Authme, AuthmeAdminModel)
admin.site.register(KonlineOnline, KonlineOnlineAdminModel)
admin.site.register(KonlineList, KonlineListAdminModel)
admin.site.register(KactivityLeaderboard, KactivityLeaderboardAdminModel)
admin.site.register(SiteProduct, SiteProductAdminModel)
admin.site.register(SiteProductCategory, SiteProductCategoryAdminModel)
admin.site.register(EmailConfirm, EmailConfirmAdminModel)
# admin.site.register(KactivityList, KactivityListAdminModel)
admin.site.register(SiteProductQueue, SiteProductQueueAdminModel)
