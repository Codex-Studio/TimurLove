from django.contrib import admin

from apps.settings.models import Complement, Photo, Movie

# Register your models here.
@admin.register(Complement)
class ComplementAdmin(admin.ModelAdmin):
    list_display = ('title', )

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'watched')