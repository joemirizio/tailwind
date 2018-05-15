from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe    

from .models import Artwork, ArtworkAttribute, Gallery, GalleryActivity, Reaction


class ArtworkAdmin(admin.ModelAdmin):
  list_display = ('id', 'gallery', 'title', 'artist', 'image', 'fact')
  list_editable = ('fact',)
  list_filter = ('gallery',)
  search_fields = ('id', 'title', 'artist')
  
  def image(self, obj):  # receives the instance as an argument
      return format_html('''
        <a href="{}"><img src="{}" height="50px" /></a>
      ''', obj.thumbnail, obj.thumbnail)

  image.allow_tags = True
  image.short_description = 'Thumbnail'


class ArtworkAttributeAdmin(admin.ModelAdmin):
  list_display = ('artwork', 'key', 'value', 'weight')


class GalleryAdmin(admin.ModelAdmin):

  class GalleryActivityInline(admin.TabularInline):
    model = GalleryActivity
  
  inlines = (GalleryActivityInline,)


class ReactionAdmin(admin.ModelAdmin):
  list_display = ('visitor', 'visitor_persona', 'reaction_type', 'artwork_link')
  list_filter = ('visitor__persona', 'artwork__gallery', 'reaction_type')
  search_fields = ('artwork',)

  def artwork_link(self, obj):
    return mark_safe('<a href="{}">{}</a>'.format(
        reverse("admin:curator_artwork_change", args=(obj.artwork.id,)),
        obj.artwork.title
    ))
  artwork_link.short_description = 'Artwork'

  def visitor_persona(self, obj):
    return obj.visitor.persona
  visitor_persona.short_description = 'Persona'


admin.site.register(Artwork, ArtworkAdmin)
admin.site.register(ArtworkAttribute, ArtworkAttributeAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Reaction, ReactionAdmin)