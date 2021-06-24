from django.contrib import admin
from .models import Authme, KonlineOnline


# Register your models here.
class AuthmeAdminModel(admin.ModelAdmin):
    list_display = ['realname', 'ip', 'is_superuser', 'email', 'password']
    search_list = ('realname', 'ip', 'email', )

    class Meta:
        model = Authme


class KonlineOnlineAdminModel(admin.ModelAdmin):
    list_display = ['server', 'players', 'status']

    class Meta:
        model = KonlineOnline


admin.site.register(Authme, AuthmeAdminModel)
admin.site.register(KonlineOnline, KonlineOnlineAdminModel)
