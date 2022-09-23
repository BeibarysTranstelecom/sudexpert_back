from django.contrib import admin
from tenders import models
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_filter = ['is_active','role', 'date_regist','structure']
    list_display = ['user_id', 'user', 'structure','is_active']
    search_fields = ['full_name']
class TendersAdmin(admin.ModelAdmin):
    list_filter = ['enable','category', 'status','date_created','customer','executor']
    list_display = ['name', 'category', 'date_start','date_end','date_created','status','enable']
    search_fields = ['name']
class OrdersAdmin(admin.ModelAdmin):
    list_filter = ['date_created','executor','tender']
    list_display = ['executor', 'price', 'date_created']

admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.Tenders, TendersAdmin)
admin.site.register(models.Orders, OrdersAdmin)
admin.site.register(models.User)
admin.site.register(models.TendersFile)
admin.site.register(models.Structure)
admin.site.register(models.Category)