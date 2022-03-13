from django.contrib import admin
from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'city', 'filial', 'peerid', 'consultant', 'auth_code')
    list_display = ('user', 'city', 'filial', 'consultant')
    readonly_fields = ('peerid',)


admin.site.register(UserProfile, UserProfileAdmin)


class ConclusionAdmin(admin.ModelAdmin):
    readonly_fields = ('all_photos',)

    def all_photos(self, obj):
        image_field = ''
        pictures = obj.get_all_photo()
        print(pictures)
        print(type(pictures))
        for i in pictures:
            image_field += '<a href="/media/{0}"><img src="/media/{0}"></a>'.format(i.img)
            print(i.img)
        return mark_safe(image_field)


admin.site.register(Consultation, ConclusionAdmin)


class PhotoAdmin(admin.ModelAdmin):
    fields = ('img', 'get_photo')
    readonly_fields = ('get_photo',)

    def get_photo(self, obj):
        return obj.photo_tag()

    get_photo.short_description = 'Photo of prescription'


admin.site.register(Photo, PhotoAdmin)

admin.site.register(AuthCode)
