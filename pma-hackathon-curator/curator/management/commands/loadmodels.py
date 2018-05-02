import requests
from django.core.management.base import BaseCommand, CommandError
from curator.models import Gallery, Artwork, ArtworkAttribute

class Command(BaseCommand):
  help = 'Loads models from the PMA API'

  def add_arguments(self, parser):
    parser.add_argument('api_uri', help='URI of the custom PMA API')

  def handle(self, *args, **options):
    gallery_ids = requests.get('{}/api/galleries'.format(options['api_uri'])).json()

    # Create Artwork and ArtworkAttribute
    for gallery_id in gallery_ids:
      # Create Gallery
      gallery = load_galleries(gallery_id)

      gallery_artwork = requests.get('{}/api/galleryObjects/{}'.format(options['api_uri'], gallery_id)).json()[0]
      for artwork_data in gallery_artwork:
        load_artwork(artwork_data, gallery)


def load_galleries(gallery_id):
  gallery = Gallery(id=int(gallery_id), name='Gallery {}'.format(gallery_id))
  gallery.save()
  return gallery

def load_artwork(artwork_data, gallery):
  artwork = Artwork(id=int(artwork_data['ObjectID']), title=artwork_data['Title'], 
    artist=artwork_data['Artists'][0]['Artist'], thumbnail=artwork_data['Thumbnail'],
    gallery=gallery)
  artwork.save()
  load_artwork_attributes(artwork_data, artwork)
  return artwork

def load_artwork_attributes(artwork_data, artwork):
  # Delete all attributes
  artwork.artworkattribute_set.all().delete()

  fields = [
    'Location.GalleryShort', 'Location.Gallery', 'Artists.Artist', 'Classification', 
    'Style', 'Movement', 'DateBegin', 'Period', 'School', 'Dynasty', 
    'Reign', 'SocialTags'
  ]
  fields.reverse()
  for i, key in enumerate(fields):
    # Check for nested properties (e.g. 'a.b')
    keyB = None
    if '.' in key:
      key, keyB = key.split('.')

    if key not in artwork_data or not artwork_data[key]:
      continue

    # Wrap single values as a list
    values = artwork_data[key]
    if type(values) is not list:
      values = [values]

    for value in values:
      if keyB:
        key = keyB
        value = value[keyB]
        if key == 'Gallery':
          key = 'Wing'
          value = value.split(', ')[1]

      weight = 2 ** (i + 1)

      art_attribute = ArtworkAttribute(artwork=artwork, key=key, value=value, weight=weight)
      art_attribute.save()
