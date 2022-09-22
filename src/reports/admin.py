from django.contrib import admin
from django.contrib.auth.models import Group
# Register your models here.
from .models import Other, Vul, Mal

class OtherMalAdmin(admin.ModelAdmin):
    list_display = ('ip', 'rede', 'data_1', 'data_2', 'count')
    list_filter = ('rede', 'rede')
    search_fields = ('ip', 'rede')

class VulAdmin(admin.ModelAdmin):
    list_display = ('ip', 'port', 'rede', 'data_1', 'data_2', 'count')
    list_filter = ('rede', 'port')
    search_fields = ('ip', 'port', 'rede')

admin.site.site_header = 'Weekly Reports'
admin.site.register(Other, OtherMalAdmin)
admin.site.register(Mal, OtherMalAdmin)
admin.site.register(Vul, VulAdmin)
admin.site.unregister(Group)