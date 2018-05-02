from django.db import models

class Gallery(models.Model):
  id = models.IntegerField(primary_key=True)
  name = models.CharField(max_length=100)
  activity = models.CharField(max_length=500)

  class Meta:
    verbose_name_plural = 'Galleries'

  def __str__(self):
    return self.name


class Artwork(models.Model):
  id = models.IntegerField(primary_key=True)
  gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
  title = models.CharField(max_length=100)
  artist = models.CharField(max_length=50)
  thumbnail = models.CharField(max_length=100)
  fact = models.CharField(max_length=500)

  class Meta:
    verbose_name_plural = 'Artwork'

  def __str__(self):
    return self.title

class ArtworkAttribute(models.Model):
  artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
  key = models.CharField(max_length=100)
  value = models.CharField(max_length=300)
  weight = models.IntegerField()

  def __str__(self):
    return '{}:{}'.format(self.key, self.value)