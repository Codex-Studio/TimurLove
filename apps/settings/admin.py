from django.contrib import admin

from apps.settings.models import Complement, Photo

# Register your models here.
@admin.register(Complement)
class ComplementAdmin(admin.ModelAdmin):
    list_display = ('title', )

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')