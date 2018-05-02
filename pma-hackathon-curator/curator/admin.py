from django.contrib import admin
from django.utils.html import format_html

from .models import Gallery, Artwork, ArtworkAttribute

class ArtworkAdmin(admin.ModelAdmin):
  list_display = ('gallery', 'title', 'artist', 'image', 'fact')
  list_editable = ['fact']
  list_filter = ['gallery']
  search_fields = ('title', 'artist')
  
  def image(self, obj):  # receives the instance as an argument
      return format_html('''
        <a href="{}"><img src="{}" height="50px" /></a>
      ''', obj.thumbnail, obj.thumbnail)

  image.allow_tags = True
  image.short_description = 'Thumbnail'

class ArtworkAttributeAdmin(admin.ModelAdmin):
  list_display = ('artwork', 'key', 'value', 'weight')


admin.site.register(Gallery)
admin.site.register(Artwork, ArtworkAdmin)
admin.site.register(ArtworkAttribute, ArtworkAttributeAdmin)