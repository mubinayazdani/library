from django.contrib import admin

from .models import PasswordReset,Contact
# Register your models here.


admin.site.register(PasswordReset)


class ContactAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'email']


admin.site.register(Contact, ContactAdmin)